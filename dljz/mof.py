import requests
import urllib3

urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
}
url = "http://dljz.mof.gov.cn/NewABMS/cxfx/jgxx/doSearch"
data = {
    'bm': '06',
    'jc': '0',
    'delFilter': '1',
    'hadVoucher': '1',
    'noVoucher': '1',
    'qylx': '-1',
    'exp': '0',
    'page': '3',
}
reqs = requests.post(url, headers=headers, data=data, verify=False)
mx = reqs.json()['mx']
for i in mx:
    F_JGMC = i['F_JGMC']
    F_DLJZZSH = i['F_DLJZZSH']
    F_FZRQ = i['F_FZRQ']
    F_DWMC = i['F_DWMC']
    F_JGFZRMC = i['F_JGFZRMC']
    F_BAND = i['F_BAND']  # 备案年度
    F_JGCJMC = i['F_JGCJMC']  # 机构层级
    F_QRCODE = i['F_QRCODE']  # 证书二维码
    F_QYLX = i['F_QYLX']  # 企业类型
    F_BGDZ = i['F_BGDZ']  # 单位地址
    print(F_JGMC, F_DLJZZSH, F_FZRQ, F_DWMC, F_JGFZRMC, F_BAND, F_JGCJMC, F_QRCODE,F_QYLX, F_BGDZ )
