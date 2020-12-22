import time
from mydistributed.mycelery.celery_app import app
from mydistributed.mycelery import cerleryconfig
import zmail

@app.task
def add(x, y):
    server = zmail.server('w1830678@163.com', 'MNZKVOUEIVQEYWNL')

    # Send mail
    server.send_mail('w1830678@163.com', {'subject': 'Hello!', 'content_text': 'By zmail.'})
    print(x, y, 'task1')
    return x + y

add(4,5)
