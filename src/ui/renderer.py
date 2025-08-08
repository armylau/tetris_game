#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渲染引擎 - 负责游戏画面渲染
"""

import pygame
from typing import Tuple
from src.core.board import Board
from src.core.piece import Piece
from src.core.game_state import GameState
from src.config.game_config import GameConfig
from src.utils.constants import BLACK, WHITE, GRAY, RED, GREEN, BLUE, YELLOW


class Renderer:
    """渲染引擎 - 负责游戏画面渲染"""
    
    def __init__(self, screen: pygame.Surface, config: GameConfig):
        self.screen = screen
        self.config = config
        
        # 字体管理器 - 延迟加载
        self._font_manager = None
        self._font = None
        self._small_font = None
    
    @property
    def font_manager(self):
        """延迟加载字体管理器"""
        if self._font_manager is None:
            try:
                from src.utils.font_utils import FontManager
                self._font_manager = FontManager()
            except ImportError:
                # 提供默认实现
                self._font_manager = self._create_default_font_manager()
        return self._font_manager
    
    @property
    def font(self):
        """延迟加载字体"""
        if self._font is None:
            self._font = self.font_manager.get_font(36)
        return self._font
    
    @property
    def small_font(self):
        """延迟加载小字体"""
        if self._small_font is None:
            self._small_font = self.font_manager.get_font(24)
        return self._small_font
    
    def _create_default_font_manager(self):
        """创建默认字体管理器"""
        class DefaultFontManager:
            @staticmethod
            def get_font(size, bold=False):
                return pygame.font.Font(None, size)
        return DefaultFontManager()
    
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
        score_text = self.font.render(f"Score: {game_state.score}", True, WHITE)
        self.screen.blit(score_text, (50, 50))
        
        # 绘制等级
        level_text = self.font.render(f"Level: {game_state.level}", True, WHITE)
        self.screen.blit(level_text, (50, 100))
        
        # 绘制已消除行数
        lines_text = self.font.render(f"Lines: {game_state.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (50, 150))
        
        # 绘制关卡信息（如果处于关卡模式）
        if hasattr(game_state, 'game_mode') and game_state.game_mode == "level":
            # 绘制关卡编号
            level_id_text = self.font.render(f"Level: {game_state.current_level_id}", True, WHITE)
            self.screen.blit(level_id_text, (50, 200))
            
            # 绘制目标行数
            if hasattr(game_state, 'level_manager') and game_state.level_manager:
                target_lines = game_state.level_manager.get_target_lines()
                target_text = self.font.render(f"Target: {target_lines} lines", True, WHITE)
                self.screen.blit(target_text, (50, 250))
                
                # 绘制剩余时间
                time_remaining = game_state.level_manager.get_time_remaining()
                if time_remaining is not None:
                    time_text = self.font.render(f"Time: {time_remaining}s", True, WHITE)
                    self.screen.blit(time_text, (50, 300))
        
        # 绘制下一个方块预览
        if game_state.next_piece:
            next_text = self.font.render("Next:", True, WHITE)
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
            game_over_text = self.font.render("GAME OVER!", True, RED)
            self.screen.blit(game_over_text, (300, 300))
        elif game_state.paused:
            pause_text = self.font.render("PAUSED", True, YELLOW)
            self.screen.blit(pause_text, (300, 300))
        elif hasattr(game_state, 'level_complete') and game_state.level_complete:
            complete_text = self.font.render("LEVEL COMPLETE!", True, GREEN)
            self.screen.blit(complete_text, (300, 300))
            
            # 绘制星级
            if hasattr(game_state, 'level_stars'):
                stars_text = self.font.render(f"Stars: {game_state.level_stars}/3", True, YELLOW)
                self.screen.blit(stars_text, (300, 350))
        elif hasattr(game_state, 'level_failed') and game_state.level_failed:
            failed_text = self.font.render("LEVEL FAILED!", True, RED)
            self.screen.blit(failed_text, (300, 300))
