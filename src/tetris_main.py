#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏主程序
基于Pygame开发的经典俄罗斯方块游戏
"""

import pygame
import sys
import time
from typing import Optional, List, Tuple
from config import GameConfig

# 游戏常量 - 使用配置类
SCREEN_WIDTH = GameConfig.SCREEN_WIDTH
SCREEN_HEIGHT = GameConfig.SCREEN_HEIGHT
BOARD_WIDTH = GameConfig.BOARD_WIDTH
BOARD_HEIGHT = GameConfig.BOARD_HEIGHT
CELL_SIZE = GameConfig.CELL_SIZE
BOARD_X = GameConfig.BOARD_X
BOARD_Y = GameConfig.BOARD_Y

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# 方块颜色映射
PIECE_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': MAGENTA,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

# 方块形状定义
PIECE_SHAPES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1],
         [1],
         [1],
         [1]]
    ],
    'O': [
        [[1, 1],
         [1, 1]]
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [1, 1],
         [0, 1]]
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]]
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1]],
        [[1, 1],
         [1, 0],
         [1, 0]],
        [[1, 1, 1],
         [0, 0, 1]],
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1]],
        [[1, 0],
         [1, 0],
         [1, 1]],
        [[1, 1, 1],
         [1, 0, 0]],
        [[1, 1],
         [0, 1],
         [0, 1]]
    ]
}


class Piece:
    """方块类，管理方块形状和旋转"""
    
    def __init__(self, piece_type: str):
        self.type = piece_type
        self.rotation = 0
        self.shape = PIECE_SHAPES[piece_type][0]
        self.color = PIECE_COLORS[piece_type]
    
    def rotate(self) -> bool:
        """旋转方块"""
        if self.type == 'O':  # O型方块不需要旋转
            return True
        
        if self.type == 'I':
            # I型方块只有两种状态
            self.rotation = (self.rotation + 1) % 2
            self.shape = PIECE_SHAPES['I'][self.rotation]
        else:
            # 其他方块有四种旋转状态
            self.rotation = (self.rotation + 1) % len(PIECE_SHAPES[self.type])
            self.shape = PIECE_SHAPES[self.type][self.rotation]
        
        return True
    
    def get_shape(self) -> List[List[int]]:
        """获取当前形状"""
        return self.shape
    
    def get_width(self) -> int:
        """获取方块宽度"""
        return len(self.shape[0])
    
    def get_height(self) -> int:
        """获取方块高度"""
        return len(self.shape)


class Board:
    """游戏板，管理方块位置和状态"""
    
    def __init__(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, piece: Piece, x: int, y: int) -> bool:
        """检查位置是否有效"""
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[0])):
                if piece.shape[row][col]:
                    board_x = x + col
                    board_y = y + row
                    
                    # 检查边界
                    if (board_x < 0 or board_x >= self.width or 
                        board_y >= self.height):
                        return False
                    
                    # 检查与其他方块的碰撞
                    if board_y >= 0 and self.grid[board_y][board_x] is not None:
                        return False
        
        return True
    
    def place_piece(self, piece: Piece, x: int, y: int) -> bool:
        """放置方块到指定位置"""
        if not self.is_valid_position(piece, x, y):
            return False
        
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[0])):
                if piece.shape[row][col]:
                    board_x = x + col
                    board_y = y + row
                    if board_y >= 0:
                        self.grid[board_y][board_x] = piece.color
        
        return True
    
    def clear_lines(self) -> int:
        """清除完整行，返回消除的行数"""
        lines_cleared = 0
        row = self.height - 1
        
        while row >= 0:
            if all(cell is not None for cell in self.grid[row]):
                # 删除完整行
                self.grid.pop(row)
                # 在顶部添加新的空行
                self.grid.insert(0, [None for _ in range(self.width)])
                lines_cleared += 1
            else:
                row -= 1
        
        return lines_cleared
    
    def is_game_over(self) -> bool:
        """检查游戏是否结束"""
        # 检查顶部行是否有方块
        return any(cell is not None for cell in self.grid[0])


class GameState:
    """游戏状态管理"""
    
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.current_piece: Optional[Piece] = None
        self.next_piece: Optional[Piece] = None
        self.piece_x = 0
        self.piece_y = 0
        self.drop_time = 0
        self.drop_delay = 1000  # 毫秒
        
        # 关卡相关属性
        self.game_mode = "classic"  # "classic" 或 "level"
        self.current_level_id = 1
        self.level_complete = False
        self.level_failed = False
        self.level_stars = 0
    
    def update_score(self, lines_cleared: int):
        """更新分数"""
        self.score += GameConfig.get_score(lines_cleared, self.level)
        self.lines_cleared += lines_cleared
    
    def update_level(self):
        """更新等级"""
        new_level = GameConfig.get_level(self.lines_cleared)
        if new_level != self.level:
            self.level = new_level
            # 更新下落延迟
            self.drop_delay = GameConfig.get_drop_delay(self.level)
    
    def spawn_piece(self, piece_type: str):
        """生成新方块"""
        self.current_piece = Piece(piece_type)
        self.piece_x = self.current_piece.get_width() // 2
        self.piece_y = 0
        
        # 检查游戏是否结束
        if not self.board.is_valid_position(self.current_piece, self.piece_x, self.piece_y):
            self.game_over = True


class Renderer:
    """渲染引擎，负责图形绘制"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
        # 确保pygame已初始化
        try:
            pygame.init()
        except:
            pass
        
        # 尝试使用支持中文的字体
        try:
            from font_utils import FontManager
            self.font = FontManager.get_font(36)
            self.small_font = FontManager.get_font(24)
        except ImportError:
            # 回退到原来的字体加载方式
            try:
                # 在macOS上尝试使用系统字体
                self.font = pygame.font.Font("/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc", 36)
                self.small_font = pygame.font.Font("/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc", 24)
            except:
                try:
                    # 尝试使用其他常见的中文字体
                    self.font = pygame.font.Font("/System/Library/Fonts/STHeiti Light.ttc", 36)
                    self.small_font = pygame.font.Font("/System/Library/Fonts/STHeiti Light.ttc", 24)
                except:
                    try:
                        # 尝试使用Helvetica
                        self.font = pygame.font.Font("/System/Library/Fonts/Helvetica.ttc", 36)
                        self.small_font = pygame.font.Font("/System/Library/Fonts/Helvetica.ttc", 24)
                    except:
                        # 回退到默认字体
                        self.font = pygame.font.Font(None, 36)
                        self.small_font = pygame.font.Font(None, 24)
    
    def render_board(self, board: Board):
        """渲染游戏板"""
        # 绘制游戏板背景
        pygame.draw.rect(self.screen, GRAY, 
                        (BOARD_X - 2, BOARD_Y - 2, 
                         BOARD_WIDTH * CELL_SIZE + 4, 
                         BOARD_HEIGHT * CELL_SIZE + 4))
        
        # 绘制网格
        for row in range(board.height):
            for col in range(board.width):
                x = BOARD_X + col * CELL_SIZE
                y = BOARD_Y + row * CELL_SIZE
                
                if board.grid[row][col]:
                    # 绘制已放置的方块
                    pygame.draw.rect(self.screen, board.grid[row][col],
                                   (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK,
                                   (x, y, CELL_SIZE, CELL_SIZE), 1)
                else:
                    # 绘制空格子
                    pygame.draw.rect(self.screen, BLACK,
                                   (x, y, CELL_SIZE, CELL_SIZE), 1)
    
    def render_piece(self, piece: Piece, x: int, y: int):
        """渲染当前方块"""
        if not piece:
            return
        
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[0])):
                if piece.shape[row][col]:
                    screen_x = BOARD_X + (x + col) * CELL_SIZE
                    screen_y = BOARD_Y + (y + row) * CELL_SIZE
                    pygame.draw.rect(self.screen, piece.color,
                                   (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK,
                                   (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 1)
    
    def render_ui(self, game_state: GameState):
        """渲染用户界面"""
        # 绘制分数
        score_text = self.font.render(f"Score: {game_state.score}", True, WHITE)
        self.screen.blit(score_text, (50, 50))
        
        # 绘制等级
        level_text = self.font.render(f"Level: {game_state.level}", True, WHITE)
        self.screen.blit(level_text, (50, 100))
        
        # 绘制已消除行数
        lines_text = self.font.render(f"Lines: {game_state.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (50, 150))
        
        # 绘制关卡信息（如果处于关卡模式）
        if hasattr(game_state, 'game_mode') and game_state.game_mode == "level":
            # 绘制关卡编号
            level_id_text = self.font.render(f"Level: {game_state.current_level_id}", True, WHITE)
            self.screen.blit(level_id_text, (50, 200))
            
            # 绘制目标行数
            if hasattr(game_state, 'level_manager') and game_state.level_manager:
                target_lines = game_state.level_manager.get_target_lines()
                target_text = self.font.render(f"Target: {target_lines} lines", True, WHITE)
                self.screen.blit(target_text, (50, 250))
                
                # 绘制剩余时间
                time_remaining = game_state.level_manager.get_time_remaining()
                if time_remaining is not None:
                    time_text = self.font.render(f"Time: {time_remaining}s", True, WHITE)
                    self.screen.blit(time_text, (50, 300))
        
        # 绘制下一个方块预览
        if game_state.next_piece:
            next_text = self.font.render("Next:", True, WHITE)
            self.screen.blit(next_text, (50, 350))
            
            # 绘制预览方块
            preview_x = 50
            preview_y = 400
            for row in range(len(game_state.next_piece.shape)):
                for col in range(len(game_state.next_piece.shape[0])):
                    if game_state.next_piece.shape[row][col]:
                        x = preview_x + col * 20
                        y = preview_y + row * 20
                        pygame.draw.rect(self.screen, game_state.next_piece.color,
                                       (x, y, 20, 20))
                        pygame.draw.rect(self.screen, BLACK, (x, y, 20, 20), 1)
        
        # 绘制游戏状态
        if game_state.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            self.screen.blit(game_over_text, (300, 300))
        elif game_state.paused:
            pause_text = self.font.render("PAUSED", True, YELLOW)
            self.screen.blit(pause_text, (300, 300))
        elif hasattr(game_state, 'level_complete') and game_state.level_complete:
            complete_text = self.font.render("LEVEL COMPLETE!", True, GREEN)
            self.screen.blit(complete_text, (300, 300))
            
            # 绘制星级
            if hasattr(game_state, 'level_stars'):
                stars_text = self.font.render(f"Stars: {game_state.level_stars}/3", True, YELLOW)
                self.screen.blit(stars_text, (300, 350))
        elif hasattr(game_state, 'level_failed') and game_state.level_failed:
            failed_text = self.font.render("LEVEL FAILED!", True, RED)
            self.screen.blit(failed_text, (300, 300))


class TetrisGame:
    """俄罗斯方块游戏主类"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris Game")
        self.clock = pygame.time.Clock()
        
        self.board = Board()
        self.game_state = GameState()
        self.game_state.board = self.board  # 设置引用
        self.renderer = Renderer(self.screen)
        
        # 关卡管理器
        try:
            from level_manager import LevelManager
            self.level_manager = LevelManager()
        except ImportError:
            self.level_manager = None
        
        self.running = True
        self.last_drop_time = time.time()
        
        # 按键状态跟踪
        self.keys_pressed = set()
        self.last_key_time = {}  # 记录按键时间
        self.key_repeat_delay = GameConfig.KEY_REPEAT_DELAY
        self.key_repeat_interval = GameConfig.KEY_REPEAT_INTERVAL
        self.down_key_hold_delay = GameConfig.DOWN_KEY_HOLD_DELAY
        
        # 返回状态
        self.return_to_menu = False
        
        # 向下键加速相关变量
        self.down_key_start_time = 0  # 向下键开始按下的时间
        self.down_key_last_move_time = 0  # 上次向下移动的时间
        self.down_key_acceleration_start = GameConfig.DOWN_KEY_ACCELERATION_START
        self.down_key_acceleration_max = GameConfig.DOWN_KEY_ACCELERATION_MAX
        self.down_key_min_interval = GameConfig.DOWN_KEY_MIN_INTERVAL
        self.down_key_max_interval = GameConfig.DOWN_KEY_MAX_INTERVAL
        
        # 初始化游戏
        self.spawn_new_piece()
    
    def spawn_new_piece(self):
        """生成新方块"""
        import random
        
        # 获取可用的方块类型
        if self.level_manager and self.game_state.game_mode == "level":
            available_pieces = self.level_manager.get_available_piece_types()
        else:
            available_pieces = list(PIECE_SHAPES.keys())
        
        if self.game_state.next_piece is None:
            self.game_state.next_piece = Piece(random.choice(available_pieces))
        
        self.game_state.current_piece = self.game_state.next_piece
        self.game_state.next_piece = Piece(random.choice(available_pieces))
        self.game_state.piece_x = BOARD_WIDTH // 2 - self.game_state.current_piece.get_width() // 2
        self.game_state.piece_y = 0
        
        # 检查游戏是否结束
        if not self.board.is_valid_position(self.game_state.current_piece, 
                                          self.game_state.piece_x, self.game_state.piece_y):
            self.game_state.game_over = True
    
    def handle_input(self):
        """处理用户输入"""
        current_time = time.time() * 1000  # 转换为毫秒
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.last_key_time[event.key] = current_time
                
                # 处理单次按键事件
                if event.key == pygame.K_LEFT:
                    self.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.move_piece(0, 1)  # 单击向下键移动一格
                    self.down_key_start_time = current_time  # 记录开始时间
                    self.down_key_last_move_time = current_time  # 记录移动时间
                elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    self.rotate_piece()
                elif event.key == pygame.K_p:
                    self.game_state.paused = not self.game_state.paused
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.return_to_menu = True
                    self.running = False
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
                if event.key in self.last_key_time:
                    del self.last_key_time[event.key]
                
                # 重置向下键加速相关变量
                if event.key == pygame.K_DOWN:
                    self.down_key_start_time = 0
                    self.down_key_last_move_time = 0
        
        # 处理连续按键（按住键的情况）
        if not self.game_state.paused:
            self.handle_continuous_input(current_time)
    
    def move_piece(self, dx: int, dy: int) -> bool:
        """移动方块"""
        if self.game_state.paused:
            return False
        
        new_x = self.game_state.piece_x + dx
        new_y = self.game_state.piece_y + dy
        
        if self.board.is_valid_position(self.game_state.current_piece, new_x, new_y):
            self.game_state.piece_x = new_x
            self.game_state.piece_y = new_y
            return True
        return False
    
    def rotate_piece(self) -> bool:
        """旋转方块"""
        if self.game_state.paused:
            return False
        
        # 检查旋转限制
        if (self.level_manager and 
            self.game_state.game_mode == "level" and
            self.level_manager.check_rule_violation("rotate")):
            return False
        
        try:
            original_rotation = self.game_state.current_piece.rotation
            self.game_state.current_piece.rotate()
            
            # 记录旋转次数
            if self.level_manager and self.game_state.game_mode == "level":
                self.level_manager.record_rotation()
            
            # 尝试墙踢算法
            if not self.board.is_valid_position(self.game_state.current_piece, 
                                              self.game_state.piece_x, self.game_state.piece_y):
                # 尝试不同的偏移位置
                offsets = [(0, -1), (1, -1), (-1, -1), (1, 0), (-1, 0)]
                for offset_x, offset_y in offsets:
                    new_x = self.game_state.piece_x + offset_x
                    new_y = self.game_state.piece_y + offset_y
                    if self.board.is_valid_position(self.game_state.current_piece, new_x, new_y):
                        self.game_state.piece_x = new_x
                        self.game_state.piece_y = new_y
                        return True
                
                # 如果所有偏移都无效，恢复原状态
                self.game_state.current_piece.rotation = original_rotation
                self.game_state.current_piece.shape = PIECE_SHAPES[self.game_state.current_piece.type][original_rotation]
                return False
            
            return True
        except Exception as e:
            print(f"旋转方块时出错: {e}")
            return False
    
    def handle_continuous_input(self, current_time):
        """处理连续按键输入"""
        # 处理左右移动的连续按键
        if pygame.K_LEFT in self.keys_pressed:
            if (current_time - self.last_key_time.get(pygame.K_LEFT, 0) > 
                self.key_repeat_delay):
                if (current_time - self.last_key_time.get(pygame.K_LEFT, 0) > 
                    self.key_repeat_interval):
                    self.move_piece(-1, 0)
                    self.last_key_time[pygame.K_LEFT] = current_time
        
        if pygame.K_RIGHT in self.keys_pressed:
            if (current_time - self.last_key_time.get(pygame.K_RIGHT, 0) > 
                self.key_repeat_delay):
                if (current_time - self.last_key_time.get(pygame.K_RIGHT, 0) > 
                    self.key_repeat_interval):
                    self.move_piece(1, 0)
                    self.last_key_time[pygame.K_RIGHT] = current_time
        
        # 处理向下加速的连续按键
        if pygame.K_DOWN in self.keys_pressed:
            # 检查向下键加速限制
            if (self.level_manager and 
                self.game_state.game_mode == "level" and
                self.level_manager.check_rule_violation("down_acceleration")):
                pass  # 跳过向下键加速
            else:
                # 计算按键持续时间
                hold_duration = current_time - self.down_key_start_time
                
                # 如果超过开始加速的时间
                if hold_duration > self.down_key_acceleration_start:
                    # 计算加速后的间隔时间（线性插值）
                    if hold_duration >= self.down_key_acceleration_max:
                        # 达到最大加速
                        interval = self.down_key_min_interval
                    else:
                        # 线性插值计算间隔
                        progress = (hold_duration - self.down_key_acceleration_start) / (self.down_key_acceleration_max - self.down_key_acceleration_start)
                        interval = self.down_key_max_interval - (self.down_key_max_interval - self.down_key_min_interval) * progress
                    
                    # 检查是否到了移动时间
                    if current_time - self.down_key_last_move_time >= interval:
                        self.move_piece(0, 1)
                        self.down_key_last_move_time = current_time
    
    def update(self):
        """更新游戏状态"""
        if self.game_state.paused:
            return
        
        # 如果游戏结束，等待用户按ESC键
        if self.game_state.game_over:
            return
        
        # 检查关卡时间限制
        if (self.level_manager and 
            self.game_state.game_mode == "level" and
            self.level_manager.is_time_up()):
            self.game_state.level_failed = True
            return
        
        current_time = time.time()
        
        # 自动下落
        if current_time - self.last_drop_time > self.game_state.drop_delay / 1000.0:
            if not self.move_piece(0, 1):
                # 无法下落，放置方块
                self.board.place_piece(self.game_state.current_piece, 
                                     self.game_state.piece_x, self.game_state.piece_y)
                
                # 清除完整行
                lines_cleared = self.board.clear_lines()
                if lines_cleared > 0:
                    self.game_state.update_score(lines_cleared)
                    self.game_state.update_level()
                
                # 检查关卡完成
                if (self.level_manager and 
                    self.game_state.game_mode == "level" and
                    self.level_manager.check_level_complete(self.game_state.lines_cleared, self.game_state.score)):
                    
                    # 计算星级
                    time_remaining = self.level_manager.get_time_remaining()
                    stars = self.level_manager.calculate_stars(
                        self.game_state.lines_cleared, 
                        self.game_state.score, 
                        time_remaining
                    )
                    
                    # 完成关卡
                    self.level_manager.complete_level(
                        self.game_state.lines_cleared,
                        self.game_state.score,
                        stars
                    )
                    
                    self.game_state.level_complete = True
                    self.game_state.level_stars = stars
                    return
                
                # 生成新方块
                self.spawn_new_piece()
            
            self.last_drop_time = current_time
    
    def render(self):
        """渲染游戏画面"""
        self.screen.fill(BLACK)
        
        # 渲染游戏板
        self.renderer.render_board(self.board)
        
        # 渲染当前方块
        if self.game_state.current_piece:
            self.renderer.render_piece(self.game_state.current_piece, 
                                     self.game_state.piece_x, self.game_state.piece_y)
        
        # 渲染用户界面
        self.renderer.render_ui(self.game_state)
        
        pygame.display.flip()
    
    def reset_game(self):
        """重置游戏"""
        self.board = Board()
        self.game_state = GameState()
        self.game_state.board = self.board
        self.last_drop_time = time.time()
        self.spawn_new_piece()
    
    def run(self):
        """主游戏循环"""
        while self.running:
            try:
                self.handle_input()
                self.update()
                self.render()
                self.clock.tick(GameConfig.TARGET_FPS)
            except Exception as e:
                print(f"游戏循环出错: {e}")
                import traceback
                traceback.print_exc()
                break
        
        # 返回是否应该回到主菜单
        return self.return_to_menu


def main():
    """主函数"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("俄罗斯方块")
    
    try:
        from main_menu import MainMenu
        from level_selector import LevelSelector
        
        while True:
            # 显示主菜单
            menu = MainMenu(screen)
            choice = menu.run()
            
            if choice == "quit":
                break
            elif choice == "classic":
                # 经典模式
                game = TetrisGame()
                game.game_state.game_mode = "classic"
                should_return_to_menu = game.run()
                if not should_return_to_menu:
                    break  # 如果游戏没有要求返回菜单，则退出程序
            elif choice == "level":
                # 关卡模式
                selector = LevelSelector(screen)
                selected_level = selector.run()
                
                if selected_level and selected_level > 0:
                    # 加载选中的关卡
                    game = TetrisGame()
                    game.game_state.game_mode = "level"
                    
                    if game.level_manager and game.level_manager.load_level(selected_level):
                        game.game_state.current_level_id = selected_level
                        should_return_to_menu = game.run()
                        if not should_return_to_menu:
                            break  # 如果游戏没有要求返回菜单，则退出程序
                    else:
                        print(f"无法加载关卡 {selected_level}")
                elif selected_level == -1:
                    # 返回主菜单
                    continue
                else:
                    # 退出游戏
                    break
    except ImportError as e:
        print(f"导入模块失败: {e}")
        # 回退到经典模式
        game = TetrisGame()
        game.run()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
