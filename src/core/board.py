#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏板类 - 负责方块放置和行消除
"""

from typing import List, Optional, Tuple
from core.piece import Piece


class Board:
    """游戏板类 - 负责方块放置和行消除"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = self._create_empty_grid()
    
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
    
    def _create_empty_grid(self) -> List[List[Optional[Tuple[int, int, int]]]]:
        """创建空网格"""
        return [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def get_grid(self) -> List[List[Optional[Tuple[int, int, int]]]]:
        """获取网格数据"""
        return self.grid
