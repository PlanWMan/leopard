import requests
from lxml import etree
import urllib3

urllib3.disable_warnings()
url = 'https://sh.sydc.anjuke.com/shangban/loupan/?keywords=%E6%B5%A6%E4%B8%9C'
# url = "https://sh.sydc.anjuke.com/xzl-zu/pudongxinqu/"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4181.9 Safari/537.36',
}
A = 0
while True:
    A +=1
    print(A)
    reqs = requests.get(url, headers=headers, verify=False)
    resq = etree.HTML(reqs.text)
    print(resq.xpath('//li[@class="list-item"]//span[@class="comm-address"]/@title'))
