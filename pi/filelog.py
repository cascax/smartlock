#coding:utf-8
import urllib, urllib2
import sys, datetime, os
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
__metaclass__ = type

class Log:
    """日志文件记录类"""

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Log, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.fileName = os.path.join(os.path.dirname(__file__), 'log.txt')
        self.fileHandle = open(self.fileName, 'a')

    def report(self, s):
        data = urllib.urlencode({'log': s})
        print data
        url = 'http://codeme.xyz/log.php'
        response = urllib2.urlopen(url, data)
        print response.read()

    def log(self, s):
        try:
            now = datetime.datetime.now()
            self.fileHandle.write('[%s] %s\n' % (now.strftime('%Y-%m-%d %H:%M:%S'), s))
            self.fileHandle.flush()
        except Exception, e:
            self.report(u'写入日志文件错误: ' + str(e).decode())

    def __call__(self, s):
        self.log(s)

    def clear(self):
        try:
            self.fileHandle.close()
            open(self.fileName, 'w')
            self.fileHandle = open(self.fileName, 'a')
            self.log('clear')
        except Exception, e:
            report(u'清理日志文件错误: ' + str(e).decode())

    def __del__(self):
        self.fileHandle.close()
