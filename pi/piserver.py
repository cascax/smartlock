#!/usr/bin/env python
#coding:utf-8
# 连接远程服务器的树莓派端

import socket, re, time
import hardware, filelog

log = filelog.Log()
msgTemplate = re.compile(r'\-(\w+) \[(.+)\]')
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
server = ('45.62.118.214', 8089)
# server = ('127.0.0.1', 8089)

def connect():
    s.connect(server)
    ifsucc = s.recv(1024).strip()
    if ifsucc == 'success':
        log('remote server(%s, %s) connected successful' % server)
    else:
        log('remote server(%s, %s) refused' % server)
        exit()
    s.send('[ServerPi]\n')

def handle():
    try:
        while True:
            msg = s.recv(1024)
            match = msgTemplate.match(msg)
            if match:
                order = match.group(1)
                identity = match.group(2)
                if order == 'opendoor':
                    log('%s open and close the door' % identity)
                    hardware.openThenClose()
                elif order == 'justopen':
                    log('%s open the door' % identity)
                    hardware.openDoor()
                elif order == 'closedoor':
                    log('%s close the door' % identity)
                    hardware.closeDoor()
                elif order == 'adjustdoor':
                    log('%s adjust the door' % identity)
                    hardware.adjustDoor()
                elif order == 'exit':
                    break
        s.close()
    except socket.error:
        print 'lost remote server(%s, %s)' % server
        log('ERROR: lost remote server(%s, %s)' % server)

def start():
    try:
        connect()
        handle()
    except socket.error, e:
        print 'connect failed [%d]: %s' % (e.errno, socket.errorTab[e.errno])
        log('ERROR: connect failed [%d]: %s' % (e.errno, socket.errorTab[e.errno]))

if __name__ == '__main__': start()