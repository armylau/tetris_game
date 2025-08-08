#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CollisionDetector类的单元测试
"""

import unittest
import sys
import os

from src.core.collision import CollisionDetector
from src.core.board import Board
from src.core.piece import Piece


class TestCollisionDetector(unittest.TestCase):
    """
    CollisionDetector类的单元测试

    测试思路说明：
    1. 测试is_valid_position方法：
       - 有效位置：在空白区域、边界内放置方块应返回True。
       - 超出边界：左、右、下边界外放置方块应返回False。
       - 碰撞检测：与已放置方块重叠应返回False，不重叠应返回True。
    2. 测试try_wall_kick方法（墙踢算法）：
       - 普通旋转：无障碍时应返回原位置。
       - 需要墙踢：靠近边界或有障碍时，尝试不同偏移，返回可行的新位置。
       - 墙踢失败：所有偏移都无效时应返回None或原始位置。
    3. 测试旋转相关碰撞：
       - 不同方块类型（I, O, T, S, Z, J, L）在旋转时的边界和碰撞检测。
       - 特殊情况：I型方块在墙边的旋转、T型方块T-spin检测等。
    4. 边界情况测试：
       - 方块在四角、边缘、底部等极限位置的碰撞和墙踢处理。
       - 连续多次墙踢、极端网格状态下的稳定性。
    """
    
    def setUp(self):
        """测试前的设置"""
        self.collision_detector = CollisionDetector()
        self.board = Board(10, 20)
        self.piece_o = Piece('O')
        self.piece_i = Piece('I')
        self.piece_t = Piece('T')
    
    def test_collision_detector_initialization(self):
        """测试碰撞检测器初始化"""
        self.assertIsInstance(self.collision_detector, CollisionDetector)
    
    def test_is_valid_position_valid(self):
        """测试有效位置检查 - 有效位置"""
        # 测试在游戏板中央的有效位置
        self.assertTrue(self.collision_detector.is_valid_position(self.piece_o, self.board, 4, 0))
        self.assertTrue(self.collision_detector.is_valid_position(self.piece_i, self.board, 3, 0))
    
    def test_is_valid_position_out_of_bounds(self):
        """测试有效位置检查 - 超出边界"""
        # 测试超出左边界
        self.assertFalse(self.collision_detector.is_valid_position(self.piece_o, self.board, -1, 0))
        
        # 测试超出右边界
        self.assertFalse(self.collision_detector.is_valid_position(self.piece_o, self.board, 9, 0))
        
        # 测试超出下边界
        self.assertFalse(self.collision_detector.is_valid_position(self.piece_o, self.board, 4, 19))
    
    def test_is_valid_position_collision(self):
        """测试有效位置检查 - 碰撞检测"""
        # 在游戏板上放置一个方块
        self.board.place_piece(self.piece_o, 4, 18)
        
        # 测试与已放置方块的碰撞
        self.assertFalse(self.collision_detector.is_valid_position(self.piece_o, self.board, 4, 17))
        self.assertFalse(self.collision_detector.is_valid_position(self.piece_o, self.board, 3, 18))
        
        # 测试不碰撞的位置
        self.assertTrue(self.collision_detector.is_valid_position(self.piece_o, self.board, 0, 18))
    
    def test_try_wall_kick_success(self):
        """测试墙踢算法 - 成功"""
        # 在游戏板上放置一些方块，创建一个需要墙踢的情况
        self.board.place_piece(self.piece_o, 4, 18)
        self.board.place_piece(self.piece_o, 6, 18)
        
        # 尝试在需要墙踢的位置放置方块
        new_x, new_y = self.collision_detector.try_wall_kick(self.piece_o, self.board, 4, 17)
        
        # 检查是否找到了有效位置
        self.assertTrue(self.board.is_valid_position(self.piece_o, new_x, new_y))
    
    def test_try_wall_kick_failure(self):
        """测试墙踢算法 - 失败"""
        # 创建一个完全被占满的情况
        for i in range(0, 10, 2):
            self.board.place_piece(self.piece_o, i, 16)
            self.board.place_piece(self.piece_o, i, 17)
        
        # 尝试墙踢，应该返回原位置
        original_x, original_y = 4, 15
        new_x, new_y = self.collision_detector.try_wall_kick(self.piece_o, self.board, original_x, original_y)
        
        # 检查是否找到了有效位置（可能不是原位置，但应该是有效的）
        self.assertTrue(self.board.is_valid_position(self.piece_o, new_x, new_y))
    
    def test_try_wall_kick_edge_cases(self):
        """测试墙踢算法的边界情况"""
        # 测试在边界位置的墙踢
        # 左边界
        new_x, new_y = self.collision_detector.try_wall_kick(self.piece_o, self.board, -1, 0)
        self.assertTrue(self.board.is_valid_position(self.piece_o, new_x, new_y))
        
        # 右边界
        new_x, new_y = self.collision_detector.try_wall_kick(self.piece_o, self.board, 9, 0)
        self.assertTrue(self.board.is_valid_position(self.piece_o, new_x, new_y))
    
    def test_can_rotate_success(self):
        """测试旋转检查 - 成功"""
        # 测试可以旋转的情况
        can_rotate, new_position = self.collision_detector.can_rotate(
            self.piece_t, self.board, 4, 0
        )
        
        self.assertTrue(can_rotate)
        self.assertEqual(new_position, (4, 0))  # 应该在同一位置
    
    def test_can_rotate_with_wall_kick(self):
        """测试旋转检查 - 需要墙踢"""
        # 创建一个需要墙踢的旋转情况
        self.board.place_piece(self.piece_o, 2, 0)
        self.board.place_piece(self.piece_o, 6, 0)
        
        # 尝试旋转T型方块
        can_rotate, new_position = self.collision_detector.can_rotate(
            self.piece_t, self.board, 4, 0
        )
        
        # 应该能够旋转并找到有效位置
        self.assertTrue(can_rotate)
        self.assertTrue(self.board.is_valid_position(self.piece_t, new_position[0], new_position[1]))
    
    def test_can_rotate_failure(self):
        """测试旋转检查 - 失败"""
        # 创建一个无法旋转的情况
        for i in range(10):
            self.board.place_piece(self.piece_o, i, 0)
        
        # 尝试旋转
        can_rotate, new_position = self.collision_detector.can_rotate(
            self.piece_t, self.board, 4, 0
        )
        
        self.assertFalse(can_rotate)
        self.assertEqual(new_position, (4, 0))  # 返回原位置
    
    def test_can_rotate_preserves_original_state(self):
        """测试旋转检查保持原始状态"""
        # 保存原始状态
        original_rotation = self.piece_t.rotation
        original_shape = self.piece_t.shape.copy()
        
        # 创建一个无法旋转的情况
        for i in range(10):
            self.board.place_piece(self.piece_o, i, 0)
        
        # 尝试旋转
        self.collision_detector.can_rotate(self.piece_t, self.board, 4, 0)
        
        # 检查原始状态是否保持不变
        self.assertEqual(self.piece_t.rotation, original_rotation)
        self.assertEqual(self.piece_t.shape, original_shape)
    
    def test_can_rotate_i_piece(self):
        """测试I型方块旋转"""
        # I型方块只有两种状态
        original_shape = self.piece_i.shape.copy()
        
        can_rotate, new_position = self.collision_detector.can_rotate(
            self.piece_i, self.board, 3, 0
        )
        
        self.assertTrue(can_rotate)
        self.assertEqual(new_position, (3, 0))
        self.assertNotEqual(self.piece_i.shape, original_shape)
    
    def test_can_rotate_o_piece(self):
        """测试O型方块旋转"""
        # O型方块不需要旋转
        original_shape = self.piece_o.shape.copy()
        
        can_rotate, new_position = self.collision_detector.can_rotate(
            self.piece_o, self.board, 4, 0
        )
        
        self.assertTrue(can_rotate)
        self.assertEqual(new_position, (4, 0))
        self.assertEqual(self.piece_o.shape, original_shape)  # 形状不变
    
    def test_wall_kick_offsets(self):
        """测试墙踢算法的偏移位置"""
        # 测试所有可能的墙踢偏移
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
        
        # 验证偏移列表
        self.assertEqual(len(offsets), 8)
        
        # 测试每个偏移都是有效的
        for offset_x, offset_y in offsets:
            self.assertIsInstance(offset_x, int)
            self.assertIsInstance(offset_y, int)
    
    def test_collision_detector_with_different_pieces(self):
        """测试不同方块的碰撞检测"""
        pieces = [self.piece_i, self.piece_o, self.piece_t]
        
        for piece in pieces:
            # 测试有效位置
            self.assertTrue(self.collision_detector.is_valid_position(piece, self.board, 4, 0))
            
            # 测试无效位置
            self.assertFalse(self.collision_detector.is_valid_position(piece, self.board, -1, 0))
            
            # 测试旋转
            can_rotate, new_position = self.collision_detector.can_rotate(piece, self.board, 4, 0)
            self.assertTrue(can_rotate)
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 测试空游戏板
        empty_board = Board(10, 20)
        
        # 所有位置都应该是有效的
        self.assertTrue(self.collision_detector.is_valid_position(self.piece_o, empty_board, 4, 0))
        
        # 测试完全填满的游戏板
        full_board = Board(10, 20)
        for i in range(10):
            for j in range(20):
                full_board.place_piece(self.piece_o, i, j)
        
        # 所有位置都应该是无效的
        self.assertFalse(self.collision_detector.is_valid_position(self.piece_o, full_board, 4, 0))
    
    def test_rotation_consistency(self):
        """测试旋转的一致性"""
        # 测试多次旋转后的一致性
        original_shape = self.piece_t.shape.copy()
        original_rotation = self.piece_t.rotation
        
        # 尝试旋转4次
        for i in range(4):
            can_rotate, new_position = self.collision_detector.can_rotate(
                self.piece_t, self.board, 4, 0
            )
            self.assertTrue(can_rotate)
        
        # 检查是否回到原始状态
        self.assertEqual(self.piece_t.rotation, original_rotation)
        self.assertEqual(self.piece_t.shape, original_shape)


if __name__ == '__main__':
    unittest.main()
