#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试游戏输入处理
验证空格键不会导致游戏退出
"""

import sys
import os
import pygame
import time

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_input_handling():
    """测试输入处理"""
    print("测试游戏输入处理...")
    
    from tetris_main import TetrisGame
    
    # 初始化游戏
    game = TetrisGame()
    
    print("游戏已启动，测试输入处理:")
    print("- 按空格键测试旋转功能")
    print("- 按ESC键退出测试")
    print("- 按其他方向键测试移动功能")
    
    # 运行游戏一小段时间来测试输入
    start_time = time.time()
    test_duration = 10  # 测试10秒
    
    while time.time() - start_time < test_duration and game.running:
        try:
            game.handle_input()
            game.update()
            game.render()
            game.clock.tick(60)
        except Exception as e:
            print(f"测试过程中出错: {e}")
            import traceback
            traceback.print_exc()
            break
    
    print("输入测试完成！")
    print("如果游戏正常运行且空格键能旋转方块，说明输入处理正常。")
    
    pygame.quit()

if __name__ == "__main__":
    test_input_handling()
