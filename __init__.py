import requests
reqs = requests.get(url='https://paat1001.b2b.hc360.com/shop/show.html')
print(reqs.url)
print(reqs.status_code)
reqs = requests.get(url="https://www.baidu.com/")
print(reqs.url)
print(reqs.status_code)