# Base python package
import logging
import time

# Scrapping tools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# local module and package
from .enums import *


class ChromeBasePage(object):
    """Base class to initialize the base page that will be called from all
    pages

    Could work for other driver, but was not tested.
    """

    def __init__(self):
        print("stating web Driver")
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1920,1080")
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(30)

    def __del__(self):
        self.driver.close()


class SearchPageQcDonator(ChromeBasePage):
    """Creating a page to access the page of donators"""

    URL = "https://www.electionsquebec.qc.ca/francais/provincial/financement-et-depenses-electorales/recherche-sur-les-donateurs.php"

    def __init__(self, name):
        super().__init__()
        self.driver.get(SearchPageQcDonator.URL)
        self.numberOfPage = None
        self.currentPage = 1
        self._counter = -1
        self.name = name

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

    def select_dropdown(self, check_entity_id: str, dropdown_class: str, ckbo_class: str, values_type: str, values: list[str] = []):
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
            logging.info("searching by %s  with %s", values_type, str(values))
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
                logging.info("could not select %s  with %s",
                             values_type, str(values))

            finally:
                # close dropdown
                entete = self.driver.find_element(By.ID, "entete")
                ActionChains(self.driver).move_to_element(
                    entete).click(entete).perform()

        else:
            logging.info("searching all %s by default", values_type)

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
        """
        calling the javascript code linked to the button search

        A timeout exception indicated that you are using to much process in the pooling
        """
        self.driver.execute_script(
            "document.getElementById('form_recherche').submit();")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tableau")))
        except TimeoutException:
            print(
                f"could not find class id tableau after loading page : {self.currentPage} in process : {self.name}")

    def getNumberOfPage(self):
        """
        Read the page number associated with the last page button

        Returns
        -------
        int
            number of html page to parse
        """
        maxPage = 1
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Fin >>')))
            maxPage = int(self.driver.find_element(
                By.PARTIAL_LINK_TEXT, 'Fin >>').get_attribute('href').split('page=')[-1])
        except TimeoutException as err:
            if maxPage == 1:
                print("WARNING : data might be missing, try reducing the pool size if you are using the multiprocess feature. (while getting last page number)")
            logging.warning(
                "timeout exception while getting the number of page for process named: %s, make sure there's only one page otherwise you only have the first page", str(self.name))
        return maxPage

    @ property
    def counter(self):
        self._counter += 1
        return self._counter

    def query(self, years: list[str] = None, parties: list[str] = None,
              members: list[str] = None, canditates: list[str] = None,
              races: list[str] = None, leaders: list[str] = None):
        """
        execute a search query on the page and call the search button

        For specific query, make sure to use the values encoded in the enum.

        If all params are None, the default website search parameter are used.(All years and all parties)

        Parameters
        ----------
        years : list[str], optional
            if None, parse all year from 2000 to 2022, by default None
        parties : list[str], optional
            if None, parse all parties, by default None
        members : list[str], optional
            if None, parse nothing, by default None
        canditates : list[str], optional
            if None, parse nothing, by default None
        races : list[str], optional
            if None, parse nothing, by default None
        leaders : list[str], optional
            if None, parse nothing, by default None
        """
        if years is not None:
            self.select_financial_years(years)
        if parties is not None:
            self.select_political_parties(parties)
        if members is not None:
            self.select_independant_members(members)
        if canditates is not None:
            self.select_independant_candidates(canditates)
        if races is not None or leaders is not None:
            races = [] if races is None else races
            leaders = [] if leaders is None else leaders
            self.select_leadership_race(
                races=races, leadears=leaders)

        self.click_on_research()

    def loadNextPage(self):
        """
         Call the driver to load the url with the next page value

         Warning will occure if too many process are behing used which could
         results in data loss.
        """
        self.currentPage += 1
        self.driver.get(SearchPageQcDonator.URL + f"?page={self.currentPage}")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tableau")))
        except TimeoutException:
            print("WARNING : data might be missing, try reducing the pool size if you are using the multiprocess feature. (while loading next page)")
            logging.warning(
                "timeout exception while loading %s for presses named : %s", str(self.currentPage), str(self.name))

    def getAllHtmlPage(self):
        htmlList = []
        self.numberOfPage = self.getNumberOfPage()
        htmlPage = self.driver.page_source
        htmlList.append(htmlPage)
        while (self.currentPage < self.numberOfPage):
            self.loadNextPage()
            htmlPage = self.driver.page_source
            htmlList.append(htmlPage)
        return htmlList


if __name__ == "__main__":

    years = []

    parties = []
    members = [IndependantMembersValues.CATHERINE_FOURNIER]
    candidates = [IndependantCandidatesValues.CLAUDE_SURPRENANT]
    races = [LeadershipRaceValues.PCQ_2021]
    leaders = [LeadershipCandidateValues.ERIC_DUHAIME]

    scrapper = SearchPageQcDonator("test")
    scrapper.query()

    htmls = scrapper.getAllHtmlPage()

    input("PARSING DONE...")
    del(scrapper)
    input("QUITTING...")
