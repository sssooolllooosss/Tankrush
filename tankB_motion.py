import pygame
import os

class TankAnimation:
    def __init__(self):
        self.images = []
        for i in range(13):
            img = pygame.image.load(os.path.join('image', 'Tank Blue', f'TBT_Shooting{i}.png')).convert_alpha()
            self.images.append(img)
            
        self._resize_images()
            
        self.current_frame = 0
        self.animation_speed = 5
        self.frame_counter = 0
        self.is_animating = False
        self.just_finished = False
        
    def _resize_images(self):
        target_width = 30
        for i in range(len(self.images)):
            original = self.images[i]
            size = original.get_size()
            ratio = target_width / size[0]
            new_size = (int(size[0] * ratio), int(size[1] * ratio))
            self.images[i] = pygame.transform.scale(original, new_size)
            
    def start_animation(self):
        self.is_animating = True
        self.current_frame = 0
        self.frame_counter = 0
        self.just_finished = False
        
    def update(self):
        self.just_finished = False
        
        if self.is_animating:
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_counter = 0
                self.current_frame += 1
                
                if self.current_frame >= len(self.images):
                    self.current_frame = 0
                    self.is_animating = False
                    self.just_finished = True
                    
    def get_current_frame(self):
        return self.images[self.current_frame]