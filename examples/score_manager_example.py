#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ScoreManager类使用示例
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.score_manager import ScoreManager


def main():
    """主函数 - 演示ScoreManager的使用"""
    print("=== ScoreManager 使用示例 ===\n")
    
    # 创建分数管理器实例
    score_manager = ScoreManager("example_scores.json")
    
    # 演示分数计算
    print("1. 分数计算示例:")
    print(f"   单行消除 (关卡1): {score_manager.calculate_score(1, 1)} 分")
    print(f"   双行消除 (关卡2): {score_manager.calculate_score(2, 2)} 分")
    print(f"   四行消除 (关卡3, 连击2): {score_manager.calculate_score(4, 3, 2)} 分")
    print()
    
    # 演示添加分数
    print("2. 添加分数示例:")
    score_manager.add_score(100)
    print(f"   当前分数: {score_manager.get_current_score()}")
    print(f"   最高分数: {score_manager.get_high_score()}")
    
    score_manager.add_score(200)
    print(f"   添加200分后 - 当前分数: {score_manager.get_current_score()}")
    print(f"   最高分数: {score_manager.get_high_score()}")
    print()
    
    # 演示保存分数
    print("3. 保存分数示例:")
    score_manager.save_score("玩家A", "classic")
    score_manager.reset_current_score()
    
    score_manager.add_score(500)
    score_manager.save_score("玩家B", "level")
    score_manager.reset_current_score()
    
    score_manager.add_score(300)
    score_manager.save_score("玩家C", "classic")
    print(f"   已保存 {len(score_manager.get_score_history())} 个分数记录")
    print()
    
    # 演示获取分数历史
    print("4. 分数历史记录:")
    history = score_manager.get_score_history()
    for i, record in enumerate(history, 1):
        print(f"   {i}. {record['player_name']}: {record['score']} 分 "
              f"({record['game_mode']}) - {record['date']}")
    print()
    
    # 演示获取前N名分数
    print("5. 前3名分数:")
    top_scores = score_manager.get_top_scores(3)
    for i, record in enumerate(top_scores, 1):
        print(f"   {i}. {record['player_name']}: {record['score']} 分")
    print()
    
    # 演示统计信息
    print("6. 统计信息:")
    stats = score_manager.get_statistics()
    print(f"   总游戏次数: {stats['total_games']}")
    print(f"   平均分数: {stats['average_score']:.1f}")
    print(f"   最高分数: {stats['highest_score']}")
    print(f"   最低分数: {stats['lowest_score']}")
    print(f"   总分数: {stats['total_score']}")
    print()
    
    print("=== 示例完成 ===")


if __name__ == "__main__":
    main()
