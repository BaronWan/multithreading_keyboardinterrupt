#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Bruce Wan
"""
import ctypes
import threading
from time import sleep
import sys

# args = [(func1,(param1,)),]
class MyThreading:
    def __init__(self, args):
        self.NULL = 0
        self.DELAY = 0.000000001
        self.targets = [ x[0] for x in args ]
        self.args = [ x[1] for x in args ]
        self.run()

    def run(self):
        # record threads
        self.ths = []
        # The threading Event() must be written before Thread()
        evt = threading.Event()
        for n in range(len(self.targets)):
            Th = threading.Thread(
                    target=self.targets[n], 
                    args=self.args[n])
            Th.start()
            self.ths.append(Th)
        try:
            while not evt.wait(timeout=self.DELAY):
                print('Main thread processing...')
        except KeyboardInterrupt:
            # Thread 事件觸發
            evt.set()
            # 進行子線程的例外(SystemExit)發布
            self.ctype_async_raise(SystemExit)
            # 等待確認所有子線程的結束
            # 少了它 join(), 主線程會先離開, 子線程先後離開。
            # 由於線程特性, 當主線程結束時, 子線程是會隨著結束的。
            # 但是當有程式上的需要, 必須有先後關係時, 那確認子線程的結束就有其必要了。
            # 我的觀點：因為不是源自子線程func中觸發結束，讓子線程先結束工作可以減少失誤發生。
            for Th in self.ths:
                Th.join()
                
            # 子線程存活清單確認
            # 先假設一種條件: 所有的子線程都存活著(True)
            th_alive = [True]*len(self.ths)
            for n in range(len(self.ths)):
                # 當有一子線程已結束,則對應列表將為(False)
                if not self.ths[n].is_alive():
                    th_alive[n] = False
            # 確認子線程是否都已離開
            if not True in th_alive:
                print('Child threads all exited.')
                return True
    
    # reference from https://gist.github.com/liuw/2407154
    def ctype_async_raise(self, exception):
        found = False
        targetID = 0
        for Th in self.ths:
            for tid,tobj in threading._active.items():
                # Have matches ?
                if tobj is Th:
                    found = True
                    targetID = tid
                    break
            # Have not any can be matches ?
            if not found:
                raise ValueError("Invalid thread object")
            # call the ctypes api func to setting a exception.    
            ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(targetID),
                    ctypes.py_object(exception))
            # 不合法的線程ID
            if ret == 0:
                raise ValueError("Invalid thread ID")
            # 遠程 api 進行子線程例外執行失敗
            elif ret > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(
                        targetID, self.NULL)
                raise SystemError("PyThreadState_SetAsyncExc failed")
            # ret < 0, 相關子線程的例外執行成功
            print("Successfully set asynchronized exception for", targetID)


# sample func of child thread 1
def f():
    try:
        while True:
            print('child thread f checking...')
            sleep(0.000001)
    finally:
        print("child 1 exited.")
        
# sample func of child thread 2
def f2():
    while True:
        print('child thread f2 checking...')
        sleep(0.000001)
    print("child 2 exited.")
        
        
if __name__ == '__main__':
    # 這樣設計可以接收來自外部有要加入子線程運行的 func 加入工作。
    # 若是都放在 class 中則為固定要運行的工作 func。
    Th = MyThreading([(f,()),(f2,())])
    if Th:
        sys.exit('system will be exit.')

"""[execute result]
child thread f checking...
child thread f2 checking...
Main thread processing...
child thread f checking...
child thread f2 checking...
Main thread processing...
child thread f checking...
child thread f2 checking...
Main thread processing...
child thread f checking...
child thread f2 checking...
...
^C <當按下鍵盤中斷 ctrl+c 時>
Successfully set asynchronized exception for 140684049725184
Successfully set asynchronized exception for 140684041332480
child 1 exited.
Child threads all exited.
system will be exit.
""" 
