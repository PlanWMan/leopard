from flask import Flask
from flask_cors import CORS

apps = Flask(__name__)
CORS(apps)

resp = {
    'state': '200',
    'message': 'success',
    'data': {}
}
fail = {
    'state': '-1',
    'message': ''
}

__ALL__ = ['apps', 'resp', 'fail']
