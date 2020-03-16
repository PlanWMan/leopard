import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
from scrapy.cmdline import execute


execute(['scrapy', 'crawl', 'guazi'])
