# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json, pymongo

from hashlib import md5
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from guaziSpider.items import CarListItem


class FilePipeline(object):
    def __init__(self):
        self.file = open('papers.json', 'w')  # wb是二进制的会报错

    def process_item(self, item, spider):
        if item['title']:
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line)
            return item
        else:
            raise DropItem("missing title in %s" % item)


class MyImagesPipeline(ImagesPipeline):
    # 可以重写images管道中的方法，比如命名
    def file_path(self, request, response=None, info=None):
        image_guid = md5(request.url.encode()).hexdigest()
        return 'full/%s.jpg' % (image_guid)


class GuaZiMongoPipline(object):
    '''
    储存到mongodb
    '''
    def __init__(self, mongo_host, mongo_db, replicaset, MONGO_COLL):
        self.mongo_host = mongo_host
        self.mongo_db = mongo_db
        self.MONGO_COLL = MONGO_COLL

        self.replicaset = replicaset

    @classmethod
    def from_settings(cls, settings):
        return cls(
            mongo_host=settings['MONGO_HOST'],
            mongo_db=settings['MONGO_DB'],
            replicaset=settings['MONGO_PORT'],
            MONGO_COLL=settings['MONGO_COLL']

        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host)
        self.db = self.client[self.mongo_db]
        carInfo = self.db[self.MONGO_COLL]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, CarListItem):
            self._process_carList_item(item)
        else:
            self._process_carDetail_item(item)
        return item

    def _process_carList_item(self, item):
        '''
        处理汽车信息
        :param item:
        :return:
        '''
        item['carId'] = str(item['carLink']).split('/')[-1].split('.')[0]
        item['carMoney'] = str(item['carMoney']).strip()
        self.db.carInfo.insert(dict(item))

    def _process_carDetail_item(self, item):
        '''
        处理汽车信息
        :param item:
        :return:
        '''
        self.db.carHot.insert(dict(item))
