import pygame
import math
from tankG_motion import TankAnimation
from base_player import BasePlayer

class Player3(BasePlayer):
    def __init__(self, x, y, char_type, selected_char=None):
        if selected_char is None:
            selected_char = char_type
        super().__init__(x, y, selected_char)
        self.tank_animation = TankAnimation()
        self.stop_distance = 20

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # 마우스 방향으로 회전
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        angle = math.degrees(math.atan2(dx, -dy))
        self.body_angle = angle
        self.rotate_body(angle)
        self.rotate_turret(angle)
        
        # 마우스 클릭으로 발사
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.shoot()
        
        # 마우스 커서 방향으로 이동
        if distance > self.stop_distance:
            dx = math.sin(math.radians(self.body_angle)) * self.speed
            dy = -math.cos(math.radians(self.body_angle)) * self.speed
            self.move(dx, dy)
            
        super().update()