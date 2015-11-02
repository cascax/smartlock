#!/usr/bin/env python
#coding:utf-8

import time, thread, hardware, music


class KeyPadServer(object):
    """树莓派端键盘输入服务器"""
    password = '28102B'

    def __init__(self):
        self.music = music.Music()

    def clear(self):
        """清除输入"""
        self.input = ''

    def doorbell(self):
        """门铃"""
        self.music.play('password_wrong')

    def ok(self):
        """按下确认键"""
        if self.input == self.password:
            print 'open the door'
            thread.start_new_thread(hardware.flickerLED, (2,))
            hardware.openThenClose()
            self.input = ''
        else:
            self.music.play('password_wrong')

    def start(self):
        kp = hardware.Keypad()
        self.input = ''

        while True:
            digit = None
            while digit == None:
                digit = kp.getKey()
            # 判断输入
            if digit == '*':
                self.clear()
            elif digit == 'A':
                self.doorbell()
            elif digit == '#':
                self.ok()
            else:
                self.input += str(digit)
            time.sleep(0.3)

if __name__ == '__main__':
    server = KeyPadServer()
    server.start()
