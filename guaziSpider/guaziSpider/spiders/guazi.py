# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from guaziSpider.items import CarListItem
from selenium import webdriver

class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['guazi.com']

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="D:/tool_wbw/chromedriver_win32/chromedriver.exe")
        super().__init__()

    def start_requests(self):
        """
        重写start方法触发selenium获取cookie保存cookie
        """
        start_url = 'https://www.guazi.com/sz/dazhong/#bread'
        yield scrapy.Request(url=start_url, callback=self.parse, dont_filter=True)

    def close(self, spider):
        self.browser.quit()

    def parse(self, response):
        '''
        获取瓜子详情url
        翻页
        :param response:
        :return:
        '''
        if response.status == 200:
            cars = response.xpath('//a[@class="car-a"]')
            for car in cars:
                detail_url = urljoin(response.url, car.xpath('./@href').extract_first())  # 详情url
                yield scrapy.Request(url=detail_url, callback=self.parse_detail)
            # 翻页
            next_page = response.xpath('//div[@class="pageBox"]//a[@class="next"]')
            if next_page:
                url_next = next_page.xpath('./@href').extract_first()
                if url_next:
                    yield scrapy.Request(url=urljoin(response.url, url_next), callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        '''
        解析详情页
        :param response:
        :return:
        '''
        if response.status == 200:
            carListItem = CarListItem()
            carListItem['carName'] = str(
                response.xpath('//h2[@class="titlebox"]/text()').extract_first()).strip()  # 汽车名称
            carListItem['carType'] = str(carListItem['carName']).split(' ')[0]
            carListItem['carMoney'] = response.xpath('//span[@class="pricestype"]/text()').extract_first()
            carListItem['carMoneyOrigin'] = response.xpath('//span[@class="originprice"]/text()').extract_first()
            carListItem['cimage_urls'] = response.xpath(
                '//ul[@class="det-picside js-picside"]//img/@data-src').extract()[:3]  # 图片连接
            nr_list = response.xpath('//ul[@class="assort clearfix"]/li/span/text()').extract()
            if len(nr_list) == 4:
                carListItem['carTime'] = nr_list[0]
                carListItem['carKilometres'] = nr_list[1]
                carListItem['carPL'] = nr_list[2]
            else:
                return
            gz_list = response.xpath('//span[@class="fc-org-text"]/preceding-sibling::span[1]/text()').extract()  # 故障
            carListItem['carJcbg'] = [str(gz_l).strip().replace('：', '') for gz_l in gz_list if
                                      len(str(gz_l).strip()) > 1]
            cs_list = response.xpath(
                '//div[@class="detailcontent clearfix js-detailcontent active"]/table[1]//tr')  # 基本参数
            cs_ = {}
            if cs_list[0].xpath('./th/text()').extract_first().find("基本参数") > -1:
                for cs_li in cs_list[1:]:
                    one, two = cs_li.xpath('./td/text()').extract()
                    cs_[one] = two
            carListItem['carJbcs'] = cs_
            carListItem['carLink'] = response.url
            yield carListItem
