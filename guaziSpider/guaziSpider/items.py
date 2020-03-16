# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarListItem(scrapy.Item):
    carId = scrapy.Field()
    carName = scrapy.Field()
    carMoney = scrapy.Field()
    carMoneyOrigin = scrapy.Field()
    carTime = scrapy.Field()
    carPL = scrapy.Field()
    carType = scrapy.Field()
    carJbcs = scrapy.Field()
    carKilometres = scrapy.Field()
    carJcbg = scrapy.Field()
    carLink = scrapy.Field()
    cimage_urls = scrapy.Field()
    cimages = scrapy.Field()
