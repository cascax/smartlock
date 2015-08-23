import socket

s = socket.socket()
# server = ('45.62.118.214', 8088)
server = ('192.168.5.105', 8088)
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
if piOnline == 'online':
    print 'Pi Server online'
else:
    print 'Pi Server offline'
    exit()

s.send('openthedoor\n')
print 'send open the door'
s.close()
