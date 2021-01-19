import hashlib
from hashlib import md5

'''
财联社 sign
e.XXX 样式加密 并且 长度为40 几乎是cryptojs sha1加密
长度为 32 是 MD5加密
'''


def USE_SHA(text):
    if not isinstance(text, bytes):
        text = bytes(text, 'utf-8')
    sha = hashlib.sha1(text)
    encrypts = sha.hexdigest()
    return encrypts


def md5value(s):
    a = md5(s.encode()).hexdigest()
    return a


a = "app=CailianpressWeb&category=&lastTime=1608802349&last_time=1608802349&os=web&refresh_type=1&rn=20&sv=7.5.5"

b = USE_SHA(a)
print(len(b), b)
c = md5value(b)
print(c)