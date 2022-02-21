import logging
from datetime import datetime

# local package
from src.runner.process import DonationScrapperRunner
from src.scrapper.enums import PoliticalPartiesValues, LeadershipCandidateValues


def main():
    outputDir = "../output/fulldata/"
    now = datetime.now().strftime("%Y_%m_%d_%H_%M")
    if(not os.path.exists(outputDir)):
        os.makedirs(outputDir)
    logging.basicConfig(filename=outputDir + f"donation_scrapper_{now}.log",
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        encoding='utf-8', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    runner = DonationScrapperRunner(
        "../output/multiprocess/", years=[], parties=[])
    runner.run()


if __name__ == "__main__":
    main()
