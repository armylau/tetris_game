#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ScoreManager类的测试文件
"""

import unittest
import tempfile
import os
import json
from datetime import datetime

# 添加src目录到Python路径
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.score_manager import ScoreManager


class TestScoreManager(unittest.TestCase):
    """ScoreManager类的测试用例"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 创建临时文件用于测试
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.score_manager = ScoreManager(self.temp_file.name)
    
    def tearDown(self):
        """测试后的清理工作"""
        # 删除临时文件
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.score_manager.current_score, 0)
        self.assertEqual(self.score_manager.high_score, 0)
        self.assertEqual(len(self.score_manager.score_history), 0)
    
    def test_add_score(self):
        """测试添加分数"""
        self.score_manager.add_score(100)
        self.assertEqual(self.score_manager.current_score, 100)
        self.assertEqual(self.score_manager.high_score, 100)
        
        # 添加更多分数
        self.score_manager.add_score(200)
        self.assertEqual(self.score_manager.current_score, 300)
        self.assertEqual(self.score_manager.high_score, 300)
    
    def test_calculate_score(self):
        """测试分数计算"""
        # 测试单行消除
        score = self.score_manager.calculate_score(1, 1)
        self.assertEqual(score, 100)
        
        # 测试双行消除
        score = self.score_manager.calculate_score(2, 2)
        self.assertEqual(score, 600)  # 300 * 2
        
        # 测试四行消除带连击
        score = self.score_manager.calculate_score(4, 3, 2)
        self.assertEqual(score, 2700)  # (800 + 100) * 3
    
    def test_reset_current_score(self):
        """测试重置当前分数"""
        self.score_manager.add_score(500)
        self.assertEqual(self.score_manager.current_score, 500)
        
        self.score_manager.reset_current_score()
        self.assertEqual(self.score_manager.current_score, 0)
        # 最高分数应该保持不变
        self.assertEqual(self.score_manager.high_score, 500)
    
    def test_save_score(self):
        """测试保存分数"""
        self.score_manager.add_score(1000)
        self.score_manager.save_score("测试玩家", "classic")
        
        self.assertEqual(len(self.score_manager.score_history), 1)
        saved_score = self.score_manager.score_history[0]
        self.assertEqual(saved_score["player_name"], "测试玩家")
        self.assertEqual(saved_score["score"], 1000)
        self.assertEqual(saved_score["game_mode"], "classic")
        self.assertIn("timestamp", saved_score)
        self.assertIn("date", saved_score)
    
    def test_get_score_history(self):
        """测试获取分数历史"""
        # 添加一些测试分数
        self.score_manager.add_score(100)
        self.score_manager.save_score("玩家1")
        self.score_manager.reset_current_score()
        
        self.score_manager.add_score(200)
        self.score_manager.save_score("玩家2")
        
        history = self.score_manager.get_score_history()
        self.assertEqual(len(history), 2)
        
        # 测试限制返回数量
        limited_history = self.score_manager.get_score_history(limit=1)
        self.assertEqual(len(limited_history), 1)
    
    def test_get_top_scores(self):
        """测试获取前N名分数"""
        # 添加多个分数
        scores = [500, 300, 800, 200, 600]
        for i, score in enumerate(scores):
            self.score_manager.add_score(score)
            self.score_manager.save_score(f"玩家{i+1}")
            self.score_manager.reset_current_score()
        
        top_scores = self.score_manager.get_top_scores(3)
        self.assertEqual(len(top_scores), 3)
        self.assertEqual(top_scores[0]["score"], 800)
        self.assertEqual(top_scores[1]["score"], 600)
        self.assertEqual(top_scores[2]["score"], 500)
    
    def test_get_statistics(self):
        """测试获取统计信息"""
        # 添加一些测试分数
        test_scores = [100, 200, 300, 400, 500]
        for i, score in enumerate(test_scores):
            self.score_manager.add_score(score)
            self.score_manager.save_score(f"玩家{i+1}")
            self.score_manager.reset_current_score()
        
        stats = self.score_manager.get_statistics()
        self.assertEqual(stats["total_games"], 5)
        self.assertEqual(stats["highest_score"], 500)
        self.assertEqual(stats["lowest_score"], 100)
        self.assertEqual(stats["average_score"], 300)
        self.assertEqual(stats["total_score"], 1500)
    
    def test_clear_history(self):
        """测试清空历史记录"""
        self.score_manager.add_score(100)
        self.score_manager.save_score("测试玩家")
        
        self.assertEqual(len(self.score_manager.score_history), 1)
        
        self.score_manager.clear_history()
        self.assertEqual(len(self.score_manager.score_history), 0)


if __name__ == '__main__':
    unittest.main()
