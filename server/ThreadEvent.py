#coding:utf-8
import threading

class ThreadEvent(object):
    """类似于threading中的_Event类。增加了name标识事件类型，
       identify用来标识发起者，通过set的参数来设置。
    """

    def __init__(self):
        self.__cond = threading.Condition()
        self.__flag = False
        self.__name = ''
        self.__identify = None

    def isSet(self):
        return self.__flag

    def set(self, name, identify=None):
        self.__cond.acquire()
        try:
            self.__flag = True
            self.__name = name
            self.__identify = identify
            self.__cond.notify_all()
        finally:
            self.__cond.release()

    def clear(self):
        self.__cond.acquire()
        try:
            self.__flag = False
            name = self.__name
            self.__name = ''
            self.__identify = ''
            return name
        finally:
            self.__cond.release()

    def wait(self, timeout=None):
        self.__cond.acquire()
        try:
            if not self.__flag:
                self.__cond.wait(timeout)
            return self.__flag
        finally:
            self.__cond.release()

    def getName(self):
        return self.__name;

    def getIdentify(self):
        return self.__identify;