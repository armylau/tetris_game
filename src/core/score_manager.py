#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分数管理器 - 负责游戏分数的计算、存储和管理
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class ScoreManager:
    """分数管理器 - 负责游戏分数的计算、存储和管理"""

    def __init__(self, score_file_path: str = "scores.json"):
        """
        初始化分数管理器

        Args:
            score_file_path: 分数文件保存路径
        """
        self.score_file_path = score_file_path
        self.current_score = 0
        self.high_score = 0
        self.score_history: List[Dict] = []
        self._load_scores()

    def add_score(self, points: int, level: int = 1, lines_cleared: int = 0) -> None:
        """
        添加分数

        Args:
            points: 要添加的分数
            level: 当前关卡
            lines_cleared: 消除的行数
        """
        self.current_score += points
        if self.current_score > self.high_score:
            self.high_score = self.current_score

    def calculate_score(self, lines_cleared: int, level: int, combo: int = 0) -> int:
        """
        根据消除行数、关卡和连击计算分数

        Args:
            lines_cleared: 消除的行数
            level: 当前关卡
            combo: 连击数

        Returns:
            计算得到的分数
        """
        # 基础分数表：单行、双行、三行、四行
        base_scores = {1: 100, 2: 300, 3: 500, 4: 800}

        # 计算基础分数
        base_score = base_scores.get(lines_cleared, 0)

        # 关卡倍数
        level_multiplier = level

        # 连击奖励
        combo_bonus = combo * 50

        # 总分数
        total_score = (base_score + combo_bonus) * level_multiplier

        return total_score

    def reset_current_score(self) -> None:
        """重置当前分数"""
        self.current_score = 0

    def save_score(self, player_name: str = "Player", game_mode: str = "classic") -> None:
        """
        保存当前分数

        Args:
            player_name: 玩家名称
            game_mode: 游戏模式
        """
        score_entry = {
            "player_name": player_name,
            "score": self.current_score,
            "game_mode": game_mode,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.score_history.append(score_entry)
        self._save_scores()

    def get_high_score(self) -> int:
        """
        获取最高分数

        Returns:
            最高分数
        """
        return self.high_score

    def get_current_score(self) -> int:
        """
        获取当前分数

        Returns:
            当前分数
        """
        return self.current_score

    def get_score_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        获取分数历史记录

        Args:
            limit: 限制返回的记录数量

        Returns:
            分数历史记录列表
        """
        if limit is None:
            return self.score_history.copy()

        return sorted(
            self.score_history,
            key=lambda x: x["score"],
            reverse=True
        )[:limit]

    def get_top_scores(self, count: int = 10) -> List[Dict]:
        """
        获取前N名分数

        Args:
            count: 返回的分数数量

        Returns:
            前N名分数列表
        """
        sorted_scores = sorted(
            self.score_history,
            key=lambda x: x["score"],
            reverse=True
        )
        return sorted_scores[:count]

    def clear_history(self) -> None:
        """清空分数历史记录"""
        self.score_history.clear()
        self._save_scores()

    def _load_scores(self) -> None:
        """从文件加载分数数据"""
        if os.path.exists(self.score_file_path):
            try:
                with open(self.score_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.score_history = data.get("score_history", [])
                    self.high_score = data.get("high_score", 0)
            except (json.JSONDecodeError, FileNotFoundError):
                self.score_history = []
                self.high_score = 0
        else:
            self.score_history = []
            self.high_score = 0

    def _save_scores(self) -> None:
        """保存分数数据到文件"""
        data = {
            "score_history": self.score_history,
            "high_score": self.high_score,
            "last_updated": datetime.now().isoformat()
        }

        try:
            with open(self.score_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"保存分数失败: {e}")

    def get_statistics(self) -> Dict:
        """
        获取分数统计信息

        Returns:
            包含统计信息的字典
        """
        if not self.score_history:
            return {
                "total_games": 0,
                "average_score": 0,
                "highest_score": 0,
                "lowest_score": 0,
                "total_score": 0
            }

        scores = [entry["score"] for entry in self.score_history]

        return {
            "total_games": len(self.score_history),
            "average_score": sum(scores) / len(scores),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "total_score": sum(scores)
        }
