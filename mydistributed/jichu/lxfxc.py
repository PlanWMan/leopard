"""
廖雪峰 协程
协程程序内部可以中断执行别的子程序，适当的时候再返回来接着执行
程序切换是由程序控制的不是线程切换所以没有线程切换的开销
不需要锁的机制
如何利用多核cpu 方法是多进程+协程
协成是通过generator实现的
"""


# def aa():
#     for i in range(10):
#         yield i
#
# print([i for i in aa()])
import  time
# 成产者消费者协成模型
def consumer():
    r = ''
    while True:
        e = yield r
        if e == 3:
            yield time.sleep(2)
        if not e:
            return
        print('consuming %s' % e)
        r = '200ok'


def produce(c):
    # 启动生成器
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('producing %s' % n)
        w = c.send(n)  # 产生了新的东西就切换到consumer里面执行返回参数
        print('consumer return %s' % w)
    c.close()


c = consumer()
produce(c)
