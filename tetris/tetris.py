#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@codebase
Project: Python Tetris Game
Version: 1.0.0
Author: ChiefHYK
Date: 2024-12-07

Dependencies:
- Python 3.x
- Pygame

File Structure:
/tetris
    /assets
        /fonts
            - simhei.ttf
        /sounds
            - move.wav
            - rotate.wav
            - drop.wav
            - clear.wav
            - gameover.wav
    - tetris.py
    - README.md
    - highscore.txt

Module Description:
This file contains the complete implementation of a Tetris game using Pygame.
Key components include:
- Config: Game configuration and constants
- FontManager: Font resource management
- Tetromino: Tetris piece implementation
- Particle: Particle effect system
- ComboSystem: Combo scoring mechanism
- GameStats: Game statistics tracking
- GameUI: User interface management
- GameLogic: Core game mechanics
- TetrisGame: Main game class
"""

import os
import sys
import random
import pygame
from pygame.locals import *

# ============= 配置和常量 =============
class Config:
    """游戏配置类"""
     # 界面布局相关
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 700
    BLOCK_SIZE = 30
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    
    # 网格偏移
    GRID_OFFSET_X = 50
    GRID_OFFSET_Y = 50
    
    # 侧边栏位置
    SIDE_PANEL_X = GRID_OFFSET_X + (GRID_WIDTH + 3) * BLOCK_SIZE
    
    # 文字位置
    SCORE_Y = GRID_OFFSET_Y + 20
    LEVEL_Y = SCORE_Y + 30
    NEXT_LABEL_Y = LEVEL_Y + 30
    NEXT_PIECE_Y = NEXT_LABEL_Y + 60
    STATS_Y = NEXT_PIECE_Y + 150      # 相应调整统计信息的位置
    
    # 预览区域
    PREVIEW_OFFSET = 0
    PREVIEW_AREA_WIDTH = 4
    
    # 网格线颜色
    GRID_COLOR = (50, 50, 50)  # 暗灰色
    GHOST_ALPHA = 40  # 阴影透明度（0-255）

    # 字体设置
    FONT_SIZE_LARGE = 48
    FONT_SIZE_NORMAL = 32
    FONT_SIZE_SMALL = 24
    
    # 游戏置
    FPS = 60
    INITIAL_FALL_SPEED = 0.3  # 初始下落速度（秒/格）
    SPEED_INCREASE = 0.05    # 每级增加的速度
    
    # 颜色定义
    COLORS = {
        'BLACK': (0, 0, 0),
        'WHITE': (255, 255, 255),
        'YELLOW': (255, 255, 0),
        'RED': (255, 0, 0),
        'GREEN': (0, 255, 0),
        'BLUE': (0, 0, 255),
        'CYAN': (0, 255, 255),
        'MAGENTA': (255, 0, 255)
    }
    
    # 方块形状定义
    SHAPES = {
        'I': [[1, 1, 1, 1]],
        'O': [[1, 1],
              [1, 1]],
        'T': [[0, 1, 0],
              [1, 1, 1]],
        'S': [[0, 1, 1],
              [1, 1, 0]],
        'Z': [[1, 1, 0],
              [0, 1, 1]],
        'J': [[1, 0, 0],
              [1, 1, 1]],
        'L': [[0, 0, 1],
              [1, 1, 1]]
    }
    
    @classmethod
    def get_resource_path(cls, *paths):
        """获取资源文件路径"""
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, *paths)

# ============= 游戏实体类 =============
class FontManager:
    """字体管理类"""
    def __init__(self):
        self.font_path = Config.get_resource_path("assets", "fonts", "simhei.ttf")
        if not os.path.exists(self.font_path):
            raise FileNotFoundError(f"���不到字体文件: {self.font_path}")
        
        self.title_font = pygame.font.Font(self.font_path, Config.FONT_SIZE_LARGE)
        self.normal_font = pygame.font.Font(self.font_path, Config.FONT_SIZE_NORMAL)
        self.small_font = pygame.font.Font(self.font_path, Config.FONT_SIZE_SMALL)

class Tetromino:
    """俄罗斯方块类"""
    def __init__(self, x=None):
        self.shape = random.choice(list(Config.SHAPES.values()))
        self.color = random.choice([v for k, v in Config.COLORS.items() 
                                  if k not in ['BLACK', 'WHITE']])
        # 简化x坐标的初始化
        self.x = x if x is not None else Config.GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
  
    def rotate(self):
        """旋转方块"""
        self.shape = list(zip(*self.shape[::-1]))
    
    def draw(self, screen, offset_x=0, offset_y=0, ghost=False, preview=False):
        """绘制方块"""
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    if preview:
                        # 预览模式下直接使用偏移量
                        x = offset_x + j * Config.BLOCK_SIZE
                        y = offset_y + i * Config.BLOCK_SIZE
                    else:
                        # 游戏区域内使用原有计算方式
                        x = offset_x + (self.x + j) * Config.BLOCK_SIZE
                        y = offset_y + (self.y + i) * Config.BLOCK_SIZE
                    
                    if ghost:
                        ghost_surface = pygame.Surface(
                            (Config.BLOCK_SIZE - 1, Config.BLOCK_SIZE - 1),
                            pygame.SRCALPHA
                        )
                        ghost_color = (*self.color[:3], Config.GHOST_ALPHA)
                        pygame.draw.rect(ghost_surface, ghost_color, 
                                       ghost_surface.get_rect())
                        screen.blit(ghost_surface, (x, y))
                    else:
                        pygame.draw.rect(
                            screen,
                            self.color,
                            (x, y, Config.BLOCK_SIZE - 1, Config.BLOCK_SIZE - 1)
                        )

class Particle:
    """粒子效果类"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-5, -1)
        self.life = 255
        self.gravity = 0.2
    
    def update(self):
        """更新粒子状态"""
        self.x += self.dx
        self.y += self.dy
        self.dy += self.gravity
        self.life -= 5
        return self.life > 0
    
    def draw(self, screen):
        """绘制粒子"""
        if self.life > 0:
            color = (*self.color[:3], self.life)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 2)

