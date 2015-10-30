import pygame, thread

pygame.mixer.init()
pygame.time.delay(500)

def play_this_thread(name):
    filename = "wav/" + name + ".ogg"
    sound = pygame.mixer.Sound(filename)
    sound.play()
    pygame.time.delay((int)(sound.get_length()*1000))

def play(name):
    thread.start_new_thread(play_this_thread, (name,))
