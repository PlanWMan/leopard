import time
from celery_app import app
import cerleryconfig

@app.task
def add(x, y):
    time.sleep(3)
    for i in cerleryconfig.aa:
        print(i)
    return x + y
