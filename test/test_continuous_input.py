#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试连续按键处理功能
验证按住向下键时方块加速下落
"""

import sys
import os
import pygame
import time

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_continuous_input():
    """测试连续按键处理"""
    print("测试连续按键处理功能...")
    
    from tetris_main import TetrisGame
    
    # 初始化游戏
    game = TetrisGame()
    
    print("游戏已启动，测试连续按键功能:")
    print("- 按住向下键测试加速下落")
    print("- 按住左右键测试连续移动")
    print("- 按ESC键退出测试")
    
    # 运行游戏一小段时间来测试连续按键
    start_time = time.time()
    test_duration = 15  # 测试15秒
    
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
    
    print("连续按键测试完成！")
    print("如果按住向下键时方块加速下落，说明连续按键功能正常。")
    
    pygame.quit()

if __name__ == "__main__":
    test_continuous_input()
