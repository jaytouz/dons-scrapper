import logging
from datetime import datetime
import os


# local package
from src.runner.process import DonationScrapperRunner
from src.scrapper.enums import PoliticalPartiesValues, LeadershipCandidateValues


def main():
    outputDir = "../output/allDataSingleProcess_03_03_2022/"
    now = datetime.now().strftime("%Y_%m_%d_%H_%M")
    if(not os.path.exists(outputDir)):
        os.makedirs(outputDir)
    logging.basicConfig(filename=outputDir + f"donation_scrapper_{now}.log",
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        encoding='utf-8', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    runner = DonationScrapperRunner(
        outputDir)
    runner.singleProcessRun(delete=True)


    #["2017", "2018", "2019", "2020", "2021", "2022"]
if __name__ == "__main__":
    main()
