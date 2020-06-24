import re
import requests
import random
import urllib3
import urllib.request
urllib3.disable_warnings()
#获取url_list,就是所有的图片链接
def get_url(url):
    response = requests.get(url, verify=False)
    response.encoding='utf-8'
    url_addr = r'<img src="(.*?)" alt=".*?" border="0"/>'
    url_list = re.findall(url_addr,response.text)
 ##   print(url_list)
    return url_list

#下载保存所有的图片
def get_GIF(url,a):
    # response = requests.get(url, verify=False)
    img_path = f'./{"".join(str(random.choice(range(10))) for _ in range(10))}.gif'  # 随机十位数字用来命名图片
    urllib.request.urlretrieve(url, img_path)

    # with open(img_path,'wb') as file:
    #     file.write(response.content)

#程序开始
if __name__=='__main__':
    url = 'http://qq.yh31.com/ql/ls/'
    url_list = get_url(url)
    a = 1
    for url in url_list:
        url = 'http://qq.yh31.com' + url
        print(url)
        get_GIF(url, a)
        a += 1
