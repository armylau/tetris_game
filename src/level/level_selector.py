#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏关卡选择界面
提供关卡选择功能
"""

import pygame
import sys
from typing import Optional, Dict, List
from src.level.level_manager import LevelManager
from src.config.level_config import LevelConfig

# 字体管理器导入
try:
    from src.utils.font_utils import FontManager
except ImportError:
    # 如果无法导入FontManager，使用简单的字体加载
    class FontManager:
        @staticmethod
        def get_font(size, bold=False):
            return pygame.font.Font(None, size)

class LevelSelector:
    """关卡选择器"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.level_manager = LevelManager()
        
        # 界面配置
        self.grid_size = 5  # 每行显示的关卡数
        self.level_button_size = 80
        self.button_margin = 20
        self.start_x = 100
        self.start_y = 150
        
        # 颜色定义
        self.BACKGROUND_COLOR = (50, 50, 50)
        self.TITLE_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (100, 100, 100)
        self.BUTTON_HOVER_COLOR = (150, 150, 150)
        self.UNLOCKED_COLOR = (0, 255, 0)
        self.LOCKED_COLOR = (100, 100, 100)
        self.COMPLETED_COLOR = (255, 215, 0)
        self.STAR_COLOR = (255, 255, 0)
        
        # 确保pygame已初始化
        try:
            pygame.init()
        except:
            pass
        
        # 字体
        self.title_font = FontManager.get_font(48, bold=True)
        self.button_font = FontManager.get_font(24)
        self.info_font = FontManager.get_font(20)
        
        # 状态
        self.selected_level = None
        self.hover_level = None
        
    def render(self):
        """渲染关卡选择界面"""
        # 绘制背景
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # 绘制标题
        title_text = self.title_font.render("Select Level", True, self.TITLE_COLOR)
        title_rect = title_text.get_rect(center=(400, 50))
        self.screen.blit(title_text, title_rect)
        
        # 绘制关卡网格
        self._render_level_grid()
        
        # 绘制关卡信息
        if self.hover_level:
            self._render_level_info(self.hover_level)
        
        # 绘制操作说明
        self._render_instructions()
        
        # 绘制进度信息
        self._render_progress_info()
    
    def _render_level_grid(self):
        """渲染关卡网格"""
        total_levels = LevelConfig.get_total_levels()
        
        for level_id in range(1, total_levels + 1):
            row = (level_id - 1) // self.grid_size
            col = (level_id - 1) % self.grid_size
            
            x = self.start_x + col * (self.level_button_size + self.button_margin)
            y = self.start_y + row * (self.level_button_size + self.button_margin)
            
            # 确定按钮颜色
            if level_id == self.hover_level:
                color = self.BUTTON_HOVER_COLOR
            elif self.level_manager.is_level_unlocked(level_id):
                if level_id in self.level_manager.completed_levels:
                    color = self.COMPLETED_COLOR
                else:
                    color = self.UNLOCKED_COLOR
            else:
                color = self.LOCKED_COLOR
            
            # 绘制按钮
            button_rect = pygame.Rect(x, y, self.level_button_size, self.level_button_size)
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
            
            # 绘制关卡编号
            level_text = self.button_font.render(str(level_id), True, (0, 0, 0))
            text_rect = level_text.get_rect(center=button_rect.center)
            self.screen.blit(level_text, text_rect)
            
            # 绘制星级
            if level_id in self.level_manager.level_stars:
                stars = self.level_manager.level_stars[level_id]
                self._render_stars(x + 5, y + 5, stars)
    
    def _render_stars(self, x: int, y: int, stars: int):
        """渲染星级"""
        star_size = 15
        for i in range(3):
            color = self.STAR_COLOR if i < stars else (100, 100, 100)
            star_rect = pygame.Rect(x + i * (star_size + 2), y, star_size, star_size)
            pygame.draw.rect(self.screen, color, star_rect)
    
    def _render_level_info(self, level_id: int):
        """渲染关卡信息"""
        config = LevelConfig.get_level_config(level_id)
        if not config:
            return
        
        # 信息框位置
        info_x = 500
        info_y = 150
        info_width = 250
        info_height = 200
        
        # 绘制信息框背景
        info_rect = pygame.Rect(info_x, info_y, info_width, info_height)
        pygame.draw.rect(self.screen, (80, 80, 80), info_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), info_rect, 2)
        
        # 绘制关卡名称
        name_text = self.title_font.render(config["name"], True, self.TITLE_COLOR)
        self.screen.blit(name_text, (info_x + 10, info_y + 10))
        
        # 绘制关卡描述
        desc_text = self.info_font.render(config["description"], True, (200, 200, 200))
        self.screen.blit(desc_text, (info_x + 10, info_y + 60))
        
        # 绘制目标行数
        target_text = self.info_font.render(f"Target Lines: {config['target_lines']}", True, (200, 200, 200))
        self.screen.blit(target_text, (info_x + 10, info_y + 90))
        
        # 绘制速度倍数
        speed_text = self.info_font.render(f"Speed Multiplier: {config['speed_multiplier']}x", True, (200, 200, 200))
        self.screen.blit(speed_text, (info_x + 10, info_y + 110))
        
        # 绘制时间限制
        if config.get("time_limit"):
            time_text = self.info_font.render(f"Time Limit: {config['time_limit']}s", True, (200, 200, 200))
            self.screen.blit(time_text, (info_x + 10, info_y + 130))
        
        # 绘制特殊规则
        if config.get("special_rules"):
            rules_text = self.info_font.render("Special Rules:", True, (255, 100, 100))
            self.screen.blit(rules_text, (info_x + 10, info_y + 150))
            
            y_offset = 170
            for rule, value in config["special_rules"].items():
                rule_text = self.info_font.render(f"• {rule}: {value}", True, (255, 150, 150))
                self.screen.blit(rule_text, (info_x + 20, info_y + y_offset))
                y_offset += 20
    
    def _render_instructions(self):
        """渲染操作说明"""
        instructions = [
            "Instructions:",
            "• Click level button to select",
            "• Hover mouse to view level info",
            "• Press ESC to return to menu",
            "• Press R to reset all progress"
        ]
        
        y = 500
        for instruction in instructions:
            text = self.info_font.render(instruction, True, (200, 200, 200))
            self.screen.blit(text, (50, y))
            y += 25
    
    def _render_progress_info(self):
        """渲染进度信息"""
        progress = self.level_manager.get_progress_summary()
        
        # 进度信息位置
        info_x = 500
        info_y = 400
        
        # 绘制进度框
        progress_rect = pygame.Rect(info_x, info_y, 250, 100)
        pygame.draw.rect(self.screen, (80, 80, 80), progress_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), progress_rect, 2)
        
        # 绘制进度信息
        completed_text = self.info_font.render(f"Completed: {len(progress['completed_levels'])}/{progress['total_levels']}", True, (200, 200, 200))
        self.screen.blit(completed_text, (info_x + 10, info_y + 10))
        
        total_stars_text = self.info_font.render(f"Total Stars: {progress['total_stars']}", True, (200, 200, 200))
        self.screen.blit(total_stars_text, (info_x + 10, info_y + 30))
        
        completion_rate = len(progress['completed_levels']) / progress['total_levels'] * 100
        rate_text = self.info_font.render(f"Completion: {completion_rate:.1f}%", True, (200, 200, 200))
        self.screen.blit(rate_text, (info_x + 10, info_y + 50))
    
    def handle_input(self, event) -> Optional[int]:
        """处理输入，返回选择的关卡ID"""
        if event.type == pygame.MOUSEMOTION:
            # 更新悬停状态
            self.hover_level = self._get_level_at_position(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                clicked_level = self._get_level_at_position(event.pos)
                if clicked_level and self.level_manager.is_level_unlocked(clicked_level):
                    return clicked_level
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return -1  # 返回主菜单
            elif event.key == pygame.K_r:
                self.level_manager.reset_progress()
        
        return None
    
    def _get_level_at_position(self, pos) -> Optional[int]:
        """获取指定位置的关卡ID"""
        x, y = pos
        total_levels = LevelConfig.get_total_levels()
        
        for level_id in range(1, total_levels + 1):
            row = (level_id - 1) // self.grid_size
            col = (level_id - 1) % self.grid_size
            
            button_x = self.start_x + col * (self.level_button_size + self.button_margin)
            button_y = self.start_y + row * (self.level_button_size + self.button_margin)
            
            button_rect = pygame.Rect(button_x, button_y, self.level_button_size, self.level_button_size)
            
            if button_rect.collidepoint(x, y):
                return level_id
        
        return None
    
    def run(self) -> Optional[int]:
        """运行关卡选择界面，返回选择的关卡ID"""
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
