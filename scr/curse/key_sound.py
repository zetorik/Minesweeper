import pygame
from random import randint

from cursed_resourses import grandpa_and_egg

class ReleaseSound:
    def __init__(self):
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(grandpa_and_egg)
        self.sound.set_volume(0.6)

    def play_audio(self):
        self.sound.play()

    def on_release(self,key):
        if randint(0,1) == 1:
            self.play_audio()
