"""
使用aiohttp 爬取纵横的网站 异步存入mongodb
"""

import aiohttp
import asyncio
import logging
from lxml import etree
from motor.motor_asyncio import AsyncIOMotorClient


from urllib.parse import urljoin


class AioZongheng(object):
    def __init__(self):
        # super.__init__()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s:%(message)s')
        self.INDEX_URL = 'http://edu.sh.gov.cn/web/xxgk/lastInfo_list.html?page=%s'
        self.PAGE_NUMBER = 10
        self.CONCURRENCY = 3
        self.semaphore = asyncio.Semaphore(self.CONCURRENCY)
        self.session = None
        self.headers = {
            'Referer': 'http://edu.sh.gov.cn/web/xxgk/lastInfo_list.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4122.7 Safari/537.36',
            'Cookie': 'UqZBpD3n3iXPAw1X9Bm4iXSKVeIXy5VDfdzH9YaHvUKaQzLNGOnb/mvUwA@@=v1IsExJQSDNu/; Hm_lvt_297b8768d7cb190436f209f6a2a1630b=1590327779; Hm_lpvt_297b8768d7cb190436f209f6a2a1630b=1590327800'
        }
        self.MONGO_STRING = 'mongodb://localhost:27017'
        self.MONGO_DB_NAME = 'books'
        self.MONGO_COLLECTION_NAME = 'books'
        self.collection = AsyncIOMotorClient(self.MONGO_STRING)[self.MONGO_DB_NAME][self.MONGO_COLLECTION_NAME]

    async def scrapy_api(self, url):
        """
        获取列表的数据
        :param url: 列表页url
        :return:
        """
        async with self.semaphore:
            try:
                logging.info('scraping %s', url)
                async with self.session.get(url, headers=self.headers) as response:
                    return await response.text()
            except aiohttp.ClientError:
                logging.error('error occurred while scraping %s', url, exc_info=True)

    async def scrape_index(self, page):
        """
        列表页翻页
        :param page:
        :return:
        """
        url = self.INDEX_URL % (page)
        return await self.scrapy_api(url)

    async def main(self):
        self.session = aiohttp.ClientSession()
        tasks = [asyncio.ensure_future(self.scrape_index(page)) for page in range(1, self.PAGE_NUMBER)]
        results = await asyncio.gather(*tasks)
        logging.info('result %s', results[:100])
        # 构建所有详情页的task
        ids = []
        for index_data in results:
            if not index_data: continue
            et_req = etree.HTML(index_data)
            liss = [urljoin(self.INDEX_URL, i) for i in et_req.xpath('//ul[@class="list-cell2 blur border_b"]//li/a/@href')]
            ids += liss
        tasks = [asyncio.ensure_future(self.scrape_detail(url)) for url in ids]
        await asyncio.wait(tasks)
        await self.session.close()

    async def save_data(self, data):
        logging.info('saving data %s', data)
        if data:
            return await self.collection.insert_one(data)

    async def scrape_detail(self, url):
        data = await self.scrapy_api(url)
        et_req = etree.HTML(data)
        name = (et_req.xpath('//div[@id="ivs_title"]/span/text()')[0]).strip()
        # nums = (et_req.xpath('//div[@class="nums"]/text()')[0]).strip()
        new_data = {
            'name': name,
            # 'nums': nums
        }
        await self.save_data(new_data)

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.main())


if __name__ == '__main__':
    AioZongheng().start()
    # import requests
    # from lxml import etree
    #
    # headers = {
    #     'Referer': 'http://www.zongheng.com/rank/details.html?rt=1&d=1',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4122.7 Safari/537.36',
    #     'Cookie': 'ZHID=B6DC912C2391BDAA94F8E1C8A74775CE; ver=2018; zh_visitTime=1590321869294; zhffr=0; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221724691f22b299-0ddca934cf17a9-6857772b-2073600-1724691f22c2a7%22%2C%22%24device_id%22%3A%221724691f22b299-0ddca934cf17a9-6857772b-2073600-1724691f22c2a7%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; v_user=%7Chttp%3A%2F%2Fwww.zongheng.com%2F%7C57198939; Hm_lvt_c202865d524849216eea846069349eb9=1590321869; Hm_up_c202865d524849216eea846069349eb9=%7B%22uid_%22%3A%7B%22value%22%3A%22B6DC912C2391BDAA94F8E1C8A74775CE%22%2C%22scope%22%3A1%7D%7D; JSESSIONID=abcerkEo9fhpWdVTFKgjx; Hm_lpvt_c202865d524849216eea846069349eb9=1590321932'
    # }
    # INDEX_URL = 'http://edu.sh.gov.cn/html/xxgk/202005/403012020003.html'
    #
    # reqs = requests.get(INDEX_URL)
    # et_req = etree.HTML(reqs.text)
    # ids = []
    # print(ids)
    # print()
    # print()
    #
    # rees = et_req.xpath('//div[@class="rank_d_book_intro fl"]')
    # for i in rees:
    #     print(i.xpath('.//div[@class="rank_d_b_name"]/@title'))
    #     print(i.xpath('.//div[@class="rank_d_b_cate"]/@title'))
    #     print(i.xpath('.//div[@class="rank_d_b_last"]/@title'))
