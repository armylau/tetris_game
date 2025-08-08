#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向下键功能演示
展示单击移动一格和长按加速下落的功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_down_key_functionality():
    """演示向下键功能"""
    print("🎮 向下键功能演示")
    print("=" * 50)
    
    from tetris_main import TetrisGame
    
    print("向下键功能说明:")
    print("1. 单击向下键: 方块移动一格")
    print("2. 长按向下键(>300ms): 方块加速下落")
    print("3. 长按延迟: 300毫秒（可调整）")
    print("4. 重复间隔: 50毫秒")
    print()
    
    print("技术实现:")
    print("- 单次按键处理: 在KEYDOWN事件中处理单击")
    print("- 连续按键处理: 在handle_continuous_input中处理长按")
    print("- 延迟控制: down_key_hold_delay = 300ms")
    print("- 状态跟踪: 使用keys_pressed和last_key_time")
    print()
    
    print("按键行为:")
    print("- 快速点击: 立即移动一格")
    print("- 短按(<300ms): 移动一格后停止")
    print("- 长按(>300ms): 开始加速下落")
    print("- 释放按键: 停止加速")
    print()
    
    print("要测试向下键功能，请运行:")
    print("python test_down_key.py")
    print()
    print("要开始游戏，请运行:")
    print("python tetris_main.py")

if __name__ == "__main__":
    demo_down_key_functionality()
