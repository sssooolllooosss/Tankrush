import pygame
import sys
import random
from map import make_maze
from player1 import Player1
from player2 import Player2
from player3 import Player3
from item import ItemSpawner
from character_stats import CharacterType
import math
import os

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Game")

MAZE_WIDTH = 7
MAZE_HEIGHT = 6
CELL_SIZE = 100

OFFSET_X = (WINDOW_WIDTH - (MAZE_WIDTH * CELL_SIZE)) // 2
OFFSET_Y = 20

maze = make_maze(MAZE_WIDTH, MAZE_HEIGHT)

def find_spawn_positions(min_distance):
    positions = []
    attempts = 0
    max_attempts = 100
    
    while len(positions) < 3 and attempts < max_attempts:
        x = random.randint(OFFSET_X + CELL_SIZE, WINDOW_WIDTH - OFFSET_X - CELL_SIZE)
        y = random.randint(OFFSET_Y + CELL_SIZE, WINDOW_HEIGHT - OFFSET_Y - CELL_SIZE)
        if all(math.sqrt((x - pos[0])**2 + (y - pos[1])**2) >= min_distance for pos in positions):
            if not check_wall_collision(x, y, 15, maze):
                positions.append((x, y))
        attempts += 1
    
    while len(positions) < 3:
        positions.append((WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    
    return positions

def draw_maze():
    screen.fill(BLACK)
    for y in range(MAZE_HEIGHT + 1):
        for x in range(MAZE_WIDTH + 1):
            if y < MAZE_HEIGHT and x < MAZE_WIDTH + 1 and maze['vertical'][y][x]:
                wall_x = OFFSET_X + x * CELL_SIZE
                wall_y = OFFSET_Y + y * CELL_SIZE
                pygame.draw.line(screen, WHITE, (wall_x, wall_y), (wall_x, wall_y + CELL_SIZE), 2)
            if y < MAZE_HEIGHT + 1 and x < MAZE_WIDTH and maze['horizontal'][y][x]:
                wall_x = OFFSET_X + x * CELL_SIZE
                wall_y = OFFSET_Y + y * CELL_SIZE
                pygame.draw.line(screen, WHITE, (wall_x, wall_y), (wall_x + CELL_SIZE, wall_y), 2)

def draw_health_bars(screen, players):
    bar_width = 200
    bar_height = 20
    padding = 10
    
    country_names = {
        CharacterType.USA: "미국", CharacterType.UK: "영국", CharacterType.FRANCE: "프랑스",
        CharacterType.USSR: "소련", CharacterType.GERMANY: "독일", CharacterType.JAPAN: "일본",
        CharacterType.ITALY: "이탈리아"
    }
    
    positions = [padding, (800 - bar_width) // 2, 800 - bar_width - padding]
    font = pygame.font.Font(os.path.join("font", "Paperlogy-6SemiBold.ttf"), 20)
    
    for i, player in enumerate(players):
        if i >= len(positions):
            break
        x, y = positions[i], WINDOW_HEIGHT - bar_height - padding
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
        health_width = int(bar_width * (player.health / player.max_health))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, health_width, bar_height))
        text = f"{country_names.get(player.char_type, 'Unknown')}: {player.health}/{player.max_health}"
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(midtop=(x + bar_width//2, y - 25))
        screen.blit(text_surface, text_rect)

def check_collision(entity1, entity2):
    dx = entity1.x - entity2.x
    dy = entity1.y - entity2.y
    distance = math.sqrt(dx * dx + dy * dy)
    return distance < (entity1.radius + entity2.radius)

def check_wall_collision(x, y, radius, maze):
    cell_x = (x - OFFSET_X) // CELL_SIZE
    cell_y = (y - OFFSET_Y) // CELL_SIZE
    
    if cell_x < 0 or cell_x >= MAZE_WIDTH or cell_y < 0 or cell_y >= MAZE_HEIGHT:
        return True
        
    if maze['vertical'][int(cell_y)][int(cell_x)]:
        wall_x = OFFSET_X + cell_x * CELL_SIZE
        if abs(x - wall_x) < radius:
            return True
            
    if maze['vertical'][int(cell_y)][int(cell_x + 1)]:
        wall_x = OFFSET_X + (cell_x + 1) * CELL_SIZE
        if abs(x - wall_x) < radius:
            return True
            
    if maze['horizontal'][int(cell_y)][int(cell_x)]:
        wall_y = OFFSET_Y + cell_y * CELL_SIZE
        if abs(y - wall_y) < radius:
            return True
            
    if maze['horizontal'][int(cell_y + 1)][int(cell_x)]:
        wall_y = OFFSET_Y + (cell_y + 1) * CELL_SIZE
        if abs(y - wall_y) < radius:
            return True
            
    return False

def check_bullet_wall_collision(bullet, maze):
    next_x = bullet.x + bullet.dx
    next_y = bullet.y + bullet.dy
    cell_x = int((next_x - OFFSET_X) // CELL_SIZE)
    cell_y = int((next_y - OFFSET_Y) // CELL_SIZE)
    
    if (cell_x < 0 or cell_x >= MAZE_WIDTH or cell_y < 0 or cell_y >= MAZE_HEIGHT):
        return True
    
    if bullet.dx > 0:
        if cell_x + 1 < len(maze['vertical'][0]) and maze['vertical'][cell_y][cell_x + 1]:
            wall_x = OFFSET_X + (cell_x + 1) * CELL_SIZE
            if next_x + bullet.radius > wall_x:
                bullet.x = wall_x - bullet.radius
                bullet.bounce(True)
                return False
    else:
        if maze['vertical'][cell_y][cell_x]:
            wall_x = OFFSET_X + cell_x * CELL_SIZE
            if next_x - bullet.radius < wall_x:
                bullet.x = wall_x + bullet.radius
                bullet.bounce(True)
                return False
    
    if bullet.dy > 0:
        if cell_y + 1 < len(maze['horizontal']) and maze['horizontal'][cell_y + 1][cell_x]:
            wall_y = OFFSET_Y + (cell_y + 1) * CELL_SIZE
            if next_y + bullet.radius > wall_y:
                bullet.y = wall_y - bullet.radius
                bullet.bounce(False)
                return False
    else:
        if maze['horizontal'][cell_y][cell_x]:
            wall_y = OFFSET_Y + cell_y * CELL_SIZE
            if next_y - bullet.radius < wall_y:
                bullet.y = wall_y + bullet.radius
                bullet.bounce(False)
                return False
    
    return False

def play_pvp(num_players, selected_chars=[CharacterType.USA] * 3):
    spawn_positions = find_spawn_positions(100)
    players = []
    
    for i in range(num_players):
        if i == 0:
            players.append(Player1(spawn_positions[i][0], spawn_positions[i][1], selected_chars[i]))
        elif i == 1:
            players.append(Player2(spawn_positions[i][0], spawn_positions[i][1], selected_chars[i]))
        else:
            players.append(Player3(spawn_positions[i][0], spawn_positions[i][1], selected_chars[i]))
    
    item_spawner = ItemSpawner(maze, MAZE_WIDTH, MAZE_HEIGHT, CELL_SIZE, OFFSET_X, OFFSET_Y, players)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MAIN"
        
        item_spawner.spawn_item()
        
        for player in players:
            prev_x, prev_y = player.x, player.y
            player.update()
            
            if check_wall_collision(player.x, player.y, player.radius, maze):
                player.x, player.y = prev_x, prev_y
            
            for other in players:
                if other != player:
                    if check_collision(player, other):
                        player.x, player.y = prev_x, prev_y
                        break
        
        for player in players:
            i = 0
            while i < len(player.bullets):
                bullet = player.bullets[i]
                if bullet.update():
                    player.bullets.pop(i)
                    continue
                
                if check_bullet_wall_collision(bullet, maze):
                    player.bullets.pop(i)
                    continue
                
                hit_player = False
                current_time = pygame.time.get_ticks()
                for other_player in players:
                    if other_player == player and current_time - bullet.creation_time < bullet.friendly_fire_delay:
                        continue
                    if check_collision(bullet, other_player):
                        other_player.take_damage(bullet.damage)
                        hit_player = True
                        player.bullets.pop(i)
                        break
                
                if not hit_player:
                    i += 1
        
        alive_players = [p for p in players if not p.is_dead]
        if len(alive_players) <= 1:
            running = False
            return "lobby"
        
        draw_maze()
        item_spawner.draw(screen)
        item_spawner.check_collisions(players)
        
        for player in players:
            for bullet in player.bullets:
                bullet.draw(screen)
            player.draw(screen)
        
        draw_health_bars(screen, players)
        
        pygame.display.flip()
        clock.tick(60)