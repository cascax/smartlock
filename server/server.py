#!/usr/bin/env python
#coding:utf-8
# 远程服务器端

from SocketServer import StreamRequestHandler, ThreadingTCPServer
from ThreadEvent import ThreadEvent
import filelog, re, threading, time

identityRe = re.compile(r'\[(.+)\]')
condition = threading.Condition()
# 收到客户端信息事件
clientMsgEvent = ThreadEvent()
# 正在操作门标志
operatingDoor = False

class ServerHandle(StreamRequestHandler):
    piName = 'ServerPi'

    def __init__(self):
        self.log = filelog.Log()
        super(ServerHandle, self).__init__()

    def handle(self):
        self.addr = self.request.getpeername()[0]
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
            self.serverHandle()
        else:
            self.clientHandle()

    def finish(self):
        self.log('Offline (%s %s)' % (self.addr, self.identity))
        StreamRequestHandler.finish(self)

    def serverHandle(self):
        global operatingDoor
        clientMsgEvent.clear()
        while True:
            # 等待客户端请求
            if not clientMsgEvent.isSet():
                clientMsgEvent.wait()
            clientName = clientMsgEvent.getIdentify()
            eventName = clientMsgEvent.clear()
            if eventName == 'opendoor':
                if not operatingDoor:
                    self.openDoor(clientName)
            elif eventName == 'justopen' or eventName == 'closedoor' or eventName == 'adjustdoor':
                if not operatingDoor:
                    self.doorOperate(eventName, clientName)
            elif eventName == 'exitpi':
                self.exitPiServer(clientName)
                break;

    def clientHandle(self):
        msg = self.rfile.readline().strip()
        # 唤醒树莓派的连接
        clientMsgEvent.set(msg, self.identity)

    def openDoor(self, name):
        # 正在开门
        self.setOperatingDoor(True)
        self.wfile.write('-opendoor [%s]' % name)
        self.log('%s open and close the door' % name)
        time.sleep(10)
        # 开门完毕
        self.setOperatingDoor(False)

    def doorOperate(self, operation, name):
        # 正在开/关门
        self.setOperatingDoor(True)
        self.wfile.write('-%s [%s]' % (operation, name))
        self.log('%s operate the door (%s)' % (name, operation))
        time.sleep(5)
        # 开/关门完毕
        self.setOperatingDoor(False)

    def exitPiServer(self, name):
        self.wfile.write('-exit [%s]' % name)
        self.log('%s close the Pi Server' % name)

    def setOperatingDoor(self, operating):
        global operatingDoor
        condition.acquire()
        try:
            operatingDoor = operating
        finally:
            condition.release()


server = ThreadingTCPServer(('0.0.0.0', 8088), ServerHandle)
server.serve_forever()
