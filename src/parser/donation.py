from cmath import log
import re
import logging
from bs4 import BeautifulSoup
import glob
import os
import pandas as pd
import itertools


class HtmlParser(object):
    """
    HtmlParser : Base class for parsing html page

    """

    def __init__(self, htmlContent: str) -> None:
        """

        Parameters
        ----------
        htmlContent : str
            string corresponding to a html page
        """
        self.soup = BeautifulSoup(htmlContent, 'html.parser')


class DonationParser(HtmlParser):
    """
    Parser for html page with donation search results.

    Parameters
    ----------
    HtmlParser : str
        string corresponding to a html page
    """

    def __init__(self, htmlContent, pageNumber) -> None:
        super().__init__(htmlContent)
        self.pageNumber = pageNumber  # to be used in logging if errors
        self.data = []
        self.header = ["firstName", "lastName", "amount",
                       "nbrPayment", "entity", "fiscYear", "postalCode", "city"]

    def extract(self):
        """
        extract all the data from the page. Results with be in self.data
        """
        rows = self.fetchTableRows()
        if(len(rows) == 101):
            # first row is same as last row of last page. Bug from the site
            rows = rows[1:]

        for row in rows:
            rowData = self.extractRowData(row)
            self.data.append(rowData)

    def fetchTableRows(self) -> list[str]:
        """
        fetchTableRows extract all tr from table tag

        Returns
        -------
        list[str]
            list of tr tag
        """
        table, body, rows = None, None, []
        table = self.soup.find('table', {'class': 'tableau'})
        if table:
            body = table.find('tbody')
        rows = []
        if body:
            rows = body.findAll('tr')
        return rows

    def extractRowData(self, row):
        if row != []:
            row = row.findAll('td')
            firstName = self.parseFirstName(row)
            LastName = self.parseLastName(row)
            amount = self.parseAmount(row)
            nbrVir = self.parseNbrPayment(row)
            polEntity = self.parsePolEntity(row)
            year = self.parseYear(row)
            postalCode = self.parsePostalCode(row)
            city = self.parseCity(row)
        else:
            logging.WARNING(f"Data is missing in page {self.pageNumber}")
            firstName = pd.NA
            LastName = pd.NA
            amount = pd.NA
            nbrVir = pd.NA
            polEntity = pd.NA
            year = pd.NA
            postalCode = pd.NA
            city = pd.NA

        return [firstName, LastName, amount, nbrVir,
                polEntity, year, postalCode, city]

    def parseFirstName(self, row: list[str]) -> str:
        """
        parseFirstName from the table row, parse the first name

        data from 2000 up to 2011 don't have an a tag in the name.

        Parameters
        ----------
        row : list[str]
            list of td tag

        Returns
        -------
        str
            first name
        """
        firstName = ""
        if (row[0].find('a') is not None):
            try:
                fullName = row[0].find('a').text
                firstName = fullName.split(',')[1].strip()
            except Exception:
                logging.error(
                    f"can't parse firstName from : {row}")
        else:
            try:
                fullName = row[0].text
                firstName = fullName.split(',')[1].strip()
            except Exception:
                logging.error(
                    f"can't parse firstName from : {row}")
        return firstName

    def parseLastName(self, row: list[str]) -> str:
        """
        parseLastName from the table row, parse the last name

        data from 2000 up to 2011 don't have an a tag in the name.

        Parameters
        ----------
        row : list[str]
            list of td tag

        Returns
        -------
        str
            last name
        """
        lastName = ""
        if (row[0].find('a') is not None):
            try:
                fullName = row[0].find('a').text
                lastName = fullName.split(',')[0].strip()
            except Exception:
                logging.error(
                    f"can't parse lastName from : {row}")
        else:
            try:
                fullName = row[0].text
                lastName = fullName.split(',')[0].strip()
            except Exception:
                logging.error(
                    f"can't parse lastName from : {row}")
        return lastName

    def parseAmount(self, row: list[str]) -> float:
        """
        parseAmount amount of the donation in canadian dollard

        Parameters
        ----------
        row : list[str]
            list of td tag element.

        Returns
        -------
        float
            donation amount in canadian dollard
        """
        amount = 0
        try:
            amount = float(row[1]
                           .text
                           .replace(u'\xa0', '')
                           .split('$')[0]
                           .strip()
                           .replace(',', '.')
                           )
        except Exception as err:
            logging.error(f"can't parse {row} to float format : {err}")
            amount = -1.0
        return amount

    def parseNbrPayment(self, row: list[str]) -> int:
        """
        parseNbrPayment number of payment to make the donation

        Parameters
        ----------
        row : list[str]
            list of td tag element

        Returns
        -------
        int
            number of payment to make the donation
        """
        payments = 0
        try:
            if row[2].text == 'N/D':
                payment = pd.NA
            else:
                payments = int(row[2].text)
        except Exception as err:
            logging.error(f"can't parse {row} to int : {err}")
            payments = -1

        return payments

    def parsePolEntity(self, row: list[str]) -> str:
        """
        parsePolEntity read the text corresponding to the political entity


        Parameters
        ----------
        row : list[str]
            list of td tag element


        Returns
        -------
        str
            political entity
        """
        entity = ""
        try:
            entity = row[3].text
        except Exception as err:
            logging.error(
                "Could not parse political entity for row %s", str(row))
        return entity

    def parseYear(self, row: list[str]) -> int:
        """
        parseYear read the fiscal year associated with the donation.

        Parameters
        ----------
        row : list[str]
            list of td tag element

        Returns
        -------
        int
            fiscal year of the donation or -1 if an error occured
        """
        year = -1
        try:
            year = int(row[4].text)
        except Exception as err:
            logging.error(f"can't parse {row} to int : {err}")
            year = -1
        return year

    def parsePostalCode(self, row: list[str]) -> str:
        """
        parsePostalCode read the postal code in the name a tag.
        Data from 2000 up to 2011 don't have an a tag in the name and therefore
        no postal code.

        Parameters
        ----------
        row : list[str]
            list of td tag element

        Returns
        -------
        str
            postal code or empty string
        """
        pc = ""
        if (row[0].find('a') is not None):
            try:
                # ?idrech=202553&an=2020&fkent=00079&v=Sainte-Marthe-Sur-Le-Lac&cp=J0N1P0'
                href = row[0].find('a').attrs['href']
                args = href.split('?')[-1]
                pc = args.split('&')[-1].split('=')[-1]  # cp=J0N1P0
            except Exception:
                logging.error(f"can't parse postal code of : {href}")
        return pc

    def parseCity(self, row: list[str]) -> str:
        """
        parseCity read the city in the name a tag.
        Data from 2000 up to 2011 don't have an a tag in the name and therefore
        no city. Also parse the malformed URL unicode into proper utf-8 character.

        Parameters
        ----------
        row : list[str]
            list of td tag element

        Returns
        -------
        str
            city name of the donator
        """
        city = ""
        if (row[0].find('a') is not None):
            try:
                # ?idrech=202553&an=2020&fkent=00079&v=Sainte-Marthe-Sur-Le-Lac&cp=J0N1P0'
                href = row[0].find('a').attrs['href']
                args = href.split('?')[-1]
                # v=Sainte-Marthe-Sur-Le-Lac
                city = args.split('&')[-2].split('=')[-1]
                city = self.cleanCityStr(city)
            except Exception:
                logging.error(f"can't parse city of : {href}")
        return city

    def cleanCityStr(self, city: str) -> str:
        """
        cleanCityStr replacing malformed URL unicode to utf-8 readable characters 


        Parameters
        ----------
        city : str
            _description_
        """
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

        city = replace_unicode(city)
        city = remove_duplicate_dash(city)
        city = city[0].upper() + city[1:].lower()
        return city

    def savePage(self, outputPath: str, year: str):
        """
        savePage saving page to csv using pandas

        Parameters
        ----------
        outputPath : str
            Directory where the data will be save (might not work with windows path)
        year : str
            fiscal year name used to create sub directory
        """
        tempPath = outputPath + f"{year}/"
        path = tempPath + f"data_p{self.pageNumber}.csv"
        df = pd.DataFrame(self.data, columns=self.header)
        self.createOutputFile(tempPath)
        df.to_csv(path)

    def createOutputFile(self, path: str):
        """
        createOutputFile Create all sub directory if it doesn't exist.

        Works with linux and macOS path. Might not work with windows path

        Parameters
        ----------
        path : str
            path directory
        """
        if(not os.path.exists(path)):
            os.makedirs(path)

    @staticmethod
    def concatOutputCsv(outputPath: str, years: list[str], delete=True):
        """
        concatOutputCsv : concatenate all csv in the outputpath directory into one csv

        Works with linux and macOS path. Might not work with windows path

        Parameters
        ----------
        outputPath : str
            path directory 
        years : str
            list of subdirectory to look in.
        delete : bool
            if true, delete all temporary subdirectory and csv used for concatenation.
        """
        paths = []
        numP = 0
        for year in years:
            pathY = glob.glob(outputPath + f"{year}/" + f"data_p*.csv")
            paths.append(pathY)
            numP += len(pathY)

        # flatten list [[p1, p2, p3], [p4, p5, p6] ... ] => [p1, p2, p3, p4, p5, p6, ...]
        paths = list(itertools.chain(*paths))
        dfs = []
        for path in paths:
            df = pd.read_csv(path, index_col=0)
            dfs.append(df)

        all_df = pd.concat(dfs)
        all_df.to_csv(outputPath + "data.csv", index=False)

        if delete:
            # delete files
            for path in paths:
                if (os.path.exists(path)):
                    os.remove(path)

            # delete temps folder for each process
            for year in years:
                subPath = outputPath + f"{year}"
                if (os.path.exists(subPath)):
                    os.rmdir(subPath)


if __name__ == "__main__":

    outputPath = "../output/testFixMultiAllData/"
    htmls = []
    for i, htmlPage in enumerate(htmls):
        pageScrapper = DonationParser(htmlPage, i+1)
        pageScrapper.extract()
        pageScrapper.savePage(outputPath)

    years = [str(y) for y in range(2000, 2023)]
    DonationParser.concatOutputCsv(outputPath, years, delete=False)
