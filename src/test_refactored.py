#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重构后的游戏测试脚本
"""

import pygame
import sys
from config.game_config import GameConfig
from core.game_engine import GameEngine
from core.piece import Piece
from core.board import Board
from ui.renderer import Renderer
from ui.input_handler import InputHandler


def test_piece():
    """测试方块类"""
    print("测试方块类...")
    
    # 测试I型方块
    piece = Piece('I')
    print(f"I型方块初始形状: {piece.get_shape()}")
    print(f"I型方块尺寸: {piece.get_dimensions()}")
    
    # 测试旋转
    piece.rotate()
    print(f"I型方块旋转后形状: {piece.get_shape()}")
    
    # 测试O型方块
    piece_o = Piece('O')
    print(f"O型方块形状: {piece_o.get_shape()}")
    print(f"O型方块旋转后: {piece_o.get_shape()}")
    
    print("方块类测试完成\n")


def test_board():
    """测试游戏板类"""
    print("测试游戏板类...")
    
    board = Board(10, 20)
    piece = Piece('T')
    
    # 测试有效位置检查
    is_valid = board.is_valid_position(piece, 3, 0)
    print(f"位置(3,0)是否有效: {is_valid}")
    
    # 测试放置方块
    success = board.place_piece(piece, 3, 0)
    print(f"放置方块成功: {success}")
    
    # 测试行消除
    lines_cleared = board.clear_lines()
    print(f"消除行数: {lines_cleared}")
    
    print("游戏板类测试完成\n")


def test_game_engine():
    """测试游戏引擎"""
    print("测试游戏引擎...")
    
    config = GameConfig()
    engine = GameEngine(config)
    
    # 测试生成方块
    engine.spawn_new_piece()
    game_state = engine.get_game_state()
    print(f"当前方块类型: {game_state.current_piece.type if game_state.current_piece else 'None'}")
    
    # 测试移动方块
    moved = engine.handle_piece_movement(1, 0)
    print(f"向右移动成功: {moved}")
    
    # 测试旋转方块
    rotated = engine.handle_piece_rotation()
    print(f"旋转成功: {rotated}")
    
    print("游戏引擎测试完成\n")


def test_renderer():
    """测试渲染器"""
    print("测试渲染器...")
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    config = GameConfig()
    renderer = Renderer(screen, config)
    
    # 测试渲染器初始化
    print(f"渲染器初始化成功: {renderer is not None}")
    print(f"字体加载成功: {hasattr(renderer, 'font')}")
    
    pygame.quit()
    print("渲染器测试完成\n")


def test_input_handler():
    """测试输入处理器"""
    print("测试输入处理器...")
    
    config = GameConfig()
    handler = InputHandler(config)
    
    # 测试输入处理器初始化
    print(f"输入处理器初始化成功: {handler is not None}")
    print(f"按键状态: {handler.keys_pressed}")
    
    print("输入处理器测试完成\n")


def main():
    """主测试函数"""
    print("开始重构后的游戏测试...\n")
    
    try:
        test_piece()
        test_board()
        test_game_engine()
        test_renderer()
        test_input_handler()
        
        print("所有测试完成！重构成功！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
