import time
from multiprocessing.managers import BaseManager
"""
工作区代码
"""

class QueueManager(BaseManager):
    pass


# 实现第一步 注册获取queue的方法名称
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
# 实现第二步 连接到服务器
server_addr = '127.0.0.1'
print('connect to server %s...' % (server_addr))
# 端口和验证口令保持一致
m = QueueManager(address=('127.0.0.1', 8001), authkey=b'abc')
# 网络连接
m.connect()
# 获取queue的对象
task = m.get_task_queue()
result = m.get_result_queue()
# 从task获取任务，并且紫萼如result 队列
while(not task.empty()):
    image_url = task.get(True,timeout=5)
    print('run task download %s' % image_url)
    time.sleep(1)
    result.put(image_url)
print('worker exit')