from selenium import webdriver
from lxml import etree

import urllib3

urllib3.disable_warnings()
driver = webdriver.Chrome('D:/tool/chromedriver_win32/chromedriver.exe')
cookies = {
    'value': 'think%3A%7B%22username%210293%31628193MDAwMDAwMLOGpZaIudFqhc6Gl7LQetmZtmfOk2RhbQ%22%2C%22expire%sfdaaswMDAwMDAwMLOGud6Gqb-whbiCmLOmdZ4%22%2C%22token%22%3A%22MDAwMDAwMDAwMMurrpWavLehhs1-3LLfgduEt4OWepuo123456123KZq6HQxtOK0ZCme5p-q6iZu2yrn4uNhJ3KedDYk7ivboS4it6910926YW0%22%7D',
    'name': 'ketangpai_home_remember'}

driver.add_cookie(cookie_dict=cookies)
reqs = driver.get("https://www.ketangpai.com/Main/index.html")
resq = etree.HTML(reqs.text)
print(resq.xpath('//a/@title'))

