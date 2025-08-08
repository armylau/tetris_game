#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
碰撞检测类 - 负责方块碰撞检测和墙踢算法
"""

from typing import List, Tuple
from src.core.piece import Piece
from src.core.board import Board


class CollisionDetector:
    """碰撞检测类 - 负责方块碰撞检测和墙踢算法"""
    
    def __init__(self):
        pass
    
    def is_valid_position(self, piece: Piece, board: Board, x: int, y: int) -> bool:
        """检查位置是否有效"""
        return board.is_valid_position(piece, x, y)
    
    def try_wall_kick(self, piece: Piece, board: Board, x: int, y: int) -> Tuple[int, int]:
        """尝试墙踢算法，返回调整后的位置"""
        # 墙踢算法的偏移位置
        offsets = [
            (0, -1),   # 向上
            (1, -1),   # 右上
            (-1, -1),  # 左上
            (1, 0),    # 右
            (-1, 0),   # 左
            (1, 1),    # 右下
            (-1, 1),   # 左下
            (0, 1),    # 下
        ]
        
        for offset_x, offset_y in offsets:
            new_x = x + offset_x
            new_y = y + offset_y
            if board.is_valid_position(piece, new_x, new_y):
                return new_x, new_y
        
        # 如果没有找到有效位置，返回原位置
        return x, y
    
    def can_rotate(self, piece: Piece, board: Board, x: int, y: int) -> Tuple[bool, Tuple[int, int]]:
        """检查是否可以旋转，如果可以则返回调整后的位置"""
        # 保存原始旋转状态
        original_rotation = piece.rotation
        original_shape = piece.shape.copy()
        
        # 尝试旋转
        piece.rotate()
        
        # 检查旋转后的位置是否有效
        if board.is_valid_position(piece, x, y):
            return True, (x, y)
        
        # 尝试墙踢算法
        new_x, new_y = self.try_wall_kick(piece, board, x, y)
        if board.is_valid_position(piece, new_x, new_y):
            return True, (new_x, new_y)
        
        # 如果都不行，恢复原始状态
        piece.rotation = original_rotation
        piece.shape = original_shape
        return False, (x, y)
