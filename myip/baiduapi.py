"""
本项目是为了获取百度地图的详细地址
思路 使用百度地图的api
每日最大请求次数为2K次
"""

import requests
from datetime import datetime
from configs import BAIDU_API, MONGO_ACCESS_TOKEN
from Tools.log_util import DevLogUtil
from DB.mongo import MongoDao

log_base = DevLogUtil()


def find_data(query, region='上海'):
    if not query:
        return None
    url = f"http://api.map.baidu.com/place/v2/search?query={query}&region={region}&output=json&ak=WF79CTqXmexflvp2QnZih2tcGr5NQMnV"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4158.4 Safari/537.36',
    }
    resp = requests.get(url, headers=headers, verify=False)
    results = resp.json()['results']
    if isinstance(results, list) and len(results) > 0:
        name = results[0]['name']
        address = results[0]['address']
        try:
            telephone = results[0]['telephone']
        except:
            telephone = None
        province = results[0]['province']
        city = results[0]['city']
        data = {'name': name, 'address': address, 'telephone': telephone, 'province': province, 'city': city}
        print(data)


class TimeAll:
    def now_datetime(self):
        now = datetime.now()
        return datetime.strftime(now, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def str_datetime(str_time):
        """
        time 类型转换
        """
        return datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")

    def time_difference(self, one_time, two_time):
        """
        都是str类型
        """
        new_one_time = self.str_datetime(one_time)
        new_two_time = self.str_datetime(two_time)
        return self.day_dif(new_one_time, new_two_time)

    @staticmethod
    def day_dif(one, two):
        """
        计算天的时间差
        """
        if isinstance(one, datetime) and isinstance(two, datetime):
            return (two - one).days


class BaiduAPI(TimeAll):
    def __init__(self):
        self.mongo = MongoDao()

    def get_access_token(self):
        """
        为了获取百度的 access_token 数据
        access_token 有效期为30天
        """
        AK = BAIDU_API.get('AK')
        SK = BAIDU_API.get('SK')
        host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={AK}&client_secret={SK}'
        response = requests.get(host)
        if response:
            access_token = response.json().get('access_token')
            if not access_token and (response.json().get('error') or response.json().get('error_description')):
                log_base.warning("AK or SK 错误")
                return None
            else:
                return access_token

    def get_mongo_token(self):
        mongo_token = self.mongo.get_row(MONGO_ACCESS_TOKEN, {'state': 0})  # access_token从mongo里面取
        if mongo_token:
            access_token = mongo_token.get('access_token')
            # 查看时间是否过期,过期之后更新数据
            mongo_time = mongo_token.get('insert_time')
            A = self.time_difference(mongo_time, self.now_datetime())
        else:
            # 没有可用的
            # 存入mongo
            access_token = self.get_access_token()
            A = 1
        if A:
            criteria = {'_id': BAIDU_API.get('PHONE')}
            newobject = {'_id': BAIDU_API.get('PHONE'), 'access_token': access_token,
                         'insert_time': self.now_datetime(), 'state': 0}
            result = self.mongo.update_insert_one(MONGO_ACCESS_TOKEN, criteria, newobject)
            if not result:
                log_base.warning(f"access_token存入mongodb失败 phone {BAIDU_API.get('PHONE')}")
        return access_token

    def discern_word(self, img_base64):
        """
        识别文字
        img是base64编码后的数据
        """
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
        params = {"image": img_base64}
        access_token = self.get_mongo_token()
        if not access_token:
            return ''
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            words = response.json().get('words_result')
            if words:
                return words[0].get('words')
            else:
                # 如果报错，请求达到上限之类的
                # 修改错误
                self.mongo.upd_row(MONGO_ACCESS_TOKEN, search_filter={'_id': BAIDU_API.get('PHONE')}, upd_data={'state': 1})
                return ''

    def __del__(self):
        self.mongo.close_client()


if __name__ == '__main__':
    # find_data('东方网', region='上海')
    word = BaiduAPI().discern_word(img_base64='iVBORw0KGgoAAAANSUhEUgAAACYAAAAQCAIAAAD1fJpJAAACHUlEQVR42uVUS6upURje/2kPkEskapfC0MCAEpIk9m4bCANlYiAZSC4ZKCOXMsREe8ZArhNRIkQJudvnOa36+nwu54zOHpx3sHq/x3rfx/OuZ62X738eLz9Aud/vX2lB0FsE8f7+3mw2qU/6T4+iVCqZzeaHKsEtFArp7Tqdjkqloja02+2Pj49HlK83sV6v397eisXiHUqbzTYcDmezGUVA2vl8vnQ6fdvuuUqCQ4DJZLpb+JsSf0Sn07VaLYyOKtvtdjKZbLPZ0Ntls1mtVvs3lFarlc/nHw4HAiqVyn6/fzXYz89PvV6fSCSossVigX2DwYDq1Wg0uFxuuVx+REkQsuIUHA4HSpDP53Mc2fl8vqIEAdpVKhV6caFQsNvtBKnX6yKRCLjH4zkej88pSeRyuVAoBCSVSjmdTqZ9qtWqVCqFUHoxpsrj8ZDk83lMCfXAA4FAOBz+o0rEcrmUy+WwCEzU7XavKCFZo9FABwydyWSosslkIhAIiL9qtRrBt9uty+Wit4ZT1Go1gxJ+xBoMBiUSid/vZzo2Ho8T4ePxmDiIlEGZ1+u91cHIp9MpdOBogMRiMawYmEKhOJ1Obrebw+Ekk0kmJfhWq9Vta+rA71KyWKxer0dsDMODw2KxRCKRr68vjHQ0GhmNRtxjeMdgMIACybMH7/kFIIFby2azgYjFYrwyjJ0gw52+XC7IITcajcLAP/fG/heUvwBhMeAha8qMQAAAAABJRU5ErkJggg==')
    print(word)
