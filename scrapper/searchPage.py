# Base python package
import logging
import os
import re

# Project specific package
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
import numpy as np
import pandas as pd

# local module and package
from enums import *


logging.basicConfig(filename='dev.log', filemode='w', level=logging.INFO)


class ChromeBasePage(object):
    """Base class to initialize the base page that will be called from all
    pages

    Could work for other driver, but was not tested.
    """

    def __init__(self, driver: webdriver.Chrome = webdriver.Chrome()):
        self.driver = driver

    def __del__(self):
        self.driver.close()


class SearchPageQcDonator(ChromeBasePage):
    """Creating a page to access the page of donators"""

    URL = "https://www.electionsquebec.qc.ca/francais/provincial/financement-et-depenses-electorales/recherche-sur-les-donateurs.php"

    def __init__(self):
        super().__init__()
        self.driver.get(SearchPageQcDonator.URL)

    def check_entity(self, entity_id: str):
        """Fetch entity webElement, if unchecked click on it"""
        box = self.driver.find_element(By.ID, entity_id)
        if not box.get_attribute('checked'):
            box.click()

    def uncheck_entity(self, entity_id: str):
        """Fetch entity webElement, if checked click on it"""
        box = self.driver.find_element(By.ID, entity_id)
        if box.get_attribute('checked'):
            box.click()

    def select_dropdown(self, check_entity_id, dropdown_class, ckbo_class, values_type, values: list[str] = []):
        """
        select_dropdown general function to select a dropdown from the searchPage of dons.

        values should be all from the same CheckboxValues child class.
        Ex : values = [PoliticalPartiesValues.ADQ,
            PoliticalPartiesValues.CAQ, PoliticalPartiesValues.CAQ_PRE]

        Parameters
        ----------
        check_entity_id : [type]
            checkbox id to check in order to make visible the dropdown
        dropdown_class : [type]
            class name of the dropdown to click on. Will make the Checkbox visible
        ckbo_class : [type]
            class name of the checkbox inside the dropdown
        values_type : [ValueType]
            value types inside the dropdown, mainly for logging details
        values : list[str], optional
            Values from a CheckboxValues object, by default []
        """
        if check_entity_id:
            self.check_entity(
                check_entity_id)  # make sure dropdown is visible (Except for financial years)
        if values:
            logging.info(f"searching by {values_type} with {values}")
            try:
                # if users selected specific years
                dropdown = self.driver.find_element(
                    By.CLASS_NAME, dropdown_class)
                divCkBox = self.driver.find_element(
                    By.CLASS_NAME, ckbo_class)
                ckbox = divCkBox.find_elements(By.TAG_NAME, "input")
                # make dropdown visible
                ActionChains(self.driver).move_to_element(
                    dropdown).click(dropdown).perform()
                # unselect all parties, make all input unchecked
                ckbox[0].click()
                # select all years
                for ck in ckbox:
                    if ck.is_displayed() and ck.get_attribute('value') in values:
                        ck.click()
            except WebDriverException as err:
                logging.error(err)
                logging.error(f"could not select the {values_type} {values}")
            finally:
                # close dropdown
                entete = self.driver.find_element(By.ID, "entete")
                ActionChains(self.driver).move_to_element(
                    entete).click(entete).perform()

        else:
            logging.info(f"searching all {values_type} by default")

    def select_financial_years(self, years: list[str] = []):
        """Select the years to search by checking box in Annee Financiere dropdown"""

        self.select_dropdown(None, DropdownClassName.YEARS,
                             CheckboxClassName.YEARS, ValuesType.YEAR, values=years)

    def select_political_parties(self, parties: list[str] = []):
        """
        select_political_parties : Select the political parties to search by checking box in Parti Politique dropdown

        Parameters
        ----------
        parties : list[str], optional
            [description], by default []
        """
        self.select_dropdown(PoliticalEntitiesId.POLITICAL_PARTIES, DropdownClassName.POLITICAL_PARTIES,
                             CheckboxClassName.POLITICAL_PARTIES, ValuesType.PARTIES, values=parties)

    def select_independant_members(self, members: list[str] = []):
        """
        select_independant_members : Select the independant deputies to search by checking box in 'Depute Independant' dropdown

        Parameters
        ----------
        members : list[str], optional
            [description], by default []
        """
        self.select_dropdown(PoliticalEntitiesId.INDEPENDANT_MEMBERS, DropdownClassName.INDEPENDANT_MEMBERS,
                             CheckboxClassName.INDEPENDANT_MEMBERS, ValuesType.MEMBERS, values=members)

    def select_independant_candidates(self, candidates: list[str] = []):
        """
        select_independant_candidates [summary]

        [extended_summary]

        Parameters
        ----------
        candidates : list[str], optional
            [description], by default []
        """
        self.select_dropdown(PoliticalEntitiesId.INDEPENDANT_CANDIDATES, DropdownClassName.INDEPENDANT_CANDIDATES,
                             CheckboxClassName.INDEPENDANT_CANDIDATES, ValuesType.CANDIDATES, values=candidates)

    def select_leadership_race(self, leadears: list[str] = [], races: list[str] = []):
        """
        select_leadership_race [summary]

        [extended_summary]

        Parameters
        ----------
        leadears : list[str], optional
            [description], by default []
        races : list[str], optional
            [description], by default []
        """
        self.select_dropdown(PoliticalEntitiesId.LEADERSHIP_RACE, DropdownClassName.LEADERSHIP_RACE,
                             CheckboxClassName.LEADERSHIP_RACE, ValuesType.RACE, values=races)
        self.select_dropdown(PoliticalEntitiesId.LEADERSHIP_RACE, DropdownClassName.LEADER,
                             CheckboxClassName.LEADER, ValuesType.LEADER, values=leadears)

    def click_on_research(self):
        boutton = self.driver.find_element(By.ID, "boutonRechercher")
        ActionChains(self.driver).move_to_element(
            boutton).click(boutton).perform()


