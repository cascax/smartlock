# coding:utf-8
# 音乐播放

import pygame, thread

pygame.mixer.init()
pygame.time.delay(500)

def play_this_thread(name):
    filename = "wav/" + name + ".ogg"
    sound = pygame.mixer.Sound(filename)
    soundLen = sound.get_length()
    if soundLen < 0.1:
        print 'music "%s" can not play!' % name
        return
    sound.play()
    pygame.time.delay((int)(soundLen*1000))

def play(name):
    thread.start_new_thread(play_this_thread, (name,))
