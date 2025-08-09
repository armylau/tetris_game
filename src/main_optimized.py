#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏主程序 - 优化渲染版本
使用优化渲染系统，提供更好的性能
"""

import pygame
import sys
import time
from src.config.game_config import GameConfig
from src.core.optimized_game_engine import OptimizedGameEngine
from src.ui.optimized_renderer import OptimizedRenderer
from src.ui.input_handler import InputHandler


class OptimizedTetrisGame:
    """俄罗斯方块游戏主类 - 优化版本"""
    
    def __init__(self, screen=None):
        self.config = GameConfig()
        
        # 如果提供了屏幕，使用它；否则创建新的
        if screen is not None:
            self.screen = screen
        else:
            pygame.init()
            self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            pygame.display.set_caption("Tetris Game - Optimized")
        
        self.clock = pygame.time.Clock()
        
        # 初始化优化游戏引擎（包含优化渲染器）
        self.game_engine = OptimizedGameEngine(self.screen, self.config)
        self.input_handler = InputHandler(self.config)
        
        self.running = True
        self.return_to_menu = False
        
        # 性能监控设置
        self.show_performance_metrics = False
        
        # 不在这里初始化游戏，等待用户选择模式后再初始化
    
    def handle_input(self):
        """处理用户输入"""
        events = self.input_handler.handle_events()
        
        for event in events:
            if event.event_type == "quit":
                self.running = False
            
            elif event.event_type == "move_left":
                self.game_engine.move_piece(-1, 0)
            
            elif event.event_type == "move_right":
                self.game_engine.move_piece(1, 0)
            
            elif event.event_type == "move_down":
                self.game_engine.move_piece(0, 1)
            
            elif event.event_type == "rotate":
                self.game_engine.rotate_piece()
            
            elif event.event_type == "toggle_pause":
                self.game_engine.game_state.paused = not self.game_engine.game_state.paused
            
            elif event.event_type == "reset_game":
                self.game_engine.reset_game()
            
            elif event.event_type == "return_to_menu":
                self.return_to_menu = True
                self.running = False
            
            # 优化渲染系统的特殊快捷键
            elif event.event_type == "toggle_performance":
                self.show_performance_metrics = not self.show_performance_metrics
                self.game_engine.performance_monitor.show_metrics = self.show_performance_metrics
            
            elif event.event_type == "export_performance":
                self.game_engine.performance_monitor.export_metrics("performance_metrics.csv")
                print("性能指标已导出到 performance_metrics.csv")
    
    def update(self):
        """更新游戏状态"""
        delta_time = self.clock.get_time() / 1000.0  # 转换为秒
        self.game_engine.update(delta_time)
    
    def render(self):
        """渲染游戏画面 - 使用优化渲染系统"""
        # 使用优化游戏引擎的渲染方法
        self.game_engine.render()
    
    def run(self):
        """主游戏循环"""
        print("启动优化渲染系统...")
        print("快捷键:")
        print("  F3: 切换性能指标显示")
        print("  F4: 导出性能指标")
        print("  ESC: 返回主菜单")
        print("  P: 暂停/继续游戏")
        print("  R: 重置游戏")
        
        while self.running:
            try:
                self.handle_input()
                self.update()
                self.render()
                self.clock.tick(self.config.TARGET_FPS)
                
                # 定期显示性能信息（可选）
                if self.show_performance_metrics:
                    fps = self.game_engine.get_performance_summary().get('current_fps', 0)
                    if fps > 0:
                        print(f"\r当前FPS: {fps:.1f}", end="", flush=True)
                
            except Exception as e:
                print(f"游戏循环出错: {e}")
                import traceback
                traceback.print_exc()
                break
        
        # 显示最终性能统计
        if hasattr(self.game_engine, 'get_performance_summary'):
            summary = self.game_engine.get_performance_summary()
            print(f"\n游戏结束 - 性能统计:")
            print(f"  平均FPS: {summary.get('average_fps', 0):.1f}")
            print(f"  平均渲染时间: {summary.get('average_render_time', 0)*1000:.2f}ms")
            print(f"  最高FPS: {summary.get('max_fps', 0):.1f}")
            print(f"  最低FPS: {summary.get('min_fps', 0):.1f}")
        
        # 返回是否应该回到主菜单
        return self.return_to_menu
    
    def start_game(self):
        """开始游戏"""
        self.game_engine.spawn_new_piece()


def main():
    """主函数"""
    print("开始启动优化版游戏...")
    pygame.init()
    screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
    pygame.display.set_caption("俄罗斯方块 - 优化版")
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
                game = OptimizedTetrisGame(screen)
                game.game_engine.game_state.game_mode = "classic"
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
                    game = OptimizedTetrisGame(screen)
                    game.game_engine.game_state.game_mode = "level"
                    
                    # 确保关卡管理器已初始化
                    if not game.game_engine.level_manager:
                        try:
                            from src.level.level_manager import LevelManager
                            game.game_engine.level_manager = LevelManager()
                        except ImportError:
                            print("无法初始化关卡管理器")
                            continue
                    
                    if game.game_engine.level_manager.load_level(selected_level):
                        game.game_engine.game_state.current_level_id = selected_level
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
        game = OptimizedTetrisGame(screen)
        game.game_engine.game_state.game_mode = "classic"
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
