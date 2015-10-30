#!/usr/bin/env python
##coding:utf-8
import time, thread, hardware, music

def start():
    kp = hardware.Keypad()
    password = ''

    while True:
        digit = None
        while digit == None:
            digit = kp.getKey()
        # 判断输入
        if digit == '*':
            password = ''
        elif digit == '#':
            if password == '28102B':
                print 'open the door'
                thread.start_new_thread(hardware.flickerLED, (2,))
                hardware.openThenClose()
                password = ''
            else:
                music.play('password_wrong')
        else:
            password += str(digit)
        time.sleep(0.3)

if __name__ == '__main__': start()
