# 测试淘宝的爬虫(港仔文艺)
import requests, urllib3, re, sys, asyncio
from taobao.tbLogin import taobao_login
from time import sleep
from random import randint
from fake_useragent import UserAgent
from json import loads
from retrying import retry

ip_port = 'secondtransfer.moguproxy.com:9001'
appKey = 'bm93WkdOc1FlS1g0TkhPTzoxbDl2UTNieWJ0S3djNVNx'

proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ua = UserAgent(verify_ssl=False)

headers = {
    "Proxy-Authorization": 'Basic ' + appKey,
    'Referer': 'https://lp930428.taobao.com/search.htm?spm=a1z10.3-c-s.w4002-21751133153.101.15451c25uUSvzW&_ksTS=1583310054461_186&callback=jsonp187&mid=w-21751133153-0&wid=21751133153&path=%2Fsearch.htm&search=y&input_charset=gbk&orderType=newOn_desc&pageNo=10'
}

pattern = re.compile(r'data-id=\\"(.*?)\\"')
pattern_title = re.compile(r'<img alt=\\"(.*?)\\"')
pattern_i = re.compile(r'ICCP_.*?:(\d+)')



class TB(object):
    def __init__(self):
        self.requests_my = requests.session()
        self.requests_num = 0
        self.cookies = ['cookie: miid=204428052058495196; thw=cn; cna=+eyEFrA7jWACAXjzVaDTEnqe; tracknick=%5Cu80D6%5Cu5B50%5Cu4E0D%5Cu8D25121; tg=0; lgc=%5Cu80D6%5Cu5B50%5Cu4E0D%5Cu8D25121; enc=tbRYIG3675YSopDeAgZ11vGP%2FXpI1KH0fSEHWxiRwEfm9Ft28VrE7TeYc8H0rB%2Fgau6xbZl39QmoSj1%2FgPRiRw%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; sgcookie=DwJmge9he4AjtOcKrKCcI; uc3=lg2=UIHiLt3xD8xYTw%3D%3D&id2=UU6lTo234Ra%2FxA%3D%3D&nk2=pkGqs940007ggQ8%3D&vt3=F8dBxd34DJr%2B5xZVqzg%3D; uc4=id4=0%40U2xo%2FjAjxNTHvfmzzmqP1WD9ONRB&nk4=0%40pI6AGskQTe9e2CajSkPC35cj679tow%3D%3D; _cc_=URm48syIZQ%3D%3D; mt=ci=-1_1; v=0; cookie2=1b46da7f07c85c380b72af31d11f024d; t=9febae4d0b4ed55665f9961d96139f63; _tb_token_=7e08d3b33d51a; _m_h5_tk=fc584b4bd62fc705653daf3f72dcd0ce_1583657699821; _m_h5_tk_enc=4f48f1167b78007162d67354df73b1c0; uc1=cookie14=UoTUOagPImP%2FUw%3D%3D; _samesite_flag_=true; tfstk=coa1BdMvmdv_s5c6bo1EuUIsmB3AZIASGGMg1kNOceYyIbV1iZTrFfUamKLK2X1..; l=dBTrvQqcQilu-RztBOCwNSLpUj7T9IRAguovph3vi_5LG1Lskq7OouLb0ep6cjWfTaTp4Lilbxw9-etuj_t6Qtk8sxAJRxDc.; isg=BOTkVg9xZjPvfpLJ1dDcWUFiteLWfQjnYlMV1f4FTK9yqYRzJ421dw-DaQGxcUA_']
        self.requests_my.cookies.set('Cookie', self.cookies[0])

    def urlOne(self, page=1):
        headers['User-Agent'] = ua.random
        request_url = "https://lp930428.taobao.com/i/asynSearch.htm?mid=w-21751133153-0&orderType=newOn_desc&pageNo={}".format(
            page)
        req = self.my_req(request_url)
        if req:
            # 获取店里所有商品链接
            r_text = req.text
            data_ids = pattern.findall(r_text)
            titles = pattern_title.findall(r_text)
            for data_id, title in zip(data_ids, titles):
                if self.requests_num % 10 == 0:
                    # 自动登录一下
                    while 1:
                        cookie = asyncio.get_event_loop().run_until_complete(taobao_login())
                        if cookie:
                            self.requests_my.cookies.set('Cookie', cookie)
                            break
                self.requests_num += 1
                # 获取人气数链接
                try:
                    sign_id = self.find_url(data_id)
                    if sign_id:
                        ic_url = "https://count.taobao.com/counter3?callback=jsonp145&inc=ICVT_7_{}&sign={}&keys=DFX_200_1_{},ICVT_7_{},ICCP_1_{},SCCP_2_101463431".format(
                            data_id, sign_id, data_id, data_id, data_id)
                        ic_num = self.find_detail_two(ic_url, data_id)  # 获取人气
                    else:
                        continue
                    price, count = self.find_detail(data_id)  # 获取价格和交易量
                    if not price:
                        sleep(4)
                        while 1:
                            cookie = asyncio.get_event_loop().run_until_complete(taobao_login())
                            if cookie:
                                self.requests_my.cookies.set('Cookie', cookie)
                                break
                    comment = self.find_detail_thre(data_id)  # 获取评论数
                    print(title, "上新价 : %s" % price, "交易量 : %s" % count, "评论数 : %s" % comment, "人气 : %s" % ic_num)
                except Exception as e:
                    print(e)
            # 判断是否是最后一页
            if str(r_text.split('J_SearchAsync')[-1].split('</a>')[0]).find("下一页"):
                page += 1
                self.urlOne(page)
            else:
                return
        else:
            print("error : %s" % (request_url))

    def find_detail(self, data_id):
        headers['Referer'] = 'https://item.taobao.com/item.htm?id=%s' % (data_id)
        purl = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId={}&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,activity,fqg,zjys,couponActivity,soldQuantity,page,originalPrice,tradeContract".format(
            data_id)
        req = self.my_req(purl)
        if req:
            req_text = req.text
            re_lo = loads(req_text)
            try:
                price = re_lo['data']['promotion']['promoData']['def'][0]['price']  # 价格
                count = re_lo['data']['soldQuantity']['confirmGoodsCount']  # 交易量
            except:  # 应该是被检测出来了
                return None, None
            return price, count

    def find_detail_two(self, url, data_id):
        headers[
            'Referer'] = 'https://item.taobao.com/item.htm?spm=a1z10.3-c-s.w4002-21751133153.53.35eb1c25MEmUMF&id=%s' % (
            data_id)
        req = self.my_req(url)
        if req:
            req_text = req.text
            try:
                result1 = pattern_i.findall(req_text)  # 获取到收藏宝贝人气
                return result1[0]
            except:
                pass
        return None

    def find_url(self, data_id):
        url = 'https://item.taobao.com/item.htm?id=%s' % (data_id)
        req = self.my_req(url)
        if req:
            sign_url = (req.text).split("counterApi")[1].split(",")[0]
            return str(sign_url).split("sign=")[1].split("&")[0]
        return None

    def find_detail_thre(self, data_id):
        url = "https://rate.taobao.com/detailCommon.htm?auctionNumId=%s" % (data_id)
        headers[
            'Referer'] = 'https://item.taobao.com/item.htm?spm=a1z10.3-c-s.w4002-21751133153.35.49d21c25BUAkgB&id=%s' % (
            data_id)
        req = self.my_req(url)
        if req:
            req_text = req.text
            try:
                total = str(req_text).split('"total":')[1].split(',')[0]
            except:  # 应该是被检测出来了
                return None
            return total

    @retry(stop_max_attempt_number=4)
    def my_req(self, url):
        # sleep(randint(3, 6))
        req = self.requests_my.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False,
                                   timeout=10)
        if req.status_code == 200:
            return req


if __name__ == '__main__':
    tb = TB()
    # cookie(数据量少不需要自动化)
    tb.urlOne()
