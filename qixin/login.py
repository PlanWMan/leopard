"""
启信宝的登陆操作
入口: https://www.qixin.com/company/75c43ce5-a43b-4c71-99a9-a4db20772429
login 密码 U2FsdGVkX1+P4jQ+wd/SEiaqwJLx7caruEzciY7OUdE=
"""

import requests
import urllib3
import json
from time import time

urllib3.disable_warnings()


class Login:
    def __init__(self):
        self.reqs = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4173.2 Safari/537.36'}

    def add_session_cookie(self, cookies):
        requests.utils.add_dict_to_cookiejar(self.reqs.cookies, cookies)

    def get_two(self):
        url = 'https://www.qixin.com/'
        # cookies = {'acw_sc__v2': '5eeb3701d107be7caf13447c972746f2c63a6c26','cookieShowLoginTip':'1'}
        # self.add_session_cookie(cookies)
        req = self.reqs.get(url, headers=self.headers, verify=False)
        self.get_challenge_gt()
        # print(req.text)

    def get_challenge_gt(self):
        url = 'https://www.qixin.com/api/captcha/register'
        data = {
            "type": 1
        }
        headers = {
            '22ffc9439b1155ac8f27': '90a9a65de6e30a19d614d8ffa184219d8ce58e4770e4257cb6ff37804daf5f7d31d815cbb6fccc7a19fd55d4680fcdc489e8937d0c6e6a94b848649a662c14c4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4173.2 Safari/537.36',
            'Host': 'www.qixin.com',
            'Content-Type': 'application/json;charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',
        }
        req = self.reqs.post(url, data=json.dumps(data), headers=headers, verify=False)
        print(req.json())
        # self.get_key()
        gt = req.json().get('gt')
        self.get_gettype(gt)
        # print(challenge, gt)
        challenge = req.json().get('challenge')
        # 极验验证
        self.get_jy(challenge, gt)
        if challenge and gt:
            self.get_challenge_two(challenge, gt)
            self.get_challenge_three(challenge, gt)
        self.get_login()

    def get_key(self):
        headers = {
            '495e22da2d7e97f60af7': '7af4448136465602fc20f57f3dbe1b954cfc92b438cc6c29a24f218fb25e2fc40a578f894a07a76b86c44f1f28d40283a6cef1ce3866d651018ea1330aff7bdf',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4173.2 Safari/537.36',
            'Host': 'www.qixin.com',
            'X-Requested-With': 'XMLHttpRequest',
        }
        url = "https://www.qixin.com/api/user/generateScanCodeKey"
        req = self.reqs.post(url, headers=headers, verify=False)
        print(req.text)


    def get_gettype(self, gt):
        data = {
            'gt': gt,
            'callback': f'geetest_{int(time() * 1000)}'
        }
        url = 'https://api.geetest.com/gettype.php'
        req = self.reqs.get(url, params=data, headers=self.headers, verify=False)
        print(req.text)

    def get_jy(self, challenge, gt):
        data_one = {
            'gt': gt,
            'challenge': challenge,
            'lang': 'zh-cn',
            'pt': '0',
            'client_type': 'web',
            'w': 'IYWLHx5OqahbbQIEGnkjVVeSLbyW5pA9lrnz5HbVApiYaK0(vYtU43HA9ur5hPJicg9TJAsex3trA9S2tVZ5VicHkRqFSr5ubaNIPG1tKotZ2BH4rYFpRwenIVXzwrsCK)z2rqpMyt015U7PQeBb2PbYhgr35UF1iFEfjFGLZVxrczyv7HK(D2W48hAJ7537LBSYHNrMggife4LrwyeNguH0Y38KqCmgXx2Mi8AU7y1ASmM3bfyVqLotH0QcxRJ2l(2gWw4bPW5n7IcLxKB3E3x6JulfaWUDpXoD5AHl0J(J55H4LTUyZocwo2blEKfmSIUTrJEj4mFtemnVBn8SM2V4(y6jsBqLfgIx0JzWvlJzEMVWLyUO1MLYO3wmaiXNoKInflgP1SV9hL4zp5EIsjz0gWIEqdLwe3kl2XncSuyAmY9t3U)Ex(BlvEFHc2sNof5byUBzcSeEXg81vVP143(0A)yntMcWX3Wc3yr(bC9q6HSUpLh760PNnSTO(eh1air6lJPgvOQ2PWF7O)wnErG5lBtEvySE8yNCN2G7IB7Law(Co3TLXOn4G5Pm90HCCHJDQB5cP46TJZiJ4zIq58tM6BYauiWAZnjEMVI58DxRPrnD2Ah4cG1lVnW2qDwx9VozWWqRv0RN3gBs5ASN8QpiqFatYqBpa9VOPU0vg3ISfEbqQSSMPaA8lNvLJzdrB6xTsAblNmbwHApRwCFPNV2b97sXy6)NLjkjJBZb2i5jUXtoi7tD(pwX7BwfWOrhGpIp4sBBBlD95uyUwDc91)BQUBtdzIWn3(w(uy9T7dmbJml3)Eo1fpN8sr5PrP48SZWMLnlSaimjLm)tqQ42NR)joihJGMMCba7XIC53CtmuT(UqzfcEF5cnkPa)j5gOCAyQCj5XgF86ktUtM(VGyy0loaL6ynZ31(3jTRaOE)hBrogPZBCeZD8vdkplHhl6UuE1rTT(OrCGvwBNBmoBfWZBxwlnyQC37XFjZQqIWbkzoGmzqYoSmTlMbkzlP1vZQYx73W572ypm2XpUh0j4N8Ixgz0pisIUn9D7XP4AnmNmEs082bsDQMliVa5sqSo)Q8klG3jkH7)hrscQuckqZr51e18xqKbzF7mSggDInXwgqJoIMxF9OWH8Y1vRpFMah8pjx7(vPQQBWkXFQb5R9L4Iceg1TT4t7)0Bt2hoBgML4XMrEdZQLHLkmgePTbqLkI2Z1Ccpx7mkqao)hTtgAQ)TonZo7pLfYSahvKEqKmpp0wvBJJWvJ3AVARcefv0oOTA3MQCloLFfZCDMF92CJRr8nv(5TJZXNH)e92NK0DlusYCf4OhRe8nQ9N)upFDZ2VrOCajwFiyETdkMOY1bjY7tt9xZVNSO4fC)TI5ZmkscvyTRFdu96tvc7lh1vDQr6DVuUkWmitaeGzk6RhpX6f3RIkVaJIqm7hsI68GINXXDLrX7cscOFVBs(SJqYBOzXXs)5e67CtzscVCVuxPN2y8Co45zbKI1Kyyk5Nmquy0n8g62KOrRgA(8ezpCi2Le5NoGsV9MVt9aRj3IN(lId)hraRlN)1SfTKV0lwPLpF7vdR2BxiYx4n1x1puHa6)xfrJzyZ9vUkeq0h8n3v7HTCMOR71zfrChOGYDrDmjkmS4MNzw2a(v)eoLWq1mbrkdhkBPHNJEbLN5cLOyWmvidWaU5eSTNnUfx30hR71Ky6nR(ioGXe80)diGN6snD9XSAjDIu4YeZWY8tG0zJstFlRojzTaInQvImvf6IhmGTASWzeeHZsMCB6Rf7uOTwThIZIhT(qePOkZbNUJFrVdTO6sAd0cPNmEJ)jkzqmf(HXfunJwNbVFDrT(QQpySM4yNUnG)u6CH8u93h8)d((WrYaDEqfFaFZJx4MZpUKWHYnFZpil7H)QYPcuHjmM5Dn9oOCLE1x92FF5H8b9utRfOkYyh64izkvQ5lq5XUZhMgOlpFr7w3p)21QEru)StqXDDbYgZG68I0S2IIlgt0SCphAmKrGlW5KU3yMaJc79EH9ZAoVW27)XmmRE7tHvJNmZpftLB)n1x82RA88pegGD6O3imdwBGVMsOP8yjCDknHCAOzHc78BIILzfyxzPwaKi0szyeF0GM(Skvi2boEwBjL1lR8z8wxUtAPosA8fSNQevWLBPx)laWI)i68hDDkWxetrw4GHjLnubQi)72uOJMlv8M8h0k0F7k0m(gQJCIIKh)p)uzMDmSvUTWEtcafqx)1TDMOuldRREzU0dkBVnRKHHqLtRnAidoneEXAvxQHGb4oqWUV02ZfN(HWK2VOLq27dd33618529fcc0ad28c3d2532b8abd69b1718e0fc5ff1f873df05a319cee12d4b17071e630e1089424806661f3c8f09c94c39158e56d06b322d0562a5589e6572afe1bf130c1b194f0ce87651a743217adea56f270c758a7c5cd47de591c9d76b62849ed7b7e6275fdb07561aa2b2a851c67b2f85be2baa2fbb30b748c88be2',
            'callback': f'geetest_{int(time() * 1000)}',
        }
        url = 'https://api.geetest.com/get.php'
        req = self.reqs.get(url, params=data_one, headers=self.headers, verify=False)
        print(req.text)
        data = {
            'gt': gt,
            'challenge': challenge,
            'lang': 'zh-cn',
            'pt': '0',
            'client_type': 'web',
            'w': 'OPOhD5QfH5KIcC7V(dEHp)HCAuZyiMtiHlif2fXi)2YUNem1Vi5FSEWAjTsIOfFwszfjoMR0xAIw8qOLMgsv7wXY3R3hFPe0O4WRu79(9j4IhguBQ3UVa0oMGGyOA7tTQHKtZxy8FVYIZeX3P6tNO7QJD(rcrZowlsoGE4ejMCYIEYBrRFsFVPSY0evdCIghK)pJMbqro(Bi(9GMBfgPZKsBzcq8ZWWS9qiBdla4WeJDKEuYWgk0J3kEmo7WyVKpjZgfmrVt2kh8w95nEzsaMkXziUuqGafdeE3ObM5mqd1rGuy)z3qoK)qNH2duG2ekvyfzY1i7FWq9KaM4L3E8NCSuJQ7LUWh2vzFbn1nOCcqE(wgPY7QScxeXWrw5J30dbIXcwYNO867K)Vy0ifK3LkDCnvYkfY11KvRtW4mZmEaZ34BPpdjQy0wD3OibQgndzmaZFsuUyn8gDugrug1dLHQ5RaVO7F)WwmYPaLyVsWVqH5TLm2s4T7hbzUqnHrCPlXAa(Ro078AgZFSvyXizGxDofTxKICMmTiIJDSfhCW4UUdBZ2JtXfrCgXSTT1T3X326aGcnCtbchAekyeKTL5IVkhxVD)o5bXsaMq0wI0ocv)iupCsF3c(2gD5GjCyLWoiEa5(vA1L9jLMb7urZAPRTxhT(Le3JYVhI4)laLStShdVGdDk6OG(dgi7E07y0hMy9bEu1m11P1RdbqU4DnQegTM5gzRBAkVutfE9P3XJy0vzNZ(5DFk4iZmJ(j(yfUk809AjThw7rn2WLxMWc3tNSqvnATE)uz5puBMo7kjY(27E5ElcSrDwNkMDTpav9fbeesVtbzjzL8mOjiFs8FOQj7QTaLP5vunS33BJDvMfFCGZ81M3Z8CQI04KowL81cTS63pupiS3Gk)u9HC9TMYE09KnMZ5Ta0Z0Hen60gKV87Ibl1AXCbhuIXdprwC1qONR3xvM6QRXR)u6(K4rlC8tuU4gJenu0HdrbjVgqu(Xhhs3IcH4nTxpI55q9pBVFItm9B)7p0mmxhrqMSJKUxBHitLg1IdhXr4)RowV2K)ckiweFKiTLvYzadTOdUrO5Y6vV5EjDkwq5mxjI7RqN)qbBFIxlnqQMuJyEAaS9UF6KPgrqA6)AJ6YsFu30pKUluvY6l5HDhSqRdDUZxIoYA05h1CjMyBKL2cW)wj6edxotekHvvt9cq1qwjYET5)ujq9dDgg3ebfI9WvU7zxZdBlo6DPCZdJa9wA93dHu1xibLg5pHhfgBuzhMLbIwoftNVJRjKPhDHAIdROgCau5w7vYDl62stvkvutN8T7(Jgn0MLlOq6u6KRoEGbGS90UJkEM8zEn6zJCcFwDVwJ70fI6m4N64fmRrLj(Y7jm069kWvH1wRfKjuTf7BAQBwySDJeKeoNneoM3CS6ndX1Sdrh19b62dpXNt49ngLn1zW7MY5NOvtbmkfc9f7j47QQF9FjT6wqOKGVESItD1EJ082sEP(0ubMJl5kLPvY6c2Os9zF0FfytmY5UE)muisdF35CzTQZylpHbPM7D87fSF7ce6wXpRA1HGGMNRoLEVOVQAaR7Dt6jz(0BHFUT)lxeT1ZdlQvp79MQmlScyrBiQPhLBIzdZICqtWQeIr8UPPYT)755V4rRYhC2o94ainmQdpdwbxCRRvxXeGL1NXRb5KvbM1EMoFTtCSlziTY97IT17)nMj31zFsxZ2pv9BDe0PcbJn0oBj8)PC3vHrMy8YoXlJTIc9KTCDsDbJor2gA2t)jjaVdB2lxc8fNXF4pyBpa7HJiV3QMFrqa(xSzjnHrH7lA..',
            'callback': f'geetest_{int(time() * 1000)}',
        }
        url = 'https://api.geetest.com/ajax.php'
        req = self.reqs.get(url, params=data, headers=self.headers, verify=False)
        print(req.text)

    def get_challenge_two(self, challenge, gt):
        url = 'https://api.geetest.com/get.php'
        data = {
            'is_next': 'true',
            'type': 'slide3',
            'gt': gt,
            'challenge': challenge,
            'lang': 'zh-cn',
            'https': 'false',
            'protocol': 'https://',
            'offline': 'false',
            'product': 'embed',
            'api_server': 'api.geetest.com',
            'isPC': 'true',
            'width': '100%',
            'callback': f'geetest_{int(time() * 1000)}',
        }
        reqss = self.reqs.get(url, params=data, headers=self.headers, verify=False)
        print(reqss.text)
        # print(reqss.url)

    def get_challenge_three(self, challenge, gt):
        url = 'https://api.geetest.com/ajax.php'
        data = {
            'gt': gt,
            'challenge': challenge,
            'lang': 'zh-cn',
            'pt': '0',
            'client_type': 'web',
            'w': 'qT3w5N)LOsuzNDYTmIoBaKmWYpmpvJBJXpGnfluQXN)Bnekt78YLT9BlHx6tHEmSRW0CyuADqYiAvvv0HQIiEZyt2aCy)vPk9iH5JSqYMIx8zMZUrbv00m2hr3WsjGJ0dvwU1bd8M)p0RQmi3dPBILKpPsqWxUpHWPOEQrcSoFIL5RPfC420E1IWAYcjlbO3f7oZ9WHb1aIPVN7rFXbEJk3dVSO8ct8)S5xujwNcUuiqytTMJD8OuXAZn3HbxpdXVYlZvdysz6Jowgk8dtiqHRyzhjP0VmJwxfFI8oxs)EgAE(iZSDrGTVZj4ZeYFB9vBNUPeQWFOIz7DEBBeKQBDZJO31VUMNeAgvPkoYrVWodr)TOk((z5FaEs3TT1BiJUEMMUANXZgpqcy8s0FCWi8jdoDDlJ00AZ6pckWs0dtQ6wPySz0XJH1(i24sFVsKb6eZJWThJ33TkvsDmvCkmzINI6bij1i4dFDeGzAfPHZ8X1czU9bEKRuMXDgw(R75b6)QF3VTxug)2MtgGMEIjm2TIQEcHyTplt6v633vq(Kh48it7aGeO8w1flDHWupGlyPy(ifEgBHvvgmb0FP8)wZhZDccsypUPkGu7G1L2k(odpiTUh5AIA(kr9ZL3ic4jecdw93qpbNU92BC0WKzZWYL1PZEGDguqhotTvWZ2xgPWzhJo3iPYw5u9EFFXYhk9OdjecmgXio2mTmxbDueInFpq8FB0T18iGB7FRvTMN11d8xgLLxxceCR4bHf)jXt4oCsl8u7Tfb9U9gAKaIVnLWi16ydbTqL1pf6062dcQzBHH3H5buyJwdeL8NztRLFEz6eqi584(ZYnt6Xvh4YtMTD)(Eot2DAJDsyyYGFXUrk0qWxYsej2fIn9vW84LhwAq46j(orpEmZFSBGW5ZC6RmvcTTTH9brdnJ67B(wSDZG483uj6qRfH5OK7OcKTnefw5SQuysT)vUMl)lE8Pb)M9CLFMxLm8Z(DA3(IrZjHbiU5IKFtiXwPA2hTgQ3k2e5K5ZlKlKHK)yAYc6)hJt1KTQYwwvy0k5LoqzpGxDjK428kXB02Ack8FCM36mVQVLt0y(1hhYlhiPTzhPsBDRQ2FPPmb61lufD(NZkozOJ)kUbyB5tMUUTokcuXHGLVhjy8wlzcILZvrcqbQ90BB5EAkNFpDDQm9TAuZ2DBuh9WgqkcrfSmNDDQt839mPu2lbGGm6oXfQyPzofDgYmBn1vhLcXEXZJWRZi1vHn1XWszGtQMWJoMAW)xQnpJL8z0fzCy6EDt92xIDfNWTGFHqQQ6rJhYR7i3T0(PHKSCoEdgj8M0wQDOS1ybB)6HGRlRdrdzB8fUER9)XJxARMOyJJJ1UJD0vmVgb3vj77E1evBCtqxoigydyVm35nTjltTjgkmTL81VGS)CfLEKzeYTXcOcJ6iYM6fKUr2AzzTzjDizGs(Gu4LaT5gfN1fOXgftt6Gu2)ALhWbDUTdogMIFCCNkA0CpAsH8b4A1hUR0K)ap96vmHUR9OFyECYMzW)tvFGPsoTh6ythWzIC(asEMoeTXl6a7tFov6CsV46ruALI5PbLCevao80HojDv2B0F8fIBJwZ)QeREL3jXbt6m1nsBOxjifALUGhtTGp3sMu8jzqToS)zNFuilI1R2T0L5r89x4ROKJJfvZLBRhf0okOQHgggq10aeleneCjRtOy0ygErzWb(Q68P4vudtyijZZJUwp5)UiHuCvxMkEOwnecuBtJKMCMl0Hj)Qe4tjDQJZEc3(01LELBmuuRiB(BBf(KMzlYuPuWZXbY)nULSP6Ggr4NLc0s17bW5daMPyB)mVUNFidVtPC6CH6QSp)LdTkByivjgOnVaRL3RC45DGysNTNxUsxQ2zQWlStHXScT4aem)u1p)XK3CDxFrBygzEgndlT7fP)1JVokrk6BxcRteApW5hZQNFqbkVOtboiLsa3Az2ieoUPU6UijELNVMRpTnITzLMKkJuE11SRw6e(ZwAAoCUP9FGUq8PApbDqVMrXodE.',
            'callback': f'geetest_{int(time() * 1000)}',
        }
        reqss = self.reqs.get(url, params=data, headers=self.headers, verify=False)
        print(reqss.text)
        print(self.reqs.cookies)
        # print(reqss.url)

    def find_pass(self):
        import execjs
        with open("./get_pass.js", "r") as f:
            data_func = f.read()  # 读取js文件
        tk = execjs.compile(data_func)  # 编译执行js代码
        tk = tk.call('get_pass', '123456qwe')  # 调用函数 token为js里面的函数  a为传的参数
        return tk

    def get_login(self):
        url = 'https://www.qixin.com/api/user/login'
        headers = {
            '0dc5f852c6411fd43e33': '1ee3ed235f34624a6d2887ed9fec4f8df7bebb2dcea4c12262ad3dba8b7fcefaadd8e9b68931d6a247560936fdf7e69739aae08d5084cd65f05f37404cedca56',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4173.2 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        # 使用js 获取加密参数

        data = {
            "acc": "18306799369",
            "pass": self.find_pass(),
            "captcha": {
                "type": 1,
                "data": {
                    "geetest_challenge": "b2ff258cf551d3d164bfca47b0c0d7cbe2",
                    "geetest_validate": "0085fa05d9559ec1d268794a80b1282d",
                    "geetest_seccode": "0085fa05d9559ec1d268794a80b1282d|jordan"
                }
            },
            "keepLogin": 'true',
            "areaCode": "86"
        }
        reqs = self.reqs.post(url, data=json.dumps(data), headers=headers, verify=False)
        print(reqs)


if __name__ == '__main__':
    Login().get_challenge_gt()
