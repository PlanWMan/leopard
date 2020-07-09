from multiprocessing import Process
import os

global_var = "I'm a global variable"


class SomeClass(object):
    def delete_mongo(self):
        print("aaa")

    def proce(self):
        trader = []
        for i in range(10):
            pr = Process(target=self.delete_mongo)
            pr.start()
            trader.append(pr)
        for i in trader:
            i.join()
        print('proce this is pid: %s' % os.getpid())




if __name__ == '__main__':
    GU = SomeClass()
    GU.proce()
