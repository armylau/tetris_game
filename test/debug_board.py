#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试Board类的行消除逻辑
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.board import Board
from core.piece import Piece

def debug_clear_lines():
    """调试行消除逻辑"""
    board = Board(10, 20)
    piece_i = Piece('I')
    
    print("初始网格:")
    for i, row in enumerate(board.get_grid()):
        print(f"行 {i}: {row}")
    
    print("\n放置方块...")
    # 创建一行完整的方块（使用I型方块，1x4）
    # 需要放置3个I型方块来填满10个位置：0-3, 4-7, 8-11
    success1 = board.place_piece(piece_i, 0, 19)  # 位置0-3
    success2 = board.place_piece(piece_i, 4, 19)  # 位置4-7
    success3 = board.place_piece(piece_i, 6, 19)  # 位置6-9
    print(f"在位置 (0, 19) 放置方块: {success1}")
    print(f"在位置 (4, 19) 放置方块: {success2}")
    print(f"在位置 (6, 19) 放置方块: {success3}")
    
    print("\n放置后的网格:")
    for i, row in enumerate(board.get_grid()):
        print(f"行 {i}: {row}")
    
    print("\n检查第19行是否完整:")
    row_19 = board.get_grid()[19]
    print(f"行19: {row_19}")
    print(f"所有单元格都不为None: {all(cell is not None for cell in row_19)}")
    
    print("\n执行行消除...")
    lines_cleared = board.clear_lines()
    print(f"消除的行数: {lines_cleared}")
    
    print("\n消除后的网格:")
    for i, row in enumerate(board.get_grid()):
        print(f"行 {i}: {row}")

if __name__ == '__main__':
    debug_clear_lines()
