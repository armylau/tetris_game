#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏关卡配置
定义所有关卡的参数和规则
"""

from typing import Dict, List, Optional

class LevelConfig:
    """关卡配置类"""
    
    # 所有方块类型
    ALL_PIECE_TYPES = ["I", "O", "T", "S", "Z", "J", "L"]
    
    # 关卡配置数据
    LEVELS = {
        1: {
            "name": "Beginner",
            "description": "Learn basic operations and game rules",
            "target_lines": 5,
            "time_limit": None,
            "speed_multiplier": 0.8,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {},
            "unlock_condition": "none",
            "star_requirements": {
                1: {"lines": 5, "score": 500},
                2: {"lines": 8, "score": 1000},
                3: {"lines": 12, "score": 1500}
            }
        },
        
        2: {
            "name": "Basic Practice",
            "description": "Improve operation proficiency",
            "target_lines": 8,
            "time_limit": None,
            "speed_multiplier": 0.9,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {},
            "unlock_condition": "complete_level_1",
            "star_requirements": {
                1: {"lines": 8, "score": 800},
                2: {"lines": 12, "score": 1500},
                3: {"lines": 18, "score": 2500}
            }
        },
        
        3: {
            "name": "Speed Up",
            "description": "Adapt to faster falling speed",
            "target_lines": 10,
            "time_limit": None,
            "speed_multiplier": 1.0,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {},
            "unlock_condition": "complete_level_2",
            "star_requirements": {
                1: {"lines": 10, "score": 1000},
                2: {"lines": 15, "score": 2000},
                3: {"lines": 22, "score": 3500}
            }
        },
        
        4: {
            "name": "Quick Reaction",
            "description": "Train quick reaction ability",
            "target_lines": 12,
            "time_limit": None,
            "speed_multiplier": 1.2,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {},
            "unlock_condition": "complete_level_3",
            "star_requirements": {
                1: {"lines": 12, "score": 1200},
                2: {"lines": 18, "score": 2500},
                3: {"lines": 25, "score": 4000}
            }
        },
        
        5: {
            "name": "Intermediate Challenge",
            "description": "Challenge medium difficulty",
            "target_lines": 15,
            "time_limit": None,
            "speed_multiplier": 1.4,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {},
            "unlock_condition": "complete_level_4",
            "star_requirements": {
                1: {"lines": 15, "score": 1500},
                2: {"lines": 22, "score": 3000},
                3: {"lines": 30, "score": 5000}
            }
        },
        
        6: {
            "name": "Piece Restriction",
            "description": "Disable some piece types to increase challenge",
            "target_lines": 15,
            "time_limit": None,
            "speed_multiplier": 1.5,
            "piece_types": ["I", "O", "T", "S", "Z"],  # 禁用J和L
            "special_rules": {},
            "unlock_condition": "complete_level_5",
            "star_requirements": {
                1: {"lines": 15, "score": 1500},
                2: {"lines": 22, "score": 3000},
                3: {"lines": 30, "score": 5000}
            }
        },
        
        7: {
            "name": "Rotation Limit",
            "description": "Each piece can only rotate once",
            "target_lines": 15,
            "time_limit": None,
            "speed_multiplier": 1.6,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {"max_rotations": 1},
            "unlock_condition": "complete_level_6",
            "star_requirements": {
                1: {"lines": 15, "score": 1500},
                2: {"lines": 22, "score": 3000},
                3: {"lines": 30, "score": 5000}
            }
        },
        
        8: {
            "name": "High Speed Mode",
            "description": "Experience high-speed falling",
            "target_lines": 18,
            "time_limit": None,
            "speed_multiplier": 1.8,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {},
            "unlock_condition": "complete_level_7",
            "star_requirements": {
                1: {"lines": 18, "score": 1800},
                2: {"lines": 25, "score": 3500},
                3: {"lines": 35, "score": 6000}
            }
        },
        
        9: {
            "name": "Precise Control",
            "description": "Train precise piece placement",
            "target_lines": 18,
            "time_limit": None,
            "speed_multiplier": 1.7,
            "piece_types": ["I", "T", "S", "Z"],  # 只允许直线和曲线方块
            "special_rules": {},
            "unlock_condition": "complete_level_8",
            "star_requirements": {
                1: {"lines": 18, "score": 1800},
                2: {"lines": 25, "score": 3500},
                3: {"lines": 35, "score": 6000}
            }
        },
        
        10: {
            "name": "No Acceleration Challenge",
            "description": "Cannot use down key to accelerate",
            "target_lines": 20,
            "time_limit": None,
            "speed_multiplier": 1.9,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {"disable_down_acceleration": True},
            "unlock_condition": "complete_level_9",
            "star_requirements": {
                1: {"lines": 20, "score": 2000},
                2: {"lines": 28, "score": 4000},
                3: {"lines": 38, "score": 7000}
            }
        },
        
        11: {
            "name": "Time Challenge",
            "description": "Complete tasks within time limit",
            "target_lines": 15,
            "time_limit": 120,  # 2分钟
            "speed_multiplier": 2.0,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {"time_limit": True},
            "unlock_condition": "complete_level_10",
            "star_requirements": {
                1: {"lines": 15, "time_remaining": 30},
                2: {"lines": 20, "time_remaining": 60},
                3: {"lines": 25, "time_remaining": 90}
            }
        },
        
        12: {
            "name": "Ultra Speed Mode",
            "description": "Experience ultra-speed falling",
            "target_lines": 20,
            "time_limit": None,
            "speed_multiplier": 2.2,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {},
            "unlock_condition": "complete_level_11",
            "star_requirements": {
                1: {"lines": 20, "score": 2000},
                2: {"lines": 28, "score": 4000},
                3: {"lines": 38, "score": 7000}
            }
        },
        
        13: {
            "name": "Specific Target",
            "description": "Must clear specific number of lines to pass",
            "target_lines": 25,
            "time_limit": None,
            "speed_multiplier": 2.0,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {"exact_lines_required": True},
            "unlock_condition": "complete_level_12",
            "star_requirements": {
                1: {"lines": 25, "score": 2500},
                2: {"lines": 32, "score": 4500},
                3: {"lines": 40, "score": 7500}
            }
        },
        
        14: {
            "name": "Piece Master",
            "description": "Only allow specific piece types",
            "target_lines": 22,
            "time_limit": None,
            "speed_multiplier": 2.1,
            "piece_types": ["I", "O"],  # 只允许I和O方块
            "special_rules": {},
            "unlock_condition": "complete_level_13",
            "star_requirements": {
                1: {"lines": 22, "score": 2200},
                2: {"lines": 30, "score": 4500},
                3: {"lines": 38, "score": 7500}
            }
        },
        
        15: {
            "name": "Advanced Challenge",
            "description": "Comprehensive challenge mode",
            "target_lines": 25,
            "time_limit": None,
            "speed_multiplier": 2.3,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {"max_rotations": 2},
            "unlock_condition": "complete_level_14",
            "star_requirements": {
                1: {"lines": 25, "score": 2500},
                2: {"lines": 32, "score": 5000},
                3: {"lines": 40, "score": 8000}
            }
        },
        
        16: {
            "name": "Time Master",
            "description": "Complete tasks in very short time",
            "target_lines": 20,
            "time_limit": 90,  # 1.5分钟
            "speed_multiplier": 2.5,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {"time_limit": True},
            "unlock_condition": "complete_level_15",
            "star_requirements": {
                1: {"lines": 20, "time_remaining": 20},
                2: {"lines": 25, "time_remaining": 45},
                3: {"lines": 30, "time_remaining": 70}
            }
        },
        
        17: {
            "name": "Reverse Controls",
            "description": "Left and right arrow keys are swapped",
            "target_lines": 20,
            "time_limit": None,
            "speed_multiplier": 2.2,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {"reverse_controls": True},
            "unlock_condition": "complete_level_16",
            "star_requirements": {
                1: {"lines": 20, "score": 2000},
                2: {"lines": 28, "score": 4000},
                3: {"lines": 35, "score": 7000}
            }
        },
        
        18: {
            "name": "Ultimate Challenge",
            "description": "Multiple restrictions ultimate challenge",
            "target_lines": 25,
            "time_limit": 120,
            "speed_multiplier": 2.4,
            "piece_types": ["I", "T", "S", "Z"],
            "special_rules": {
                "max_rotations": 1,
                "disable_down_acceleration": True,
                "time_limit": True
            },
            "unlock_condition": "complete_level_17",
            "star_requirements": {
                1: {"lines": 25, "time_remaining": 30},
                2: {"lines": 30, "time_remaining": 60},
                3: {"lines": 35, "time_remaining": 90}
            }
        },
        
        19: {
            "name": "Ultimate Challenge",
            "description": "Ultimate challenge mode",
            "target_lines": 30,
            "time_limit": None,
            "speed_multiplier": 2.6,
            "piece_types": ALL_PIECE_TYPES,
            "special_rules": {"ultimate_mode": True},
            "unlock_condition": "complete_level_18",
            "star_requirements": {
                1: {"lines": 30, "score": 3000},
                2: {"lines": 38, "score": 5500},
                3: {"lines": 45, "score": 9000}
            }
        },
        
        20: {
            "name": "Legendary Mode",
            "description": "Only true Tetris masters can pass",
            "target_lines": 35,
            "time_limit": 180,  # 3分钟
            "speed_multiplier": 3.0,
            "piece_types": ["I", "O"],
            "special_rules": {
                "max_rotations": 1,
                "disable_down_acceleration": True,
                "time_limit": True,
                "legendary_mode": True
            },
            "unlock_condition": "complete_level_19",
            "star_requirements": {
                1: {"lines": 35, "time_remaining": 60},
                2: {"lines": 40, "time_remaining": 120},
                3: {"lines": 45, "time_remaining": 150}
            }
        }
    }
    
    @classmethod
    def get_level_config(cls, level_id: int) -> Optional[Dict]:
        """获取指定关卡的配置"""
        return cls.LEVELS.get(level_id)
    
    @classmethod
    def get_total_levels(cls) -> int:
        """获取总关卡数"""
        return len(cls.LEVELS)
    
    @classmethod
    def get_unlock_condition(cls, level_id: int) -> str:
        """获取关卡的解锁条件"""
        config = cls.get_level_config(level_id)
        return config.get("unlock_condition", "none") if config else "none"
    
    @classmethod
    def get_star_requirements(cls, level_id: int) -> Dict:
        """获取关卡的星级要求"""
        config = cls.get_level_config(level_id)
        return config.get("star_requirements", {}) if config else {}
    
    @classmethod
    def is_level_unlocked(cls, level_id: int, completed_levels: List[int]) -> bool:
        """检查关卡是否已解锁"""
        if level_id == 1:
            return True
        
        config = cls.get_level_config(level_id)
        if not config:
            return False
        
        unlock_condition = config.get("unlock_condition", "none")
        if unlock_condition == "none":
            return True
        elif unlock_condition.startswith("complete_level_"):
            required_level = int(unlock_condition.split("_")[-1])
            return required_level in completed_levels
        
        return False
