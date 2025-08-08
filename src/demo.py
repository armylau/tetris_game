#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏演示脚本
展示游戏的核心功能和特性
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_piece_creation():
    """演示方块创建功能"""
    print("🎮 俄罗斯方块游戏演示")
    print("=" * 50)
    
    from tetris_main import Piece, PIECE_SHAPES, PIECE_COLORS
    
    print("1. 方块创建演示")
    print("-" * 30)
    
    for piece_type in PIECE_SHAPES.keys():
        piece = Piece(piece_type)
        print(f"✓ {piece_type} 方块:")
        print(f"  颜色: {piece.color}")
        print(f"  形状: {piece.shape}")
        print(f"  尺寸: {piece.get_width()}x{piece.get_height()}")
        print()

def demo_board_operations():
    """演示游戏板操作"""
    print("2. 游戏板操作演示")
    print("-" * 30)
    
    from tetris_main import Board, Piece
    
    board = Board()
    piece = Piece('I')
    
    print("✓ 创建游戏板 (10x20)")
    print("✓ 放置方块到位置 (3, 0)")
    board.place_piece(piece, 3, 0)
    
    # 显示游戏板状态
    print("✓ 游戏板状态:")
    for row in range(min(5, board.height)):  # 只显示前5行
        row_str = ""
        for col in range(board.width):
            if board.grid[row][col]:
                row_str += "█"
            else:
                row_str += "□"
        print(f"  行{row}: {row_str}")
    print()

def demo_rotation():
    """演示方块旋转"""
    print("3. 方块旋转演示")
    print("-" * 30)
    
    from tetris_main import Piece
    
    piece = Piece('T')
    print(f"✓ T型方块初始形状: {piece.shape}")
    
    piece.rotate()
    print(f"✓ 旋转后形状: {piece.shape}")
    
    piece.rotate()
    print(f"✓ 再次旋转: {piece.shape}")
    print()

def demo_scoring():
    """演示得分系统"""
    print("4. 得分系统演示")
    print("-" * 30)
    
    from tetris_main import GameState
    
    game_state = GameState()
    
    print("✓ 初始分数: 0")
    game_state.update_score(1)
    print(f"✓ 消除1行后: {game_state.score}")
    
    game_state.update_score(4)
    print(f"✓ 消除4行后: {game_state.score}")
    
    game_state.lines_cleared = 10
    game_state.update_level()
    print(f"✓ 当前等级: {game_state.level}")
    print()

def demo_collision_detection():
    """演示碰撞检测"""
    print("5. 碰撞检测演示")
    print("-" * 30)
    
    from tetris_main import Board, Piece
    
    board = Board()
    piece = Piece('I')
    
    print("✓ 边界检测:")
    print(f"  左边界 (-1, 0): {'无效' if not board.is_valid_position(piece, -1, 0) else '有效'}")
    print(f"  右边界 (7, 0): {'无效' if not board.is_valid_position(piece, 7, 0) else '有效'}")
    print(f"  正常位置 (3, 0): {'有效' if board.is_valid_position(piece, 3, 0) else '无效'}")
    
    # 测试方块间碰撞
    board.place_piece(piece, 3, 18)
    new_piece = Piece('I')
    print(f"✓ 方块间碰撞检测: {'无效' if not board.is_valid_position(new_piece, 3, 18) else '有效'}")
    print()

def demo_game_features():
    """演示游戏特性"""
    print("6. 游戏特性演示")
    print("-" * 30)
    
    print("✓ 支持的操作:")
    print("  - 方向键左右: 移动方块")
    print("  - 方向键下: 快速下落")
    print("  - 空格键/上方向键: 旋转方块")
    print("  - P键: 暂停/继续游戏")
    print("  - R键: 重新开始游戏")
    print("  - ESC键: 退出游戏")
    print()
    
    print("✓ 游戏特性:")
    print("  - 7种经典方块形状")
    print("  - 智能碰撞检测")
    print("  - 行消除系统")
    print("  - 动态速度调整")
    print("  - 实时分数显示")
    print("  - 下一个方块预览")
    print()

def run_demo():
    """运行完整演示"""
    try:
        demo_piece_creation()
        demo_board_operations()
        demo_rotation()
        demo_scoring()
        demo_collision_detection()
        demo_game_features()
        
        print("🎉 演示完成！")
        print("\n要开始游戏，请运行:")
        print("python tetris_main.py")
        print("\n要运行测试，请运行:")
        print("python test_tetris.py")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_demo()
