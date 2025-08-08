#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试游戏板渲染功能
验证底部行是否正确显示
"""

import sys
import os
import pygame

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_board_rendering():
    """测试游戏板渲染"""
    print("测试游戏板渲染...")
    
    from tetris_main import Board, Piece, Renderer, SCREEN_WIDTH, SCREEN_HEIGHT
    
    # 初始化Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("渲染测试")
    
    # 创建游戏板和渲染器
    board = Board()
    renderer = Renderer(screen)
    
    # 在底部放置一些方块来测试渲染
    print("在游戏板底部放置方块...")
    
    # 放置I型方块在底部
    piece1 = Piece('I')
    board.place_piece(piece1, 0, 18)  # 最底部
    
    # 放置O型方块在倒数第二行
    piece2 = Piece('O')
    board.place_piece(piece2, 3, 17)
    
    # 放置T型方块在倒数第三行
    piece3 = Piece('T')
    board.place_piece(piece3, 6, 16)
    
    # 渲染游戏板
    screen.fill((0, 0, 0))  # 黑色背景
    renderer.render_board(board)
    
    # 显示游戏板信息
    print(f"游戏板尺寸: {board.width}x{board.height}")
    print(f"屏幕尺寸: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"游戏板位置: ({200}, {50})")
    print(f"游戏板底部Y坐标: {50 + 20 * 30}")
    
    # 检查底部几行的状态
    print("\n底部5行的状态:")
    for row in range(15, 20):
        row_str = ""
        for col in range(board.width):
            if board.grid[row][col]:
                row_str += "█"
            else:
                row_str += "□"
        print(f"行{row}: {row_str}")
    
    # 更新显示
    pygame.display.flip()
    
    print("\n渲染测试完成！")
    print("如果能看到完整的游戏板，包括底部的方块，说明渲染正常。")
    print("按任意键退出...")
    
    # 等待用户按键
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    test_board_rendering()
