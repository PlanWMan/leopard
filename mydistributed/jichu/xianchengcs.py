"""
线程测试
"""

import threading
import time


def print_time(delay):
    x = delay
    time.sleep(delay)
    print("time sleep %s" % (x))


def print_time_two(delay):
    x = delay
    time.sleep(1)
    print("time sleep %s" % (x))


# 创建两个线程
thread1 = threading.Thread(target=print_time, args=[2, ])
thread2 = threading.Thread(target=print_time_two, args=[4, ])
thread1.start()
thread2.start()
thread1.join()
thread2.join()
