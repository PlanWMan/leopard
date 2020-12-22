import time
from mydistributed.mycelery.celery_app import app

@app.task
def multiply(x, y):

    print(x, y, 'task2')
    return x * y
