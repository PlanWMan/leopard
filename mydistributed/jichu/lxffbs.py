"""
廖雪峰版分布式的讲解
服务器代码

"""

import random
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support, Queue

# 最大任务个数
task_number = 10
# 发送任务的队列:
task_queue = Queue(task_number)
# 接收结果的队列:
result_queue = Queue(task_number)


def get_task():
    return task_queue


def get_result():
    return result_queue


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


def win_run():
    # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
    QueueManager.register('get_task_queue', callable=get_task)
    QueueManager.register('get_result_queue', callable=get_result)
    # 绑定端口5000, 设置验证码'abc':
    manager = QueueManager(address=('127.0.0.1', 8001), authkey=b'abc')
    # 启动Queue:
    manager.start()
    try:
        # 获得通过网络访问的Queue对象:
        task = manager.get_task_queue()
        result = manager.get_result_queue()
        # 放几个任务进去:
        for i in range(10):
            n = random.randint(0, 10000)
            print('Put task %d' % n)
            task.put(n)
        # 从result队列读取结果:
        print('try get result')
        for i in range(10):
            print('result is %s' % result.get(timeout=10))
    # 关闭:
    except Exception as e:
        print(e)
    finally:
        manager.shutdown()
        print('master exit.')


if __name__ == '__main__':
    freeze_support()
    win_run()
