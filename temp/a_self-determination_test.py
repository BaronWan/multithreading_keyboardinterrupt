#!/usr/bin/env python3
import signal
from queue import Queue
from time import sleep
import sys,os


def child1(q):
    if q.qsize() > 0:
        data = q.get(block=False)
        if data == 'QUIT':
            print('child1 will be exit.')
            return data
        else:
            print('Getted the queue message:',data)
    else:
        print('queue is empty')


def main(func=None,args=None):
    def sighandler(sig, frame):
        q.put('QUIT')
    
    def tester(sec):
        print('now in tester func, and sec is',sec)
        signal.signal(signal.SIGALRM, sighandler)
        signal.alarm(sec)

    q = Queue()
    if func:
        eval('%s(%d)' %(func,args))
    while True:
        try:
            print('hello ~',end=' ')
            if not q:
                q.put('wait.')
            sleep(1)
            if child1(q) == 'QUIT':
                break
        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, sighandler)
            break
    return True


if __name__ == '__main__':
    if main('tester',3):
        sys.exit('system will be exit.')
    else:
        sys.exit('program may be have some question~')


