"""
flask 的学习
"""

# 一个小的flask应用

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
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



