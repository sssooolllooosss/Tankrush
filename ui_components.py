import pygame
import os
from character_stats import CharacterType

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 223, 0)
RED = (255, 0, 0)

def get_fonts():
    font_path = os.path.join('font', 'Paperlogy-6SemiBold.ttf')
    return {
        'normal': pygame.font.Font(font_path, 36),
        'small': pygame.font.Font(font_path, 24),
        'large': pygame.font.Font(font_path, 72)
    }

TANKS = [
    {"name": "미국", "skill": "기본 탱크", "image": "usa.png", "type": CharacterType.USA},
    {"name": "영국", "skill": "기본 탱크", "image": "uk.png", "type": CharacterType.UK},
    {"name": "프랑스", "skill": "기본 탱크", "image": "france.png", "type": CharacterType.FRANCE},
    {"name": "소련", "skill": "기본 탱크", "image": "russia.png", "type": CharacterType.USSR},
    {"name": "독일", "skill": "기본 탱크", "image": "germany.png", "type": CharacterType.GERMANY},
    {"name": "일본", "skill": "기본 탱크", "image": "japan.png", "type": CharacterType.JAPAN},
    {"name": "이탈리아", "skill": "기본 탱크", "image": "italy.png", "type": CharacterType.ITALY}
]

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.selected = False
        
    def draw(self, surface, font=None):
        if font is None:
            font = get_fonts()['normal']
            
        color = YELLOW if self.is_hovered or self.selected else GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False
