#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏状态管理类 - 负责游戏状态和分数管理
"""

from typing import Optional, Tuple
from src.core.piece import Piece
from src.config.game_config import GameConfig


class GameState:
    """游戏状态管理类 - 负责游戏状态和分数管理"""
    
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.current_piece: Optional[Piece] = None
        self.next_piece: Optional[Piece] = None
        self.piece_position = (0, 0)
        self.drop_delay = 1000
        
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
        self.piece_position = (self.current_piece.get_width() // 2, 0)
    
    def set_piece_position(self, x: int, y: int):
        """设置方块位置"""
        self.piece_position = (x, y)
    
    def get_piece_position(self) -> Tuple[int, int]:
        """获取方块位置"""
        return self.piece_position
    
    def reset(self):
        """重置游戏状态"""
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.current_piece = None
        self.next_piece = None
        self.piece_position = (0, 0)
        self.drop_delay = 1000
        self.game_mode = "classic"
        self.current_level_id = 1
        self.level_complete = False
        self.level_failed = False
        self.level_stars = 0
