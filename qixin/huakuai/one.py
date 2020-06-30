import requests
import json
import execjs
import urllib3
urllib3.disable_warnings()

class Login:
    def __init__(self):
        self.reqs = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4173.2 Safari/537.36'}

    def get_challenge_gt(self):
        url = 'https://www.qixin.com/'
        req = self.reqs.get(url, headers=self.headers, verify=False)
        url = 'https://www.qixin.com/api/captcha/register'
        data = {
            "type": 1
        }
        headers = {
            '7de9a5d8ca91915568da':'c606bb658598f9afb637746f2b47cc67e9a4e540fa83c3e5acff7737c4b0c31e1b3c00876a5fab86c496fb848828e89bc174fdc29bc3a16259c575ee84865a1c',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4173.2 Safari/537.36',
            'Host': 'www.qixin.com',
            'Content-Type': 'application/json;charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',
        }
        req = self.reqs.post(url, data=json.dumps(data), headers=headers, verify=False)
        gt = req.json().get('gt')
        challenge = req.json().get('challenge')
        print(gt, challenge)
        if gt and challenge:
            with open('./mix.js', 'r', encoding='utf-8')as f:
                content = f.read()
            ctx = execjs.compile(content)
            res = ctx.call('first_w', gt, challenge)
            print(res)

if __name__ == '__main__':
    Login().get_challenge_gt()