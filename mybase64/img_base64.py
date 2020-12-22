'''
网络图片文字识别
'''
import base64
import requests
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
# 二进制方式打开图片文件
f = open('9151973406.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
access_token = '24.539ac640aa3bdc702da8d791fec8bd4f.2592000.1598076391.282335-19018359'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())