class ComboSystem:
    """连击系统"""
    def __init__(self):
        self.combo = 0
        self.max_combo = 0
        self.last_combo_time = 0
        self.COMBO_TIME_LIMIT = 1000  # 连击时间限制（毫秒）
    
    def update(self, current_time):
        """更新连击状态"""
        if current_time - self.last_combo_time > self.COMBO_TIME_LIMIT:
            self.combo = 0
    
    def on_line_clear(self, lines, current_time):
        """处理消行连击"""
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        self.last_combo_time = current_time
        return self.combo * lines * 50

class GameStats:
    """游戏统计类"""
    def __init__(self, font_manager):
        self.pieces_placed = 0
        self.lines_cleared = 0
        self.max_combo = 0
        self.play_time = 0
        self.start_time = pygame.time.get_ticks()
        self.max_score = self.load_highscore()
        self.games_played = 0
        self.font_manager = font_manager
    
    @staticmethod
    def load_highscore():
        """加载最高分"""
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0
    
    @staticmethod
    def save_highscore(score):
        """保存最高分"""
        with open("highscore.txt", "w") as f:
            f.write(str(score))
    
    def update(self, current_time):
        """更新统计信息"""
        self.play_time = (current_time - self.start_time) // 1000
    
    def draw(self, screen):
        """绘制统计信息"""
        stats_text = [
            ("游戏统计", Config.COLORS['YELLOW']),
            (f"游戏次数: {self.games_played}", Config.COLORS['WHITE']),
            (f"已放置方块: {self.pieces_placed}", Config.COLORS['WHITE']),
            (f"已消除行数: {self.lines_cleared}", Config.COLORS['WHITE']),
            (f"最大连击: {self.max_combo}", Config.COLORS['WHITE']),
            (f"游戏时间: {self.play_time}秒", Config.COLORS['WHITE']),
            (f"最高分数: {self.max_score}", Config.COLORS['WHITE'])
        ]
        
        y = Config.STATS_Y
        for text, color in stats_text:
            surface = self.font_manager.small_font.render(text, True, color)
            screen.blit(surface, (Config.SIDE_PANEL_X, y))
            y += 30

