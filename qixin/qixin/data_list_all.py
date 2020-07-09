"""
获取所有列表的数据
"""
from Tools.log_util import DevLogUtil
from urllib.parse import quote
from app.qixin.views import Qixin
from json import loads
from app.qixin.helper.login import SeleQixin
from lxml import etree
from time import sleep

log_base = DevLogUtil()


class QixinList(Qixin):

    def new_requests(self, url, num=0):
        if num > 2:
            return False
        success = self.get_cookie()
        if not success:
            log_base.warning("cookie导入错误")
            return None
        resp = self.get_session_request(url, headers=self.headers, verify=False)
        if resp:
            return resp
        elif self.cookie_load:
            # 这边是被查出频率异样 需要点击过频率
            num += 1
            web_login = SeleQixin()
            success = web_login.get_dj(url=url, cookies=self.cookie_load)
            self.new_requests(url, num=num)



    def get_resp(self, cname):
        """
        获取列表的数据
        """
        url = f'https://www.qixin.com/search?key={quote(cname)}'
        resp = self.new_requests(url)
        sleep(10)
        if resp:
            # 获取页面数据
            company_list = resp.text.split('.concat(')[1].split(')||$')[0]
            try:
                new_company_list = loads(company_list)
                companys = new_company_list.get('o').get('w')[0][2].get('companies').get('items')
            except:
                log_base.warning("生成company列表错误")
                return
            for company in companys:
                com_items = {}
                com_items['name'] = company.get('name')
                com_items['start_date'] = company.get('start_date')
                com_items['oper_name'] = company.get('oper_name')
                com_items['status'] = company.get("status")
                com_items['eid'] = "https://www.qixin.com/company/%s" % company.get("eid")
                com_items['reg_capi'] = company.get("reg_capi")
                com_items['credit_no'] = company.get("credit_no")
                com_items['org_no'] = company.get("org_no")
                com_items['reg_no'] = company.get("reg_no")
                com_items['tags'] = [_.get('tag') for _ in company.get('tags')]
                com_items['address'] = company.get('address')
                com_items['phone'] = company.get('phone')
                com_items['email'] = company.get('email')
                com_items['districtCode'] = company.get("districtCode")
                for k, v in com_items.items():
                    if isinstance(v, str) and not v.strip().replace('-', ''):
                        com_items[k] = ''
                print(com_items)


    def mains(self, cname="普道科技"):
        # 获取所有的地区和地址的拼接
        url = f'https://www.qixin.com/search?key={quote(cname)}'
        resp = self.new_requests(url)
        if resp:
            try:
                company_list = resp.text.split('.concat(')[1].split(')||$')[0]
                html_grade = etree.HTML(resp.text)
                grades = html_grade.xpath('//div[@class="wrapper top-grade"]/div/a/text()')
                new_company_list = loads(company_list)
                provinces = new_company_list.get('o').get('w')[0][2].get('provinces')
                for grad in grades:
                    for prov in provinces:
                        self.get_resp(grad + (prov.get('name')))
            except:
                log_base.warning("生成关键词列表错误")
                return


if __name__ == '__main__':
    item = QixinList().mains()
