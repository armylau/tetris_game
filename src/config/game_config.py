#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏配置类
"""

class GameConfig:
    """游戏配置类 - 集中管理游戏配置"""
    
    # 屏幕配置
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    # 游戏板配置
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    CELL_SIZE = 30
    BOARD_X = 200
    BOARD_Y = 50
    
    # 游戏参数
    TARGET_FPS = 60
    KEY_REPEAT_DELAY = 200
    KEY_REPEAT_INTERVAL = 50
    DOWN_KEY_HOLD_DELAY = 100
    DOWN_KEY_ACCELERATION_START = 500
    DOWN_KEY_ACCELERATION_MAX = 2000
    DOWN_KEY_MIN_INTERVAL = 50
    DOWN_KEY_MAX_INTERVAL = 200
    
    @classmethod
    def get_score(cls, lines_cleared: int, level: int) -> int:
        """计算分数"""
        # 计算分数的规则如下：
        # - 消除1行：100分
        # - 消除2行：300分
        # - 消除3行：500分
        # - 消除4行（四连消/“Tetris”）：800分
        # 分数会乘以当前等级（level），等级越高得分越高
        # 若一次消除的行数不在1~4之间，则得分为0
        base_scores = {1: 100, 2: 300, 3: 500, 4: 800}
        return base_scores.get(lines_cleared, 0) * level
    
    @classmethod
    def get_level(cls, lines_cleared: int) -> int:
        """计算等级"""
        return (lines_cleared // 10) + 1
    
    @classmethod
    def get_drop_delay(cls, level: int) -> int:
        """计算下落延迟（毫秒）"""
        # 等级越高，下落速度越快
        # 根据当前等级计算方块自动下落的延迟（单位：毫秒）
        # 等级越高，下落速度越快，最低为原始速度的10%
        # 例如：
        #   level=1 时，delay=1000ms
        #   level=2 时，delay=900ms
        #   level=3 时，delay=800ms
        #   ...
        #   level>=10 时，delay=100ms（不再继续减少）
        base_delay = 1000
        level_factor = max(0.1, 1.0 - (level - 1) * 0.1)
        return int(base_delay * level_factor)
