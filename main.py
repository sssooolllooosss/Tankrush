import pygame
import os
import sys
from select_pvp import select_pvp
from select_pve import select_pve

def play_main():
    pygame.init()
    
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Tank Trouble - Main Menu")
    
    GRAY = (128, 128, 128)
    YELLOW = (255, 223, 0)
    WHITE = (255, 255, 255)
    
    background = pygame.image.load(os.path.join('image', 'main', 'main.png'))
    background = pygame.transform.scale(background, (800, 800))
    
    class Button:
        def __init__(self, x, y, width, height, text):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.is_hovered = False
            self.font = pygame.font.Font(os.path.join('font', 'Paperlogy-6SemiBold.ttf'), 36)
            
        def draw(self, surface):
            color = YELLOW if self.is_hovered else GRAY
            pygame.draw.rect(surface, color, self.rect, border_radius=10)
            pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
            
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
            
        def handle_event(self, event):
            if event.type == pygame.MOUSEMOTION:
                self.is_hovered = self.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_hovered:
                    return self.text
            return None
    
    pvp_button = Button(250, 550, 300, 60, "PVP MODE")
    pve_button = Button(250, 650, 300, 60, "PVE MODE")
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            pvp_result = pvp_button.handle_event(event)
            pve_result = pve_button.handle_event(event)
            
            if pvp_result:
                return "PVP"
            elif pve_result:
                return "PVE"
        
        screen.blit(background, (0, 0))
        
        pvp_button.draw(screen)
        pve_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    return None
