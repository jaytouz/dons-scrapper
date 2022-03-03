from re import S
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# from searchPage import SearchPageQcDonator
# from .enums import *


class wait_for_all_tr(object):
    def __init__(self, number: int):
        self.number_rows = number

    def __call__(self, driver):
        # Finding the referenced element
        tbody = driver.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        if len(rows) < self.number_rows:
            return False
        else:
            return rows


class wait_for_number_of_rows_text(object):

    def __call__(self, driver):
        # Finding the referenced element
        element = driver.find_element(By.TAG_NAME, 'tfoot')
        if element:
            s = element.text
            if "Enregistrement" in s:
                idxS = s.find(':') + 1
                idxE = s.index("sur") - 1
                str_with_number = s[idxS:idxE].strip()
                list_of_number = s[idxS:idxE].strip().split(' à ')
                firstRow = int(list_of_number[0])
                lastRow = int(list_of_number[1])
                numberOfRow = lastRow - firstRow + 1
                return numberOfRow
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    years = []

    parties = []
    members = [IndependantMembersValues.CATHERINE_FOURNIER]
    candidates = [IndependantCandidatesValues.CLAUDE_SURPRENANT]
    races = [LeadershipRaceValues.PCQ_2021]
    leaders = [LeadershipCandidateValues.ERIC_DUHAIME]

    scrapper = SearchPageQcDonator("test")
    scrapper.query(years=["2022"])
    scrapper.loadNextPage()
    numRow = 0
    try:
        driver = WebDriverWait(scrapper.driver, 10)
        numRow = driver.until(
            wait_for_number_of_rows_text())
        print(numRow)
    except TimeoutException:
        print('nothing found')

    try:
        driver = WebDriverWait(scrapper.driver, 10)
        rows = driver.until(
            wait_for_all_tr(number=numRow))
        print(rows[0].text)
    except TimeoutException:
        print('nothing found')

    print("done")
