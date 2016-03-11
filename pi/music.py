# coding:utf-8
# 音乐播放

import pygame, os, time
from threading import Thread
from config import Config

class Play(Thread):
    """多线程播放类"""
    def __init__(self, sound):
        super(Play, self).__init__()
        self.sound = sound
        config = Config('pi.ini')
        try:
            self.notDisturb = config.getint('music', 'not_disturb')
            self.notDisturbStart = time.strptime(config('music', 'not_disturb_time_begin'), '%H:%M')
            self.notDisturbEnd = time.strptime(config('music', 'not_disturb_time_end'), '%H:%M')
        except ValueError:
            print 'not_disturb configs error'
            self.notDisturb = 0

    def run(self):
        # 检查免打扰
        if self.__checkDistrub():
            print 'music do not play. (do not disturb)'
            return

        soundLen = self.sound.get_length()
        if soundLen < 0.1:
            print 'music can not play!'
            return
        self.sound.play()
        pygame.time.delay((int)(soundLen*1000))

    def __checkDistrub(self):
        if self.notDisturb != 1:
            return False
        now = time.localtime()
        now = time.strptime('%d:%d' % (now[3],now[4]), '%H:%M')
        if self.notDisturbStart<=self.notDisturbEnd:
            if self.notDisturbStart<=now and self.notDisturbEnd>=now:
                return True
        elif now>=self.notDisturbStart or now<=self.notDisturbEnd:
            return True
        return False

class Music(object):
    """音乐播放类"""

    def __init__(self):
        pygame.mixer.init()
        pygame.time.delay(500)

    def play(self, name):
        if hasattr(self, 'soundThread') and self.soundThread.is_alive():
            self.sound.stop()
        filename = self._getFileName(name)
        self.sound = pygame.mixer.Sound(filename)
        self.soundThread = Play(self.sound)
        self.soundThread.start()

    def _getFileName(self, name):
        return os.path.join(os.path.dirname(__file__), 'wav', name + '.ogg')
