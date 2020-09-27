#!/usr/bin/env python3
# Wan Pei Chih <davidwan58@gmail.com>

from queue import Queue
import threading
from time import sleep
import sys

# args = [(func1,(param1,)),(func2,(param1,)),...]
class MyThreading:
    def __init__(self, **args):
        self.DELAY = 1
        self.targets = [x[0] for x in args]
        self.args = [x[1] for x in args]
        self.run()
    
    def run(self):
        self.evt = threading.Event()
        self.qs = [Queue()]*len(self.targets)
        self.ths = []
        for n in range(len(self.targets)):
            Th = threading.Thread(
                    target=self.targets[n],
                    args=self.args[n])
            Th.start()
            self.ths.append(Th)
        try:
            while not self.evt.wait(timeout=self.DELAY):
                print('Main thread processing...')
        except KeyboardInterrupt:
            self.evt.set()
            for n in range(len(self.ths)):
                self.qs[n].put('QUIT')
                self.ths[n].join()
        


def world(outq):
      while True:
          if outq.qsize() > 0:
              data = outq.get()
              print('Get the queue: %s' %data)
              if data == 'QUIT':
                  sys.exit('world will be exit...')
          print('world checking...')
  
def hello(outq):
      while True:
          if outq.qsize() > 0:
              data = outq.get()
              print('Get the queue: %s' %data)
              if data == 'QUIT':
                  sys.exit('hello will be exit...')
          print('hello checking...')


if __name__ == '__main__':
     q1 = Queue()    # th1 專用
     q2 = Queue()    # th2 專用
     th1 = threading.Thread(target=hello, args=(q1,))
     th2 = threading.Thread(target=world, args=(q2,))
     th1.start()
     th2.start()
     while True:
         try:
             sleep(1)
             if not th1.is_alive() and not th2.is_alive():
                 print('Child threading all exited.')
                 break
         except KeyboardInterrupt:
             q1.put('QUIT')
             q2.put('QUIT')
             th1.join()
             th2.join()
     sys.exit('main thead has be exit')
 
