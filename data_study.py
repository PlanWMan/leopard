"""
mongodb 的另一种应用
"""

from mongoengine import *

connect('test', host='localhost', port=27017)
import datetime


class Users(Document):
    name = StringField(required=True, max_length=200)
    age = IntField(required=True)


user1 = Users(
    name='zz',
    age=11
)
user1.save()
print(user1.name)
user1.name = 'zz11'
user1.save()
print(user1.name)
