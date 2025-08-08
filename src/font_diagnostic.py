#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体诊断程序
检查系统字体和中文支持情况
"""

import pygame
import os
import sys

def check_system_fonts():
    """检查系统字体"""
    print("=== 系统字体检查 ===")
    
    # 检查pygame可用的系统字体
    try:
        pygame.init()
        available_fonts = pygame.font.get_fonts()
        print(f"pygame可用的字体数量: {len(available_fonts)}")
        
        # 查找可能支持中文的字体
        chinese_candidates = []
        for font_name in available_fonts:
            if any(keyword in font_name.lower() for keyword in ['chinese', 'pingfang', 'stheiti', 'arial', 'helvetica']):
                chinese_candidates.append(font_name)
        
        print(f"可能支持中文的字体: {chinese_candidates[:10]}")  # 只显示前10个
        
    except Exception as e:
        print(f"获取系统字体时出错: {e}")

def test_font_loading():
    """测试字体加载"""
    print("\n=== 字体加载测试 ===")
    
    # 常见的中文字体路径
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = pygame.font.Font(font_path, 24)
                print(f"✓ 成功加载: {font_path}")
                
                # 测试中文渲染
                test_text = "测试中文"
                try:
                    rendered = font.render(test_text, True, (255, 255, 255))
                    print(f"  - 中文渲染测试: 成功")
                except Exception as e:
                    print(f"  - 中文渲染测试: 失败 - {e}")
                    
            except Exception as e:
                print(f"✗ 加载失败: {font_path} - {e}")
        else:
            print(f"- 文件不存在: {font_path}")

def test_sysfont():
    """测试系统字体"""
    print("\n=== 系统字体测试 ===")
    
    font_names = [
        "PingFang SC", "PingFang TC", "PingFang HK",
        "STHeiti", "STHeiti Light", "STHeiti Medium",
        "Arial Unicode MS", "Arial", "Helvetica",
        "Microsoft YaHei", "SimSun", "SimHei"
    ]
    
    for font_name in font_names:
        try:
            font = pygame.font.SysFont(font_name, 24)
            print(f"✓ 成功加载系统字体: {font_name}")
            
            # 测试中文渲染
            test_text = "测试中文"
            try:
                rendered = font.render(test_text, True, (255, 255, 255))
                print(f"  - 中文渲染测试: 成功")
            except Exception as e:
                print(f"  - 中文渲染测试: 失败 - {e}")
                
        except Exception as e:
            print(f"✗ 加载失败: {font_name} - {e}")

def interactive_font_test():
    """交互式字体测试"""
    print("\n=== 交互式字体测试 ===")
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("字体测试")
    
    # 测试不同的字体加载方式
    fonts_to_test = []
    
    # 1. 系统字体
    try:
        fonts_to_test.append(("PingFang SC", pygame.font.SysFont("PingFang SC", 24)))
    except:
        pass
    
    try:
        fonts_to_test.append(("STHeiti Light", pygame.font.SysFont("STHeiti Light", 24)))
    except:
        pass
    
    # 2. 文件字体
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = pygame.font.Font(font_path, 24)
                fonts_to_test.append((os.path.basename(font_path), font))
            except:
                pass
    
    # 3. 默认字体
    try:
        fonts_to_test.append(("默认字体", pygame.font.Font(None, 24)))
    except:
        pass
    
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
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((0, 0, 0))
        
        y = 50
        for font_name, font in fonts_to_test:
            # 显示字体名称
            try:
                name_surface = pygame.font.Font(None, 16).render(f"字体: {font_name}", True, (255, 255, 0))
                screen.blit(name_surface, (50, y))
                y += 25
                
                # 测试每个文本
                for text in test_texts[:3]:  # 只测试前3个文本
                    try:
                        rendered = font.render(text, True, (255, 255, 255))
                        screen.blit(rendered, (70, y))
                        y += 25
                    except Exception as e:
                        error_text = f"渲染失败: {text[:10]}..."
                        error_surface = pygame.font.Font(None, 16).render(error_text, True, (255, 0, 0))
                        screen.blit(error_surface, (70, y))
                        y += 25
                
                y += 20
                
            except Exception as e:
                error_text = f"字体 {font_name} 出错: {e}"
                error_surface = pygame.font.Font(None, 16).render(error_text, True, (255, 0, 0))
                screen.blit(error_surface, (50, y))
                y += 25
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    print("开始字体诊断...")
    
    check_system_fonts()
    test_font_loading()
    test_sysfont()
    
    print("\n启动交互式测试窗口...")
    interactive_font_test()
    
    print("字体诊断完成!")
