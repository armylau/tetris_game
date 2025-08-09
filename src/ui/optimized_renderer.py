#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版优化渲染引擎v2 - 使用更简单的层合成方法
"""

import pygame
import time
from typing import Tuple, List, Dict, Set, Optional
from src.core.board import Board
from src.core.piece import Piece
from src.core.game_state import GameState
from src.config.game_config import GameConfig
from src.utils.constants import BLACK, WHITE, GRAY, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE


class OptimizedRenderer:
    """优化渲染引擎"""
    
    def __init__(self, screen: pygame.Surface, config: GameConfig):
        self.screen = screen
        self.config = config
        
        # 字体缓存
        self.font_cache = {}
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # 性能监控
        self.render_times = []
    
    def get_cached_text(self, text: str, color: Tuple[int, int, int], font_size: int = 36) -> pygame.Surface:
        """获取缓存的文本"""
        font = self.font if font_size == 36 else self.small_font
        key = f"{text}_{color}_{font_size}"
        if key not in self.font_cache:
            self.font_cache[key] = font.render(text, True, color)
        return self.font_cache[key]
    
    def render_board(self, board: Board):
        """渲染游戏板"""
        # 绘制游戏板背景
        pygame.draw.rect(self.screen, GRAY, 
                        (self.config.BOARD_X - 2, self.config.BOARD_Y - 2, 
                         self.config.BOARD_WIDTH * self.config.CELL_SIZE + 4, 
                         self.config.BOARD_HEIGHT * self.config.CELL_SIZE + 4))
        
        # 绘制网格
        for row in range(board.height):
            for col in range(board.width):
                x = self.config.BOARD_X + col * self.config.CELL_SIZE
                y = self.config.BOARD_Y + row * self.config.CELL_SIZE
                
                if board.grid[row][col]:
                    # 绘制已放置的方块
                    pygame.draw.rect(self.screen, board.grid[row][col],
                                   (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK,
                                   (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE), 1)
                else:
                    # 绘制空格子
                    pygame.draw.rect(self.screen, BLACK,
                                   (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE), 1)
    
    def render_piece(self, piece: Piece, position: Tuple[int, int]):
        """渲染方块"""
        if not piece:
            return
        
        x, y = position
        
        # 直接绘制方块
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[0])):
                if piece.shape[row][col]:
                    screen_x = self.config.BOARD_X + (x + col) * self.config.CELL_SIZE
                    screen_y = self.config.BOARD_Y + (y + row) * self.config.CELL_SIZE
                    pygame.draw.rect(self.screen, piece.color,
                                   (screen_x, screen_y, self.config.CELL_SIZE, self.config.CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK,
                                   (screen_x, screen_y, self.config.CELL_SIZE, self.config.CELL_SIZE), 1)
    
    def render_ui(self, game_state: GameState):
        """渲染用户界面"""
        # 绘制分数
        score_text = self.get_cached_text(f"Score: {game_state.score}", WHITE)
        self.screen.blit(score_text, (50, 50))
        
        # 绘制等级
        level_text = self.get_cached_text(f"Level: {game_state.level}", WHITE)
        self.screen.blit(level_text, (50, 100))
        
        # 绘制已消除行数
        lines_text = self.get_cached_text(f"Lines: {game_state.lines_cleared}", WHITE)
        self.screen.blit(lines_text, (50, 150))
        
        # 绘制关卡信息（如果处于关卡模式）
        if hasattr(game_state, 'game_mode') and game_state.game_mode == "level":
            # 绘制关卡编号
            level_id_text = self.get_cached_text(f"Level: {game_state.current_level_id}", WHITE)
            self.screen.blit(level_id_text, (50, 200))
            
            # 绘制目标行数
            if hasattr(game_state, 'level_manager') and game_state.level_manager:
                target_lines = game_state.level_manager.get_target_lines()
                target_text = self.get_cached_text(f"Target: {target_lines} lines", WHITE)
                self.screen.blit(target_text, (50, 250))
                
                # 绘制剩余时间
                time_remaining = game_state.level_manager.get_time_remaining()
                if time_remaining is not None:
                    time_text = self.get_cached_text(f"Time: {time_remaining}s", WHITE)
                    self.screen.blit(time_text, (50, 300))
        
        # 绘制下一个方块预览
        if game_state.next_piece:
            next_text = self.get_cached_text("Next:", WHITE)
            self.screen.blit(next_text, (50, 350))
            
            # 绘制预览方块
            preview_x = 50
            preview_y = 400
            for row in range(len(game_state.next_piece.shape)):
                for col in range(len(game_state.next_piece.shape[0])):
                    if game_state.next_piece.shape[row][col]:
                        x = preview_x + col * 20
                        y = preview_y + row * 20
                        pygame.draw.rect(self.screen, game_state.next_piece.color,
                                       (x, y, 20, 20))
                        pygame.draw.rect(self.screen, BLACK, (x, y, 20, 20), 1)
        
        # 绘制游戏状态
        if game_state.game_over:
            game_over_text = self.get_cached_text("GAME OVER!", RED)
            self.screen.blit(game_over_text, (300, 300))
        elif game_state.paused:
            pause_text = self.get_cached_text("PAUSED", YELLOW)
            self.screen.blit(pause_text, (300, 300))
        elif hasattr(game_state, 'level_complete') and game_state.level_complete:
            complete_text = self.get_cached_text("LEVEL COMPLETE!", GREEN)
            self.screen.blit(complete_text, (300, 300))
            
            # 绘制星级
            if hasattr(game_state, 'level_stars'):
                stars_text = self.get_cached_text(f"Stars: {game_state.level_stars}/3", YELLOW)
                self.screen.blit(stars_text, (300, 350))
        elif hasattr(game_state, 'level_failed') and game_state.level_failed:
            failed_text = self.get_cached_text("LEVEL FAILED!", RED)
            self.screen.blit(failed_text, (300, 300))
    
    def render_frame(self):
        """渲染完整帧"""
        start_time = time.time()
        
        # 更新显示
        pygame.display.flip()
        
        # 记录渲染时间
        render_time = time.time() - start_time
        self.render_times.append(render_time)
        
        # 保持最近100次的渲染时间
        if len(self.render_times) > 100:
            self.render_times.pop(0)
    
    def get_average_render_time(self) -> float:
        """获取平均渲染时间"""
        if self.render_times:
            return sum(self.render_times) / len(self.render_times)
        return 0.0
    
    def get_fps(self) -> float:
        """获取当前FPS"""
        if len(self.render_times) >= 2:
            return 1.0 / self.get_average_render_time()
        return 0.0
