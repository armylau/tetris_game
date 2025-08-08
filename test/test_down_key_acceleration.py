#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试向下键加速功能
"""

import pygame
import time
import sys
from tetris_main import TetrisGame

def test_down_key_acceleration():
    """测试向下键加速功能"""
    print("测试向下键加速功能...")
    
    # 初始化游戏
    game = TetrisGame()
    
    # 模拟向下键按下
    down_key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
    pygame.event.post(down_key_event)
    
    # 记录开始时间
    start_time = time.time()
    move_count = 0
    
    print("按住向下键，观察加速效果...")
    print("预期行为：")
    print("1. 初始0.5秒内：正常速度")
    print("2. 0.5-2秒：线性加速")
    print("3. 2秒后：最大速度")
    
    # 模拟按住向下键2.5秒
    while time.time() - start_time < 2.5:
        current_time = time.time() * 1000  # 转换为毫秒
        
        # 处理输入
        game.handle_input()
        
        # 检查是否移动了方块
        if game.game_state.piece_y > 0:
            move_count += 1
            print(f"时间: {time.time() - start_time:.2f}s, 移动次数: {move_count}")
        
        # 短暂延迟
        time.sleep(0.05)
    
    # 模拟释放向下键
    up_key_event = pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN)
    pygame.event.post(up_key_event)
    game.handle_input()
    
    print(f"测试完成！总移动次数: {move_count}")
    print("如果移动次数逐渐增加，说明加速功能正常工作。")

if __name__ == "__main__":
    test_down_key_acceleration()
