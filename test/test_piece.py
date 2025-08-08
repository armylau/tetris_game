#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Piece类的单元测试
"""

import unittest
import sys
import os

from src.core.piece import Piece
from src.utils.constants import PIECE_SHAPES, PIECE_COLORS


class TestPiece(unittest.TestCase):
    """Piece类的单元测试"""
    
    def setUp(self):
        """测试前的设置"""
        self.piece_i = Piece('I')
        self.piece_o = Piece('O')
        self.piece_t = Piece('T')
        self.piece_s = Piece('S')
        self.piece_z = Piece('Z')
        self.piece_j = Piece('J')
        self.piece_l = Piece('L')
    
    def test_piece_initialization(self):
        """测试方块初始化"""
        # 测试基本属性
        self.assertEqual(self.piece_i.type, 'I')
        self.assertEqual(self.piece_o.type, 'O')
        self.assertEqual(self.piece_t.type, 'T')
        
        # 测试初始旋转状态
        self.assertEqual(self.piece_i.rotation, 0)
        self.assertEqual(self.piece_o.rotation, 0)
        self.assertEqual(self.piece_t.rotation, 0)
        
        # 测试颜色
        self.assertEqual(self.piece_i.color, PIECE_COLORS['I'])
        self.assertEqual(self.piece_o.color, PIECE_COLORS['O'])
        self.assertEqual(self.piece_t.color, PIECE_COLORS['T'])
    
    def test_piece_shape_initialization(self):
        """测试方块形状初始化"""
        # 测试初始形状
        self.assertEqual(self.piece_i.shape, PIECE_SHAPES['I'][0])
        self.assertEqual(self.piece_o.shape, PIECE_SHAPES['O'][0])
        self.assertEqual(self.piece_t.shape, PIECE_SHAPES['T'][0])
    
    def test_get_shape(self):
        """测试获取形状"""
        shape_i = self.piece_i.get_shape()
        shape_o = self.piece_o.get_shape()
        shape_t = self.piece_t.get_shape()
        
        self.assertEqual(shape_i, PIECE_SHAPES['I'][0])
        self.assertEqual(shape_o, PIECE_SHAPES['O'][0])
        self.assertEqual(shape_t, PIECE_SHAPES['T'][0])
    
    def test_get_dimensions(self):
        """测试获取方块尺寸"""
        # I型方块初始是1x4
        width, height = self.piece_i.get_dimensions()
        self.assertEqual(width, 4)
        self.assertEqual(height, 1)
        
        # O型方块是2x2
        width, height = self.piece_o.get_dimensions()
        self.assertEqual(width, 2)
        self.assertEqual(height, 2)
        
        # T型方块初始是3x2
        width, height = self.piece_t.get_dimensions()
        self.assertEqual(width, 3)
        self.assertEqual(height, 2)
    
    def test_get_width_height(self):
        """测试获取宽度和高度"""
        self.assertEqual(self.piece_i.get_width(), 4)
        self.assertEqual(self.piece_i.get_height(), 1)
        
        self.assertEqual(self.piece_o.get_width(), 2)
        self.assertEqual(self.piece_o.get_height(), 2)
        
        self.assertEqual(self.piece_t.get_width(), 3)
        self.assertEqual(self.piece_t.get_height(), 2)
    
    def test_rotate_i_piece(self):
        """测试I型方块旋转"""
        # I型方块只有两种状态
        original_shape = self.piece_i.shape.copy()
        
        # 第一次旋转
        self.assertTrue(self.piece_i.rotate())
        self.assertEqual(self.piece_i.rotation, 1)
        self.assertNotEqual(self.piece_i.shape, original_shape)
        
        # 第二次旋转，回到原始状态
        self.assertTrue(self.piece_i.rotate())
        self.assertEqual(self.piece_i.rotation, 0)
        self.assertEqual(self.piece_i.shape, original_shape)
    
    def test_rotate_o_piece(self):
        """测试O型方块旋转"""
        # O型方块不需要旋转
        original_shape = self.piece_o.shape.copy()
        
        self.assertTrue(self.piece_o.rotate())
        self.assertEqual(self.piece_o.rotation, 0)  # 旋转状态不变
        self.assertEqual(self.piece_o.shape, original_shape)  # 形状不变
    
    def test_rotate_t_piece(self):
        """测试T型方块旋转"""
        # T型方块有四种旋转状态
        original_shape = self.piece_t.shape.copy()
        
        # 第一次旋转
        self.assertTrue(self.piece_t.rotate())
        self.assertEqual(self.piece_t.rotation, 1)
        self.assertNotEqual(self.piece_t.shape, original_shape)
        
        # 第二次旋转
        self.assertTrue(self.piece_t.rotate())
        self.assertEqual(self.piece_t.rotation, 2)
        
        # 第三次旋转
        self.assertTrue(self.piece_t.rotate())
        self.assertEqual(self.piece_t.rotation, 3)
        
        # 第四次旋转，回到原始状态
        self.assertTrue(self.piece_t.rotate())
        self.assertEqual(self.piece_t.rotation, 0)
        self.assertEqual(self.piece_t.shape, original_shape)
    
    def test_rotate_all_pieces(self):
        """测试所有方块的旋转"""
        pieces = [self.piece_s, self.piece_z, self.piece_j, self.piece_l]
        
        for piece in pieces:
            original_shape = piece.shape.copy()
            original_rotation = piece.rotation
            
            # 旋转4次，应该回到原始状态
            for i in range(4):
                self.assertTrue(piece.rotate())
            
            self.assertEqual(piece.rotation, original_rotation)
            self.assertEqual(piece.shape, original_shape)
    
    def test_piece_shape_validation(self):
        """测试方块形状验证"""
        # 测试所有方块的形状都是有效的二维数组
        pieces = [self.piece_i, self.piece_o, self.piece_t, self.piece_s, 
                 self.piece_z, self.piece_j, self.piece_l]
        
        for piece in pieces:
            shape = piece.get_shape()
            self.assertIsInstance(shape, list)
            self.assertGreater(len(shape), 0)
            
            for row in shape:
                self.assertIsInstance(row, list)
                self.assertGreater(len(row), 0)
                
                for cell in row:
                    self.assertIn(cell, [0, 1])
    
    def test_piece_color_validation(self):
        """测试方块颜色验证"""
        # 测试所有方块都有有效的颜色
        pieces = [self.piece_i, self.piece_o, self.piece_t, self.piece_s, 
                 self.piece_z, self.piece_j, self.piece_l]
        
        for piece in pieces:
            color = piece.color
            self.assertIsInstance(color, tuple)
            self.assertEqual(len(color), 3)
            
            for component in color:
                self.assertIsInstance(component, int)
                self.assertGreaterEqual(component, 0)
                self.assertLessEqual(component, 255)
    
    def test_piece_rotation_consistency(self):
        """测试方块旋转的一致性"""
        # 测试旋转后尺寸的一致性
        pieces = [self.piece_t, self.piece_s, self.piece_z, self.piece_j, self.piece_l]
        
        for piece in pieces:
            original_width = piece.get_width()
            original_height = piece.get_height()
            
            # 旋转4次
            for i in range(4):
                piece.rotate()
                # 检查尺寸是否合理
                self.assertGreater(piece.get_width(), 0)
                self.assertGreater(piece.get_height(), 0)
            
            # 回到原始状态
            for i in range(4):
                piece.rotate()
            
            # 检查是否回到原始尺寸
            self.assertEqual(piece.get_width(), original_width)
            self.assertEqual(piece.get_height(), original_height)
    
    def test_piece_edge_cases(self):
        """测试边界情况"""
        # 测试无效的方块类型（如果传入的话）
        # 注意：这里我们假设Piece类会正确处理无效类型
        # 在实际实现中，可能需要添加异常处理
        
        # 测试旋转后的形状变化
        self.piece_t.rotate()
        self.assertNotEqual(self.piece_t.shape, PIECE_SHAPES['T'][0])
        self.assertEqual(self.piece_t.shape, PIECE_SHAPES['T'][1])
    
    def test_piece_shape_after_rotation(self):
        """测试旋转后的形状"""
        # 测试T型方块旋转后的具体形状
        # 初始状态：[[0, 1, 0], [1, 1, 1]]
        self.assertEqual(self.piece_t.shape, [[0, 1, 0], [1, 1, 1]])
        
        # 第一次旋转：[[1, 0], [1, 1], [1, 0]]
        self.piece_t.rotate()
        self.assertEqual(self.piece_t.shape, [[1, 0], [1, 1], [1, 0]])
        
        # 第二次旋转：[[1, 1, 1], [0, 1, 0]]
        self.piece_t.rotate()
        self.assertEqual(self.piece_t.shape, [[1, 1, 1], [0, 1, 0]])
        
        # 第三次旋转：[[0, 1], [1, 1], [0, 1]]
        self.piece_t.rotate()
        self.assertEqual(self.piece_t.shape, [[0, 1], [1, 1], [0, 1]])


if __name__ == '__main__':
    unittest.main()
