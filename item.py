import pygame
import random
from sound_manager import SoundManager

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.x = x
        self.y = y
        self.size = 30
        self.item_type = item_type
        self.radius = self.size // 2
        self.sound = SoundManager()
        
        # 아이템 타입별 텍스트
        self.type_properties = {
            "health": "H",
            "speed": "S",
            "attack": "A",
            "iron": "Fe",    # 철 포탄
            "tungsten": "T",   # 텅스텐 포탄
            "aluminum": "AL",  # 알루미늄 포탄
            "chrome": "C"     # 크롬 포탄
        }
    
    def draw(self, screen):
        # 검은색 정사각형 그리기
        rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
        pygame.draw.rect(screen, (0, 0, 0), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        
        # 아이템 타입에 따른 텍스트 그리기
        font = pygame.font.Font(None, 36)
        text = font.render(self.type_properties[self.item_type], True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
    
    def check_collision(self, player):
        distance = ((player.x - self.x) ** 2 + (player.y - self.y) ** 2) ** 0.5
        if distance < player.radius + self.radius:
            self.sound.play_item()
            return True
        return False
    
    def apply_effect(self, player):
        """아이템 효과를 플레이어에게 적용"""
        self.sound.play_item()
        if self.item_type == "health":
            player.heal(30)
        elif self.item_type == "speed":
            player.apply_speed_boost(10000)
        elif self.item_type == "attack":
            player.apply_attack_boost(10000)
        elif self.item_type in ["iron", "tungsten", "aluminum", "chrome"]:
            player.current_shell_type = self.item_type
        return True

class ItemSpawner:
    def __init__(self, maze, maze_width, maze_height, cell_size, offset_x, offset_y, players):
        self.maze = maze
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.players = players
        self.items = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = 10000  # 10초마다 아이템 생성
        
        # 아이템 종류 확장
        self.item_types = ["health", "speed", "attack", "iron", "tungsten", "aluminum", "chrome"]
        self.weights = [20, 20, 20, 10, 10, 10, 10]  # 일반 아이템이 더 자주 나오도록
        
    def find_empty_cell_positions(self):
        """미로에서 빈 셀(벽이 없는 위치)의 중심 좌표를 찾는 함수"""
        empty_positions = []
        
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                # 현재 셀의 중심 좌표 계산
                cell_x = self.offset_x + (x + 0.5) * self.cell_size
                cell_y = self.offset_y + (y + 0.5) * self.cell_size
                
                # 현재 위치가 벽이 아닌지 확인
                has_wall = False
                if x < self.maze_width and y < self.maze_height:
                    if self.maze['vertical'][y][x]:  # 수직 벽
                        has_wall = True
                    if self.maze['horizontal'][y][x]:  # 수평 벽
                        has_wall = True
                
                if not has_wall:
                    empty_positions.append((cell_x, cell_y))
        
        return empty_positions

    def spawn_item(self):
        """아이템 생성"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time < self.spawn_delay:
            return

        # 빈 셀 위치 찾기
        empty_positions = self.find_empty_cell_positions()
        if not empty_positions:
            return

        # 랜덤한 빈 셀 선택
        cell = random.choice(empty_positions)
        
        # 이미 아이템이 있는 위치인지 확인
        for item in self.items:
            if abs(item.x - cell[0]) < self.cell_size // 2 and abs(item.y - cell[1]) < self.cell_size // 2:
                return
        
        # 새 아이템 생성 (아이템 종류 확률 조정)
        item_type = random.choices(self.item_types, weights=self.weights, k=1)[0]
        
        new_item = Item(cell[0], cell[1], item_type)
        self.items.append(new_item)
        self.last_spawn_time = current_time
    
    def update(self):
        """아이템 업데이트"""
        self.spawn_item()
        
        # 플레이어의 부스트 효과 시간 체크
        current_time = pygame.time.get_ticks()
        for player in self.players:
            # 스피드 부스트 체크
            if hasattr(player, 'speed_boost_end_time') and current_time >= player.speed_boost_end_time:
                player.speed = player.original_speed
                
            # 공격력 부스트 체크
            if hasattr(player, 'attack_boost_end_time') and current_time >= player.attack_boost_end_time:
                player.attack_power = player.original_attack_power
                
            # 특수 포탄 효과 체크
            if hasattr(player, 'shell_effect_end_time') and current_time >= player.shell_effect_end_time:
                player.current_shell_type = "normal"
                
    def draw(self, screen):
        """아이템 그리기"""
        for item in self.items:
            item.draw(screen)
            
    def check_collisions(self, players):
        """아이템과 플레이어의 충돌 체크"""
        for item in self.items[:]:  # 복사본으로 순회
            for player in players:
                if not player.is_dead and item.check_collision(player):
                    # 아이템 효과 적용
                    if item.item_type == "health":
                        player.heal(30)  # 30 체력 회복
                    elif item.item_type == "speed":
                        player.apply_speed_boost(10000)  # 10초
                    elif item.item_type == "attack":
                        player.apply_attack_boost(10000)  # 10초
                    else:  # 특수 포탄 아이템
                        player.current_shell_type = item.item_type
                        player.shell_effect_end_time = pygame.time.get_ticks() + 10000  # 10초 동안 지속
                    
                    # 아이템 제거
                    self.items.remove(item)
                    break
