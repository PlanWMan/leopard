# -*- coding: utf-8 -*-
import os

# Scrapy settings for guaziSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'guaziSpider'

SPIDER_MODULES = ['guaziSpider.spiders']
NEWSPIDER_MODULE = 'guaziSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'guaziSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'guaziSpider.middlewares.GuazispiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'guaziSpider.middlewares.RandomUserAgentMiddleware': 543,
    'guaziSpider.middlewares.SeleniumMiddleware': 300,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
# 对文件下载的配置
project_dir = os.path.abspath(os.path.dirname(__file__))
FILES_STORE = os.path.join(project_dir, "files")  # 下载地址
FILES_URLS_FIELD = 'file_urls'  # 这里对应着item.py文件中的字段
FILES_RESULT_FIELD = 'files'  # 同样对应item.py文件中的字段
# 120 days of delay for files expiration
FILES_EXPIRES = 30

# 对图片下载的配置
IMAGES_STORE = os.path.join(project_dir, "images")  # 路径
IMAGES_URLS_FIELD = "cimage_urls"
IMAGES_RESULT_FIELD = "cimages"
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}  # 设置图片大小
IMAGES_EXPIRES = 30  # 过期时间

# redis配置
# 使用scrapy_redis的调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后回复
SCHEDULER_PERSIST = True
# 设置重爬
# SCHEDULER_FLUSH_ON_START = True
# 使用redis的去重方式
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
LOG_LEVEL = 'DEBUG'

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'guaziSpider.pipelines.FilePipeline': 1,
    # 'guaziSpider.pipelines.MyImagesPipeline': 1,
   'scrapy_redis.pipelines.RedisPipeline': 100 ,
   'guaziSpider.pipelines.GuaZiMongoPipline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
DOWNLOAD_DELAY = 0.25  # 等待的时间
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


MONGO_HOST = "mongodb://localhost:27017"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "spider_data"  # 库名
MONGO_COLL = "carInfo"  # collection名
# redis配置
REDIS_HOST = 'localhost'
REDIS_POST = '6379'