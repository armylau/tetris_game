#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连续按键处理功能演示
展示按住向下键时方块加速下落的功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_continuous_input():
    """演示连续按键处理功能"""
    print("🎮 连续按键处理功能演示")
    print("=" * 50)
    
    from tetris_main import TetrisGame
    
    print("新功能说明:")
    print("1. 按住向下键: 方块加速下落")
    print("2. 按住左右键: 方块连续移动")
    print("3. 按键重复延迟: 150毫秒")
    print("4. 按键重复间隔: 50毫秒")
    print()
    
    print("技术实现:")
    print("- 按键状态跟踪: 使用set记录按下的键")
    print("- 时间戳记录: 记录每个按键的时间")
    print("- 连续处理: 在游戏循环中处理连续按键")
    print("- 延迟控制: 防止按键过于敏感")
    print()
    
    print("游戏控制:")
    print("- 方向键左右: 移动方块（支持按住连续移动）")
    print("- 方向键下: 快速下落（支持按住加速下落）")
    print("- 空格键/上方向键: 旋转方块")
    print("- P键: 暂停/继续游戏")
    print("- R键: 重新开始游戏")
    print("- ESC键: 退出游戏")
    print()
    
    print("要测试连续按键功能，请运行:")
    print("python test_continuous_input.py")
    print()
    print("要开始游戏，请运行:")
    print("python tetris_main.py")

if __name__ == "__main__":
    demo_continuous_input()
