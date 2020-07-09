from multiprocessing import Process
import os, time, random


class aa():
    def long_time_task(self, name):
        print('Run task %s (%s)...' % (name, os.getpid()))
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print('Task %s runs %0.2f seconds.' % (name, (end - start)))

    def proce(self):
        trader = []
        for i in range(10):
            pr = Process(target=self.long_time_task, args=(i,))
            pr.start()
            trader.append(pr)
        for i in trader:
            i.join()
        print('proce this is pid: %s' % os.getpid())


if __name__ == '__main__':
    p1 = aa()
    p1.proce()