class DonationScrapper(ChromeBasePage):
    def __init__(self, output="../output/"):
        super().__init__()
        self.searchPage = SearchPageQcDonator()
        self.numberOfPage = None
        self.currentPage = 1
        self.outputPath = output
        self.header = ["index", "firstName", "lastName", "amount",
                       "nbrPayment", "entity", "fiscYear", "postalCode", "city"]
        self._counter = -1

    def getNumberOfPage(self):
        # self.driver.find_elements(By.TAG_NAME, "table")
        return int(scrapper.driver.find_elements(
            By.PARTIAL_LINK_TEXT, 'Fin >>')[0].get_attribute('href').split('page=')[-1])

    @property
    def counter(self):
        self._counter += 1
        return self._counter

    def query(self, years=None, parties=None, members=None, canditates=None, races=None, leaders=None):
        if years is not None:
            self.searchPage.select_financial_years(years)
        if parties is not None:
            self.searchPage.select_political_parties(parties)
        if members is not None:
            self.searchPage.select_independant_members(members)
        if canditates is not None:
            self.searchPage.select_independant_candidates(canditates)
        if races is not None or leaders is not None:
            races = [] if races is None else races
            leaders = [] if leaders is None else leaders
            self.searchPage.select_leadership_race(
                races=races, leadears=leaders)

        self.searchPage.click_on_research()

    def savePage(self, page):
        if len(page) == 101:
            # fixing bug that last page result is same as first of next page.
            page = page[:100]
        df = pd.DataFrame(page, columns=self.header)
        df.to_csv(self.outputPath + "data.csv",
                  index=False, header=False, mode="a")
        df = None

    def createOutputFile(self):
        if(not os.path.exists(self.outputPath)):
            os.makedirs(self.outputPath)

    def loadNextPage(self):
        """
         Call the driver to load the url with the next page value

        [extended_summary]
        """
        self.currentPage += 1
        print(f"loading {self.currentPage} out of {self.numberOfPage}")
        self.driver.get(SearchPageQcDonator.URL + f"?page={self.currentPage}")

    def parseResults(self):
        """
         Parse all page from the search results.

        BUG : The last result of everypage is the same as the first of the next page.
        """
        self.numberOfPage = self.getNumberOfPage()
        self.createOutputFile()
        while (self.currentPage < self.numberOfPage):
            page = self.parsePage()
            print(page[0], len(page))
            self.savePage(page)
            self.loadNextPage()

        page = self.parsePage()
        print(page[0], len(page))
        self.savePage(page)

    def parsePage(self):
        """
        Read all the results and create a (100,M) list of list.
        Where M is the number of attributes.

        [extended_summary]
        """

        pageData = []
        table = self.driver.find_element(By.CLASS_NAME, 'tableau')
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        if (len(rows) == 100):
            for row in rows:
                rowData = row.find_elements(By.TAG_NAME, 'td')
                pageData.append(self.parseRow(rowData))
        else:
            # skipping first since its same as last element of the last page.
            for i in range(1, len(rows)):
                rowData = rows[i].find_elements(By.TAG_NAME, 'td')
                pageData.append(self.parseRow(rowData))

        return pageData

    def parseRow(self, td: list[WebElement]) -> list:
        index = self.counter
        firstName = self.parseFirstName(td[0].text)
        lastName = self.parseLastName(td[0].text)
        amout = self.parseAmount(td[1].text)
        nbr_v = self.parseNbrPayments(td[2].text)
        p_entity = td[3].text
        year = self.parseYear(td[4].text)
        try:
            href = td[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
        except Exception:
            logging.error("can't parse href from td")
            href = ''
        postalCode = self.parsePostalCode(href)
        city = self.parseCity(href)

        return[index, firstName, lastName, amout, nbr_v,
               p_entity, year, postalCode, city]

    def parseFirstName(self, fullName: str):
        firstName = ""
        try:
            firstName = fullName.split(',')[1].strip()
        except Exception:
            logging.error(f"can't parse firstName from : {fullName}")

        return firstName

    def parseLastName(self, fullName: str):
        lastName = ""
        try:
            lastName = fullName.split(',')[0].strip()
        except Exception:
            logging.error(f"can't parse lastName from : {fullName}")

        return lastName

    def parseAmount(self, amount_txt: str) -> float:
        amount = 0
        try:
            amount = float(amount_txt.split('$')[0].strip().replace(',', '.'))
        except Exception as err:
            logging.error(f"can't parse {amount_txt} to float format : {err}")
            amount = -1.0
        return amount

    def parseNbrPayments(self, nbr_txt: str) -> int:
        payments = 0
        try:
            payments = int(nbr_txt)
        except Exception as err:
            logging.error(f"can't parse {nbr_txt} to int : {err}")
            payments = -1

        return payments

    def parseYear(self, year_txt: str) -> int:
        year = -1
        try:
            year = int(year_txt)
        except Exception as err:
            logging.error(f"can't parse {year_txt} to int : {err}")
            year = -1
        return year

    def parsePostalCode(self, href: str):
        pc = ""
        try:
            # ?idrech=202553&an=2020&fkent=00079&v=Sainte-Marthe-Sur-Le-Lac&cp=J0N1P0'
            args = href.split('?')[-1]
            pc = args.split('&')[-1].split('=')[-1]  # cp=J0N1P0
        except Exception:
            logging.error(f"can't parse postal code of : {href}")
        return pc

    def parseCity(self, href: str):
        city = ""
        try:
            # ?idrech=202553&an=2020&fkent=00079&v=Sainte-Marthe-Sur-Le-Lac&cp=J0N1P0'
            args = href.split('?')[-1]
            # v=Sainte-Marthe-Sur-Le-Lac
            city = args.split('&')[-2].split('=')[-1]
            city = self.cleanCityStr(city)
        except Exception:
            logging.error(f"can't parse city of : {href}")
        return city

    def cleanCityStr(self, city: str):
        def replace_unicode(text):
            replacement = {"%E9": "é", "%C9": "é", "%E8": "è",
                           "_": " ", "%2C": ",",
                           "%C7": "ç", "%E7": "ç", "%27": "'", "+": "-", "%EE": "î", "%CE": "î",
                           "%F4": "ô", "%BF": "'", "%C0": "à", "%E0": "à", "%E2": "â", "%EA": "ê", "%EB": "ë"
                           }
            for k, v in zip(replacement.keys(), replacement.values()):
                text = text.replace(k, v)
            return text

        def remove_duplicate_dash(c): return re.sub("[-]{2,}", '-', c)
        def capitalizeFirst(c): return c.lower()

        city = replace_unicode(city)
        city = remove_duplicate_dash(city)
        city = capitalizeFirst(city)
        return city


if __name__ == "__main__":

    years = ["2019", "2020", "2021", "2022"]
    parties = [PoliticalPartiesValues.PCQ_CPQ]
    members = [IndependantMembersValues.CATHERINE_FOURNIER]
    candidates = [IndependantCandidatesValues.CLAUDE_SURPRENANT]
    races = [LeadershipRaceValues.PCQ_2021]
    leaders = [LeadershipCandidateValues.ERIC_DUHAIME]

    scrapper = DonationScrapper()
    scrapper.query(years=years, parties=parties)
    scrapper.parseResults()

    input("PARSING DONE...")
    del(scrapper)
    input("QUITTING...")
