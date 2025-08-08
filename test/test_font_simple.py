#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单字体测试程序
专门测试游戏中的字体渲染
"""

import pygame
import sys

def test_game_font():
    """测试游戏字体"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("游戏字体测试")
    
    # 测试不同的字体加载方式
    fonts = []
    
    # 1. 使用系统字体名称
    try:
        fonts.append(("PingFang SC", pygame.font.SysFont("PingFang SC", 24)))
        print("✓ 成功加载 PingFang SC")
    except Exception as e:
        print(f"✗ 加载 PingFang SC 失败: {e}")
    
    try:
        fonts.append(("STHeiti Light", pygame.font.SysFont("STHeiti Light", 24)))
        print("✓ 成功加载 STHeiti Light")
    except Exception as e:
        print(f"✗ 加载 STHeiti Light 失败: {e}")
    
    # 2. 使用字体文件路径
    font_paths = [
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    
    for font_path in font_paths:
        try:
            font = pygame.font.Font(font_path, 24)
            fonts.append((os.path.basename(font_path), font))
            print(f"✓ 成功加载 {font_path}")
        except Exception as e:
            print(f"✗ 加载 {font_path} 失败: {e}")
    
    # 3. 默认字体
    try:
        fonts.append(("默认字体", pygame.font.Font(None, 24)))
        print("✓ 成功加载默认字体")
    except Exception as e:
        print(f"✗ 加载默认字体失败: {e}")
    
    # 测试文本
    test_texts = [
        "分数: 1000",
        "等级: 5",
        "行数: 15",
        "关卡: 1",
        "目标: 20行",
        "时间: 120秒",
        "关卡完成!",
        "获得3星!",
        "游戏结束",
        "已暂停"
    ]
    
    # 颜色定义
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    
    colors = [WHITE, RED, GREEN, YELLOW, BLUE]
    
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
        for i, (font_name, font) in enumerate(fonts):
            # 显示字体名称
            try:
                name_surface = pygame.font.Font(None, 16).render(f"字体: {font_name}", True, YELLOW)
                screen.blit(name_surface, (50, y))
                y += 25
                
                # 测试每个文本
                for j, text in enumerate(test_texts[:5]):  # 只测试前5个文本
                    try:
                        color = colors[j % len(colors)]
                        rendered = font.render(text, True, color)
                        screen.blit(rendered, (70, y))
                        y += 25
                    except Exception as e:
                        error_text = f"渲染失败: {text[:10]}... - {e}"
                        error_surface = pygame.font.Font(None, 16).render(error_text, True, RED)
                        screen.blit(error_surface, (70, y))
                        y += 25
                
                y += 20
                
            except Exception as e:
                error_text = f"字体 {font_name} 出错: {e}"
                error_surface = pygame.font.Font(None, 16).render(error_text, True, RED)
                screen.blit(error_surface, (50, y))
                y += 25
        
        # 显示说明
        info_texts = [
            "游戏字体测试程序",
            "按ESC键退出",
            "如果看到乱码，说明字体不支持中文",
            "如果看到正常中文，说明字体配置成功"
        ]
        
        y = 500
        for info in info_texts:
            try:
                rendered_info = pygame.font.Font(None, 16).render(info, True, WHITE)
                screen.blit(rendered_info, (50, y))
                y += 20
            except Exception as e:
                print(f"渲染说明文本时出错: {e}")
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    import os
    print("开始简单字体测试...")
    test_game_font()
    print("简单字体测试完成!")
