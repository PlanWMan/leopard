from flask import Flask
from flask import request, jsonify
import requests

apps = Flask(__name__)

def app_info():
    reqs = requests.get(url="https://www.baidu.com/")
    print(reqs.url)
    print(reqs.status_code)
    reqs = requests.get(url='https://paat1001.b2b.hc360.com/shop/show.html')
    print(reqs.url)
    print(reqs.status_code)

def aa():
    apps.add_url_rule('/get_info/', view_func=app_info, methods=["POST"])

aa()


def run_app():
    apps.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    # WSGIServer(('0.0.0.0', 5000), apps).serve_forever()


if __name__ == '__main__':
    run_app()
