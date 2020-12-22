BROKER_URL = 'redis://localhost:6379/1' # 使用Redis作为消息代理

CELERY_RESULT_BACKEND = 'redis://localhost:6379/2' # 把任务结果存在了Redis

CELERY_TIMEZONE = "Asia/Shanghai"

CELERY_IMPORTS = (
        'mydistributed.mycelery.celery_app.task1',
        'mydistributed.mycelery.celery_app.task2',
    )
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
        'task1': {
            "task": "mydistributed.mycelery.celery_app.task1.add",
            "schedule": timedelta(seconds=20),
            "args": (2, 8),
        },
        'task2': {
            "task": "mydistributed.mycelery.celery_app.task2.multiply",
            "schedule": timedelta(seconds=15),
            "args": (4, 6),
        }
    }