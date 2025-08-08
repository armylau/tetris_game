#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体调试程序
检查字体加载的具体问题
"""

import pygame
import sys
import os

def debug_font_loading():
    """调试字体加载"""
    print("字体调试程序")
    print("=" * 50)
    
    # 初始化pygame
    try:
        pygame.init()
        print("pygame初始化成功")
    except Exception as e:
        print(f"pygame初始化失败: {e}")
        return
    
    # 测试不同的字体加载方法
    test_texts = [
        "俄罗斯方块",
        "经典模式", 
        "关卡模式",
        "选择关卡",
        "新手入门"
    ]
    
    print("\n测试字体加载方法:")
    
    # 方法1: 默认字体
    print("\n1. 测试默认字体:")
    try:
        font = pygame.font.Font(None, 36)
        for text in test_texts:
            try:
                surface = font.render(text, True, (255, 255, 255))
                print(f"  ✓ '{text}' 渲染成功")
            except Exception as e:
                print(f"  ✗ '{text}' 渲染失败: {e}")
    except Exception as e:
        print(f"  默认字体加载失败: {e}")
    
    # 方法2: 系统字体
    print("\n2. 测试系统字体:")
    system_fonts = [
        "STHeiti", "STHeiti Light", "STHeiti Medium",
        "Arial", "Helvetica", "Arial Unicode MS"
    ]
    
    for font_name in system_fonts:
        try:
            font = pygame.font.SysFont(font_name, 36)
            success_count = 0
            for text in test_texts:
                try:
                    surface = font.render(text, True, (255, 255, 255))
                    success_count += 1
                except:
                    pass
            
            if success_count > 0:
                print(f"  ✓ {font_name}: {success_count}/{len(test_texts)} 文本渲染成功")
            else:
                print(f"  ✗ {font_name}: 所有文本渲染失败")
        except Exception as e:
            print(f"  ✗ {font_name}: 字体加载失败 - {e}")
    
    # 方法3: 字体文件
    print("\n3. 测试字体文件:")
    font_files = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Helvetica.ttc"
    ]
    
    for font_path in font_files:
        if os.path.exists(font_path):
            try:
                font = pygame.font.Font(font_path, 36)
                success_count = 0
                for text in test_texts:
                    try:
                        surface = font.render(text, True, (255, 255, 255))
                        success_count += 1
                    except:
                        pass
                
                if success_count > 0:
                    print(f"  ✓ {font_path}: {success_count}/{len(test_texts)} 文本渲染成功")
                else:
                    print(f"  ✗ {font_path}: 所有文本渲染失败")
            except Exception as e:
                print(f"  ✗ {font_path}: 字体加载失败 - {e}")
        else:
            print(f"  ✗ {font_path}: 文件不存在")
    
    # 测试FontManager
    print("\n4. 测试FontManager:")
    try:
        from font_utils import FontManager
        font = FontManager.get_font(36)
        success_count = 0
        for text in test_texts:
            try:
                surface = font.render(text, True, (255, 255, 255))
                success_count += 1
            except:
                pass
        
        if success_count > 0:
            print(f"  ✓ FontManager: {success_count}/{len(test_texts)} 文本渲染成功")
        else:
            print(f"  ✗ FontManager: 所有文本渲染失败")
    except Exception as e:
        print(f"  ✗ FontManager: {e}")
    
    pygame.quit()
    print("\n字体调试完成!")

if __name__ == "__main__":
    debug_font_loading()
