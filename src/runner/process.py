from ..runner import SearchPageQcDonator


class DonationScrapperRunner(object):

    def __init__(self, scrapper):
        self.scrapper = scrapper

    def query():
        pass


if __name__ == "__main__":

    years = []

    parties = []
    members = [IndependantMembersValues.CATHERINE_FOURNIER]
    candidates = [IndependantCandidatesValues.CLAUDE_SURPRENANT]
    races = [LeadershipRaceValues.PCQ_2021]
    leaders = [LeadershipCandidateValues.ERIC_DUHAIME]

    scrapper = SearchPageQcDonator()
    scrapper.query(years=years, parties=parties)
    # scrapper.parseResults()
    outputPath = ".../output/multipoool/"

    htmls = scrapper.getAllHtmlPage()

    for i, htmlPage in enumerate(htmls):
        pageScrapper = DonationScrapper(htmlPage, i+1)
        pageScrapper.extract()
        pageScrapper.savePage(outputPath)

    DonationScrapper.concatOutputCsv(outputPath)

    input("PARSING DONE...")
    del(scrapper)
    input("QUITTING...")
