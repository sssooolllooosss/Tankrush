import pygame
import os

class TankAnimation:
    def __init__(self):
        self.shooting_frames = []
        for i in range(16):
            image = pygame.image.load(os.path.join('image', 'Tank Green', f'TGT_Shooting{i}.png')).convert_alpha()
            self.shooting_frames.append(image)
            
        self._resize_images()
            
        self.current_frame = 0
        self.animation_speed = 5
        self.frame_counter = 0
        self.is_animating = False
        self.just_finished = False
        
    def _resize_images(self):
        target_width = 30
        for i in range(len(self.shooting_frames)):
            original = self.shooting_frames[i]
            size = original.get_size()
            ratio = target_width / size[0]
            new_size = (int(size[0] * ratio), int(size[1] * ratio))
            self.shooting_frames[i] = pygame.transform.scale(original, new_size)
            
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
                
                if self.current_frame >= len(self.shooting_frames):
                    self.current_frame = 0
                    self.is_animating = False
                    self.just_finished = True
                    
    def get_current_frame(self):
        return self.shooting_frames[self.current_frame]