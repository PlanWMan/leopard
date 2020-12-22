"""
图片还原
"""

from pymongo import MongoClient
import random

db = MongoClient(host='172.16.6.196', port=28018)['py_business']
db.authenticate('py_yangying', 'Cyke746TGSBunbQ8Y')
collect = db['icr_data_sectioning']


def img_address(img_type):
    """
    饭后路径和名称
    """
    return f'./{"".join(str(random.choice(range(10))) for _ in range(10))}.{img_type}'


def img_save(img_path, content):
    """
    保存图片
    """
    with open(img_path, 'wb') as f:
        f.write(content)


i = collect.find_one({'_id': '0136371bf56b26c8ecc7d3cc1bc70956'})
import base64
# img_base64=base64.b64encode(im)
img_path = img_address('jpg')
img_save(img_path, i['img'])
# import pytesseract
# from PIL import Image

# image = Image.open('ImageIdentification/test.png')
# code = pytesseract.image_to_string(i['img'], lang="chi_sim+eng")
# print(code)
# import requests
# r = requests.get('https://avatar.csdn.net/2/E/C/3_u010590983.jpg')
# with open('avatar.jpg','wb') as f:
#     f.write(r.content)
