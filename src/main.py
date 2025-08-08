#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏主程序
重构后的模块化版本
"""

import pygame
import sys
import time
from src.config.game_config import GameConfig
from src.core.game_engine import GameEngine
from src.ui.renderer import Renderer
from src.ui.input_handler import InputHandler


class TetrisGame:
    """俄罗斯方块游戏主类"""
    
    def __init__(self):
        pygame.init()
        self.config = GameConfig()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris Game")
        self.clock = pygame.time.Clock()
        
        # 初始化游戏组件
        self.game_engine = GameEngine(self.config)
        self.renderer = Renderer(self.screen, self.config)
        self.input_handler = InputHandler(self.config)
        
        self.running = True
        self.return_to_menu = False
        
        # 不在这里初始化游戏，等待用户选择模式后再初始化
    
    def handle_input(self):
        """处理用户输入"""
        events = self.input_handler.handle_events()
        
        for event in events:
            if event.event_type == "quit":
                self.running = False
            
            elif event.event_type == "move_left":
                self.game_engine.handle_piece_movement(-1, 0)
            
            elif event.event_type == "move_right":
                self.game_engine.handle_piece_movement(1, 0)
            
            elif event.event_type == "move_down":
                self.game_engine.handle_piece_movement(0, 1)
            
            elif event.event_type == "rotate":
                self.game_engine.handle_piece_rotation()
            
            elif event.event_type == "toggle_pause":
                self.game_engine.get_game_state().paused = not self.game_engine.get_game_state().paused
            
            elif event.event_type == "reset_game":
                self.game_engine.reset_game()
            
            elif event.event_type == "return_to_menu":
                self.return_to_menu = True
                self.running = False
    
    def update(self):
        """更新游戏状态"""
        delta_time = self.clock.get_time() / 1000.0  # 转换为秒
        self.game_engine.update(delta_time)
    
    def render(self):
        """渲染游戏画面"""
        self.screen.fill((0, 0, 0))  # 黑色背景
        
        # 渲染游戏板
        self.renderer.render_board(self.game_engine.get_board())
        
        # 渲染当前方块
        game_state = self.game_engine.get_game_state()
        if game_state.current_piece:
            self.renderer.render_piece(game_state.current_piece, game_state.get_piece_position())
        
        # 渲染用户界面
        self.renderer.render_ui(game_state)
        
        pygame.display.flip()
    
    def run(self):
        """主游戏循环"""
        while self.running:
            try:
                self.handle_input()
                self.update()
                self.render()
                self.clock.tick(self.config.TARGET_FPS)
            except Exception as e:
                print(f"游戏循环出错: {e}")
                import traceback
                traceback.print_exc()
                break
        
        # 返回是否应该回到主菜单
        return self.return_to_menu
    
    def start_game(self):
        """开始游戏"""
        self.game_engine.spawn_new_piece()


def main():
    """主函数"""
    print("开始启动游戏...")
    pygame.init()
    screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
    pygame.display.set_caption("俄罗斯方块")
    print("✓ 游戏窗口创建成功")
    
    try:
        print("正在导入主菜单模块...")
        from src.ui.main_menu import MainMenu
        print("✓ 主菜单模块导入成功")
        
        print("正在导入关卡选择器模块...")
        from src.level.level_selector import LevelSelector
        print("✓ 关卡选择器模块导入成功")
        
        print("开始主游戏循环...")
        while True:
            print("显示主菜单...")
            # 显示主菜单
            menu = MainMenu(screen)
            print("✓ 主菜单创建成功")
            
            print("等待用户选择...")
            choice = menu.run()
            print(f"用户选择: {choice}")
            
            if choice == "quit":
                print("用户选择退出")
                break
            elif choice == "classic":
                print("用户选择经典模式")
                # 经典模式
                game = TetrisGame()
                game.game_engine.get_game_state().game_mode = "classic"
                game.start_game()  # 开始游戏
                should_return_to_menu = game.run()
                if not should_return_to_menu:
                    print("游戏结束，退出程序")
                    break  # 如果游戏没有要求返回菜单，则退出程序
            elif choice == "level":
                print("用户选择关卡模式")
                # 关卡模式
                selector = LevelSelector(screen)
                selected_level = selector.run()
                print(f"选择的关卡: {selected_level}")
                
                if selected_level and selected_level > 0:
                    # 加载选中的关卡
                    game = TetrisGame()
                    game.game_engine.get_game_state().game_mode = "level"
                    
                    if game.game_engine.level_manager and game.game_engine.level_manager.load_level(selected_level):
                        game.game_engine.get_game_state().current_level_id = selected_level
                        game.start_game()  # 开始游戏
                        should_return_to_menu = game.run()
                        if not should_return_to_menu:
                            print("关卡游戏结束，退出程序")
                            break  # 如果游戏没有要求返回菜单，则退出程序
                    else:
                        print(f"无法加载关卡 {selected_level}")
                elif selected_level == -1:
                    print("用户返回主菜单")
                    # 返回主菜单
                    continue
                else:
                    print("用户退出游戏")
                    # 退出游戏
                    break
    except ImportError as e:
        print(f"导入模块失败: {e}")
        import traceback
        traceback.print_exc()
        # 回退到经典模式
        print("回退到经典模式")
        game = TetrisGame()
        game.game_engine.get_game_state().game_mode = "classic"
        game.start_game()  # 开始游戏
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
    
    print("游戏结束，正在退出...")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
