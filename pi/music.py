# coding:utf-8
# 音乐播放

import pygame
from threading import Thread

class Play(Thread):
    """多线程播放类"""
    def __init__(self, sound):
        super(Play, self).__init__()
        self.sound = sound

    def run(self):
        soundLen = self.sound.get_length()
        if soundLen < 0.1:
            print 'music can not play!'
            return
        self.sound.play()
        pygame.time.delay((int)(soundLen*1000))


class Music(object):
    """音乐播放类"""

    def __init__(self):
        pygame.mixer.init()
        pygame.time.delay(500)

    def play(self, name):
        if hasattr(self, 'soundThread') and self.soundThread.is_alive():
            self.sound.stop()
        filename = "wav/" + name + ".ogg"
        self.sound = pygame.mixer.Sound(filename)
        self.soundThread = Play(self.sound)
        self.soundThread.start()
