#!/usr/bin/env python3
# Wan Pei Chih <davidwan58@gmail.com>
# 假設情境一：
#    程式中正在運用 Queue 進行線程間的資訊傳遞，這時我們可以利用此一溝通管道進行,
#  當使用者觸發一 keyboard interrupt 的事件時, 主線程經由 Queue 通知所有子線程準備結束。
#
from queue import Queue
import threading
from time import sleep
import sys

# args = [(func1,(param1,)),(func2,(param1,)),...]
class MyThreading:
    def __init__(self):
        self.DELAY = 0.000000001
        self.targets = [self.f1, self.f2]
        self.args = [(Queue(),), (Queue(),)]
        self.run()

    def run(self):
        self.evt = threading.Event()
        self.ths = []
        for n in range(len(self.targets)):
            Th = threading.Thread(
                    target=self.targets[n],
                    args=self.args[n])
            Th.start()
            self.ths.append(Th)
        try:
            # Event.wait() 擁有比 time.sleep() 更高的響應速度
            while not self.evt.wait(timeout=self.DELAY):
                print('Main thread processing...')
        except KeyboardInterrupt:
            # 使用者觸發鍵盤中斷, 設定事件已觸發。(Event.set()=True)
            self.evt.set()
            for n in range(len(self.ths)):
                self.args[n][0].put('QUIT')
                # 少了它 join(), 主線程會先離開, 子線程先後離開。
                # 由於線程特性, 當主線程結束時, 子線程是會隨著結束的。
                # 但是當有程式上的需要, 必須有先後關係時, 那確認子線程的結束就有其必要了。
                self.ths[n].join()
                
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


    def f1(self, outq):
        while True:
            # 雖然 queue.get() 具備 blocking 的作用, 但測試後還是認為於 get() 前判斷 queue() 中是否有值出現會比較好。
            if outq.qsize() > 0:
                data = outq.get()
                print('Get the queue: %s' %data)
                if data == 'QUIT':
                    print('f1 will be exit...')
                    break
            print('f1 checking...')
            # 調整行進速度
            sleep(self.DELAY*1000)
        return
    

    def f2(self, outq):
        while True:
            if outq.qsize() > 0:
                data = outq.get()
                print('Get the queue: %s' %data)
                if data == 'QUIT':
                    print('f2 will be exit...')
                    break
            print('f2 checking...')
            # 調整行進速度
            sleep(self.DELAY*1000)
        return


if __name__ == '__main__':
     Th = MyThreading()
     if Th:
         sys.exit('System will be exit.')

