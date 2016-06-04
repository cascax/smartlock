#!/usr/bin/env python
#coding:utf-8

import time, thread, hardware, music, filelog
from config import Config
import getopt, sys


class KeyPadServer(object):
    """树莓派端键盘输入服务器"""

    def __init__(self, debug = False):
        self.music = music.Music()
        config = Config('pi.ini')
        self.password = config('keyserver', 'password')
        self.debug = debug
        self.filelog = filelog.Log()
        self.log('KeyPadServer Start', True)

    def log(self, str, fileOutput = False):
        if self.debug:
            print str
        if fileOutput:
            self.filelog('KeyServer: ' + str)

    def clear(self):
        """清除输入"""
        self.input = ''
        self.log('clear password')

    def doorbell(self):
        """门铃"""
        self.music.play('doorbell')
        self.log('play doorbell')

    def ok(self):
        """按下确认键"""
        if self.input == self.password:
            thread.start_new_thread(hardware.flickerLED, (2,))
            hardware.openThenClose()
            self.log('open the door', True)
        else:
            self.music.play('password_wrong')
            self.log('password wrong')
        self.clear()

    def cleanUp(self):
        """清除GPIO状态"""
        if self.input == self.password:
            hardware.clean()
            self.log('clean up')
        self.clear()

    def adjust(self):
        """调整电机"""
        if self.input == self.password:
            hardware.adjustDoor()
            self.log('adjust')
        self.clear()

    def start(self):
        kp = hardware.Keypad()
        self.input = ''

        while True:
            digit = None
            while digit == None:
                digit = kp.getKey()
            self.log(digit)
            # 判断输入
            if digit == '*':
                self.clear()
            elif digit == 'A':
                self.doorbell()
            elif digit == 'B':
                self.cleanUp()
            elif digit == 'C':
                self.adjust()
            elif digit == '#':
                self.ok()
            else:
                self.input += str(digit)
            time.sleep(0.3)

    def end(self):
        hardware.clean()
        self.log('KeyPadServer End', True)

if __name__ == '__main__':
    debug = False
    opts, args = getopt.getopt(sys.argv[1:], 'd', ['debug'])
    for o, v in opts:
        if o in ('-d', '--debug'):
            debug = True
    server = KeyPadServer(debug)
    try:
        server.start()
    except KeyboardInterrupt:
        server.end()
