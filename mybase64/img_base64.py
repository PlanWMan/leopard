import base64

img_base64 = 'iVBORw0KGgoAAAANSUhEUgAAACYAAAAQCAIAAAD1fJpJAAABd0lEQVR42mP4T3fAQLZOY2NjqlmJaZYxEkDjwgWximOqQVhJjNKurq6ZM2diugyTgd8bKL48efJkbW0tUHrhwoUvX75Elurt7Z02bRoex8HNxSOFsPLv379Hjx4tLCycOnXqr1+/gNK/f/9uaGhYt27dnz9/gAr6+vqmTJmCy+G4fInMRbeyurq6ra3t6dOnyNL//v1bv349UArZ4SYmJvjjklhf4opONG+9ffs2MDAQfypD45aXl1+9ehVfXELAwYMHvb29W1pa4CKZmZnXrl07fvx4ZWUlQV8iW3nr1i2grYStBEpPnDgRWWTp0qXFxcXNzc07d+4k6EuiMgnB/ARMTYmJiZ6enkAGHuPIySS4dAJjERi2Tk5OpaWl+/fvBya0z58/A5X9+PHj+/fvQPb79+9JLgqQTTc1NUUTBIbqpk2bvn37Nn/+/Pj4eEdHRzMzM2DqhRsXGxtLpi+dnZ2B9hUVFRFfYALz0l8woEexPgA1CdkAAPfCc9aaoG9pAAAAAElFTkSuQmCC'
# imgdata = base64.b64decode(img_base64)
# file = open('1.jpg', 'wb')
# file.write(imgdata)
# file.close()

# 使用百度的打码平台 认证图片


# encoding:utf-8

import requests
import base64

'''
通用文字识别
'''
# encoding:utf-8
import requests

# client_id 为官网获取的AK， client_secret 为官网获取的SK
# AK = '50oFSKIswtU9Ukoss5eGvI9t'
# SK = 'VEhkW3hGrlYCN7uWF9luY6PVMZjshxyA'
# host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={AK}&client_secret={SK}'
# response = requests.get(host)
# if response:
#     print(response.json())

request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
# 二进制方式打开图片文件
# f = open('[本地文件]', 'rb')
# img = base64.b64encode(f.read())

params = {"image": img_base64}
# access_token = response.json()['access_token']
access_token = '24.b14b83f6a46560f51147822e826052ce.2592000.1594538160.282335-19018359'
print(access_token)
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print(response.json())
