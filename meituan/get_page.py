import requests
import urllib3
from json import dumps, loads

urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.26 Safari/537.36',
    # 'x-requested-with': 'XMLHttpRequest',
    # 'Cookie': '__mta=219045798.1595839108006.1595839332974.1595839617482.3; uuid=5b7df77ca8a94a45a6d4.1595835836.1.0.0; _lxsdk_cuid=1738f3a6d71c8-099b2d23bca51a-63557029-1fa400-1738f3a6d71c8; rvct=1%2C10; IJSESSIONID=1kj616rcw59hro0m9v4p3sqnm; iuuid=1E3D4482231A44F5BE875308E1811E23F13A06B4E2FD06D3FABDD88345A4FC6E; _lxsdk=1E3D4482231A44F5BE875308E1811E23F13A06B4E2FD06D3FABDD88345A4FC6E; webp=1; ci3=1; __utma=74597006.115267133.1595839100.1595839100.1595839100.1; __utmc=74597006; __utmz=74597006.1595839100.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); client-id=5d7850da-f171-49f3-a5c5-733d84b02a61; _hc.v=031c25b1-fc38-0d72-10e8-a7f8fee2046c.1595839108; logan_custom_report=; latlng=; ci=42; cityname=%E8%A5%BF%E5%AE%89; __utmb=74597006.11.9.1595839616563; i_extend=C_b1Gimthomepagecategory11H__a; meishi_ci=42; cityid=42; logan_session_token=l1tc3xyh5zlq5ew7y824; _lxsdk_s=1738f681184-de4-42f-7c7%7C%7C138'
}


def get_uuid_page(uuid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4209.3 Safari/537.36',
        'Referer': 'https://sh.meituan.com/jiankangliren/c74b5/pn5/',
        'Origin': 'https://sh.meituan.com',
        'Host': 'apimobile.meituan.com',
        'Cookie': f'uuid={uuid}'
    }
    url = "https://apimobile.meituan.com/group/v4/poi/pcsearch/10"  # 后缀城市
    data = {
        'uuid': uuid,
        'userid': '-1',
        'limit': '32',
        'offset': '32',  # 变量  页数
        'cateId': '74',  # 变量  类型
        'areaId': '5',  # 变量   区号
    }
    reqs = requests.get(url, params=data, headers=headers, verify=False, timeout=5)
    print(reqs.text)


def get_page(url, uuid=''):
    if not uuid:
        url = "https://bj.meituan.com/jiankangliren/b14/pn1/"
    reqs = requests.get(url, headers=headers, verify=False, timeout=5)
    js_nr = str(reqs.text).split("window.AppData = ")[1].split(';</script>')[0]
    print(js_nr)
    js_dum = loads(js_nr)
    uuid = js_dum['poiParam']['uuid']
    get_uuid_page(uuid)


def get_meishi():
    headers = {
        'x-requested-with': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4209.3 Safari/537.36',
        'Origin': 'http://meishi.meituan.com',
        'Referer': 'http://meishi.meituan.com/i/?ci=45&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
        'Cookie': 'ci=1; uuid=73b17a5f-c45e-4ceb-a1a5-500a1b1fbe80',

    }
    url = "http://meishi.meituan.com/i/api/channel/deal/list"
    data = {
        "platform": 3,
        "partner": 126,
        "riskLevel": 1,
        "optimusCode": 10,
        "originUrl": "http://meishi.meituan.com/i/?ci=1&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",  # ci代表城市
        "offset": 0,  # 翻页
        "limit": 50,  # 一页最多显示 50条
        "cateId": 1,
        "lineId": 0,
        "stationId": 0,
        "areaId": 0,
        "sort": "default",
    }

    reqs = requests.post(url=url, data=dumps(data), headers=headers, verify=False, timeout=5)
    print(reqs.json()['data']['poiList'])
    for i in reqs.json()['data']['poiList']['poiInfos']:
        print(i['name'])


# get_page(url='')


# get_uuid_page(uuid='')
# get_meishi()

