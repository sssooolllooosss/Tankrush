import pygame
import os
import sys

def play_intro():
    pygame.init()
    
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Tank Trouble - Intro")
    
    images = []
    for i in range(1, 4):  
        image = pygame.image.load(os.path.join('image', 'intro', f'intro{i}.jpg'))
        images.append(image)
    
    descriptions = [
        "전투의 열기 속에서, 당신의 전차는 전쟁의 상징이 되어\n적의 방어선을 뚫고 승리를 쟁취해야 합니다.",
        "동료 전차들과의 협동을 통해 전략적으로\n적의 약점을 파악하고 전투력을 극대화하는 것이 중요합니다.",
        "혼돈 속에서도 팀워크와 결단력으로\n전장의 패러다임을 바꾸고 역사를 새롭게 써 내려갈 준비가 되셨습니까?"
    ]
    
    font = pygame.font.Font(os.path.join('font', 'Paperlogy-6SemiBold.ttf'), 20)
    
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    frame_duration = 4666  
    
    running = True
    current_frame = 0
    
    while running:
        current_time = pygame.time.get_ticks() - start_time
        
        if current_time >= 14000:
            running = False
            continue
            
        current_frame = min(current_time // frame_duration, 2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "skip"
        
        screen.fill((0, 0, 0))
        
        image = pygame.transform.scale(images[current_frame], (800, 900))  
        screen.blit(image, (0, -50))  
        
        blur = pygame.Surface((800, 800))
        blur.fill((0, 0, 0))
        blur.set_alpha(100)  
        screen.blit(blur, (0, 0))
        
        s = pygame.Surface((800, 100))  
        s.set_alpha(200)  
        s.fill((0, 0, 0))
        screen.blit(s, (0, 700))
        
        text_lines = descriptions[current_frame].split('\n')  
        for i, line in enumerate(text_lines):
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 730 + i * 30))  
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return "complete"
