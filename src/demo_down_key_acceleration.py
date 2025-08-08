#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示向下键加速功能
展示新的线性加速下落功能
"""

import pygame
import sys
from tetris_main import TetrisGame

def demo_down_key_acceleration():
    """演示向下键加速功能"""
    print("向下键加速功能演示")
    print("=" * 50)
    print("操作说明：")
    print("1. 按向下键：立即下落一格")
    print("2. 按住向下键0.5秒后：开始线性加速")
    print("3. 按住向下键2秒后：达到最大速度")
    print("4. 释放向下键：恢复正常速度")
    print("=" * 50)
    
    # 初始化游戏
    game = TetrisGame()
    
    # 游戏主循环
    while game.running:
        # 处理输入
        game.handle_input()
        
        # 更新游戏状态
        game.update()
        
        # 渲染游戏
        game.render()
        
        # 控制帧率
        game.clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    demo_down_key_acceleration()
