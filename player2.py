import pygame
import os
import math
from tankB_motion import TankAnimation
from base_player import BasePlayer

class Player2(BasePlayer):
    def __init__(self, x, y, char_type, selected_char=None):
        if selected_char is None:
            selected_char = char_type
        super().__init__(x, y, selected_char)
        
        self.body_image = pygame.image.load(os.path.join('image', 'Tank Blue', 'TBB_Idle.png')).convert_alpha()
        self.turret_image = pygame.image.load(os.path.join('image', 'Tank Blue', 'TBT_Shooting0.png')).convert_alpha()
        self._resize_images()
        self.rotated_body = self.body_image
        self.rotated_turret = self.turret_image
        self.tank_animation = TankAnimation()

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.body_angle -= self.rotation_speed
            self.rotate_body(self.body_angle)
            self.rotate_turret(self.body_angle)
        if keys[pygame.K_RIGHT]:
            self.body_angle += self.rotation_speed
            self.rotate_body(self.body_angle)
            self.rotate_turret(self.body_angle)
            
        if keys[pygame.K_UP]:
            dx = math.sin(math.radians(self.body_angle)) * self.speed
            dy = -math.cos(math.radians(self.body_angle)) * self.speed
            self.move(dx, dy)
        if keys[pygame.K_DOWN]:
            dx = -math.sin(math.radians(self.body_angle)) * self.speed
            dy = math.cos(math.radians(self.body_angle)) * self.speed
            self.move(dx, dy)
            
        if keys[pygame.K_PERIOD]:
            self.shoot()
            
        super().update()