#!/usr/bin/env python
#coding:utf-8
# 树莓派端网络服务器

from SocketServer import StreamRequestHandler, ThreadingTCPServer
from music import Music
import filelog, re, threading, time
import hardware

# 身份验证正则
identityRe = re.compile(r'\[(.+)\]')
# 声音命令正则
soundRe = re.compile(r'sound\[(.+)\]')

# 操作门标志锁
condition = threading.Condition()
# 正在操作门标志
operatingDoor = False

music = Music()

class ServerHandle(StreamRequestHandler):

    def handle(self):
        self.log = filelog.Log()
        self.addr = self.request.getpeername()[0]
        self.wfile.write('success\n')
        msg = self.rfile.readline().strip()
        match = identityRe.match(msg)
        if match:
            self.identity = match.group(1)
            self.log('Got connection from %s(%s)' % (self.identity, self.addr))
        else:
            self.identity = ''
            self.log('False connection from (%s)' % self.addr)
            return
        
        self.clientHandle()

    def clientHandle(self):
        # 等待客户端请求
        msg = self.rfile.readline().strip()
        if msg == 'exitpi':
            self.exitPiServer(self.identity)
        else:
            global operatingDoor
            if not operatingDoor:
                self.doorOperate(msg, self.identity)

    def doorOperate(self, order, identity):
        # 正在开/关门
        self.setOperatingDoor(True)

        sound = soundRe.match(order)
        if order == 'opendoor':
            self.log('%s open and close the door' % identity)
            hardware.openThenClose()
        elif order == 'justopen':
            self.log('%s open the door' % identity)
            hardware.openDoor()
        elif order == 'closedoor':
            self.log('%s close the door' % identity)
            hardware.closeDoor()
        elif order == 'adjustdoor':
            self.log('%s adjust the door' % identity)
            hardware.rotateMotor(20, True)
        elif sound:
            self.log('%s palyed %s' % (identity, sound.group(1)))
            music.play(sound.group(1))

        # 开/关门完毕
        self.setOperatingDoor(False)

    def exitPiServer(self, name):
        self.log('%s close the Pi Server' % name)
        exit()

    def setOperatingDoor(self, operating):
        global operatingDoor
        condition.acquire()
        try:
            operatingDoor = operating
        finally:
            condition.release()

def start():
    try:
        server = ThreadingTCPServer(('0.0.0.0', 8088), ServerHandle)
        server.serve_forever()
    except KeyboardInterrupt:
        hardware.clean()

if __name__ == '__main__': start()