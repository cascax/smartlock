#!/usr/bin/env python
#coding:utf-8
from SocketServer import StreamRequestHandler, ThreadingTCPServer
import filelog, re, threading

identityRe = re.compile(r'\[(.+)\]')
condition = threading.Condition()
piOnline = False
openingDoor = False
clientName = ''

class ServerHandle(StreamRequestHandler):
    piName = 'ServerPi'

    def handle(self):
        self.addr = self.request.getpeername()[0]
        self.log = filelog.Log()
        self.wfile.write('success')
        msg = self.rfile.readline().strip()
        match = identityRe.match(msg)
        if match:
            self.identity = match.group(1)
            self.log('Got connection from %s(%s)' % (self.identity, self.addr))
        else:
            self.identity = ''
            self.log('False connection from (%s)' % self.addr)
            return
        
        if self.identity == self.piName:
            global piOnline
            # 更改树莓派服务器状态
            condition.acquire()
            piOnline = True
            condition.release()
            self.serverHandle()
        else:
            self.clientHandle()

    def finish(self):
        self.log('Offline (%s %s)' % (self.addr, self.identity))
        if self.identity == self.piName:
            global piOnline
            # 更改树莓派服务器状态
            condition.acquire()
            piOnline = False
            condition.release()
        StreamRequestHandler.finish(self)

    def serverHandle(self):
        global openingDoor
        while True:
            # print '-s'
            condition.acquire()
            if not openingDoor:
                condition.wait()
            self.openDoor(clientName)
            openingDoor = False
            condition.release()

    def clientHandle(self):
        global openingDoor, clientName
        if not piOnline:
            self.wfile.write('offline')
            return
        self.wfile.write('online')
        # while True:
            # print '-c'
        msg = self.rfile.readline().strip()
        if msg == 'openthedoor':
            condition.acquire()
            openingDoor = True
            clientName = self.identity
            condition.notify()
            condition.release()

    def openDoor(self, name):
        self.wfile.write('-opendoor [%s]' % name)
        self.log('%s open the door' % name)

server = ThreadingTCPServer(('0.0.0.0', 8088), ServerHandle)
server.serve_forever()
