#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏调试脚本
帮助诊断游戏问题
"""

import sys
import os
import pygame

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_game():
    """调试游戏"""
    print("🎮 俄罗斯方块游戏调试模式")
    print("=" * 50)
    
    try:
        from tetris_main import TetrisGame, Piece, Board
        
        print("✓ 成功导入游戏模块")
        
        # 测试方块创建
        print("\n1. 测试方块创建...")
        for piece_type in ['I', 'O', 'T', 'S', 'Z', 'J', 'L']:
            piece = Piece(piece_type)
            print(f"  ✓ {piece_type} 方块: 形状={piece.shape}, 旋转={piece.rotation}")
        
        # 测试游戏板
        print("\n2. 测试游戏板...")
        board = Board()
        print(f"  ✓ 游戏板尺寸: {board.width}x{board.height}")
        
        # 测试方块旋转
        print("\n3. 测试方块旋转...")
        piece = Piece('T')
        print(f"  ✓ 初始形状: {piece.shape}")
        piece.rotate()
        print(f"  ✓ 旋转后形状: {piece.shape}")
        
        # 测试游戏初始化
        print("\n4. 测试游戏初始化...")
        game = TetrisGame()
        print(f"  ✓ 游戏状态: 分数={game.game_state.score}, 等级={game.game_state.level}")
        print(f"  ✓ 当前方块: {game.game_state.current_piece.type if game.game_state.current_piece else 'None'}")
        
        print("\n🎉 所有调试测试通过！")
        print("\n要开始游戏，请运行:")
        print("python tetris_main.py")
        
    except Exception as e:
        print(f"❌ 调试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_game()
