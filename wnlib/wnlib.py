'''
经过测试本网站不需要cookie,只要获取接口就能不断的获取数据
使用生产者消费者加快下载速度，进程数为4
使用selenium模拟点击登录获取pid, sid
cv2获取图像坐标
log记录日志
---王博文---
'''
import requests, log, os, sys
from retrying import retry
from urllib.parse import urljoin
from hashlib import md5
from lxml import etree
from wnliblogin_two import CrackWeiboSlide
from multiprocessing import Process, Queue
from time import sleep


dama_log = log.Log_two('files', "dama")


class Wnlib(object):
    def __init__(self):
        self.url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&parentQid=&qid=21&SID=E5LT6pH4luQvY7UcTNU&&update_back2search_link_param=yes&page=2'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Host': 'apps.webofknowledge.com',
            'Referer': 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&qid=21&SID=E5LT6pH4luQvY7UcTNU&&page=1&action=changePageSize&pageSize=50',
        }
        self.reqs = requests.session()

    @retry(stop_max_attempt_number=4)
    def my_req(self, url):
        req = self.reqs.get(url, headers=self.headers, verify=False, allow_redirects=False, timeout=30)
        return req

    def findurl(self, que, url, qid, sid):
        # 获取到连接
        dama_log.info("开始")
        for page in range(1, 1000):
            new_url = url.format(qid, sid, page)
            req = self.my_req(new_url)
            if req.status_code != 200:
                dama_log.error(new_url)
                continue
            con_et = etree.HTML(req.text)
            hrefs = con_et.xpath('//a[@class="smallV110 snowplow-full-record"]/@href')
            for href in hrefs:
                # 获取到详细页面
                new_href = urljoin(new_url, href)
                que.put(new_href)
            print('获取到第 : %s页, 数量为 : %s' % (page, len(hrefs)))
            dama_log.info('获取到第 : %s页, 数量为 : %s' % (page, len(hrefs)))

    def findnr(self, que):
        while 1:
            if que.qsize() == 0:
                sleep(3)
            else:
                break
        print('Process to read: %s' % os.getpid())
        q_siz = 0
        while True:
            try:
                new_href = que.get()
                q_siz = 0
            except Exception as e:
                q_siz += 1
                if q_siz > 5:
                    print("%s 进程结束" % os.getpid())
                    sys.exit()
                else:
                    sleep(3)
                    continue
            req_href = self.my_req(new_href)
            if req_href.status_code != 200:
                dama_log.error(new_href)
                continue
            # 可以将源码储存
            file_name = self.md5_generator(new_href)  # 命名
            with open('./files/%s.html' % (file_name), "w", encoding='gb18030') as f:
                f.write(req_href.text)


    def md5_generator(self, url):
        return md5(url.encode()).hexdigest()


if __name__ == '__main__':
    w = Wnlib()
    # 经过检测只要找到到pid和sid就能找到数据
    username = 'imr2019@163.com'
    password = 'Jp5vzgbV'
    cws = CrackWeiboSlide()
    while True:
        try:
            qid, sid = cws.imgcheck(username, password)
            break
        except:
            sleep(3)
    # qid, sid = '5', 'F3Ify69RVc6YDxt7cld'
    url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&qid={}&SID={}&&page={}&pageSize=50'
    q = Queue(maxsize=100)
    pw = Process(target=w.findurl, args=(q, url, qid, sid))
    pw.start()
    pros = []
    for i in range(4):
        pr = Process(target=w.findnr, args=(q,))
        pr.start()
        sleep(0.5)
        pros.append(pr)
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    for i in pros:
        i.terminate()