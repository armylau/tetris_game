#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
菜单字体测试程序
专门测试主菜单和关卡选择器的字体显示
"""

import pygame
import sys
from font_utils import FontManager

def test_menu_fonts():
    """测试菜单字体"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("菜单字体测试")
    
    # 测试文本 - 来自主菜单和关卡选择器
    test_texts = [
        # 主菜单文本
        ("俄罗斯方块", 72),
        ("经典模式", 36),
        ("关卡模式", 36),
        ("退出游戏", 36),
        ("游戏说明:", 24),
        ("• 经典模式: 无限游戏，挑战高分", 24),
        ("• 关卡模式: 20个精心设计的关卡", 24),
        ("• 方向键: 移动方块", 24),
        ("• 空格键: 旋转方块", 24),
        ("• P键: 暂停游戏", 24),
        ("• R键: 重新开始", 24),
        ("• ESC键: 返回菜单", 24),
        
        # 关卡选择器文本
        ("选择关卡", 48),
        ("新手入门", 48),
        ("基础练习", 48),
        ("速度提升", 48),
        ("快速反应", 48),
        ("中级挑战", 48),
        ("方块限制", 48),
        ("旋转限制", 48),
        ("高速模式", 48),
        ("精确控制", 48),
        ("无加速挑战", 48),
        ("时间挑战", 48),
        ("极速模式", 48),
        ("特定目标", 48),
        ("方块大师", 48),
        ("高级挑战", 48),
        ("时间大师", 48),
        ("反向控制", 48),
        ("极限挑战", 48),
        ("终极挑战", 48),
        ("传奇模式", 48),
        
        # 游戏界面文本
        ("分数: 1000", 36),
        ("等级: 5", 36),
        ("行数: 15", 36),
        ("关卡: 1", 36),
        ("目标: 20行", 36),
        ("时间: 120秒", 36),
        ("关卡完成!", 36),
        ("获得3星!", 24),
        ("游戏结束", 48),
        ("已暂停", 36),
    ]
    
    # 颜色定义
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GRAY = (200, 200, 200)
    
    colors = [WHITE, RED, GREEN, BLUE, YELLOW, GRAY]
    
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
        y = 20
        for i, (text, size) in enumerate(test_texts):
            try:
                # 使用FontManager获取字体
                font = FontManager.get_font(size)
                color = colors[i % len(colors)]
                
                # 渲染文本
                rendered_text = font.render(text, True, color)
                screen.blit(rendered_text, (20, y))
                
                # 显示字体信息
                info_font = FontManager.get_font(12)
                info_text = f"字体大小: {size}, 文本: {text}"
                info_surface = info_font.render(info_text, True, GRAY)
                screen.blit(info_surface, (20, y + size + 5))
                
                y += size + 25
                
                # 如果超出屏幕，重新开始
                if y > 550:
                    y = 20
                    
            except Exception as e:
                print(f"渲染文本 '{text}' 时出错: {e}")
                # 使用默认字体作为回退
                try:
                    fallback_font = pygame.font.Font(None, size)
                    rendered_text = fallback_font.render(text, True, WHITE)
                    screen.blit(rendered_text, (20, y))
                    y += size + 25
                except Exception as e2:
                    print(f"回退字体也失败: {e2}")
        
        # 显示说明
        try:
            info_font = FontManager.get_font(16)
            info_texts = [
                "菜单字体测试程序",
                "按ESC键退出",
                "如果看到乱码，说明字体不支持中文",
                "如果看到正常中文，说明字体配置成功"
            ]
            
            y = 550
            for info in info_texts:
                rendered_info = info_font.render(info, True, WHITE)
                screen.blit(rendered_info, (20, y))
                y += 20
        except Exception as e:
            print(f"渲染说明文本时出错: {e}")
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    print("开始菜单字体测试...")
    test_menu_fonts()
    print("菜单字体测试完成!")
