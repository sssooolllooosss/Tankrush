import pygame
import os
import random

class SoundManager:
    def __init__(self):
        self.sounds = {
            'item': pygame.mixer.Sound(os.path.join('sound', 'item.mp3')),
            'fire': pygame.mixer.Sound(os.path.join('sound', 'fire.mp3')),
            'hit1': pygame.mixer.Sound(os.path.join('sound', 'hit1.mp3')),
            'hit2': pygame.mixer.Sound(os.path.join('sound', 'hit2.mp3')),
            'explo': pygame.mixer.Sound(os.path.join('sound', 'explo.mp3'))
        }
        
    def play_item(self):
        self.sounds['item'].play()
        
    def play_fire(self):
        self.sounds['fire'].play()
        
    def play_hit(self):
        random.choice([self.sounds['hit1'], self.sounds['hit2']]).play()
        
    def play_explosion(self):
        self.sounds['explo'].play()
