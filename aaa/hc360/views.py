"""
本项目是为了获取慧聪网的公司信息
"""

import os
import random
import re
import requests
from time import time
# from base.requestbase import RequestBase
from lxml import etree
# from base.xpathbase import XpathBase
# from base.appbase import AppBase
from urllib.parse import urljoin
# from Tools.log_util import DevLogUtil

# log_base = DevLogUtil()


class Hc360():

    def __init__(self):
        super().__init__()
        self.item = dict()

    def get_resp(self, cname="普道科技"):
        """
        获取数据的方法
        """
        # 搜索公司的名称,和链接
        url = f'https://s.hc360.com/company/search.html?kwd={cname}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4122.7 Safari/537.36',
            'Referer': 'https://www.hc360.com/',
            # 'Connection': 'close'
        }
        reqs = requests.get(url="https://www.baidu.com/")
        # resp = self.get_request(url, headers=headers)
        resp = requests.get(url, headers=headers)

        if resp:
            # 获取页面数据
            rese = etree.HTML(resp.text)
            hrefs = rese.xpath('//div[@class="contbox"]/dl')
            for company in hrefs:
                # 选择第一个地址不为空的公司
                address = company.xpath('.//em[contains(text(),"所在地址")]/parent::a[1]/text()')[-1].strip()
                if not address:
                    continue
                self.item['url'] = company.xpath('./dt[@class="til"]/h3/a[1]/@href')[0].strip()
                company_name = company.xpath('./dt[@class="til"]/h3/a/text()')[0].strip()
                self.item['companyName'] = company_name
                company_url = company.xpath('./dt[@class="info"]/a/@href')[0]
                # 查询公司信息
                self.get_contact(urljoin(url, company_url))
                # 获取key，value
                # key, value = self.get_key_value()
                # if value:
                #     # 获取图片
                #     img_number = self.get_img_number(value)
                #     if userId and key and img_number:
                #         self.get_jjzz(userId, key, img_number)
                return self.item

    def get_contact(self, company_url):
        """
        获取链接的数据
        """
        # headers = {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "zh-CN,zh;q=0.9",
        #     "Connection": "keep-alive",
        #     "Cookie": "showFlagLogin=1; contactViewCount=1; visitid_time=2020-6-9%2013%3A1%3A32; hc360visitid=C8F002759C300001A539CA801AC21BC2; hc360first_time=2020-06-09; hcbrowserid=C8F002759C40000180E7EE2619F6BEA0; hckIndex=C8F002759CB00001D55F5AA4345F1F6E; hccordet=00; hcpreurl=; hc360analyid=C8F00275E9E0000156E791B7160E1600; hc360analycopyid=C8F00275E9E00001A35DCD64CD7E17A4; Hm_lvt_e1e386be074a459371b2832363c0d7e7=1591678894; Hm_lpvt_e1e386be074a459371b2832363c0d7e7=1591678894; hc360sessionid=C8F00275FBB0000138B84625F8602010; hc360sessionid=C8F00275FBB0000138B84625F8602010; hc360firstvisittime=1591678894053; hc360firstvisittime=1591678894053; _ga=GA1.2.1176012621.1591678895; _gid=GA1.2.331622190.1591678895; hc5minbeat=1591686498030",
        #     "Host": "b2b.hc360.com",
        #     "Upgrade-Insecure-Requests": "1",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4164.4 Safari/537.36",
        # }
        print(company_url)
        # resp = self.get_request(company_url, allow_redirects=True, headers=headers)
        resp = requests.get(company_url)
        # print(resp.url)
        # if resp:
        #     html = etree.HTML(resp.text)
        #     self.item['companyProduct'] = self.get_xpath_data(html, '主营产品或服务', td='th')
        #     self.item['industry'] = self.get_xpath_data(html, '主营行业', td='th')
        #     self.item['companyType'] = self.get_xpath_data(html, '企业类型', td='th')
        #     self.item['pattern'] = self.get_xpath_data(html, '经营模式', td='th')
        #     self.item['registerAddress'] = self.get_xpath_data(html, '注册地址', td='th')
        #     self.item['manageAddress'] = self.get_xpath_data(html, '经营地址', td='th')
        #     self.item['establishTime'] = self.get_xpath_data(html, '成立时间', td='th')
        #     self.item['Representative'] = self.get_xpath_data(html, '法定代表人', td='th')
        #     self.item['peopleNumber'] = self.get_xpath_data(html, '员工人数', td='th')
        #     self.item['turnover'] = self.get_xpath_data(html, '营业额', td='th')
        #     self.item['brand'] = self.get_xpath_data(html, '品牌', td='th')
        #     self.item['capital'] = self.get_xpath_data(html, '注册资本', td='th')
        #     self.item['customerBase'] = self.get_xpath_data(html, '主要客户群', td='th')
        #     self.item['market'] = self.get_xpath_data(html, '主要市场', td='th')
        #     self.item['yearExport'] = self.get_xpath_data(html, '年出口额', td='th')
        #     self.item['yearImport'] = self.get_xpath_data(html, '年进口额', td='th')
        #     self.item['peopleResearch'] = self.get_xpath_data(html, '研发部门人数', td='th')
        #     self.item['production'] = self.get_xpath_data(html, '月产量', td='th')
        #     self.item['area'] = self.get_xpath_data(html, '厂房面积', td='th')
        #     self.item['quality'] = self.get_xpath_data(html, '质量控制', td='th')
        #     self.item['managementSystem'] = self.get_xpath_data(html, '管理体系', td='th')
        #     self.item['authentication'] = self.get_xpath_data(html, '认证信息', td='th')
        #     self.item['certificate'] = self.get_xpath_data(html, '证书及荣誉', td='th')
        #     self.item['referencePerson'] = self.get_xpath_data(html, '资信参考人', td='th')
        #     self.item['QQ'] = self.get_xpath_data(html, 'QQ', td='th')
        #     self.item['email'] = self.get_xpath_data(html, '邮箱', td='th')
        #     self.item['companyUrl'] = self.get_xpath_data(html, '公司主页', td='th')
        # else:
        #     self.item.clear()

            # userId = re.findall(r'userId\D*(\d*?)\D+', resp.text)  # 查找userid
            # if userId:
            #     return userId[0]
            # return None

    # def get_key_value(self):
    #     url = f'https://sso.hc360.com/LoginTicket.jsp?callback=success_jsonpCallback&_={int(time() * 1000)}'
    #     headers = {
    #         'Referer': 'https://youdaoxgq.b2b.hc360.com/shop/show.html'
    #     }
    #     reqs = self.get_request(url, headers=headers)
    #     if reqs:
    #         value = reqs.text.split('value:"')[1].split('"')[0]  # 是图片请求的参数
    #         key = reqs.text.split('key:"')[1].split('"')[0]  # 是提交表单的参数
    #         return key, value
    #     return None, None
    #
    # def get_img_number(self, value):
    #     # 获取并且取得图片验证码的数字
    #     url = f'https://sso.hc360.com/ValidImage.jsp?seed={value}'
    #     resp = self.get_request(url)
    #     img_path = f'./{"".join(str(random.choice(range(10))) for _ in range(10))}.jpg'  # 随机十位数字用来命名图片
    #     with open(img_path, 'wb') as f:
    #         f.write(resp.content)
    #     # 使用打码平台查看数字
    #     result = None
    #     if os.path.exists(img_path):
    #         try:
    #             # cid, result = get_captcha(img_path, 1004)
    #             # 手动打码
    #             result = input("图片数字")
    #         except Exception as e:
    #             log_base.warning(f"图片识别报错 error {e}")
    #         finally:
    #             os.remove(img_path)
    #         return result
    #     return None
    #
    # def get_jjzz(self, userId, key, img_number):
    #     """
    #     获取详情的数据
    #     """
    #     data = {
    #         'userId': str(userId),
    #         'ctoken': str(key),
    #         'valicode': str(img_number),
    #     }
    #     headers = {
    #         'Referer': 'https://youdaoxgq.b2b.hc360.com/shop/show.html',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4122.7 Safari/537.36'
    #     }
    #     url = 'https://my.b2b.hc360.com/my/getCompany?'
    #     reqs = self.get_request(url=url, params=data, headers=headers)
    #     if reqs:
    #         if reqs.text.find("验证码错误") > -1:
    #             key, value = self.get_key_value()
    #             if value:
    #                 # 获取图片
    #                 img_number = self.get_img_number(value)
    #                 self.get_jjzz(userId, key, img_number)
    #         print(reqs.json())


# if __name__ == '__main__':
#     text = f"开始慧聪网的爬取 时间{time()}"
#     log_base.info(text)
#     item = Hc360().get_resp("普道科技")
#     print(item)
