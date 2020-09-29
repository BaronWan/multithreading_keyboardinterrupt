#!/usr/bin/env python3
# @author: Bruce Wan

from queue import Queue
import threading
import signal
from time import sleep
import sys


def world(outq):
    while True:
        if outq.qsize() > 0:
            data = outq.get()
            print('Get the queue: %s' % data)
            if data == 'QUIT':
                sys.exit('world will be exit...')
        print('world checking...')
        sleep(0.0001)


def hello(outq):
    while True:
        if outq.qsize() > 0:
            data = outq.get()
            print('Get the queue: %s' % data)
            if data == 'QUIT':
                sys.exit('hello will be exit...')
        print('hello checking...')
        sleep(0.0001)


# args = (func,(params,))
def main(args=None):
    def _quit():
        q1.put('QUIT')
        q2.put('QUIT')
        th1.join()
        th2.join()

    def __sighandler(sig, frame):
        raise KeyboardInterrupt

    def tester(sec):
        signal.signal(signal.SIGALRM, __sighandler)
        signal.alarm(sec)

    q1 = Queue()    # th1 專用
    q2 = Queue()    # th2 專用
    th1 = threading.Thread(target=hello, args=(q1,))
    th2 = threading.Thread(target=world, args=(q2,))
    th1.start()
    th2.start()
    if args:
        eval('%s(%s)' % (args[0], args[1][0]))
    while True:
        try:
            #sleep(0.00000001)
            if not th1.is_alive() and not th2.is_alive():
                print('Child threading all exited.')
                break
        except KeyboardInterrupt:
            _quit()
            return True


if __name__ == '__main__':
    # if main(('tester',(1,))):
    if main():
        sys.exit('system has be exit')
