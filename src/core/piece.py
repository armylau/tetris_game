#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方块类 - 负责方块形状和旋转逻辑
"""

from typing import List, Tuple
from src.utils.constants import PIECE_SHAPES, PIECE_COLORS


class Piece:
    """方块类 - 负责方块形状和旋转逻辑"""
    
    def __init__(self, piece_type: str):
        self.type = piece_type
        self.rotation = 0
        self.shape = self._get_shape()
        self.color = self._get_color()
    
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
    
    def get_dimensions(self) -> Tuple[int, int]:
        """获取方块尺寸"""
        return len(self.shape[0]), len(self.shape)
    
    def get_width(self) -> int:
        """获取方块宽度"""
        return len(self.shape[0])
    
    def get_height(self) -> int:
        """获取方块高度"""
        return len(self.shape)
    
    def _get_shape(self) -> List[List[int]]:
        """获取形状数据"""
        return PIECE_SHAPES[self.type][0]
    
    def _get_color(self) -> Tuple[int, int, int]:
        """获取颜色"""
        return PIECE_COLORS[self.type]
