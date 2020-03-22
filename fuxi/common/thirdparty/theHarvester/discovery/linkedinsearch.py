from fuxi.common.thirdparty.theHarvester.discovery.constants import *
from fuxi.common.thirdparty.theHarvester.lib.core import *
from fuxi.common.thirdparty.theHarvester.parsers import myparser
import asyncio


class SearchLinkedin:

    def __init__(self, word, limit):
        self.word = word.replace(' ', '%20')
        self.results = ""
        self.totalresults = ""
        self.server = 'www.google.com'
        self.quantity = '100'
        self.limit = int(limit)
        self.counter = 0
        self.proxy = False

    async def do_search(self):
        urly = 'http://' + self.server + '/search?num=100&start=' + str(self.counter) + '&hl=en&meta=&q=site%3Alinkedin.com/in%20' + self.word
        try:
            headers = {'User-Agent': Core.get_user_agent()}
            resp = await AsyncFetcher.fetch_all([urly], headers=headers, proxy=self.proxy)
            self.results = resp[0]
            if await search(self.results):
                try:
                    self.results = await google_workaround(urly)
                    if isinstance(self.results, bool):
                        print('Google is blocking your ip and the workaround, returning')
                        return
                except Exception:
                    # google blocked, no useful result
                    return
        except Exception as e:
            print(e)
        await asyncio.sleep(getDelay())
        self.totalresults += self.results

    async def get_people(self):
        rawres = myparser.Parser(self.totalresults, self.word)
        return await rawres.people_linkedin()

    async def get_links(self):
        links = myparser.Parser(self.totalresults, self.word)
        return await splitter(await links.links_linkedin())

    async def process(self, proxy=False):
        self.proxy = proxy
        while self.counter < self.limit:
            await self.do_search()
            await asyncio.sleep(getDelay())
            self.counter += 100
            print(f'\tSearching {self.counter} results.')