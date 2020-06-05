"""
flask 自带的服务器配置为debug模式
"""
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    print("请求方式为-----》", request.method)
    # args = request.args.get("name") or "args 没有参数"  # get 请求
    args = request.args.to_dict()
    print("args 参数是---》", args)
    form = request.form.to_dict() or 'form 没有参数'  # post请求
    print('form参数是--->', form)
    return jsonify(args=args, form=form)  # 数据的变为json格式


if __name__ == '__main__':
    app.run(debug=True)
