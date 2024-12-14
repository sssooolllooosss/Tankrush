import pygame
import math

class Shell:
    def __init__(self, x, y, angle, owner, shell_type="normal"):
        self.x = x
        self.y = y
        self.angle = angle
        self.owner = owner
        self.shell_type = shell_type
        
        self.speed = 2
        self.damage = owner.attack
        self.radius = 10
        self.color = (255, 255, 255)
        self.penetrate = False
        self.lifetime = 3000
        
        if shell_type == "iron":
            self.radius *= 1.5  # 50% 더 큰 크기
            self.speed *= 0.8   # 20% 더 느린 속도
            self.damage *= 1.5  # 50% 더 강한 데미지
            self.color = (139, 69, 19)
        elif shell_type == "tungsten":
            self.damage *= 2.0  # 2배 데미지
            self.penetrate = True  # 관통
            self.color = (128, 128, 128)
        elif shell_type == "aluminum":
            self.speed *= 2.0   # 2배 빠른 속도
            self.damage *= 0.8  # 20% 약한 데미지
            self.color = (192, 192, 192)
        elif shell_type == "chrome":
            self.lifetime = 4500  # 50% 더 긴 지속시간
            self.damage *= 1.2   # 20% 더 강한 데미지
            self.speed *= 1.2    # 20% 더 빠른 속도
            self.color = (0, 255, 255)
        
        angle_rad = math.radians(angle)
        self.dx = math.sin(angle_rad) * self.speed
        self.dy = -math.cos(angle_rad) * self.speed
        
        self.creation_time = pygame.time.get_ticks()
        self.friendly_fire_delay = 500
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
        current_time = pygame.time.get_ticks()
        return current_time - self.creation_time > self.lifetime
    
    def bounce(self, is_vertical):
        if is_vertical:
            self.dx = -self.dx
        else:
            self.dy = -self.dy
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)