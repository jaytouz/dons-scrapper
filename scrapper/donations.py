# Base python package
import logging

# Project specific package
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

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

    def __init__(self, driver: webdriver.Chrome = webdriver.Chrome()):
        super().__init__(driver)
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
        pass


if __name__ == "__main__":

    years = ["2020", "2019", "2021"]
    parties = [PoliticalPartiesValues.CAQ,
               PoliticalPartiesValues.ADQ, PoliticalPartiesValues.CAQ_PRE]
    members = [IndependantMembersValues.CATHERINE_FOURNIER]
    candidates = [IndependantCandidatesValues.CLAUDE_SURPRENANT]
    races = [LeadershipRaceValues.PCQ_2021]
    leaders = [LeadershipCandidateValues.ERIC_DUHAIME]

    searchPage = SearchPageQcDonator()
    searchPage.select_financial_years(years=years)
    searchPage.select_political_parties(
        parties=parties)
    searchPage.select_independant_members(members=members)
    searchPage.select_independant_candidates(candidates=candidates)
    searchPage.select_leadership_race(races=races, leadears=leaders)
    input()
    del(searchPage)
    input()
