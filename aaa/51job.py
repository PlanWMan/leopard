from urllib.parse import quote
# print(quote("平安国际融资租赁有限公司", encoding='gb23312'))
import requests
import time
import urllib3
req_session = requests.session()
urllib3.disable_warnings()
# 先用推荐看看是否有公司
url = "https://kwdsrv.51job.com/KwdSrvByKey/default.aspx"
t = time.time()
data = {
    'src': '51joball',
    'kwd': '平安国际融资租赁有限公司',
    '_': (int(round(t * 1000)))
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.8 Safari/537.36',
    'Referer':'https://search.51job.com/list/000000,000000,0000,00,9,99,java%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=',
    'Accept': 'application/json, text/javascript, */*;'
}

print()
reqs = req_session.get(url=url, params=data, headers=headers, verify=False)
print(reqs.text)
url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{quote("平安国际融资租赁有限公司")},2,1.html'
reqs = req_session.get(url=url, headers=headers, verify=False)
print(reqs.text)