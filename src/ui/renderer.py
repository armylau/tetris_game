#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渲染引擎 - 负责游戏画面渲染
"""

import pygame
from typing import Tuple
from core.board import Board
from core.piece import Piece
from core.game_state import GameState
from config.game_config import GameConfig
from utils.constants import BLACK, WHITE, GRAY, RED, GREEN, BLUE, YELLOW


class Renderer:
    """渲染引擎 - 负责游戏画面渲染"""
    
    def __init__(self, screen: pygame.Surface, config: GameConfig):
        self.screen = screen
        self.config = config
        self.font_manager = None
        
        # 尝试使用支持中文的字体
        try:
            from utils.font_utils import FontManager
            self.font_manager = FontManager()
            self.font = self.font_manager.get_font(36)
            self.small_font = self.font_manager.get_font(24)
        except ImportError:
            # 回退到原来的字体加载方式
            try:
                # 在macOS上尝试使用系统字体
                self.font = pygame.font.Font("/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc", 36)
                self.small_font = pygame.font.Font("/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc", 24)
            except:
                try:
                    # 尝试使用其他常见的中文字体
                    self.font = pygame.font.Font("/System/Library/Fonts/STHeiti Light.ttc", 36)
                    self.small_font = pygame.font.Font("/System/Library/Fonts/STHeiti Light.ttc", 24)
                except:
                    try:
                        # 尝试使用Helvetica
                        self.font = pygame.font.Font("/System/Library/Fonts/Helvetica.ttc", 36)
                        self.small_font = pygame.font.Font("/System/Library/Fonts/Helvetica.ttc", 24)
                    except:
                        # 回退到默认字体
                        self.font = pygame.font.Font(None, 36)
                        self.small_font = pygame.font.Font(None, 24)
    
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
