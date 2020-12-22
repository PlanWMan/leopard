# 京东的登录

import requests
import urllib3
import random
import base64
from json import loads
from JD.quekou import get_gap

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 获取背景图片,和滑块图片
reqs_session = requests.session()
data = {
    'appId': '167641c8938',
    'scene': 'login',
    'product': 'click-bind-suspend',
    'e': 'W4QLDOCEGDWGIUI5736DVXFDKHCO26XY7KK77JFPGMXCPGROA7JGLNGRGKGNVZLELRRMH5J2WAQTMCILWKUH5PBEO4',
    'lang': 'zh_CN',
    'callback': 'jsonp_039583990963708215'
}
url = "https://iv.jd.com/slide/g.html"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.8 Safari/537.36',
}

reqs = reqs_session.get(url, headers=headers, params=data, verify=False, allow_redirects=False, timeout=20)
img_nr = (loads((reqs.text.split("(")[1]).split(")")[0]))


# 还原图片
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


img_save('bg.jpg', base64.b64decode(img_nr['bg']))
img_save('patch.jpg', base64.b64decode(img_nr['patch']))

x = (get_gap('patch.jpg', 'bg.webp')) * 0.73  # 水平缺口距离

challenge = img_nr['challenge']  # 参数


# 登陆的链接


# 先生成路径 参数d

def get_y_path(random_num, y_list, y=380):
    # 获取随机数
    # 生成一个列表
    if len(y_list) > random_num:
        return y_list
    a = ([y] * 10) + [y - 1, y - 1] + [y + 1, y + 1] + [y + 2] + [y - 2]
    b = random.choice(a)
    y_list.append(b)
    return get_y_path(random_num, y_list, y=b)


# 生成 x 路径
def get_track7(distance):
    """
    根据偏移量和手动操作模拟计算移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    """
    # 移动轨迹
    tracks = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 时间间隔
    t = 0.2
    # 初始速度
    v = 0
    sum_ = 0

    while current < distance:
        if current < mid:
            a = random.uniform(2, 5)
        else:
            a = -(random.uniform(12.5, 13.5))
        v0 = v
        v = v0 + a * t
        x = v0 * t + 1 / 2 * a * t * t
        current += x

        if 0.6 < current - distance < 1:
            x = x - 0.53
        elif 1 < current - distance < 1.5:
            x = x - 1.4
        elif 1.5 < current - distance < 3:
            x = x - 1.8
        tt = round(x, 2)
        sum_ += tt
        tracks.append(sum_)

    return tracks


def get_time_path(state_time, end_time, size=70):
    # 获取时间戳的列表
    return sorted(random.sample(range(state_time, end_time), size))


y_list = []
# 时间
path_time = int(random.uniform(3, 5) * 100) / 100
print(path_time)
x = get_track7(distance=x)
# 将列表里每一项数都加 884
x = [884] + [int(i + 884) for i in x]
print(x)
print(len(x))
y = get_y_path(random_num=len(x), y_list=y_list)
print(y)
# 生成时间戳

import time

t = time.time()
end_time = int(round(t * 1000))
state_time = int(end_time - path_time * 1000)
times = get_time_path(state_time, end_time, len(x))
end_time = ([[o, t, s] for o, t, s in zip(x, y, times)])
print(end_time)
import execjs

with open('./login.js', 'r', encoding='utf-8') as fp:
    js = fp.read()
ctx = execjs.compile(js)
results = ctx.call("papi", end_time)
# print(ctx.call("get_y9r",[7,28,16]))
print(results)

# 滑块
data = {
    'd': results,
    'c': challenge,
    'w': 226,
    'appId': '167641c8938',
    'scene': 'login',
    'product': 'click-bind-suspend',
    'e': 'W4QLDOCEGDWGIUI5736DVXFDKHCO26XY7KK77JFPGMXCPGROA7JGLNGRGKGNVZLELRRMH5J2WAQTMCILWKUH5PBEO4',
    's': '',
    'o': '',
    'lang': 'zh_CN',
    'callback': 'jsonp_09397679174027942',
}
url = "https://iv.jd.com/slide/s.html"
reqs = reqs_session.get(url, headers=headers, params=data, verify=False, allow_redirects=False, timeout=20)
print(reqs.text)
