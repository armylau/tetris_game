#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关卡系统演示程序
展示完整的关卡功能
"""

import pygame
import sys
from tetris_main import TetrisGame
from main_menu import MainMenu
from level_selector import LevelSelector

def demo_level_system():
    """演示关卡系统"""
    print("关卡系统演示")
    print("=" * 50)
    print("功能说明:")
    print("1. 主菜单: 选择游戏模式")
    print("2. 经典模式: 无限游戏")
    print("3. 关卡模式: 20个精心设计的关卡")
    print("4. 关卡选择: 查看关卡信息和进度")
    print("5. 特殊规则: 旋转限制、时间限制等")
    print("6. 星级评价: 根据表现获得1-3星")
    print("7. 进度保存: 自动保存游戏进度")
    print("=" * 50)
    
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 700))
    pygame.display.set_caption("俄罗斯方块 - 关卡系统演示")
    
    try:
        while True:
            # 显示主菜单
            print("\n显示主菜单...")
            menu = MainMenu(screen)
            choice = menu.run()
            
            if choice == "quit":
                print("退出游戏")
                break
            elif choice == "classic":
                print("进入经典模式")
                game = TetrisGame()
                game.game_state.game_mode = "classic"
                game.run()
            elif choice == "level":
                print("进入关卡模式")
                selector = LevelSelector(screen)
                selected_level = selector.run()
                
                if selected_level and selected_level > 0:
                    print(f"选择关卡 {selected_level}")
                    game = TetrisGame()
                    game.game_state.game_mode = "level"
                    
                    if game.level_manager and game.level_manager.load_level(selected_level):
                        game.game_state.current_level_id = selected_level
                        level_info = game.level_manager.get_level_info()
                        print(f"加载关卡: {level_info['name']}")
                        print(f"目标行数: {level_info['target_lines']}")
                        print(f"速度倍数: {level_info['speed_multiplier']}")
                        print(f"特殊规则: {level_info['special_rules']}")
                        game.run()
                    else:
                        print(f"无法加载关卡 {selected_level}")
                elif selected_level == -1:
                    print("返回主菜单")
                    continue
                else:
                    print("退出游戏")
                    break
    except Exception as e:
        print(f"演示过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__ == "__main__":
    demo_level_system()
