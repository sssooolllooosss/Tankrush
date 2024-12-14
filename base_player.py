import pygame
import os
import math
from shell import Shell
from character_stats import CharacterStats
from tankG_motion import TankAnimation
from sound_manager import SoundManager

class BasePlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, char_type):
        super().__init__()
        self.stats = CharacterStats(char_type)
        self.char_type = char_type
        self.sound = SoundManager()
        
        self.health = self.stats.get_current_stats()["health"]
        self.max_health = self.stats.get_current_stats()["health"]
        self.base_speed = self.stats.get_current_stats()["speed"]
        self.speed = self.base_speed
        self.attack = self.stats.get_current_stats()["attack"]
        self.reload_time = self.stats.get_current_stats()["reload_time"]
        self.rotation_speed = 3
        self.last_shot = 0
        self.is_dead = False
        
        self.x = x
        self.y = y
        self.body_angle = 0
        self.turret_angle = 0
        
        self.body_image = pygame.image.load(os.path.join('image', 'Tank Green', 'TGB_Idle.png')).convert_alpha()
        self.turret_image = pygame.image.load(os.path.join('image', 'Tank Green', 'TGT_Shooting0.png')).convert_alpha()
        self._resize_images()
        
        self.rotated_body = self.body_image
        self.rotated_turret = self.turret_image
        self.rect = self.body_image.get_rect(center=(self.x, self.y))
        
        self.bullets = []
        self.radius = 15
        self.current_shell_type = "normal"
        self.tank_animation = TankAnimation()

    def _resize_images(self):
        target_width = 30
        for image_attr in ['body_image', 'turret_image']:
            original = getattr(self, image_attr)
            size = original.get_size()
            ratio = target_width / size[0]
            new_size = (int(size[0] * ratio), int(size[1] * ratio))
            setattr(self, image_attr, pygame.transform.scale(original, new_size))

    def rotate_body(self, angle):
        self.body_angle = angle
        self.rotated_body = pygame.transform.rotate(self.body_image, -self.body_angle)
        
    def rotate_turret(self, angle):
        self.turret_angle = angle
        self.rotated_turret = pygame.transform.rotate(self.turret_image, -self.turret_angle)
        
    def move(self, dx, dy):
        if not self.is_dead:
            self.x += dx
            self.y += dy
            self.rect.center = (self.x, self.y)
        
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.reload_time * 1000:
            new_bullet = Shell(self.x, self.y, self.turret_angle, self, self.current_shell_type)
            self.bullets.append(new_bullet)
            self.last_shot = current_time
            self.tank_animation.start_animation()
            self.sound.play_fire()
            
            # 특수 포탄 사용 후 일반 포탄으로 변경
            if self.current_shell_type in ["iron", "tungsten", "aluminum", "chrome"]:
                self.current_shell_type = "normal"
            
    def update(self):
        if self.is_dead:
            return
            
        self.tank_animation.update()
        
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.x < 0 or bullet.x > 800 or bullet.y < 0 or bullet.y > 800:
                self.bullets.remove(bullet)
        
    def draw(self, screen):
        if self.is_dead:
            return
            
        body_rect = self.rotated_body.get_rect(center=(self.x, self.y))
        screen.blit(self.rotated_body, body_rect)
        
        turret_x = self.x + math.sin(math.radians(self.body_angle)) * 24
        turret_y = self.y - math.cos(math.radians(self.body_angle)) * 24
        
        if self.tank_animation.is_animating:
            current_frame = self.tank_animation.get_current_frame()
            rotated_frame = pygame.transform.rotate(current_frame, -self.turret_angle)
            turret_rect = rotated_frame.get_rect(center=(turret_x, turret_y))
            screen.blit(rotated_frame, turret_rect)
        else:
            turret_rect = self.rotated_turret.get_rect(center=(turret_x, turret_y))
            screen.blit(self.rotated_turret, turret_rect)
        
        for bullet in self.bullets:
            bullet.draw(screen)
        
    def take_damage(self, damage):
        if not self.is_dead:
            self.health -= damage
            self.sound.play_hit()
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
                self.sound.play_explosion()
                # 탱크를 화면 밖으로 이동
                self.x = -1000
                self.y = -1000
                self.rect.center = (self.x, self.y)
                
    def heal(self, amount):
        if not self.is_dead:
            self.health = min(self.max_health, self.health + amount)

    def apply_speed_boost(self, duration):
        self.speed = self.base_speed * 1.5
        
    def apply_attack_boost(self, duration):
        self.attack *= 1.5
