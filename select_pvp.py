import pygame
import sys
from ui_components import Button, WHITE, BLACK, GRAY, YELLOW, RED, get_fonts, TANKS
from character_stats import CharacterStats

def select_pvp():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Tank Trouble - PVP Character Selection")
    
    fonts = get_fonts()
    screen_center_x = 400
    
    player_buttons = [
        Button(screen_center_x - 100, 300, 200, 60, "2 Players"),
        Button(screen_center_x - 100, 400, 200, 60, "3 Players")
    ]
    
    current_tank = 0
    selected_tanks = []
    num_players = 0
    selecting_player = 0
    
    STATE_SELECT_PLAYERS = 0
    STATE_SELECT_CHARACTERS = 1
    current_state = STATE_SELECT_PLAYERS
    
    running = True
    clock = pygame.time.Clock()
    
    def draw_tank_stats(tank, x, y):
        stats = CharacterStats(tank["type"]).get_current_stats()
        stat_texts = [
            f"체력: {stats['health']}",
            f"공격력: {stats['attack']}",
            f"이동속도: {stats['speed']}",
            f"재장전 시간: {stats['reload_time']}초"
        ]
        for i, text in enumerate(stat_texts):
            stat_surface = fonts['small'].render(text, True, WHITE)
            screen.blit(stat_surface, (x - stat_surface.get_width()//2, y + i * 30))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None
                
            if current_state == STATE_SELECT_PLAYERS:
                for i, button in enumerate(player_buttons):
                    if button.handle_event(event):
                        num_players = i + 2
                        current_state = STATE_SELECT_CHARACTERS
                        
            elif current_state == STATE_SELECT_CHARACTERS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_tank = (current_tank - 1) % len(TANKS)
                    elif event.key == pygame.K_RIGHT:
                        current_tank = (current_tank + 1) % len(TANKS)
                    elif event.key == pygame.K_RETURN:
                        if TANKS[current_tank]["type"] not in [tank["type"] for tank in selected_tanks]:
                            selected_tanks.append(TANKS[current_tank])
                            selecting_player += 1
                            if selecting_player >= num_players:
                                return num_players, [tank["type"] for tank in selected_tanks]
        
        screen.fill(BLACK)
        
        if current_state == STATE_SELECT_PLAYERS:
            title = fonts['large'].render("Select Players", True, WHITE)
            title_rect = title.get_rect(center=(screen_center_x, 150))
            screen.blit(title, title_rect)
            
            for button in player_buttons:
                button.draw(screen)
                
        elif current_state == STATE_SELECT_CHARACTERS:
            player_text = fonts['normal'].render(f"Player {selecting_player + 1} Select", True, WHITE)
            screen.blit(player_text, (50, 50))
            
            tank = TANKS[current_tank]
            tank_name = fonts['normal'].render(tank["name"], True, RED if tank["type"] in [t["type"] for t in selected_tanks] else WHITE)
            tank_skill = fonts['small'].render(tank["skill"], True, WHITE)
            screen.blit(tank_name, (screen_center_x - tank_name.get_width()//2, 300))
            screen.blit(tank_skill, (screen_center_x - tank_skill.get_width()//2, 350))
            
            if tank["type"] in [t["type"] for t in selected_tanks]:
                unavailable_text = fonts['small'].render("(이미 선택된 캐릭터입니다)", True, RED)
                screen.blit(unavailable_text, (screen_center_x - unavailable_text.get_width()//2, 380))
            
            draw_tank_stats(tank, screen_center_x, 420)
            
            selected_text = fonts['small'].render("Selected: " + ", ".join(t["name"] for t in selected_tanks), True, WHITE)
            screen.blit(selected_text, (50, 700))
            
            controls = fonts['small'].render("← → to navigate, Enter to select", True, WHITE)
            screen.blit(controls, (50, 750))
        
        pygame.display.flip()
        clock.tick(60)
    
    return None, None
