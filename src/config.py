#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏配置类
管理所有可调参数
"""

class GameConfig:
    """游戏配置类"""
    
    # 屏幕配置
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 700
    
    # 游戏板配置
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    CELL_SIZE = 30
    BOARD_X = 200
    BOARD_Y = 50
    
    # 按键配置
    KEY_REPEAT_DELAY = 100      # 按键重复延迟（毫秒）- 从150减少到100
    KEY_REPEAT_INTERVAL = 30    # 按键重复间隔（毫秒）- 从50减少到30
    DOWN_KEY_HOLD_DELAY = 200   # 向下键长按延迟（毫秒）- 从300减少到200
    
    # 向下键加速配置
    DOWN_KEY_ACCELERATION_START = 500   # 开始加速的时间（毫秒）
    DOWN_KEY_ACCELERATION_MAX = 2000    # 最大加速时间（毫秒）
    DOWN_KEY_MIN_INTERVAL = 10          # 最小下落间隔（毫秒）
    DOWN_KEY_MAX_INTERVAL = 100         # 最大下落间隔（毫秒）
    
    # 游戏速度配置
    BASE_DROP_DELAY = 1000      # 基础下落延迟（毫秒）
    LEVEL_SPEED_INCREASE = 50   # 每级速度增加（毫秒）
    MIN_DROP_DELAY = 100        # 最小下落延迟（毫秒）
    
    # 得分配置
    SCORE_BASE = {
        1: 100,   # 单行
        2: 300,   # 双行
        3: 500,   # 三行
        4: 800    # 四行
    }
    LEVEL_BONUS_MULTIPLIER = 10  # 等级奖励倍数
    COMBO_BONUS = 50            # 连击奖励
    
    # 等级配置
    LINES_PER_LEVEL = 10        # 每消除多少行升一级
    MAX_LEVEL = 20              # 最大等级
    
    # 性能配置
    TARGET_FPS = 60             # 目标帧率
    MAX_MEMORY_USAGE = 100      # 最大内存使用（MB）
    
    @classmethod
    def get_drop_delay(cls, level: int) -> int:
        """根据等级计算下落延迟"""
        delay = cls.BASE_DROP_DELAY - (level - 1) * cls.LEVEL_SPEED_INCREASE
        return max(delay, cls.MIN_DROP_DELAY)
    
    @classmethod
    def get_score(cls, lines_cleared: int, level: int, combo: int = 0) -> int:
        """计算得分"""
        base_score = cls.SCORE_BASE.get(lines_cleared, 0)
        level_bonus = level * cls.LEVEL_BONUS_MULTIPLIER
        combo_bonus = combo * cls.COMBO_BONUS
        return base_score + level_bonus + combo_bonus
    
    @classmethod
    def get_level(cls, lines_cleared: int) -> int:
        """根据消除行数计算等级"""
        return min((lines_cleared // cls.LINES_PER_LEVEL) + 1, cls.MAX_LEVEL)
