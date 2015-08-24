import socket

# server = ('45.62.118.214', 8088)
# server = ('192.168.5.105', 8088)
server = ('127.0.0.1', 8088)

s = socket.socket()
s.settimeout(4)
s.connect(server)
ifsucc = s.recv(1024).strip()
if ifsucc == 'success':
    print 'remote server(%s, %s) connected successful' % server
else:
    print 'connect failed'
    exit()

s.send('[msir]\n')
piOnline = s.recv(1024).strip()
if not piOnline == 'online':
    print 'Pi Server offline'
    exit()

operation = 'opendoor'
# operation = 'justopen'
# operation = 'closedoor'
# operation = 'exitpi'

s.send(operation + '\n')
print 'sent operation [%s]' % operation
s.close()
