"""
本项目是为了企信宝的数据
"""

import urllib3
import random

from json import loads
from base.requestbase import RequestBase
from lxml import etree
from base.xpathbase import XpathBase
from base.appbase import AppBase
from Tools.log_util import DevLogUtil
from urllib.parse import quote
from DB.mongo import MongoDao
from Tools.utils import email
from urllib.parse import urljoin

urllib3.disable_warnings()
log_base = DevLogUtil()


class Qixin(XpathBase, RequestBase, AppBase):

    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }
        self.item = dict()
        self.mongo = MongoDao()
        self._id = ''
        self.cookie_load = ''

    def __del__(self):
        self.mongo.close_client()

    def warning_mongo(self, url):
        # 修改cookie 状态
        self.mongo.upd_row('qixin_cookie', {'_id': self._id}, {'is_normal': 1})
        # 发送邮件
        email('启信宝cookie失效', f'cookie _id: {self._id}')

    def get_cookie(self, is_vip=False):
        """
        随机取出一个可用cookie
        """
        users = self.mongo.get_datas('qixin_cookie', {'is_vip': is_vip, 'is_normal': 0})
        user_list = [u for u in users]
        if user_list:
            user = random.choice(user_list)
            # 将cookie插入到headers中
            cookie = user.get("cookie")
            self._id = user.get('_id')
            self.cookie_load = self.add_session_cookie_two(cookie)
            success = self.add_session_cookie(self.cookie_load)
            if not success:
                self.headers['Cookie'] = cookie
            return True
        else:
            email('启信宝', 'cookie 获取不到了')
            return False

    def get_resp(self, cname):
        """
        获取数据的方法
        """
        # 添加cookie
        success = self.get_cookie()
        if not success:
            log_base.warning("cookie导入错误")
            return None
        # 搜索公司的名称,和链接
        url = f'https://www.qixin.com/search?key={quote(cname)}'
        resp = self.get_session_request(url, headers=self.headers, verify=False)
        if resp:
            # 获取页面数据
            resq = etree.HTML(resp.text)
            hrefs = resq.xpath('//div[@class="col-2-1"]')
            for href in hrefs:
                res = href.xpath('.//span[contains(text(),"电话")]/..//text()')
                if res:
                    res_nr = str("".join([str(_).strip() for _ in res])).strip()
                    if len(res_nr) > 4 and res_nr.find("*") > -1:
                        # cookie 登陆未成功 需要重新获取
                        self.warning_mongo(url)  # 修改cookie 状态
                        return self.get_resp(cname)
                    # 查询公司信息
                    new_url = href.xpath('.//a[contains(@title,"点击查看公司")]/@href')
                    if new_url:
                        new_url = new_url[0]
                    else:
                        continue
                    self.get_contact(urljoin(url, new_url))
                    break
        return self.item

    def get_contact(self, company_url):
        """
        获取链接的数据
        """
        resp = self.get_session_request(company_url, headers=self.headers, verify=False)
        if resp:
            html = etree.HTML(resp.text)
            # 切割数据 转换成json
            contacts = loads(resp.text.split('"contacts":')[1].split(',"viewCount"')[0])
            gs = []
            for item in contacts['gs']['items']:
                gs.append(item.get('contact'))
            for item in contacts['zd']['items']:
                gs.append(item.get('contact'))
            self.item['url'] = company_url
            self.item['companyName'] = html.xpath("//span/h1/text()")[0]
            self.item['email'] = self.get_xpath_two(html, '邮箱', value_name='span')
            self.item['website'] = self.get_xpath_two(html, '官网', value_name='span')
            self.item['address'] = self.get_xpath_two(html, '地址', value_name='span')
            # self.item['address'] = self.get_xpath_two(html, '社保人数', value_name='span')

            self.item['contacts'] = self.get_xpath_five(html, '统一社会信用代码')
            self.item['phoneNumber'] = self.get_xpath_five(html, '组织机构代码')
            self.item['telephone'] = self.get_xpath_five(html, '经营状态')
            self.item['businessMain'] = self.get_xpath_five(html, '所属行业')
            self.item['businessMain'] = self.get_xpath_five(html, '公司类型')
            self.item['businessMain'] = self.get_xpath_five(html, '成立日期')
            self.item['businessMain'] = self.get_xpath_five(html, '营业期限')
            self.item['businessMain'] = self.get_xpath_five(html, '核准日期')
            self.item['businessMain'] = self.get_xpath_five(html, '法定代表人')
            self.item['businessMain'] = self.get_xpath_five(html, '注册资本')
            self.item['businessMain'] = self.get_xpath_five(html, '登记机关')
            self.item['businessMain'] = self.get_xpath_five(html, '企业地址')
            self.item['businessMain'] = self.get_xpath_five(html, '经营范围')

            self.get_info(company_url)
        else:
            self.item.clear()

    def get_info(self, company_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4122.7 Safari/537.36',
        }
        resp = self.get_request(company_url, headers=headers, verify=False)
        if resp:
            html = etree.HTML(resp.text)
            res = html.xpath('//div[@class="byw-mainRight"]/div[@class="byw-mainRightB am-cf"][1]//p/text()')
            self.item['companyInfo'] = str("\n".join([str(_).strip() for _ in res])).strip()
        else:
            self.item['companyInfo'] = ''

    def by_info(self):
        return self.app_info()


if __name__ == '__main__':
    item = Qixin().get_resp("普道科技")
    print(item)
