#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化游戏引擎 - 集成优化渲染系统和性能监控
"""

import pygame
import time
import random
from typing import Optional, List
from src.core.board import Board
from src.core.game_state import GameState
from src.core.piece import Piece
from src.core.collision import CollisionDetector
from src.config.game_config import GameConfig
from src.utils.constants import PIECE_SHAPES
from src.ui.optimized_renderer import OptimizedRenderer
from src.utils.performance_monitor import PerformanceMonitor, RenderProfiler


class OptimizedGameEngine:
    """优化游戏引擎 - 集成优化渲染系统和性能监控"""
    
    def __init__(self, screen: pygame.Surface, config: GameConfig):
        self.config = config
        self.screen = screen
        
        # 游戏组件
        self.board = Board(config.BOARD_WIDTH, config.BOARD_HEIGHT)
        self.game_state = GameState()
        self.collision_detector = CollisionDetector()
        
        # 优化渲染器
        self.renderer = OptimizedRenderer(screen, config)
        
        # 性能监控
        self.performance_monitor = PerformanceMonitor()
        self.render_profiler = RenderProfiler()
        
        # 游戏状态
        self.last_drop_time = time.time()
        self.running = True
        self.return_to_menu = False
        
        # 关卡管理器 - 通过依赖注入传入，避免循环导入
        try:
            from src.level.level_manager import LevelManager
            self.level_manager = LevelManager()
        except ImportError:
            self.level_manager = None
        
        # 输入处理
        self.keys_pressed = set()
        self.last_key_time = {}
        self.key_repeat_delay = config.KEY_REPEAT_DELAY
        self.key_repeat_interval = config.KEY_REPEAT_INTERVAL
        
        # 向下键加速相关变量
        self.down_key_start_time = 0
        self.down_key_last_move_time = 0
        self.down_key_acceleration_start = config.DOWN_KEY_ACCELERATION_START
        self.down_key_acceleration_max = config.DOWN_KEY_ACCELERATION_MAX
        self.down_key_min_interval = config.DOWN_KEY_MIN_INTERVAL
        self.down_key_max_interval = config.DOWN_KEY_MAX_INTERVAL
    
    def spawn_new_piece(self):
        """生成新方块"""
        # 获取可用的方块类型
        if self.level_manager and self.game_state.game_mode == "level":
            available_pieces = self.level_manager.get_available_piece_types()
        else:
            available_pieces = list(PIECE_SHAPES.keys())
        
        if self.game_state.next_piece is None:
            self.game_state.next_piece = Piece(random.choice(available_pieces))
        
        self.game_state.current_piece = self.game_state.next_piece
        self.game_state.next_piece = Piece(random.choice(available_pieces))
        
        # 设置初始位置
        x = self.config.BOARD_WIDTH // 2 - self.game_state.current_piece.get_width() // 2
        y = 0
        self.game_state.set_piece_position(x, y)
        
        # 检查游戏是否结束
        if not self.board.is_valid_position(self.game_state.current_piece, x, y):
            self.game_state.game_over = True
    
    def handle_input(self):
        """处理输入 - 这个方法不应该被直接调用，因为主游戏有自己的输入处理"""
        # 这个方法保留用于独立运行时的兼容性
        # 在主游戏中，输入处理由OptimizedTetrisGame.handle_input()负责
        pass
    
    def handle_continuous_input(self, current_time):
        """处理连续输入"""
        if self.game_state.paused or self.game_state.game_over:
            return
        
        # 处理左右移动
        for key in [pygame.K_LEFT, pygame.K_RIGHT]:
            if key in self.keys_pressed:
                if key in self.last_key_time:
                    time_since_press = current_time - self.last_key_time[key]
                    if time_since_press > self.key_repeat_delay:
                        time_since_last = current_time - self.last_key_time.get(f"{key}_last", 0)
                        if time_since_last > self.key_repeat_interval:
                            dx = -1 if key == pygame.K_LEFT else 1
                            self.move_piece(dx, 0)
                            self.last_key_time[f"{key}_last"] = current_time
        
        # 处理向下移动（带加速）
        if pygame.K_DOWN in self.keys_pressed:
            time_held = current_time - self.down_key_start_time
            if time_held > self.down_key_acceleration_start:
                # 计算加速间隔
                acceleration_factor = min(time_held / self.down_key_acceleration_max, 1.0)
                interval = self.down_key_max_interval - (self.down_key_max_interval - self.down_key_min_interval) * acceleration_factor
                
                if current_time - self.down_key_last_move_time > interval:
                    self.move_piece(0, 1)
                    self.down_key_last_move_time = current_time
    
    def move_piece(self, dx: int, dy: int) -> bool:
        """移动方块"""
        if self.game_state.paused or self.game_state.game_over:
            return False
        
        if not self.game_state.current_piece:
            return False
        
        current_x, current_y = self.game_state.get_piece_position()
        new_x = current_x + dx
        new_y = current_y + dy
        
        if self.board.is_valid_position(self.game_state.current_piece, new_x, new_y):
            self.game_state.set_piece_position(new_x, new_y)
            return True
        return False
    
    def rotate_piece(self) -> bool:
        """旋转方块"""
        if self.game_state.paused or self.game_state.game_over:
            return False
        
        if not self.game_state.current_piece:
            return False
        
        # 检查旋转限制
        if (self.level_manager and 
            self.game_state.game_mode == "level" and
            self.level_manager.check_rule_violation("rotate")):
            return False
        
        current_x, current_y = self.game_state.get_piece_position()
        can_rotate, new_position = self.collision_detector.can_rotate(
            self.game_state.current_piece, 
            self.board, 
            current_x, 
            current_y
        )
        
        if can_rotate:
            self.game_state.set_piece_position(*new_position)
            
            # 记录旋转次数
            if self.level_manager and self.game_state.game_mode == "level":
                self.level_manager.record_rotation()
            
            return True
        return False
    
    def drop_piece(self):
        """方块下落"""
        if not self.move_piece(0, 1):
            self.place_current_piece()
    
    def place_current_piece(self):
        """放置当前方块"""
        if not self.game_state.current_piece:
            return
        
        current_x, current_y = self.game_state.get_piece_position()
        
        # 放置方块到游戏板
        if self.board.place_piece(self.game_state.current_piece, current_x, current_y):
            # 清除完整行
            lines_cleared = self.board.clear_lines()
            if lines_cleared > 0:
                self.game_state.update_score(lines_cleared)
                self.game_state.update_level()
            
            # 检查关卡完成
            if (self.level_manager and 
                self.game_state.game_mode == "level" and
                self.level_manager.check_level_complete(self.game_state.lines_cleared, self.game_state.score)):
                
                # 计算星级
                time_remaining = self.level_manager.get_time_remaining()
                stars = self.level_manager.calculate_stars(
                    self.game_state.lines_cleared, 
                    self.game_state.score, 
                    time_remaining
                )
                
                # 完成关卡
                self.level_manager.complete_level(
                    self.game_state.lines_cleared,
                    self.game_state.score,
                    stars
                )
                
                self.game_state.level_complete = True
                self.game_state.level_stars = stars
                return
            
            # 生成新方块
            self.spawn_new_piece()
    
    def update(self, delta_time: float):
        """更新游戏状态"""
        if self.game_state.paused or self.game_state.game_over:
            return
        
        # 自动下落
        current_time = time.time()
        drop_interval = self.config.get_drop_delay(self.game_state.level) / 1000.0  # 转换为秒
        
        if current_time - self.last_drop_time > drop_interval:
            self.drop_piece()
            self.last_drop_time = current_time
        
        # 更新关卡管理器
        if self.level_manager and self.game_state.game_mode == "level":
            self.level_manager.update(delta_time)
            
            # 检查关卡失败
            if self.level_manager.check_level_failed():
                self.game_state.level_failed = True
    
    def render(self):
        """渲染游戏画面"""
        # 开始性能监控
        frame_start_time = self.performance_monitor.start_frame()
        
        # 渲染游戏板
        self.render_profiler.start_render_call("board")
        self.renderer.render_board(self.board)
        self.render_profiler.end_render_call("board", self.render_profiler.start_render_call("board"))
        
        # 渲染当前方块
        if self.game_state.current_piece:
            self.render_profiler.start_render_call("piece")
            self.renderer.render_piece(self.game_state.current_piece, 
                                     self.game_state.get_piece_position())
            self.render_profiler.end_render_call("piece", self.render_profiler.start_render_call("piece"))
        
        # 渲染UI
        self.render_profiler.start_render_call("ui")
        self.renderer.render_ui(self.game_state)
        self.render_profiler.end_render_call("ui", self.render_profiler.start_render_call("ui"))
        
        # 渲染性能指标
        if self.performance_monitor.show_metrics:
            self.render_profiler.start_render_call("metrics")
            self.performance_monitor.render_metrics(self.screen)
            self.render_profiler.render_profiler_info(self.screen)
            self.render_profiler.end_render_call("metrics", self.render_profiler.start_render_call("metrics"))
        
        # 渲染完整帧
        self.render_profiler.start_render_call("frame")
        self.renderer.render_frame()
        self.render_profiler.end_render_call("frame", self.render_profiler.start_render_call("frame"))
        
        # 结束性能监控
        self.performance_monitor.end_frame(frame_start_time)
    
    def reset_game(self):
        """重置游戏"""
        self.board = Board(self.config.BOARD_WIDTH, self.config.BOARD_HEIGHT)
        self.game_state = GameState()
        self.last_drop_time = time.time()
        self.spawn_new_piece()
    
    def run(self):
        """主游戏循环"""
        clock = pygame.time.Clock()
        
        while self.running:
            try:
                # 处理输入
                self.handle_input()
                
                if self.return_to_menu:
                    break
                
                # 更新游戏状态
                delta_time = clock.tick(self.config.TARGET_FPS) / 1000.0
                self.update(delta_time)
                
                # 渲染游戏画面
                self.render()
                
            except Exception as e:
                print(f"游戏循环出错: {e}")
                import traceback
                traceback.print_exc()
                break
        
        return self.return_to_menu
    
    def get_board(self) -> Board:
        """获取游戏板"""
        return self.board
    
    def get_game_state(self) -> GameState:
        """获取游戏状态"""
        return self.game_state
    
    def get_performance_summary(self):
        """获取性能摘要"""
        return self.performance_monitor.get_performance_summary()
