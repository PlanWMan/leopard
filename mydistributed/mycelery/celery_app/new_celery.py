from celery import Celery

app = Celery('demo', include=['mydistributed.mycelery.celery_app.task1','mydistributed.mycelery.celery_app.task2'])
app.config_from_object('mydistributed.mycelery.celery_app.celeryconfig') # 通过celery实例加载配置模块

if __name__ == '__main__':

    app.start()