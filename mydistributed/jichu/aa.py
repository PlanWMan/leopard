# 编写多线程和多进程的应用
import threading
import time


def sjc(func):
    def nh(*args, **kwargs):
        a_ = int(time.time() * 1000)
        a = func(*args, kwargs)
        b_ = int(time.time() * 1000)
        print(b_ - a_)
        return a

    return nh


def target(second):
    print(f'Threading {threading.current_thread().name} is runing')
    print(f'Threading {threading.current_thread().name} sleep {second}s')
    time.sleep(second)
    print(f'threading {threading.current_thread().name} is targetend')


# print(f'Threading {threading.current_thread().name} is runding')
@sjc
def ccc(*args, **kwargs):
    kk = []
    for i in [3, 5]:
        t = threading.Thread(target=target, args=[i, ])
        t.start()
        kk.append(t)
    for i in kk:
        i.join()

    print(f'Threading {threading.current_thread().name} is end')


# @sjc
# def ccc(*args, **kwargs):
#     time.sleep(3)


# 还有守护线程，如果有join方法 守护线程也会等待
# python的多线程还会有GIL问题


"""
多进程可以发挥多核的优势
"""
import multiprocessing, os


def process(index):
    print(f'process: {os.getpid()}')


def dddone():
    for i in range(5):
        p = multiprocessing.Process(target=process, args=(i,))
        p.start()
    print(f'cpu number {multiprocessing.cpu_count()}')
    for p in multiprocessing.active_children():
        print(f'child process name:{p.name} id:{p.pid}')
    print('process ended')


# 直接继承process 来设置进程
class Myprocess(multiprocessing.Process):
    def __init__(self, loop):
        super().__init__()
        self.loop = loop

    def run(self):
        print(f'process: {os.getpid()} , loop:{self.loop}')
        time.sleep(self.loop)
        print('end')


@sjc
def ddd(*args, **kwargs):
    rr = []
    for i in range(2, 5):
        p = Myprocess(i)
        # p.daemon = True  # 设置为守护进程
        p.start()
        rr.append(p)

    for i in rr:
        i.join(1)  # 可以设置超时时间


# 进程池pool的使用

from multiprocessing import Pool


def function(index):
    print(f'start process : {index}')
    time.sleep(index)
    print(f'end process {index}')


@sjc
def ttt(*args, **kwargs):
    pool = Pool(processes=3)
    for i in range(4):
        pool.apply_async(function, args=(i,))
    print('main process stated')
    pool.close()
    pool.join()
    print('main process end')


# 进程map方法的使用
import requests


def scrape(url):
    try:
        print(f'url {url} scraped')
        req = requests.get(url)
    except Exception as e:
        print(e)
    finally:
        print(f"{os.getpid()} end")


def uuu():
    pool = Pool(processes=3)
    urls = [
        'https://baidu.com',
        'https://baidu1.com',
        'https://baidu2.com',
        'https://baidu3.com',

    ]
    pool.map(scrape, urls)
    pool.close()


from retrying import retry  # 异常重试包


@retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None)
def fetch():
    try:
        url = 'https://baidu1.com'
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        return None


if __name__ == '__main__':
    fetch()
    # f = lambda x: x is None
    # print(f(None))
