#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏字体测试程序
验证游戏界面中的字体显示
"""

import pygame
import sys
from tetris_main import TetrisGame, Renderer

def test_game_font():
    """测试游戏字体"""
    pygame.init()
    screen = pygame.display.set_mode((800, 700))
    pygame.display.set_caption("游戏字体测试")
    
    # 创建渲染器
    renderer = Renderer(screen)
    
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
    
    colors = [WHITE, RED, GREEN, YELLOW]
    
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
        for i, text in enumerate(test_texts):
            try:
                # 使用渲染器的字体
                font = renderer.font if i < 5 else renderer.small_font
                color = colors[i % len(colors)]
                
                # 渲染文本
                rendered_text = font.render(text, True, color)
                screen.blit(rendered_text, (50, y))
                
                # 显示字体信息
                info_font = renderer.small_font
                info_text = f"字体大小: {font.get_size()}, 文本: {text}"
                info_surface = info_font.render(info_text, True, (200, 200, 200))
                screen.blit(info_surface, (50, y + 30))
                
                y += 60
                
            except Exception as e:
                print(f"渲染文本 '{text}' 时出错: {e}")
        
        # 显示说明
        try:
            info_texts = [
                "游戏字体测试程序",
                "按ESC键退出",
                "如果看到乱码，说明字体不支持中文",
                "如果看到正常中文，说明字体配置成功"
            ]
            
            y = 500
            for info in info_texts:
                rendered_info = renderer.small_font.render(info, True, WHITE)
                screen.blit(rendered_info, (50, y))
                y += 25
        except Exception as e:
            print(f"渲染说明文本时出错: {e}")
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    print("开始游戏字体测试...")
    test_game_font()
    print("游戏字体测试完成!")
