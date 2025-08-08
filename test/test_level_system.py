#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试关卡系统功能
"""

import pygame
import time
import sys
from level_manager import LevelManager
from level_config import LevelConfig

def test_level_manager():
    """测试关卡管理器"""
    print("测试关卡管理器...")
    
    # 创建关卡管理器
    manager = LevelManager()
    
    # 测试关卡配置
    print(f"总关卡数: {LevelConfig.get_total_levels()}")
    
    # 测试关卡加载
    for level_id in range(1, 6):  # 测试前5关
        config = LevelConfig.get_level_config(level_id)
        if config:
            print(f"关卡 {level_id}: {config['name']}")
            print(f"  目标行数: {config['target_lines']}")
            print(f"  速度倍数: {config['speed_multiplier']}")
            print(f"  可用方块: {config['piece_types']}")
            print(f"  特殊规则: {config['special_rules']}")
            print()
    
    # 测试关卡解锁
    print("测试关卡解锁:")
    for level_id in range(1, 6):
        unlocked = manager.is_level_unlocked(level_id)
        print(f"关卡 {level_id}: {'已解锁' if unlocked else '未解锁'}")
    
    # 测试关卡加载
    print("\n测试关卡加载:")
    for level_id in range(1, 4):
        success = manager.load_level(level_id)
        print(f"加载关卡 {level_id}: {'成功' if success else '失败'}")
        
        if success:
            info = manager.get_level_info()
            print(f"  关卡信息: {info['name']}")
            print(f"  目标行数: {info['target_lines']}")
            print(f"  可用方块: {info['piece_types']}")
    
    print("关卡管理器测试完成!")

def test_level_completion():
    """测试关卡完成逻辑"""
    print("\n测试关卡完成逻辑...")
    
    manager = LevelManager()
    manager.load_level(1)  # 加载第1关
    
    # 测试关卡完成检查
    test_cases = [
        (5, 1000, True),   # 达到目标行数
        (3, 1000, False),  # 未达到目标行数
        (10, 2000, True),  # 超过目标行数
    ]
    
    for lines, score, expected in test_cases:
        result = manager.check_level_complete(lines, score)
        print(f"行数: {lines}, 分数: {score}, 预期: {expected}, 实际: {result}")
    
    # 测试星级计算
    print("\n测试星级计算:")
    test_cases = [
        (5, 500, None, 1),    # 1星
        (8, 1000, None, 2),   # 2星
        (12, 1500, None, 3),  # 3星
    ]
    
    for lines, score, time_remaining, expected in test_cases:
        stars = manager.calculate_stars(lines, score, time_remaining)
        print(f"行数: {lines}, 分数: {score}, 预期星级: {expected}, 实际星级: {stars}")
    
    print("关卡完成逻辑测试完成!")

def test_special_rules():
    """测试特殊规则"""
    print("\n测试特殊规则...")
    
    manager = LevelManager()
    
    # 测试旋转限制
    manager.load_level(7)  # 旋转限制关卡
    print("测试旋转限制:")
    for i in range(5):
        violation = manager.check_rule_violation("rotate")
        print(f"旋转 {i+1}: {'违反规则' if violation else '允许'}")
        if not violation:
            manager.record_rotation()
    
    # 测试向下键加速限制
    manager.load_level(10)  # 无加速挑战关卡
    print("\n测试向下键加速限制:")
    violation = manager.check_rule_violation("down_acceleration")
    print(f"向下键加速: {'禁止' if violation else '允许'}")
    
    print("特殊规则测试完成!")

def test_progress_saving():
    """测试进度保存"""
    print("\n测试进度保存...")
    
    manager = LevelManager()
    
    # 模拟完成一些关卡
    manager.complete_level(5, 1000, 2)  # 关卡1，2星
    manager.complete_level(8, 1500, 3)  # 关卡2，3星
    
    # 获取进度摘要
    progress = manager.get_progress_summary()
    print(f"已完成关卡: {progress['completed_levels']}")
    print(f"关卡分数: {progress['level_scores']}")
    print(f"关卡星级: {progress['level_stars']}")
    print(f"总星级: {progress['total_stars']}")
    
    print("进度保存测试完成!")

if __name__ == "__main__":
    print("关卡系统功能测试")
    print("=" * 50)
    
    test_level_manager()
    test_level_completion()
    test_special_rules()
    test_progress_saving()
    
    print("\n所有测试完成!")