# ============= 界面管理 =============
class GameUI:
    """游戏界面管理类"""
    @staticmethod
    def show_start_screen(screen, highscore, font_manager):
        """显示开始界面"""
        screen.fill(Config.COLORS['BLACK'])
        
        # 渲染文本
        title = font_manager.title_font.render("俄罗斯方块", True, Config.COLORS['WHITE'])
        start_text = font_manager.normal_font.render("按空格键开始", True, Config.COLORS['WHITE'])
        score_text = font_manager.normal_font.render(f"最高分: {highscore}", True, Config.COLORS['WHITE'])
        
        # 显示文本
        screen.blit(title, (Config.SCREEN_WIDTH//2 - title.get_width()//2, 200))
        screen.blit(start_text, (Config.SCREEN_WIDTH//2 - start_text.get_width()//2, 300))
        screen.blit(score_text, (Config.SCREEN_WIDTH//2 - score_text.get_width()//2, 400))
        
        pygame.display.flip()
        
        # 等待用户输入
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        return True
                    if event.key == K_ESCAPE:
                        return False
        
    @staticmethod
    def show_game_over_screen(screen, score, highscore, font_manager):
        """显示游戏结束界面"""
        screen.fill(Config.COLORS['BLACK'])
        
        texts = [
            ("游戏结束", Config.COLORS['WHITE'], 200),
            (f"得分: {score}", Config.COLORS['WHITE'], 300),
            (f"最高分: {highscore}", Config.COLORS['WHITE'], 350),
            ("按空格键重新开始", Config.COLORS['WHITE'], 450),
            ("按ESC键退出", Config.COLORS['WHITE'], 500)
        ]
        
        for text, color, y in texts:
            surface = font_manager.normal_font.render(text, True, color)
            screen.blit(surface, (Config.SCREEN_WIDTH//2 - surface.get_width()//2, y))
        
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        return True
                    if event.key == K_ESCAPE:
                        return False

# ============= 游戏逻辑 =============
class GameLogic:
    """游戏逻辑类"""
    
    @staticmethod
    def lock_piece(piece, grid):
        """锁定方块"""
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell and piece.y + i >= 0:
                    grid[piece.y + i][piece.x + j] = piece.color
        return grid

    @staticmethod
    def get_ghost_position(piece, grid):
        """获取方块的落点位置（返回完整的影子方块）"""
        ghost_piece = Tetromino()
        ghost_piece.shape = piece.shape.copy()  # 复制形状
        ghost_piece.color = piece.color         # 使用相同颜色
        ghost_piece.x = piece.x                 # 相同x坐标
        ghost_piece.y = piece.y                 # 从当前位置开始
        
        # 下移直到碰到底部或其他方块
        while GameLogic.valid_move(ghost_piece, grid, dy=1):
            ghost_piece.y += 1
            
        return ghost_piece

    @staticmethod
    def valid_move(piece, grid, dx=0, dy=0, test_y=None):
        """检查移动是否有效"""
        if test_y is None:
            test_y = piece.y
        
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = piece.x + j + dx
                    new_y = test_y + i + dy
                    
                    if (new_x < 0 or new_x >= Config.GRID_WIDTH or
                        new_y >= Config.GRID_HEIGHT or
                        (new_y >= 0 and grid[new_y][new_x])):
                        return False
        return True

    @staticmethod
    def clear_lines(grid, particles):
        """清除已完成的行"""
        lines_cleared = 0
        y = Config.GRID_HEIGHT - 1
        while y >= 0:
            if all(grid[y]):
                # 创建粒子效果
                for x in range(Config.GRID_WIDTH):
                    for _ in range(5):
                        particles.append(Particle(
                            x * Config.BLOCK_SIZE + Config.BLOCK_SIZE/2,
                            y * Config.BLOCK_SIZE + Config.BLOCK_SIZE/2,
                            grid[y][x]
                        ))
                
                # 下移上方的行
                for y2 in range(y, 0, -1):
                    grid[y2] = grid[y2-1][:]
                grid[0] = [0] * Config.GRID_WIDTH
                lines_cleared += 1
            else:
                y -= 1
        return lines_cleared

# ============= 主程序 =============
class TetrisGame:
    """俄罗斯方块游戏主类"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption('俄罗斯方块')
        
        self.font_manager = FontManager()
        self.game_stats = GameStats(self.font_manager)
        self.clock = pygame.time.Clock()
        
        # 加载音效
        self.load_sounds()
    
    def load_sounds(self):
        """加载游戏音效"""
        self.sounds = {}
        for sound_name in ['move', 'rotate', 'drop', 'clear', 'gameover']:
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(
                    Config.get_resource_path("assets", "sounds", f"{sound_name}.wav")
                )
            except:
                print(f"无法加载音效: {sound_name}")
    
    def play_sound(self, sound_name):
        """播放音效"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
     
    def run(self):
        """运行游戏"""
        while True:
            if not GameUI.show_start_screen(self.screen, self.game_stats.max_score, self.font_manager):
                break
            
            if not self.game_loop():
                break
        
        pygame.quit()
    
    def game_loop(self):
        """游戏主循环"""
        # 初始化游戏状态
        grid = [[0 for _ in range(Config.GRID_WIDTH)] for _ in range(Config.GRID_HEIGHT)]
        current_piece = Tetromino()
        next_piece = Tetromino()  # 删除x参数
        particles = []
        combo_system = ComboSystem()
        
        fall_time = 0
        score = 0
        level = 1
        lines_cleared_total = 0
        
        while True:
            # 处理时间和速度
            current_time = pygame.time.get_ticks()
            delta_time = self.clock.get_rawtime()
            fall_time += delta_time
            self.clock.tick(Config.FPS)
            
            # 更新游戏状态
            combo_system.update(current_time)
            self.game_stats.update(current_time)
            particles = [p for p in particles if p.update()]
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        if GameLogic.valid_move(current_piece, grid, dx=-1):
                            current_piece.x -= 1
                            self.play_sound('move')
                    elif event.key == K_RIGHT:
                        if GameLogic.valid_move(current_piece, grid, dx=1):
                            current_piece.x += 1
                            self.play_sound('move')
                    elif event.key == K_UP:
                        original_shape = current_piece.shape
                        current_piece.rotate()
                        if not GameLogic.valid_move(current_piece, grid):
                            current_piece.shape = original_shape
                        else:
                            self.play_sound('rotate')
                    elif event.key == K_DOWN:
                        if GameLogic.valid_move(current_piece, grid, dy=1):
                            current_piece.y += 1
                            self.play_sound('move')
                    elif event.key == K_SPACE:
                        while GameLogic.valid_move(current_piece, grid, dy=1):
                            current_piece.y += 1
                        self.play_sound('drop')
            
            # 自动下落
            if fall_time >= Config.INITIAL_FALL_SPEED * 1000 / (1 + (level-1) * Config.SPEED_INCREASE):
                if GameLogic.valid_move(current_piece, grid, dy=1):
                    current_piece.y += 1
                else:
                    grid = GameLogic.lock_piece(current_piece, grid)
                    self.game_stats.pieces_placed += 1
                    
                    lines = GameLogic.clear_lines(grid, particles)
                    if lines > 0:
                        self.game_stats.lines_cleared += lines
                        combo_bonus = combo_system.on_line_clear(lines, current_time)
                        score += lines * 100 * level + combo_bonus
                        self.play_sound('clear')
                        
                        lines_cleared_total += lines
                        level = lines_cleared_total // 10 + 1
                    else:
                        combo_system.combo = 0
                    
                    current_piece = next_piece
                    current_piece.x = Config.GRID_WIDTH // 2 - len(current_piece.shape[0]) // 2
                    current_piece.y = 0
                    next_piece = Tetromino(x=Config.GRID_WIDTH + 1)
                    
                    if not GameLogic.valid_move(current_piece, grid):
                        self.play_sound('gameover')
                        self.game_stats.on_game_over(score)
                        if score > self.game_stats.max_score:
                            self.game_stats.max_score = score
                            self.game_stats.save_highscore(score)
                        
                        if not GameUI.show_game_over_screen(self.screen, score, 
                                                          self.game_stats.max_score, 
                                                          self.font_manager):
                            return False
                        return True
                
                fall_time = 0
            
            # 绘制游戏画面
            self.draw_game(grid, current_piece, next_piece, particles, score, level)
            
            pygame.display.flip()
        
        return True
    
    def draw_game(self, grid, current_piece, next_piece, particles, score, level):
        """绘制游戏界面"""
        self.screen.fill(Config.COLORS['BLACK'])
        
        # 1. 绘制网格
        self.draw_grid()
        
        # 2. 绘制游戏区域边框
        pygame.draw.rect(
            self.screen,
            Config.COLORS['WHITE'],
            (Config.GRID_OFFSET_X, Config.GRID_OFFSET_Y,
             Config.GRID_WIDTH * Config.BLOCK_SIZE,
             Config.GRID_HEIGHT * Config.BLOCK_SIZE),
            1
        )
        
        # 3. 绘制已放置的方块
        for y in range(Config.GRID_HEIGHT):
            for x in range(Config.GRID_WIDTH):
                if grid[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        grid[y][x],
                        (Config.GRID_OFFSET_X + x * Config.BLOCK_SIZE,
                         Config.GRID_OFFSET_Y + y * Config.BLOCK_SIZE,
                         Config.BLOCK_SIZE - 1, Config.BLOCK_SIZE - 1)
                    )
        
        # 4. 绘制阴影
        ghost_piece = GameLogic.get_ghost_position(current_piece, grid)
        if ghost_piece.y != current_piece.y:  # 只在阴影不与当前方块重叠时绘制
            ghost_piece.draw(self.screen, Config.GRID_OFFSET_X, Config.GRID_OFFSET_Y, ghost=True)   
        # 5. 绘制当前方块
        current_piece.draw(self.screen, Config.GRID_OFFSET_X, Config.GRID_OFFSET_Y)
        
        # 6. 绘制右侧信息面板
         # 绘制分数和等级（减小间距的文字）
        score_text = self.font_manager.normal_font.render(f"分数: {score}", True, Config.COLORS['WHITE'])
        level_text = self.font_manager.normal_font.render(f"等级: {level}", True, Config.COLORS['WHITE'])
        next_label = self.font_manager.normal_font.render("下一个:", True, Config.COLORS['WHITE'])
        
        self.screen.blit(score_text, (Config.SIDE_PANEL_X, Config.SCORE_Y))
        self.screen.blit(level_text, (Config.SIDE_PANEL_X, Config.LEVEL_Y))
        self.screen.blit(next_label, (Config.SIDE_PANEL_X, Config.NEXT_LABEL_Y))
        
        # 计算预览区域位置（确保与下一个方块对齐）
        preview_width = Config.PREVIEW_AREA_WIDTH * Config.BLOCK_SIZE
        
        # 计算预览区域的X坐标（预览框和下一个方块共用）
        preview_x = Config.SIDE_PANEL_X + (Config.PREVIEW_OFFSET * Config.BLOCK_SIZE)
        
        # 绘制预览框
        pygame.draw.rect(
            self.screen,
            Config.COLORS['WHITE'],
            (preview_x, Config.NEXT_PIECE_Y,
             Config.PREVIEW_AREA_WIDTH * Config.BLOCK_SIZE,
             Config.PREVIEW_AREA_WIDTH * Config.BLOCK_SIZE),
            1
        )
        
        # 计算方块在预览框中的居中位置
        piece_width = len(next_piece.shape[0]) * Config.BLOCK_SIZE
        piece_height = len(next_piece.shape) * Config.BLOCK_SIZE
        center_offset_x = (Config.PREVIEW_AREA_WIDTH * Config.BLOCK_SIZE - piece_width) // 2
        center_offset_y = (Config.PREVIEW_AREA_WIDTH * Config.BLOCK_SIZE - piece_height) // 2
        
        # 绘制下一个方块（居中显示）
        next_piece.draw(
            self.screen, 
            preview_x + center_offset_x, 
            Config.NEXT_PIECE_Y + center_offset_y, 
            preview=True
        )
        
        # 7. 绘制统计信息
        self.game_stats.draw(self.screen)
        
        # 8. 绘制粒子效果
        for particle in particles:
            particle.draw(self.screen)
        
        pygame.display.flip()

 
    def draw_grid(self):
        """绘制网格线"""
        for x in range(Config.GRID_WIDTH + 1):
            x_pos = Config.GRID_OFFSET_X + x * Config.BLOCK_SIZE
            pygame.draw.line(
                self.screen,
                Config.GRID_COLOR,
                (x_pos, Config.GRID_OFFSET_Y),
                (x_pos, Config.GRID_OFFSET_Y + Config.GRID_HEIGHT * Config.BLOCK_SIZE)
            )
        
        for y in range(Config.GRID_HEIGHT + 1):
            y_pos = Config.GRID_OFFSET_Y + y * Config.BLOCK_SIZE
            pygame.draw.line(
                self.screen,
                Config.GRID_COLOR,
                (Config.GRID_OFFSET_X, y_pos),
                (Config.GRID_OFFSET_X + Config.GRID_WIDTH * Config.BLOCK_SIZE, y_pos)
            )

def main():
    """游戏入口函数"""
    try:
        game = TetrisGame()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())