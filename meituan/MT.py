import os
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd())))
sys.path.append(path)
import urllib3
import requests
import execjs
from urllib.parse import urlencode
from time import sleep
from Tools.proxy import get_proxy
from json import loads
from address.utils import MongoDao
from multiprocessing import Process
from loguru import logger
from base.UAbase import UA

logger.add("./MT.log",
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
           retention="3 days",
           enqueue=True)

urllib3.disable_warnings()
UA = UA()

headers = {
    'User-Agent': UA.get_header(),
}


def parse_token():
    """
    获取美团的 _token
    """
    originUrl = 'https://sh.meituan.com/meishi/'
    base_url = 'https://sz.meituan.com/meishi/api/poi/getPoiList?'
    params = {
        "areaId": "0",
        "cateId": "0",
        "cityName": '上海',
        "dinnerCountAttrId": '',
        "optimusCode": "10",
        "originUrl": originUrl,
        "page": 3,
        "partner": "126",
        "platform": "1",
        "riskLevel": "1",
        "sort": "",
        "userId": "",
        # "uuid": "0fc358af-a3ea-4562-a9e0-ff7cab9dff01",
    }

    url = base_url + urlencode(params)
    with open('./meituan.js', 'r', encoding='utf-8') as fp:
        js = fp.read()
    ctx = execjs.compile(js)
    token = ctx.call("get_token", url, originUrl)
    return token


def get_citys():
    """
    获取所有城市的名称和链接
    """
    mongo = MongoDao()
    url = "https://www.meituan.com/changecity/"
    reqs = requests.get(url, timeout=5, headers=headers, verify=False)
    if reqs.status_code == 200:
        js_nr = str(reqs.text).split("window.AppData = ")[1].split(';</script>')[0]
        js_dum = loads(js_nr)
        for zm in js_dum['openCityList']:
            for city in zm[1]:
                items = {}
                items['_id'] = city['name']
                items['id'] = city['id']
                items['pinyin'] = city['pinyin']
                items['acronym'] = city['acronym']
                items['rank'] = city['rank']
                items['firstChar'] = city['firstChar']
                print(items)
                # 存入mongo
                print(mongo.insert_mongo(data=items, collection='MT_Citys'))


