BROKER_URL = 'redis://localhost:6379/1' # 使用Redis作为消息代理

CELERY_RESULT_BACKEND = 'redis://localhost:6379/2' # 把任务结果存在了Redis

CELERY_TIMEZONE = "Asia/Shanghai"

CELERY_IMPORTS = (
        'celery_app.task1',
        'celery_app.task2',
    )
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
        'task1': {
            "task": "celery_app.task1.add",
            "schedule": timedelta(seconds=10),
            "args": (2, 8),
        },
        'task2': {
            "task": "celery_app.task2.multiply",
            "schedule": timedelta(seconds=3),
            "args": (4, 6),
        }
    }