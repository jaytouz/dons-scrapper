import logging

# local package
from src.runner.process import DonationScrapperRunner
from src.scrapper.enums import PoliticalPartiesValues, LeadershipCandidateValues


def main():
    logging.basicConfig(filename='../output/multiprocess/multiThread.log',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        encoding='utf-8', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    runner = DonationScrapperRunner(
        "../output/multiprocess/", years=["2022", "2021", "2020", "2019"], parties=[PoliticalPartiesValues.PCQ_CPQ, PoliticalPartiesValues.PLQ_QLP])
    runner.run(poolSize=4)


if __name__ == "__main__":
    main()
