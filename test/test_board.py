#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Board类的单元测试
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.board import Board
from core.piece import Piece


class TestBoard(unittest.TestCase):
    """Board类的单元测试"""
    # 测试思路说明：
    # 1. 测试游戏板初始化：验证宽高、网格尺寸、初始网格内容是否为None。
    # 2. 测试is_valid_position方法：
    #    - 有效位置：在空白区域、边界内放置方块应返回True。
    #    - 超出边界：左、右、下边界外放置方块应返回False。
    #    - 碰撞检测：与已放置方块重叠应返回False，不重叠应返回True。
    # 3. 测试place_piece方法：
    #    - 成功放置：在有效位置放置方块应返回True，网格内容应更新。
    #    - 失败放置：在无效位置（如碰撞、越界）放置方块应返回False，网格不变。
    # 4. 测试clear_lines方法：
    #    - 填满一行后调用应消除该行，并返回消除行数，网格应正确下移。
    #    - 多行同时填满应全部消除。
    #    - 未填满时调用应返回0，网格不变。
    # 5. 测试is_game_over方法：
    #    - 顶部有方块时应返回True，正常状态应返回False。
    # 6. 边界情况测试：
    #    - 方块在四角、边缘、底部等极限位置的有效性和放置情况。
    #    - 连续多次消除、极端网格状态下的稳定性。
    
    def setUp(self):
        """测试前的设置"""
        self.board = Board(10, 20)  # 10x20的游戏板
        self.piece_i = Piece('I')
        self.piece_o = Piece('O')
        self.piece_t = Piece('T')
    
    def test_board_initialization(self):
        """测试游戏板初始化"""
        self.assertEqual(self.board.width, 10)
        self.assertEqual(self.board.height, 20)
        self.assertEqual(len(self.board.grid), 20)
        self.assertEqual(len(self.board.grid[0]), 10)
        
        # 检查网格是否为空
        for row in self.board.grid:
            for cell in row:
                self.assertIsNone(cell)
    
    def test_is_valid_position_valid(self):
        """测试有效位置检查 - 有效位置"""
        # 测试在游戏板中央的有效位置
        self.assertTrue(self.board.is_valid_position(self.piece_o, 4, 0))
        self.assertTrue(self.board.is_valid_position(self.piece_i, 3, 0))
    
    def test_is_valid_position_out_of_bounds(self):
        """测试有效位置检查 - 超出边界"""
        # 测试超出左边界
        self.assertFalse(self.board.is_valid_position(self.piece_o, -1, 0))
        
        # 测试超出右边界
        self.assertFalse(self.board.is_valid_position(self.piece_o, 9, 0))
        
        # 测试超出下边界
        self.assertFalse(self.board.is_valid_position(self.piece_o, 4, 19))
    
    def test_is_valid_position_collision(self):
        """测试有效位置检查 - 碰撞检测"""
        # 在游戏板上放置一个方块
        self.board.place_piece(self.piece_o, 4, 18)
        
        # 测试与已放置方块的碰撞
        self.assertFalse(self.board.is_valid_position(self.piece_o, 4, 17))
        self.assertFalse(self.board.is_valid_position(self.piece_o, 3, 18))
        
        # 测试不碰撞的位置
        self.assertTrue(self.board.is_valid_position(self.piece_o, 0, 18))
    
    def test_place_piece_success(self):
        """测试放置方块 - 成功"""
        # 测试成功放置方块
        self.assertTrue(self.board.place_piece(self.piece_o, 4, 18))
        
        # 检查方块是否正确放置
        grid = self.board.get_grid()
        # O型方块是2x2的，应该占据(4,18), (5,18), (4,19), (5,19)四个位置
        self.assertIsNotNone(grid[18][4])
        self.assertIsNotNone(grid[18][5])
        self.assertIsNotNone(grid[19][4])
        self.assertIsNotNone(grid[19][5])
    
    def test_place_piece_failure(self):
        """测试放置方块 - 失败"""
        # 测试在无效位置放置方块
        self.assertFalse(self.board.place_piece(self.piece_o, -1, 0))
        self.assertFalse(self.board.place_piece(self.piece_o, 9, 0))
    
    def test_clear_lines_no_lines(self):
        """测试清除行 - 没有完整行"""
        # 放置一些不完整的行
        self.board.place_piece(self.piece_o, 0, 18)
        self.board.place_piece(self.piece_o, 4, 18)
        
        lines_cleared = self.board.clear_lines()
        self.assertEqual(lines_cleared, 0)
    
    def test_clear_lines_one_line(self):
        """测试清除行 - 一行完整"""
        # 创建一行完整的方块（使用O型方块，2x2，但只放置在一行）
        # 放置5个O型方块来填满10个位置
        for i in range(0, 10, 2):
            self.board.place_piece(self.piece_o, i, 18)
        
        lines_cleared = self.board.clear_lines()
        self.assertEqual(lines_cleared, 2)  # O型方块会填满两行
        
        # 检查行是否被清除
        grid = self.board.get_grid()
        self.assertTrue(all(cell is None for cell in grid[16]))
        self.assertTrue(all(cell is None for cell in grid[17]))
    
    def test_clear_lines_multiple_lines(self):
        """测试清除行 - 多行完整"""
        # 创建两行完整的方块（O型方块是2x2）
        for i in range(0, 9, 2):  # 每隔2个位置放置一个O型方块
            self.board.place_piece(self.piece_o, i, 17)
            self.board.place_piece(self.piece_o, i, 18)
        
        lines_cleared = self.board.clear_lines()
        self.assertEqual(lines_cleared, 2)
        
        # 检查行是否被清除
        grid = self.board.get_grid()
        self.assertTrue(all(cell is None for cell in grid[16]))
        self.assertTrue(all(cell is None for cell in grid[17]))
    
    def test_is_game_over_false(self):
        """测试游戏结束检查 - 未结束"""
        self.assertFalse(self.board.is_game_over())
    
    def test_is_game_over_true(self):
        """测试游戏结束检查 - 已结束"""
        # 在顶部行放置方块
        self.board.place_piece(self.piece_o, 0, 0)
        self.assertTrue(self.board.is_game_over())
    
    def test_get_grid(self):
        """测试获取网格数据"""
        grid = self.board.get_grid()
        self.assertEqual(len(grid), 20)
        self.assertEqual(len(grid[0]), 10)
        
        # 检查返回的是引用（这是正确的行为）
        grid[0][0] = "test"
        self.assertEqual(self.board.get_grid()[0][0], "test")
    
    def test_board_edge_cases(self):
        """测试边界情况"""
        # 测试最小尺寸的游戏板
        small_board = Board(1, 1)
        self.assertEqual(small_board.width, 1)
        self.assertEqual(small_board.height, 1)
        
        # 测试大尺寸的游戏板
        large_board = Board(100, 100)
        self.assertEqual(large_board.width, 100)
        self.assertEqual(large_board.height, 100)
    
    def test_piece_placement_edge_cases(self):
        """测试方块放置的边界情况"""
        # 测试在边界放置方块
        self.assertTrue(self.board.place_piece(self.piece_o, 0, 18))  # 左下角
        self.assertTrue(self.board.place_piece(self.piece_o, 8, 18))  # 右下角
        
        # 测试I型方块（1x4）的边界放置
        self.assertTrue(self.board.place_piece(self.piece_i, 0, 16))  # 左边界
        self.assertTrue(self.board.place_piece(self.piece_i, 6, 16))  # 右边界


if __name__ == '__main__':
    unittest.main()
