import requests
from time import time
import random, os
import urllib3
urllib3.disable_warnings()
import base64

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4122.7 Safari/537.36',
}


def get_img():
    """
    获取图片验证码
    """
    img_url = f'https://www.b2b315.com/skin/m03skinBlue/tel.php?auth=f6308ndCAMkrjNXlAmewfgL9id9MvBu-P-r5jkaG0nOKMck1Y5GKpc4jtZuJQ7'
    # img_url = 'https://qq.yh31.com/tp/zjbq/201912111206170144.gif'
    resp = requests.get(img_url, headers=headers, verify=False)
    img_path = f'./{"".join(str(random.choice(range(10))) for _ in range(10))}.gif'  # 随机十位数字用来命名图片
    with open(img_path, 'wb') as f:
        f.write(resp.content)

    # temp_file = open(img_path, 'rb')
    # temp_image = temp_file.read()
    # temp_file.close()
    # temp_data = {
    #     'image': base64.b64encode(temp_image)
    # }
    # 使用打码平台查看数字
    # result = None
    # if os.path.exists(img_path):
    #     try:
    #         # cid, result = get_captcha(img_path, 1004)
    #         # 手动打码
    #         result = input("图片数字")
    #     except Exception as e:
    #         print("图片识别报错")
    #     finally:
    #         os.remove(img_path)
    #     return result
    # return None

get_img()
