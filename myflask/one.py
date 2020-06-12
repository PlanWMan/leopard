"""
flask 的学习
"""

# 一个小的flask应用

from flask import Flask
import requests

app = Flask(__name__)


@app.route("/")
def index():
    reqs = requests.get(url="https://www.baidu.com/")
    print(reqs.url)
    print(reqs.status_code)
    reqs = requests.get(url='https://paat1001.b2b.hc360.com/shop/show.html')
    print(reqs.url)
    print(reqs.status_code)
    return "index page"


@app.route("/hello")
def hello():
    return "Hello, word"

@app.route('/user/<username>')
def show_user_profile(username):
    return 'user %s' % (username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % (subpath)



