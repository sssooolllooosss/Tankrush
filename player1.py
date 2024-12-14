import pygame
import math
from tankG_motion import TankAnimation
from base_player import BasePlayer

class Player1(BasePlayer):
    def __init__(self, x, y, char_type, selected_char=None):
        if selected_char is None:
            selected_char = char_type
        super().__init__(x, y, selected_char)
        self.tank_animation = TankAnimation()

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.body_angle -= self.rotation_speed
            self.rotate_body(self.body_angle)
            self.rotate_turret(self.body_angle)
        if keys[pygame.K_d]:
            self.body_angle += self.rotation_speed
            self.rotate_body(self.body_angle)
            self.rotate_turret(self.body_angle)
            
        if keys[pygame.K_w]:
            dx = math.sin(math.radians(self.body_angle)) * self.speed
            dy = -math.cos(math.radians(self.body_angle)) * self.speed
            self.move(dx, dy)
        if keys[pygame.K_s]:
            dx = -math.sin(math.radians(self.body_angle)) * self.speed
            dy = math.cos(math.radians(self.body_angle)) * self.speed
            self.move(dx, dy)
            
        if keys[pygame.K_q]:
            self.shoot()
            
        super().update()