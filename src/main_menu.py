#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏主菜单
提供游戏模式选择
"""

import pygame
import sys
from typing import Optional
from level_selector import LevelSelector

try:
    from font_utils import FontManager
except ImportError:
    # 如果无法导入FontManager，使用简单的字体加载
    class FontManager:
        @staticmethod
        def get_font(size, bold=False):
            return pygame.font.Font(None, size)

class MainMenu:
    """主菜单"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
        # 颜色定义
        self.BACKGROUND_COLOR = (30, 30, 30)
        self.TITLE_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (100, 100, 100)
        self.BUTTON_HOVER_COLOR = (150, 150, 150)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)
        
        # 确保pygame已初始化
        try:
            pygame.init()
        except:
            pass
        
        # 字体
        try:
            from font_utils import FontManager
            self.title_font = FontManager.get_font(72, bold=True)
            self.button_font = FontManager.get_font(36)
            self.info_font = FontManager.get_font(24)
        except ImportError:
            # 如果无法导入FontManager，使用简单的字体加载
            self.title_font = pygame.font.Font(None, 72)
            self.button_font = pygame.font.Font(None, 36)
            self.info_font = pygame.font.Font(None, 24)
        
        # 按钮配置
        self.buttons = [
            {"text": "Classic Mode", "action": "classic", "y": 250},
            {"text": "Level Mode", "action": "level", "y": 320},
            {"text": "Quit Game", "action": "quit", "y": 390}
        ]
        
        self.hover_button = None
    
    def render(self):
        """渲染主菜单"""
        # 绘制背景
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # 绘制标题
        title_text = self.title_font.render("TETRIS", True, self.TITLE_COLOR)
        title_rect = title_text.get_rect(center=(400, 100))
        self.screen.blit(title_text, title_rect)
        
        # 绘制按钮
        for i, button in enumerate(self.buttons):
            color = self.BUTTON_HOVER_COLOR if i == self.hover_button else self.BUTTON_COLOR
            button_rect = pygame.Rect(250, button["y"], 300, 50)
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
            
            # 绘制按钮文字
            text = self.button_font.render(button["text"], True, self.BUTTON_TEXT_COLOR)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
        # 绘制说明
        instructions = [
            "Game Instructions:",
            "• Classic Mode: Endless game, challenge high score",
            "• Level Mode: 20 carefully designed levels",
            "• Arrow Keys: Move pieces",
            "• Space: Rotate pieces",
            "• P: Pause game",
            "• R: Restart game",
            "• ESC: Back to menu"
        ]
        
        y = 500
        for instruction in instructions:
            text = self.info_font.render(instruction, True, (200, 200, 200))
            self.screen.blit(text, (50, y))
            y += 25
    
    def handle_input(self, event) -> Optional[str]:
        """处理输入，返回选择的动作"""
        if event.type == pygame.MOUSEMOTION:
            # 更新悬停状态
            self.hover_button = self._get_button_at_position(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                clicked_button = self._get_button_at_position(event.pos)
                if clicked_button is not None:
                    return self.buttons[clicked_button]["action"]
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"
            elif event.key == pygame.K_1:
                return "classic"
            elif event.key == pygame.K_2:
                return "level"
        
        return None
    
    def _get_button_at_position(self, pos) -> Optional[int]:
        """获取指定位置的按钮索引"""
        x, y = pos
        
        for i, button in enumerate(self.buttons):
            button_rect = pygame.Rect(250, button["y"], 300, 50)
            if button_rect.collidepoint(x, y):
                return i
        
        return None
    
    def run(self) -> Optional[str]:
        """运行主菜单，返回选择的动作"""
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                result = self.handle_input(event)
                if result is not None:
                    return result
            
            self.render()
            pygame.display.flip()
            clock.tick(60)
