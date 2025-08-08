#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体工具类
用于统一管理字体加载，解决中文显示问题
"""

import pygame
import os
import sys

class FontManager:
    """字体管理器"""
    
    # 常见的中文字体路径
    CHINESE_FONTS = [
        # macOS 系统字体 - 使用正确的路径
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc",
        "/System/Library/PrivateFrameworks/FontServices.framework/Versions/A/Resources/Reserved/PingFangUI.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        
        # Windows 系统字体
        "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        "C:/Windows/Fonts/simsun.ttc",  # 宋体
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        
        # Linux 系统字体
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    
    @classmethod
    def get_chinese_font(cls, size: int) -> pygame.font.Font:
        """获取支持中文的字体"""
        # 确保pygame已初始化
        try:
            pygame.init()
        except:
            pass
        
        # 首先尝试系统默认字体
        try:
            return pygame.font.Font(None, size)
        except:
            pass
        
        # 尝试使用pygame的系统字体
        try:
            # 尝试常见的中文字体名称
            chinese_font_names = [
                "PingFang SC", "PingFang TC", "PingFang HK",
                "STHeiti", "STHeiti Light", "STHeiti Medium",
                "Arial Unicode MS", "Arial", "Helvetica",
                "Microsoft YaHei", "SimSun", "SimHei",
                "DejaVu Sans", "Liberation Sans"
            ]
            
            for font_name in chinese_font_names:
                try:
                    return pygame.font.SysFont(font_name, size)
                except:
                    continue
        except:
            pass
        
        # 尝试加载字体文件
        for font_path in cls.CHINESE_FONTS:
            if os.path.exists(font_path):
                try:
                    return pygame.font.Font(font_path, size)
                except Exception as e:
                    print(f"无法加载字体 {font_path}: {e}")
                    continue
        
        # 最后的回退方案
        try:
            return pygame.font.SysFont(None, size)
        except:
            return pygame.font.Font(None, size)
    
    @classmethod
    def get_font(cls, size: int, bold: bool = False) -> pygame.font.Font:
        """获取字体，支持粗体选项"""
        font = cls.get_chinese_font(size)
        
        # 如果需要粗体，尝试设置粗体
        if bold:
            try:
                # 尝试使用粗体字体
                bold_fonts = [
                    "/System/Library/Fonts/STHeiti Medium.ttc",
                    "/System/Library/Fonts/Helvetica.ttc",
                    "C:/Windows/Fonts/simhei.ttf",
                ]
                
                for font_path in bold_fonts:
                    if os.path.exists(font_path):
                        try:
                            return pygame.font.Font(font_path, size)
                        except:
                            continue
            except:
                pass
        
        return font
    
    @classmethod
    def test_font_rendering(cls):
        """测试字体渲染"""
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        
        # 测试不同大小的字体
        test_texts = [
            ("小字体测试", 20),
            ("中字体测试", 36),
            ("大字体测试", 72),
        ]
        
        y = 50
        for text, size in test_texts:
            font = cls.get_font(size)
            rendered_text = font.render(text, True, (255, 255, 255))
            screen.blit(rendered_text, (50, y))
            y += size + 20
        
        pygame.display.flip()
        
        # 等待用户关闭窗口
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        pygame.quit()

if __name__ == "__main__":
    # 测试字体渲染
    FontManager.test_font_rendering()
