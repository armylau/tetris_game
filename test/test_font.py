#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体测试程序
验证中文字体显示是否正常
"""

import pygame
import sys
from font_utils import FontManager

def test_font_rendering():
    """测试字体渲染"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("字体测试")
    
    # 测试文本
    test_texts = [
        ("俄罗斯方块", 72),
        ("经典模式", 48),
        ("关卡模式", 36),
        ("选择关卡", 24),
        ("分数: 1000", 20),
        ("等级: 5", 20),
        ("行数: 15", 20),
        ("目标: 20行", 20),
        ("时间: 120秒", 20),
        ("关卡完成!", 36),
        ("获得3星!", 24),
        ("游戏结束", 48),
    ]
    
    # 颜色定义
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    
    colors = [WHITE, RED, GREEN, BLUE, YELLOW]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 清屏
        screen.fill(BLACK)
        
        # 渲染测试文本
        y = 50
        for i, (text, size) in enumerate(test_texts):
            try:
                font = FontManager.get_font(size)
                color = colors[i % len(colors)]
                rendered_text = font.render(text, True, color)
                screen.blit(rendered_text, (50, y))
                y += size + 10
            except Exception as e:
                print(f"渲染文本 '{text}' 时出错: {e}")
                # 使用默认字体作为回退
                try:
                    fallback_font = pygame.font.Font(None, size)
                    rendered_text = fallback_font.render(text, True, WHITE)
                    screen.blit(rendered_text, (50, y))
                    y += size + 10
                except Exception as e2:
                    print(f"回退字体也失败: {e2}")
        
        # 显示说明
        try:
            info_font = FontManager.get_font(16)
            info_texts = [
                "字体测试程序",
                "按ESC键退出",
                "如果看到乱码，说明字体不支持中文",
                "如果看到正常中文，说明字体配置成功"
            ]
            
            y = 500
            for info in info_texts:
                rendered_info = info_font.render(info, True, WHITE)
                screen.blit(rendered_info, (50, y))
                y += 20
        except Exception as e:
            print(f"渲染说明文本时出错: {e}")
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    print("开始字体测试...")
    test_font_rendering()
    print("字体测试完成!")
