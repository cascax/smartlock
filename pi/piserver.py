#!/usr/bin/env python
##coding:utf-8
import socket, re, time
import hardware

msgTemplate = re.compile(r'\-(\w+) \[(.+)\]')
s = socket.socket()
# server = ('45.62.118.214', 8088)
server = ('127.0.0.1', 8088)

def connect():
    s.connect(server)
    ifsucc = s.recv(1024).strip()
    if ifsucc == 'success':
        print 'remote server(%s, %s) connected successful' % server
    else:
        print 'remote server(%s, %s) refused' % server
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
                    print '%s open and close the door' % identity
                    hardware.openThenClose()
                elif order == 'justopen':
                    print '%s open the door' % identity
                    hardware.openDoor()
                elif order == 'closedoor':
                    print '%s close the door' % identity
                    hardware.closeDoor()
                elif order == 'exit':
                    break
        s.close()
    except socket.error:
        print 'lost remote server(%s, %s)' % server

def begin():
    try:
        connect()
        handle()
    except socket.error, e:
        print 'connect failed [%d]: %s' % (e.errno, socket.errorTab[e.errno])

begin()