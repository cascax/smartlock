#!/usr/bin/env python
##coding:utf-8
import time, hardware

def main():
    kp = hardware.Keypad()
    password = ''

    while True:
        digit = None
        while digit == None:
            digit = kp.getKey()
        # 判断输入
        if digit == '*':
            password = ''
        elif digit == '#' and password == '28102B':
            print 'open the door'
            hardware.openThenClose()
            password = ''
        else:
            password += str(digit)
        time.sleep(0.3)

if __name__ == '__main__': main()
