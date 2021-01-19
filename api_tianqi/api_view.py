import requests
import os
import execjs
os.environ["EXECJS_RUNTIME"] = "Node"


if __name__ == '__main__':

    city = '北京'
    type = 'HOUR'
    file = './aqistudy.js'
    node = execjs.get()
    ctx = node.compile(open(file).read())
    js = 'pNg63WJXHfm8r("GETDATA", {city: "长春"})'
    params = ctx.eval(js)
    print(params)
    api = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
    response = requests.post(api, data={'h0lgYxgR3': params})
    decode_js = f'dX506x9jVK3vuMMhoz6ZXx("{str(response.text)}")'
    decrypted_data = ctx.eval(decode_js)
    print(decrypted_data)