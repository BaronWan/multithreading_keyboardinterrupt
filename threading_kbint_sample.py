#!/usr/bin/env python3
__author__ = 'Wan Pei Chih <davidwan58@gmail.com>'

from queue import Queue
from threading import Thread
from time import sleep
import sys, os

def world(outq):
    while True:
        if outq.qsize() > 0:
            data = outq.get()
            print('Get the queue: %s' %data)
            if data == 'QUIT':
                sys.exit('world will be exit...')
        print('world checking...')
        sleep(1.5)

def hello(outq):
    while True:
        if outq.qsize() > 0:
            data = outq.get()
            print('Get the queue: %s' %data)
            if data == 'QUIT':
                sys.exit('hello will be exit...')
        print('hello checking...')
        sleep(1)

if __name__ == '__main__':
    q1 = Queue()    # th1 專用
    q2 = Queue()    # th2 專用
    th1 = Thread(target=hello, args=(q1,))
    th2 = Thread(target=world, args=(q2,))
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