class MS:
    def __init__(self):
        pass

    def get_requests(self, url, params='', data="", headers=''):
        for num in range(10):
            try:
                proxies = get_proxy(proxy_type='proxy_less')
                if data:
                    resp = requests.post(url, timeout=10, headers=headers, data=data, verify=False, proxies=proxies)
                else:
                    resp = requests.get(url, timeout=10, headers=headers, params=params, verify=False, proxies=proxies)
                if not isinstance(resp, requests.models.Response):
                    sleep(1)
                    continue
                try:
                    if resp.status_code != 200:
                        sleep(0.2)
                        continue
                except:
                    sleep(1)
                    continue
                # 判断是否被封ip
                return resp
            except:
                sleep(1)
                pass

    def get_uuid(self, city_acronym):
        """
        返回uuid 和 ci 参数
        """
        url = f"https://{city_acronym}.meituan.com/"
        reqs = self.get_requests(url, headers=headers, )
        if reqs.status_code == 200:
            return reqs.cookies.get_dict()

    def get_teactid(self, city_acronym, num=1):
        if num > 5:
            return None, None
        try:
            url = f"https://{city_acronym}.meituan.com/meishi/"
            reqs = self.get_requests(url=url, headers=headers)
            if reqs:
                js_nr = str(reqs.text).split("window._appState = ")[1].split(';</script>')[0]
                js_dum = loads(js_nr)
                items = {}
                items_two = {}
                for i in js_dum['filters']['areas']:
                    items[i['id']] = i['name']
                for _ in js_dum['filters']['cates']:
                    items_two[_['id']] = _['name']
                return items, items_two
        except:
            num += 1
            self.get_teactid(city_acronym, num)

    def get_City_Progress(self, CityProgressMd5):
        return self.mongo.find_mongo(find_data={'_id': CityProgressMd5},
                                     collection="MT_City_Progress", cut='one')

    def get_id(self, number):
        self.mongo = MongoDao()
        getType = "美食"
        while True:
            try:
                company_nr = self.mongo.find_update(find_data={'state': 0},
                                                    update_data={'state': 1}, collection="MT_Citys")
                if not company_nr:
                    return
                city_name = str(company_nr.get("_id")).strip()
                # city_id = company_nr.get("id")
                city_acronym = company_nr.get("acronym")
                # 获取 uuid 和 ci 参数
                # uu_itmes = self.get_uuid(city_acronym)
                # if uu_itmes:
                #     uuid = uu_itmes['uuid']
                #     ci = uu_itmes['ci']
                # else:
                #     return None
                headers = {
                    # "Host": "sz.meituan.com",
                    # "Accept": "application/json",
                    "User-Agent": UA.get_header(),
                    "Referer": f"https://{city_acronym}.meituan.com/meishi/",
                    # 'Cookie': f'ci={ci}; uuid={uuid}',
                }
                # 获取区号
                areas, cates = self.get_teactid(city_acronym)
                if not areas or not cates:
                    continue
                success_two = True
                # data_url = f'https://{city_acronym}.meituan.com/meishi/api/poi/getPoiList?'
                for cate in cates.items():
                    cateId = cate[0]
                    cateName = str(cate[1]).strip()
                    if str(cateName).find("代金券") > -1:
                        continue
                    for area_ in areas.items():
                        areaId = area_[0]
                        area = str(area_[1]).strip()
                        CityProgressMd5 = self.mongo.get_md5_by_str(
                            str(city_name) + str(cateName) + str(area) + str(getType))
                        CityProgress = self.get_City_Progress(CityProgressMd5)
                        if CityProgress:
                            continue
                        # payload = {
                        #     "cityName": city_name,
                        #     "cateId": cateId,
                        #     "areaId": area[0],  # 区号
                        #     "page": 2,
                        #     "uuid": uuid,
                        #     "platform": "1",
                        #     "partner": "126",
                        #     "originUrl": f'https://{city_acronym}.meituan.com/meishi/',
                        #     "riskLevel": "1",
                        #     "optimusCode": "10",
                        #     "_token": parse_token()
                        # }
                        # 直接解文件
                        data_url_two = f"https://{city_acronym}.meituan.com/meishi/c{cateId}b{areaId}"
                        try:
                            success = self.get_page_two(data_url_two, city_name, headers, area, number, cateName)
                            # success = self.get_page(data_url, payload, headers, area[1], number, city_acronym, cateName)
                            if not success:
                                success_two = success
                            else:
                                # 直接存储数据
                                newObject = {
                                    '_id': CityProgressMd5,
                                    'city_name': city_name,
                                    'cateName': cateName,
                                    'area': area,
                                    'type': getType,
                                    'update_time': self.mongo.current_time()

                                }
                                self.mongo.insert_mongo(data=newObject, collection="MT_City_Progress")
                        except Exception as e:
                            logger.error(e)
                            success_two = False
                if success_two:
                    self.mongo.update_one(criteria={'_id': company_nr.get('_id')}, newobject={'state': 2},
                                          collection="MT_Citys")
            except Exception as e:
                logger.error(e)
                pass

    def get_page_two(self, url, city_name, headers, area, number, cateName, page=1, retry=0):
        if retry > 10:
            logger.error("重试十次错误,退出循环")
            return False
        new_url = url + f'/pn{page}/'
        resp = self.get_requests(url=new_url, headers=headers)
        if resp:
            try:
                js_nr = str(resp.text).split("window._appState = ")[1].split(';</script>')[0]
                js_dum = loads(js_nr)
                poiInfos = js_dum['poiLists']['poiInfos']
                retry = 0
            except:
                retry += 1
                return self.get_page_two(url, city_name, headers, area, number, cateName, page, retry)
            for i in poiInfos:
                items = {'_id': i['poiId'],
                         'title': i['title'],
                         'address': i['address'],
                         'cityName': city_name,
                         'area': area,
                         'cateName': cateName,
                         'state': 0,
                         'update_time': self.mongo.current_time()}
                self.mongo.insert_mongo(data=items, collection='MT_meishi_ids')
            logger.info(
                f"进程 = {os.getpid()} | city = {city_name} | area = {area} | page = {page} | len = {len(poiInfos)} | cateName = {cateName} | number = {number} | type = 美食")
            if len(poiInfos) < 15:
                return True
        page += 1
        return self.get_page_two(url, city_name, headers, area, number, cateName, page, retry)

    def get_page(self, url, payload, headers, area, number, city_acronym, cateName, page=1, retry=0):
        if retry > 5:
            logger.error("重试五次错误,退出循环")
            return False
        payload['page'] = page
        resp = self.get_requests(url=url, params=payload, headers=headers)
        # resp = requests.get(url=url, params=payload, headers=headers, verify=False)
        try:
            poiInfos = resp.json()['data']['poiInfos']
            retry = 0
        except:
            payload['_token'] = parse_token()
            # uuid 过期
            try:
                uu_itmes = self.get_uuid(city_acronym)
                if uu_itmes:
                    payload['uuid'] = uu_itmes['uuid']
            except:
                return False
            retry += 1
            return self.get_page(url, payload, headers, area, number, city_acronym, cateName, page, retry)
        city_name = payload['cityName']
        for i in poiInfos:
            # 存入mongo
            items = {'_id': i['poiId'],
                     'title': i['title'],
                     'address': i['address'],
                     'cityName': city_name,
                     'area': area,
                     'cateName': cateName,
                     'state': 0,
                     'update_time': self.mongo.current_time()}
            # 存入mongo
            self.mongo.insert_mongo(data=items, collection='MT_meishi_ids')
        logger.info(
            f"进程 = {os.getpid()} | city = {city_name} | area = {area} | page = {page} | len = {len(poiInfos)} | cateName = {cateName} | number = {number} | type = 美食")
        if len(poiInfos) < 15:
            return True
        page += 1
        return self.get_page(url, payload, headers, area, number, city_acronym, cateName, page=page, retry=retry)

    def get_contact(self, number):
        self.mongo = MongoDao()
        A = 0
        while True:
            A += 1
            try:
                company_nr = self.mongo.find_update(find_data={'state': 0},
                                                    update_data={'state': 1}, collection="MT_Citys")
                if not company_nr:
                    return
            except Exception as e:
                logger.error(e)
                pass

    def __del__(self):
        self.mongo.close_client()

    def run(self):
        """
        使用多进程下载数据
        """
        logger.info("消费进程开始执行")
        trader = []
        for i in range(3):
            pr = Process(target=self.get_id, args=(i,))
            pr.start()
            sleep(3)
            trader.append(pr)
        for i in trader:
            i.join()
        logger.info('proce this is pid: %s' % os.getpid())
        return

    def run_two(self):
        """
        使用多进程下载数据
        """
        logger.info("获取联系方式消费进程开始执行")
        trader = []
        for i in range(1):
            pr = Process(target=self.get_contact, args=(i,))
            pr.start()
            sleep(3)
            trader.append(pr)
        for i in trader:
            i.join()
        logger.info('proce this is pid: %s' % os.getpid())
        return


if __name__ == '__main__':
    ms = MS()
    ms.run()
    ms.run_two()
