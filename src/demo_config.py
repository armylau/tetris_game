#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置参数演示
展示所有可调参数和如何调整
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_config():
    """演示配置参数"""
    print("🎮 游戏配置参数演示")
    print("=" * 50)
    
    from config import GameConfig
    
    print("📋 当前配置参数:")
    print()
    
    print("🎮 按键配置:")
    print(f"  - 按键重复延迟: {GameConfig.KEY_REPEAT_DELAY}ms (原150ms)")
    print(f"  - 按键重复间隔: {GameConfig.KEY_REPEAT_INTERVAL}ms (原50ms)")
    print(f"  - 向下键长按延迟: {GameConfig.DOWN_KEY_HOLD_DELAY}ms (原300ms)")
    print()
    
    print("⚡ 游戏速度配置:")
    print(f"  - 基础下落延迟: {GameConfig.BASE_DROP_DELAY}ms")
    print(f"  - 每级速度增加: {GameConfig.LEVEL_SPEED_INCREASE}ms")
    print(f"  - 最小下落延迟: {GameConfig.MIN_DROP_DELAY}ms")
    print()
    
    print("🏆 得分配置:")
    print(f"  - 等级奖励倍数: {GameConfig.LEVEL_BONUS_MULTIPLIER}")
    print(f"  - 连击奖励: {GameConfig.COMBO_BONUS}")
    print(f"  - 基础得分: {GameConfig.SCORE_BASE}")
    print()
    
    print("📊 等级配置:")
    print(f"  - 每消除行数升一级: {GameConfig.LINES_PER_LEVEL}")
    print(f"  - 最大等级: {GameConfig.MAX_LEVEL}")
    print()
    
    print("🖥️ 屏幕配置:")
    print(f"  - 屏幕宽度: {GameConfig.SCREEN_WIDTH}")
    print(f"  - 屏幕高度: {GameConfig.SCREEN_HEIGHT}")
    print(f"  - 目标帧率: {GameConfig.TARGET_FPS}")
    print()
    
    print("🎯 游戏板配置:")
    print(f"  - 游戏板宽度: {GameConfig.BOARD_WIDTH}")
    print(f"  - 游戏板高度: {GameConfig.BOARD_HEIGHT}")
    print(f"  - 单元格大小: {GameConfig.CELL_SIZE}")
    print()
    
    print("🔧 如何调整参数:")
    print("1. 编辑 config.py 文件")
    print("2. 修改相应的配置值")
    print("3. 保存文件并重新运行游戏")
    print()
    
    print("💡 常用调整建议:")
    print("- 加快移动: 减少 KEY_REPEAT_INTERVAL")
    print("- 更快响应: 减少 KEY_REPEAT_DELAY")
    print("- 更快下落: 减少 DOWN_KEY_HOLD_DELAY")
    print("- 更快游戏: 减少 BASE_DROP_DELAY")
    print("- 更高分数: 增加 SCORE_BASE 值")
    print()
    
    print("📝 示例调整:")
    print("# 在 config.py 中修改:")
    print("KEY_REPEAT_INTERVAL = 20    # 更快的重复间隔")
    print("DOWN_KEY_HOLD_DELAY = 150   # 更快的长按响应")
    print("BASE_DROP_DELAY = 800       # 更快的下落速度")
    print()
    
    print("要应用新配置，请运行:")
    print("python tetris_main.py")

if __name__ == "__main__":
    demo_config()
