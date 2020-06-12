# -*- coding: utf-8 -*-
from aaa.urls import *
# from app import apps
# from gevent.pywsgi import WSGIServer
import requests
# from flask import Flask
# from gevent import monkey
# apps = Flask(__name__)
# from app import apps
# monkey.patch_all()
def app_info():
    reqse = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4164.4 Safari/537.36',
        'Connection': 'keep-alive'
    }
    reqs = reqse.get(url="https://www.baidu.com/")
    print(reqs.headers)
    print(reqs.request.headers)
    print(reqs.url)
    print(reqs.status_code)

    reqs = requests.get(url='https://b2b.hc360.com/company/paat1001.html')
    print(reqs.url)
    print(reqs.status_code)
    reqs = requests.get(url='https://paat1001.b2b.hc360.com/shop/show.html')
    print(reqs.url)
    print(reqs.status_code)
    return "index page"

def aa():
    apps.add_url_rule('/get_info/', view_func=app_info(), methods=["POST"])

def add_urls():
    """
    添加路由功能
    :return:
    """
    # create_qcm()
    # create_maimai()
    # create_b2b()
    # create_sq()
    # create_huangye()
    # create_xizhi()
    # create_zhaodao()
    create_hc()
    # aa()


add_urls()


def run_app():
    apps.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    # WSGIServer(('0.0.0.0', 5000), apps).serve_forever()


if __name__ == '__main__':
    run_app()
