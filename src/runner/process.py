import logging
from multiprocessing.pool import ThreadPool
import os
from multiprocessing import Pool, cpu_count, Process
from threading import Thread
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait
from concurrent import futures
import math


from ..scrapper.searchPage import SearchPageQcDonator
from ..parser.donation import DonationParser


class DonationScrapperRunner(object):
    """
    DonationScrapperRunner Object managing multiprocessing scrapping. Each process
    will be a google chrome headless window.

    """

    def __init__(self, outputPath: str, years: list[str] = None, parties: list[str] = None, members: list[str] = None, candidates: list[str] = None, races: list[str] = None, leaders: list[str] = None):
        """
        For specific query, make sure to use the values encoded in scrapper.enums.

        If all params are None, the default website search parameter are used.(All years and all parties)

        Parameters
        ----------
        outputPath : str
            Directory path where the data will be saved (Not tested with windows path)
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
        self.outputPath = outputPath
        self._years = years
        self._parties = parties
        self._members = members
        self._candidates = candidates
        self._races = races
        self._leaders = leaders
        self._processes = []

    @property
    def years(self):
        if self._years is None or self._years == []:
            return [str(y) for y in range(2000, 2022+1)]
        else:
            return self._years

    @property
    def parties(self):
        return self._parties

    @property
    def members(self):
        return self._members

    @property
    def candidates(self):
        return self._candidates

    @property
    def races(self):
        return self._races

    @property
    def leaders(self):
        return self._leaders

    @property
    def processes(self):
        return self._processes

    def append(self, p):
        self._processes.append(p)

    def join(self):
        for p in self.processes:
            p.join()

    def close(self):
        for p in self.processes:
            p.close()

    def run(self, poolSize: int = None, delete=False):
        """
        run : start a pool of process where each year will be process sequentially as a seperate query.

        Parameters
        ----------
        poolSize : int, optional
            If None, use number of cpu - 2, by default None
        """
        if poolSize is None:
            poolSize = os.cpu_count() - 2
            if poolSize < 1:
                poolSize = 1
        if poolSize > len(self.years):
            poolSize = len(self.years)
        logging.info(f"starting pool with {poolSize} processes...")

        with ProcessPoolExecutor(poolSize) as executor:
            executor.map(self.process_data, self.years)

        logging.info("concatenating data...")
        DonationParser.concatOutputCsv(
            self.outputPath, self.years, delete=delete)
        print("Done...")

    def process_data(self, year):
        """
        process_data: Sequential task used to parallelize the work.

        Each process query the specifed data for 1 year, saves it in a temp sub directory

        Parameters
        ----------
        year : str
            fiscal year to query
        """
        logging.info(f"starting {year}")
        scrapper = SearchPageQcDonator(year)
        logging.info(f"querying {year}")
        scrapper.query(years=year, parties=self.parties, members=self.members,
                       canditates=self.candidates, races=self.races, leaders=self.leaders)

        logging.info(f"getting all html for {year}")

        htmls = scrapper.getAllHtmlPage()
        scrapper.driver.quit()
        for i, htmlPage in enumerate(htmls):
            pageScrapper = DonationParser(htmlPage, i+1)
            pageScrapper.extract()
            pageScrapper.savePage(self.outputPath, year)


if __name__ == "__main__":

    # runner = DonationScrapperRunner()
    # runner.run()

    # scrapper = SearchPageQcDonator
    pass