def get_meishi_two():
    url = "https://bj.meituan.com/meishi/api/poi/getPoiList"
    data = {
        'cityName': '北京',
        'cateId': '0',
        'areaId': '14',
        # 'sort': '',
        # 'dinnerCountAttrId': '',
        'page': '5',
        # 'userId': '',
        'uuid': '137631d0-4e35-431e-ac6d-a1305d81f8f0',
        'platform': '1',
        'partner': '126',
        'originUrl': 'https://bj.meituan.com/meishi/b14/pn5/',
        'riskLevel': '1',
        'optimusCode': '10',
        '_token': 'eJxdT8tugkAU/ZfZSmAGeSddAEp5SAWfoHGhlAJSKM4gKE3/vdNEN01uch73LM75Bth5BxqCUIWQAV2KgQYQC1kJMKAl9COqosqL8liAvMqA5J83FhhwwpsJ0PYyQowqqYc/Y0H1Hqk8ZBBU4IF5coFyXqBHU9WKhiiWDzw+sH1qn1ahLUiR1ZSlbv85rKDXl3popKbcuNm9uuexab05XmmTwDeX9i4wZH00EMGNlIlUGLdZIMR4MxKwnQpwQ+qrbce3rRRyW161pL77wFxdKn00ddypT8IovazPJCxlp0vjYk7mSmaWSrLCswy7+I6aTGlFMS76cfs645vh7J+WdlxEb0mId0GMh2NoXbraM0R56kuRjlBzScSF5VnlqIMo4st1EOovdNXJoStB3rYN0TiO5GyVFu31WLPJV8VRTvKCozFw+PkFy4B7IA==',
    }
    headers = {
        # 'Host': 'bj.meituan.com',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400',
        'Referer': 'https://bj.meituan.com/meishi/b14/pn5/',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'ci=1; uuid=9260d748e1d34c3783ed.1595924404.1.0.0',
        # 'Connection': 'keep-alive',
    }
    reqs = requests.get(url, params=data, headers=headers, verify=False)
    print(reqs.text)

def get_meishi_thre():
    # url = "https://as.meituan.com/meishi/c17b2496/pn2/"
    # url = "https://as.meituan.com/meishi/c17b2496/pn1/"
    url = 'https://bj.meituan.com/meishi/c11b4750/pn11/'
    headers = {
        # 'Cookie': '_lxsdk_cuid=1738f3168d78-0fdb04212f442-335f4b7b-1fa400-1738f3168d8c8; _lxsdk=1738f3168d78-0fdb04212f442-335f4b7b-1fa400-1738f3168d8c8; _hc.v=776b8631-a558-96eb-f70a-88e9075ff599.1595835248; client-id=c65a6d4c-92e7-4f2f-b86c-7b287c5e326e; uuid=a076f727-bd5b-457c-a928-09e6aadfc065; ci=151; rvct=151%2C1%2C238%2C197%2C1204%2C42%2C10; __mta=175495069.1595928278119.1595928278119.1595928278119.1; lat=41.112438; lng=122.993076; _lxsdk_s=17394663798-34b-6d-af%7C%7C77',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400',
        'Referer' :'https://as.meituan.com/meishi/c17b2496/',
    }
    reqs = requests.get(url, headers=headers, verify=False)
    print(str(reqs.text).split("window._appState = ")[1].split(';</script>')[0])


# get_meishi_two()
# get_meishi_thre()

def get_meituan_other():
    data = {
        # 'uuid': '5de531c3957240059514.1596090646.1.0.0',
        'userid': '-1',
        'limit': '32',
        'offset': '0',
        'cateId': '52',
        'areaId': '5',
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400',
        'Referer': 'https://sh.meituan.com/xiuxianyule/',
        'Cookie': '_lxsdk_cuid=1739ea626f9c8-0241da30d13e41-6e557028-1fa400-1739ea626f9c8'
    }
    reqs = requests.get(url="https://apimobile.meituan.com/group/v4/poi/pcsearch/10", headers=header, params=data, verify=False)
    print(reqs.text)
    print(reqs.cookies)
get_meituan_other()