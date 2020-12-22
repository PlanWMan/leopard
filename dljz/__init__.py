import base64

# print(base64.b64encode("mink"))
print(base64.b64encode(("海南海产市场").encode()))  # 5LiK5rW35pmu6YGT56eR5oqA
# print(base64.b64encode(("上海普道科技").encode()))
print(f's0k{base64.b64encode(("海南海产市场").encode()).decode()}p0')
# s0k5rW35Y2X5rW35Lqn5biC5Zy6p0

# Base64.encode(keywords)
from urllib.parse import quote

keyword = (quote("上海", encoding='gb2312'))

import requests

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.26 Safari/537.36',
#     'Content-Type': 'application/x-www-form-urlencoded'
# }
#

# print(keyword)
# data = {
#     'Keyword': keyword,
#     'Country': '0',
#     'province': '0',
#     'city': '0',
#     'Lb': '0',
#     'Buy_Type': '9',
# }
# from json import loads
# data = 'Keyword=%C9%CF%BA%A3&Country=0&province=0&city=0&Lb=0&Buy_Type=9'
#
# reqs = requests.post(url, data=data, headers=headers, allow_redirects=False)
# print(reqs.headers)


url = "https://www.b2b168.com/Index.aspx"
data = {
    'q': '深圳宝博电子科技有限公司',
    'act': 'ComSearch',
    'page': '',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.26 Safari/537.36',

}
reqs = requests.post(url, data=data, headers=headers, allow_redirects=False, verify=False)
print(reqs.text)
