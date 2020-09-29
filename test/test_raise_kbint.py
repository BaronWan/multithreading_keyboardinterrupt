#!/usr/bin/env python3
import unittest
import signal
import sys

sys.path.append('../src')
import threading_ctypes_raise_sample as thcx
from threading_kbint_sample_class import MyThreading
import threading_kbint_sample as thks


class UnitTesting(unittest.TestCase):
    def test_kbint_sample_of_1(self):
        res = thks.main(('tester', (1,)))
        self.assertTrue(res)

    def test_kbint_sample_of_2(self):
        def kbint_handler(*args):
            q1.put('QUIT')
            q2.put('QUIT')
            raise KeyboardInterrupt
        if __name__ == '__main__':
            q1 = thks.Queue()
            q2 = thks.Queue()
            # on-click [ctrl+c]
            # self.onKbInt()
            # Using alarm to click except of keyboardInterrupt
            signal.signal(signal.SIGALRM, kbint_handler)
            signal.alarm(1)
            Th = thcx.MyThreading([
                (thks.hello, (q1,)),
                (thks.world, (q2,))])
            self.assertTrue(Th)

    def test_kbint_sample_class(self):
        def kbint_handler(*args):
            raise KeyboardInterrupt
        signal.signal(signal.SIGALRM, kbint_handler)
        signal.alarm(1)
        Th = MyThreading()
        self.assertTrue(Th)

    def test_ctypes_raise_sample(self):
        def kbint_handler(sig, frame):
            raise KeyboardInterrupt
        signal.signal(signal.SIGALRM, kbint_handler)
        signal.alarm(1)
        Th = thcx.MyThreading([
            (thcx.f, ()),
            (thcx.f2, ())])
        self.assertTrue(Th)


if __name__ == '__main__':
    unittest.main()
