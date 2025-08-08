#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试向下键功能
验证单击移动一格和长按加速下落的功能
"""

import sys
import os
import pygame
import time

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_down_key_functionality():
    """测试向下键功能"""
    print("测试向下键功能...")
    
    from tetris_main import TetrisGame
    
    # 初始化游戏
    game = TetrisGame()
    
    print("向下键功能测试:")
    print("1. 单击向下键: 方块移动一格")
    print("2. 长按向下键(>300ms): 方块加速下落")
    print("3. 按ESC键退出测试")
    print()
    
    print("测试说明:")
    print("- 快速点击向下键应该只移动一格")
    print("- 按住向下键超过300毫秒会触发加速")
    print("- 左右键仍然支持连续移动")
    print()
    
    # 运行游戏一小段时间来测试向下键功能
    start_time = time.time()
    test_duration = 20  # 测试20秒
    
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
    
    print("向下键功能测试完成！")
    print("如果单击向下键移动一格，长按加速下落，说明功能正常。")
    
    pygame.quit()

if __name__ == "__main__":
    test_down_key_functionality()
