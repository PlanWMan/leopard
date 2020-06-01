"""
获取ip3366的ip代理
"""

from mydistributed.myproxpool.crawlers.base import BaseCrawler
from mydistributed.myproxpool.schemas.proxy import Proxy
import re

MAX_PAGE = 5
BASE_URL = 'http://www.ip3366.net/free/?stype=1&page={page}'  # 获取ip的连接


class IP3366Crawler(BaseCrawler):
    """
    ip3366
    """
    urls = [BASE_URL.format(page=i) for i in range(1, 8)]

    def parse(self, html):
        """
        解析html
        :param html:
        :return:
        """
        ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
        re_ip_address = ip_address.findall(html)
        for address, port in re_ip_address:
            proxy = Proxy(host=address.strip(), port=int(port.strip()))
            yield proxy


if __name__ == '__main__':
    crawler = IP3366Crawler()
    for proxy in crawler.crawl():
        print(proxy)
