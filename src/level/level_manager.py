#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏关卡管理器
负责关卡加载、进度跟踪和特殊规则处理
"""

import pygame
import time
import json
import os
from typing import Dict, List, Optional, Tuple
from src.config.level_config import LevelConfig

class LevelManager:
    """关卡管理器"""
    
    def __init__(self):
        self.current_level_id = 1
        self.current_level_config = None
        self.completed_levels = []
        self.level_scores = {}
        self.level_stars = {}
        self.game_mode = "level"  # "level" 或 "classic"
        
        # 特殊规则状态
        self.special_rules = {}
        self.rotation_count = 0
        self.start_time = 0
        self.time_limit = None
        
        # 加载进度
        self.load_progress()
    
    def load_level(self, level_id: int) -> bool:
        """加载指定关卡"""
        config = LevelConfig.get_level_config(level_id)
        if not config:
            return False
        
        # 检查解锁条件
        if not self.is_level_unlocked(level_id):
            return False
        
        self.current_level_id = level_id
        self.current_level_config = config
        
        # 重置特殊规则状态
        self.special_rules = config.get("special_rules", {})
        self.rotation_count = 0
        self.start_time = time.time()
        self.time_limit = config.get("time_limit")
        
        return True
    
    def is_level_unlocked(self, level_id: int) -> bool:
        """检查关卡是否已解锁"""
        return LevelConfig.is_level_unlocked(level_id, self.completed_levels)
    
    def get_available_piece_types(self) -> List[str]:
        """获取当前关卡可用的方块类型"""
        if not self.current_level_config:
            return LevelConfig.ALL_PIECE_TYPES
        
        return self.current_level_config.get("piece_types", LevelConfig.ALL_PIECE_TYPES)
    
    def get_speed_multiplier(self) -> float:
        """获取当前关卡的速度倍数"""
        if not self.current_level_config:
            return 1.0
        
        return self.current_level_config.get("speed_multiplier", 1.0)
    
    def get_target_lines(self) -> int:
        """获取当前关卡的目标行数"""
        if not self.current_level_config:
            return 10
        
        return self.current_level_config.get("target_lines", 10)
    
    def check_level_complete(self, lines_cleared: int, score: int) -> bool:
        """检查关卡是否完成"""
        if not self.current_level_config:
            return False
        
        target_lines = self.get_target_lines()
        
        # 检查是否有时间限制
        if self.time_limit and self.start_time:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > self.time_limit:
                return False  # 超时失败
        
        # 检查是否达到目标行数
        return lines_cleared >= target_lines
    
    def calculate_stars(self, lines_cleared: int, score: int, time_remaining: Optional[int] = None) -> int:
        """计算星级评价"""
        if not self.current_level_config:
            return 0
        
        star_requirements = self.current_level_config.get("star_requirements", {})
        stars = 0
        
        for star_level, requirements in star_requirements.items():
            if self._check_star_requirement(star_level, lines_cleared, score, time_remaining):
                stars = star_level
            else:
                break
        
        return stars
    
    def _check_star_requirement(self, star_level: int, lines_cleared: int, score: int, time_remaining: Optional[int]) -> bool:
        """检查是否满足星级要求"""
        if not self.current_level_config:
            return False
        
        star_requirements = self.current_level_config.get("star_requirements", {})
        requirements = star_requirements.get(star_level, {})
        
        # 检查行数要求
        if "lines" in requirements and lines_cleared < requirements["lines"]:
            return False
        
        # 检查分数要求
        if "score" in requirements and score < requirements["score"]:
            return False
        
        # 检查时间要求
        if "time_remaining" in requirements and time_remaining is not None:
            if time_remaining < requirements["time_remaining"]:
                return False
        
        return True
    
    def check_rule_violation(self, action: str) -> bool:
        """检查是否违反特殊规则"""
        if not self.special_rules:
            return False
        
        # 检查旋转限制
        if action == "rotate" and "max_rotations" in self.special_rules:
            max_rotations = self.special_rules["max_rotations"]
            if self.rotation_count >= max_rotations:
                return True
        
        # 检查向下键加速限制
        if action == "down_acceleration" and self.special_rules.get("disable_down_acceleration", False):
            return True
        
        return False
    
    def record_rotation(self):
        """记录旋转次数"""
        self.rotation_count += 1
    
    def get_time_remaining(self) -> Optional[int]:
        """获取剩余时间（秒）"""
        if not self.time_limit or not self.start_time:
            return None
        
        elapsed = time.time() - self.start_time
        remaining = self.time_limit - elapsed
        return max(0, int(remaining))
    
    def is_time_up(self) -> bool:
        """检查是否时间到"""
        if not self.time_limit:
            return False
        
        return self.get_time_remaining() <= 0
    
    def complete_level(self, lines_cleared: int, score: int, stars: int):
        """完成关卡"""
        if self.current_level_id not in self.completed_levels:
            self.completed_levels.append(self.current_level_id)
        
        # 更新最高分
        if self.current_level_id not in self.level_scores or score > self.level_scores[self.current_level_id]:
            self.level_scores[self.current_level_id] = score
        
        # 更新最高星级
        if self.current_level_id not in self.level_stars or stars > self.level_stars[self.current_level_id]:
            self.level_stars[self.current_level_id] = stars
        
        # 保存进度
        self.save_progress()
    
    def get_level_info(self) -> Dict:
        """获取当前关卡信息"""
        if not self.current_level_config:
            return {}
        
        return {
            "id": self.current_level_id,
            "name": self.current_level_config.get("name", ""),
            "description": self.current_level_config.get("description", ""),
            "target_lines": self.get_target_lines(),
            "time_limit": self.time_limit,
            "speed_multiplier": self.get_speed_multiplier(),
            "piece_types": self.get_available_piece_types(),
            "special_rules": self.special_rules
        }
    
    def get_progress_summary(self) -> Dict:
        """获取进度摘要"""
        return {
            "completed_levels": self.completed_levels,
            "level_scores": self.level_scores,
            "level_stars": self.level_stars,
            "total_levels": LevelConfig.get_total_levels(),
            "total_stars": sum(self.level_stars.values())
        }
    
    def save_progress(self):
        """保存进度到文件"""
        progress_data = {
            "completed_levels": self.completed_levels,
            "level_scores": self.level_scores,
            "level_stars": self.level_stars,
            "game_mode": self.game_mode
        }
        
        try:
            with open("level_progress.json", "w", encoding="utf-8") as f:
                json.dump(progress_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存进度失败: {e}")
    
    def load_progress(self):
        """从文件加载进度"""
        try:
            if os.path.exists("level_progress.json"):
                with open("level_progress.json", "r", encoding="utf-8") as f:
                    progress_data = json.load(f)
                
                self.completed_levels = progress_data.get("completed_levels", [])
                self.level_scores = progress_data.get("level_scores", {})
                self.level_stars = progress_data.get("level_stars", {})
                self.game_mode = progress_data.get("game_mode", "level")
        except Exception as e:
            print(f"加载进度失败: {e}")
    
    def reset_progress(self):
        """重置所有进度"""
        self.completed_levels = []
        self.level_scores = {}
        self.level_stars = {}
        self.current_level_id = 1
        self.save_progress()
    
    def get_next_unlocked_level(self) -> Optional[int]:
        """获取下一个可解锁的关卡"""
        for level_id in range(1, LevelConfig.get_total_levels() + 1):
            if self.is_level_unlocked(level_id) and level_id not in self.completed_levels:
                return level_id
        return None
