#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏测试文件
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_piece_creation():
    """测试方块创建"""
    print("测试方块创建...")
    
    # 导入必要的类
    from tetris_main import Piece, PIECE_SHAPES, PIECE_COLORS
    
    # 测试所有方块类型
    for piece_type in PIECE_SHAPES.keys():
        piece = Piece(piece_type)
        print(f"✓ {piece_type} 方块创建成功")
        print(f"  颜色: {piece.color}")
        print(f"  形状: {piece.shape}")
        print(f"  尺寸: {piece.get_width()}x{piece.get_height()}")
    
    print("所有方块创建测试通过！\n")

def test_board_operations():
    """测试游戏板操作"""
    print("测试游戏板操作...")
    
    from tetris_main import Board, Piece
    
    board = Board()
    piece = Piece('I')
    
    # 测试有效位置检查
    assert board.is_valid_position(piece, 3, 0) == True, "位置应该有效"
    assert board.is_valid_position(piece, -1, 0) == False, "位置应该无效（超出左边界）"
    assert board.is_valid_position(piece, 8, 0) == False, "位置应该无效（超出右边界）"
    
    # 测试方块放置
    assert board.place_piece(piece, 3, 0) == True, "方块应该能成功放置"
    
    # 测试行消除
    # 先填满一行
    for col in range(board.width):
        board.grid[board.height - 1][col] = (255, 0, 0)
    
    lines_cleared = board.clear_lines()
    assert lines_cleared == 1, f"应该消除1行，实际消除{lines_cleared}行"
    
    print("✓ 游戏板操作测试通过！\n")

def test_game_state():
    """测试游戏状态"""
    print("测试游戏状态...")
    
    from tetris_main import GameState
    
    game_state = GameState()
    
    # 测试分数更新
    game_state.update_score(1)
    assert game_state.score == 110, f"分数应该是110，实际是{game_state.score}"
    
    game_state.update_score(4)
    assert game_state.score == 920, f"分数应该是920，实际是{game_state.score}"
    
    # 测试等级更新
    game_state.lines_cleared = 10
    game_state.update_level()
    assert game_state.level == 2, f"等级应该是2，实际是{game_state.level}"
    
    print("✓ 游戏状态测试通过！\n")

def test_rotation():
    """测试方块旋转"""
    print("测试方块旋转...")
    
    from tetris_main import Piece, PIECE_SHAPES
    
    # 测试T型方块旋转
    piece = Piece('T')
    original_shape = piece.shape.copy()
    
    piece.rotate()
    assert piece.shape != original_shape, "旋转后形状应该改变"
    
    # 测试O型方块旋转（不应该改变）
    o_piece = Piece('O')
    original_o_shape = o_piece.shape.copy()
    
    o_piece.rotate()
    assert o_piece.shape == original_o_shape, "O型方块旋转后应该保持不变"
    
    print("✓ 方块旋转测试通过！\n")

def test_collision_detection():
    """测试碰撞检测"""
    print("测试碰撞检测...")
    
    from tetris_main import Board, Piece
    
    board = Board()
    piece = Piece('I')
    
    # 测试边界碰撞
    assert board.is_valid_position(piece, -1, 0) == False, "左边界碰撞检测失败"
    assert board.is_valid_position(piece, 7, 0) == False, "右边界碰撞检测失败"
    # I型方块高度为1，所以y=19时应该有效（在边界内）
    assert board.is_valid_position(piece, 3, 19) == True, "下边界检测错误 - 方块应该在边界内"
    # 测试真正的下边界碰撞
    assert board.is_valid_position(piece, 3, 20) == False, "下边界碰撞检测失败"
    
    # 测试方块间碰撞
    board.place_piece(piece, 3, 18)  # 在底部放置一个方块
    # 创建一个新的方块来测试碰撞
    new_piece = Piece('I')
    # 检查新方块是否能放在已放置方块的上方（应该可以）
    assert board.is_valid_position(new_piece, 3, 17) == True, "方块间碰撞检测错误 - 应该可以放在上方"
    # 检查新方块是否能放在已放置方块的位置（应该不可以）
    assert board.is_valid_position(new_piece, 3, 18) == False, "方块间碰撞检测失败"
    
    print("✓ 碰撞检测测试通过！\n")

def run_all_tests():
    """运行所有测试"""
    print("开始运行俄罗斯方块游戏测试...\n")
    
    try:
        test_piece_creation()
        test_board_operations()
        test_game_state()
        test_rotation()
        test_collision_detection()
        
        print("🎉 所有测试通过！游戏核心功能正常。")
        print("\n游戏控制说明:")
        print("- 方向键左右: 移动方块")
        print("- 方向键下: 快速下落")
        print("- 空格键/上方向键: 旋转方块")
        print("- P键: 暂停/继续游戏")
        print("- R键: 重新开始游戏")
        print("- ESC键: 退出游戏")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
