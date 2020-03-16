# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from time import sleep
# from selenium import webdriver
from scrapy.http import HtmlResponse

ua = UserAgent(verify_ssl=False)


class GuazispiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GuazispiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # request.cookies = {
        #     'antipas': '291A5514J7948800o9N2589102',
        #     'uuid': '0eab0734-7f6a-4e22-b653-db379a7cd003',
        #     'cityDomain': 'hz',
        #     'clueSourceCode': '%2A%2300',
        #     'cainfo': '%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%220eab0734-7f6a-4e22-b653-db379a7cd003%22%2C%22ca_city%22%3A%22hz%22%2C%22sessionid%22%3A%221729768c-85ac-43f5-b824-a4ad1d360c11%22%7D',
        #     'user_city_id': '26',
        #     'preTime': '%7B%22last%22%3A1584006110%2C%22this%22%3A1584006110%2C%22pre%22%3A1584006110%7D',
        #     'ganji_uuid': '2096112643603810431187',
        #     'sessionid': '1729768c-85ac-43f5-b824-a4ad1d360c11',
        #     'Hm_lvt_936a6d5df3f3d309bda39e92da3dd52f': '1584006112',
        #     'Hm_lpvt_936a6d5df3f3d309bda39e92da3dd52f': '1584006112',
        #     'lg': '1',
        #     'lng_lat': '120.19422_30.25514',
        #     'gps_type': '1',
        # }

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class SeleniumMiddleware(object):
    '''
    调用selenium请求cookie考虑到资源问题只在请求首页的时候使用
    把cookie写入到文件夹保存
    '''
    def __init__(self):
        super(SeleniumMiddleware, self).__init__()
        file = open("./cookies.txt", "r")
        self.cookie_text = file.readline()

    def process_request(self, request, spider):
        if spider.name == 'guazi':
            request.headers[
                "User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
            if self.cookie_text:
                request.headers["Cookie"] = self.cookie_text
        return None

    def process_response(self, request, response, spider):
        '''
        # selenium请求了网页 获得的Response 因此process_request不需要再返回Request给Downloader
        # request: 响应对象所对应的请求对象
        # response: 拦截到的响应对象
        # spider: 爬虫文件中对应的爬虫类 WangyiSpider 的实例对象, 可以通过这个参数拿到 WangyiSpider 中的一些属性或方法
        '''
        if response.status != 200:
            # 获取新的cookie
            spider.browser.get(url=request.url)
            sleep(2)  # 延时3s 待网页完全加载
            cook = "; ".join(["%s=%s" % (cookie['name'], cookie['value']) for cookie in spider.browser.get_cookies()])
            row_response = spider.browser.page_source
            with open("./cookies.txt", 'w') as file_object:
                file_object.write(cook)
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)
        else:
            return response

    # 请求出错了的操作, 比如ip被封了,可以在这里设置ip代理
    def process_exception(self, request, exception, spider):
        pass
        # print("添加代理开始")
        # ret_proxy = get_proxy()
        # request.meta["proxy"] = ret_proxy
        # print("为%s添加代理%s" % (request.url, ret_proxy), end="")
        # return None
