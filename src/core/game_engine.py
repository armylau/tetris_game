#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏引擎 - 负责游戏主循环和逻辑协调
"""

import time
import random
from typing import Optional, List
from src.core.board import Board
from src.core.game_state import GameState
from src.core.piece import Piece
from src.core.collision import CollisionDetector
from src.config.game_config import GameConfig
from src.utils.constants import PIECE_SHAPES


class GameEngine:
    """游戏引擎 - 负责游戏主循环和逻辑协调"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        self.board = Board(config.BOARD_WIDTH, config.BOARD_HEIGHT)
        self.game_state = GameState()
        self.collision_detector = CollisionDetector()
        self.last_drop_time = time.time()
        
        # 关卡管理器 - 通过依赖注入传入，避免循环导入
        self.level_manager = None
    
    def spawn_new_piece(self):
        """生成新方块"""
        # 获取可用的方块类型
        if self.level_manager and self.game_state.game_mode == "level":
            available_pieces = self.level_manager.get_available_piece_types()
        else:
            available_pieces = list(PIECE_SHAPES.keys())
        
        if self.game_state.next_piece is None:
            self.game_state.next_piece = Piece(random.choice(available_pieces))
        
        self.game_state.current_piece = self.game_state.next_piece
        self.game_state.next_piece = Piece(random.choice(available_pieces))
        
        # 设置初始位置
        x = self.config.BOARD_WIDTH // 2 - self.game_state.current_piece.get_width() // 2
        y = 0
        self.game_state.set_piece_position(x, y)
        
        # 检查游戏是否结束
        if not self.board.is_valid_position(self.game_state.current_piece, x, y):
            self.game_state.game_over = True
    
    def handle_piece_movement(self, dx: int, dy: int) -> bool:
        """处理方块移动"""
        if self.game_state.paused or self.game_state.game_over:
            return False
        
        # 检查是否有当前方块
        if not self.game_state.current_piece:
            return False
        
        current_x, current_y = self.game_state.get_piece_position()
        new_x = current_x + dx
        new_y = current_y + dy
        
        if self.board.is_valid_position(self.game_state.current_piece, new_x, new_y):
            self.game_state.set_piece_position(new_x, new_y)
            return True
        return False
    
    def handle_piece_rotation(self) -> bool:
        """处理方块旋转"""
        if self.game_state.paused or self.game_state.game_over:
            return False
        
        # 检查是否有当前方块
        if not self.game_state.current_piece:
            return False
        
        # 检查旋转限制
        if (self.level_manager and 
            self.game_state.game_mode == "level" and
            self.level_manager.check_rule_violation("rotate")):
            return False
        
        current_x, current_y = self.game_state.get_piece_position()
        can_rotate, new_position = self.collision_detector.can_rotate(
            self.game_state.current_piece, 
            self.board, 
            current_x, 
            current_y
        )
        
        if can_rotate:
            self.game_state.set_piece_position(*new_position)
            
            # 记录旋转次数
            if self.level_manager and self.game_state.game_mode == "level":
                self.level_manager.record_rotation()
            
            return True
        
        return False
    
    def drop_piece(self):
        """方块下落"""
        if self.game_state.paused or self.game_state.game_over:
            return False
        
        return self.handle_piece_movement(0, 1)
    
    def place_current_piece(self):
        """放置当前方块"""
        if not self.game_state.current_piece:
            return
        
        current_x, current_y = self.game_state.get_piece_position()
        
        # 放置方块
        if self.board.place_piece(self.game_state.current_piece, current_x, current_y):
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
    
    def update(self, delta_time: float):
        """更新游戏状态"""
        if self.game_state.paused or self.game_state.game_over:
            return
        
        # 检查关卡时间限制
        if (self.level_manager and 
            self.game_state.game_mode == "level" and
            self.level_manager.is_time_up()):
            self.game_state.level_failed = True
            return
        
        # 只有在有当前方块时才进行更新
        if not self.game_state.current_piece:
            return
        
        # 只有在游戏模式设置后才进行更新
        if self.game_state.game_mode not in ["classic", "level"]:
            return
        
        current_time = time.time()
        
        # 自动下落
        if current_time - self.last_drop_time > self.game_state.drop_delay / 1000.0:
            if not self.drop_piece():
                # 无法下落，放置方块
                self.place_current_piece()
            
            self.last_drop_time = current_time
    
    def reset_game(self):
        """重置游戏"""
        self.board = Board(self.config.BOARD_WIDTH, self.config.BOARD_HEIGHT)
        self.game_state.reset()
        self.last_drop_time = time.time()
        self.spawn_new_piece()
    
    def get_board(self) -> Board:
        """获取游戏板"""
        return self.board
    
    def get_game_state(self) -> GameState:
        """获取游戏状态"""
        return self.game_state
