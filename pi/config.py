#coding:utf-8
import sys, os, ConfigParser
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
__metaclass__ = type

class Config:
    """配置类"""

    def __init__(self, fileName):
        configFileName = os.path.join(os.path.dirname(__file__), fileName)
        self.config = ConfigParser.ConfigParser()
        try:
            fileHandle = open(configFileName, 'r')
            fileHandle.close()
            self.config.read(configFileName)
        except IOError:
            print '配置文件读取失败'

    def get(self, section, key):
        try:
            return self.config.get(section, key)
        except Exception, e:
            print e

    def getint(self, section, key):
        try:
            return self.config.getint(section, key)
        except Exception, e:
            print e

    def __call__(self, section, key):
        return self.get(section, key)
