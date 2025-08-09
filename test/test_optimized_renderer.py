#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化渲染器测试程序
"""

import sys
import os
import pygame
import time
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.game_config import GameConfig
from src.ui.optimized_renderer import OptimizedRenderer, TextureCache, FontCache
from src.core.board import Board
from src.core.piece import Piece
from src.core.game_state import GameState
from src.utils.performance_monitor import PerformanceMonitor


class TestOptimizedRenderer(unittest.TestCase):
    """优化渲染器测试类"""
    
    def setUp(self):
        """测试前准备"""
        pygame.init()
        self.config = GameConfig()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        self.renderer = OptimizedRenderer(self.screen, self.config)
        self.board = Board(self.config.BOARD_WIDTH, self.config.BOARD_HEIGHT)
        self.game_state = GameState()
    
    def tearDown(self):
        """测试后清理"""
        pygame.quit()
    
    def test_texture_cache(self):
        """测试纹理缓存"""
        texture_cache = TextureCache(self.config)
        texture_cache.pre_render_pieces()
        
        # 测试所有方块类型都有纹理
        piece_types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        for piece_type in piece_types:
            texture = texture_cache.get_piece_texture(piece_type)
            self.assertIsNotNone(texture)
            self.assertIsInstance(texture, pygame.Surface)
    
    def test_font_cache(self):
        """测试字体缓存"""
        font_cache = FontCache()
        
        # 测试文本缓存
        text1 = font_cache.get_cached_text("Test", (255, 255, 255))
        text2 = font_cache.get_cached_text("Test", (255, 255, 255))
        
        self.assertEqual(text1, text2)  # 应该返回相同的缓存对象
        
        # 测试不同颜色的文本
        text3 = font_cache.get_cached_text("Test", (255, 0, 0))
        self.assertNotEqual(text1, text3)  # 不同颜色应该不同
    
    def test_renderer_initialization(self):
        """测试渲染器初始化"""
        self.assertIsNotNone(self.renderer)
        self.assertIsNotNone(self.renderer.texture_cache)
        self.assertIsNotNone(self.renderer.font_cache)
        self.assertIsNotNone(self.renderer.layered_renderer)
    
    def test_board_rendering(self):
        """测试游戏板渲染"""
        # 在游戏板上放置一些方块
        piece = Piece('I')
        self.board.place_piece(piece, 0, 18)
        
        # 渲染游戏板
        self.renderer.render_board(self.board)
        
        # 验证渲染没有抛出异常
        self.assertTrue(True)
    
    def test_piece_rendering(self):
        """测试方块渲染"""
        piece = Piece('T')
        position = (5, 10)
        
        # 渲染方块
        self.renderer.render_piece(piece, position)
        
        # 验证渲染没有抛出异常
        self.assertTrue(True)
    
    def test_ui_rendering(self):
        """测试UI渲染"""
        # 设置游戏状态
        self.game_state.score = 1000
        self.game_state.level = 5
        self.game_state.lines_cleared = 15
        
        # 渲染UI
        self.renderer.render_ui(self.game_state)
        
        # 验证渲染没有抛出异常
        self.assertTrue(True)
    
    def test_performance_monitoring(self):
        """测试性能监控"""
        monitor = PerformanceMonitor()
        
        # 模拟帧渲染
        start_time = monitor.start_frame()
        time.sleep(0.01)  # 模拟渲染时间
        render_time = monitor.end_frame(start_time)
        
        self.assertGreater(render_time, 0)
        self.assertIsInstance(render_time, float)
    
    def test_render_frame(self):
        """测试完整帧渲染"""
        # 设置游戏状态
        self.game_state.current_piece = Piece('O')
        self.game_state.set_piece_position(5, 10)
        
        # 渲染完整帧
        self.renderer.render_frame()
        
        # 验证渲染没有抛出异常
        self.assertTrue(True)
    
    def test_fps_calculation(self):
        """测试FPS计算"""
        # 模拟多次渲染
        for i in range(10):
            start_time = time.time()
            time.sleep(0.01)  # 模拟渲染时间
            self.renderer.render_times.append(time.time() - start_time)
        
        fps = self.renderer.get_fps()
        self.assertGreater(fps, 0)
        self.assertIsInstance(fps, float)


class PerformanceBenchmark:
    """性能基准测试"""
    
    def __init__(self):
        pygame.init()
        self.config = GameConfig()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
    
    def benchmark_texture_cache(self):
        """基准测试纹理缓存"""
        print("测试纹理缓存性能...")
        
        texture_cache = TextureCache(self.config)
        
        # 测试预渲染时间
        start_time = time.time()
        texture_cache.pre_render_pieces()
        pre_render_time = time.time() - start_time
        
        print(f"纹理预渲染时间: {pre_render_time*1000:.2f}ms")
        
        # 测试纹理获取时间
        piece_types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        start_time = time.time()
        for _ in range(1000):
            for piece_type in piece_types:
                texture = texture_cache.get_piece_texture(piece_type)
        get_time = time.time() - start_time
        
        print(f"1000次纹理获取时间: {get_time*1000:.2f}ms")
        print(f"平均每次获取时间: {get_time/7000*1000:.4f}ms")
    
    def benchmark_font_cache(self):
        """基准测试字体缓存"""
        print("\n测试字体缓存性能...")
        
        font_cache = FontCache()
        
        # 测试文本渲染时间
        texts = ["Score: 1000", "Level: 5", "Lines: 15", "Next:", "GAME OVER!"]
        colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0)]
        
        # 不使用缓存
        start_time = time.time()
        for _ in range(1000):
            for text in texts:
                for color in colors:
                    font_cache.font.render(text, True, color)
        no_cache_time = time.time() - start_time
        
        # 使用缓存
        start_time = time.time()
        for _ in range(1000):
            for text in texts:
                for color in colors:
                    font_cache.get_cached_text(text, color)
        cache_time = time.time() - start_time
        
        print(f"不使用缓存时间: {no_cache_time*1000:.2f}ms")
        print(f"使用缓存时间: {cache_time*1000:.2f}ms")
        print(f"性能提升: {(no_cache_time - cache_time) / no_cache_time * 100:.1f}%")
    
    def benchmark_renderer(self):
        """基准测试渲染器"""
        print("\n测试渲染器性能...")
        
        renderer = OptimizedRenderer(self.screen, self.config)
        board = Board(self.config.BOARD_WIDTH, self.config.BOARD_HEIGHT)
        game_state = GameState()
        
        # 填充游戏板
        for row in range(10):
            for col in range(self.config.BOARD_WIDTH):
                if row % 2 == 0:
                    board.grid[row][col] = (255, 0, 0)
        
        # 测试游戏板渲染
        start_time = time.time()
        for _ in range(100):
            renderer.render_board(board)
        board_render_time = time.time() - start_time
        
        # 测试方块渲染
        piece = Piece('T')
        start_time = time.time()
        for _ in range(100):
            renderer.render_piece(piece, (5, 10))
        piece_render_time = time.time() - start_time
        
        # 测试UI渲染
        game_state.score = 1000
        game_state.level = 5
        start_time = time.time()
        for _ in range(100):
            renderer.render_ui(game_state)
        ui_render_time = time.time() - start_time
        
        print(f"游戏板渲染(100次): {board_render_time*1000:.2f}ms")
        print(f"方块渲染(100次): {piece_render_time*1000:.2f}ms")
        print(f"UI渲染(100次): {ui_render_time*1000:.2f}ms")
        print(f"总渲染时间: {(board_render_time + piece_render_time + ui_render_time)*1000:.2f}ms")
    
    def run_all_benchmarks(self):
        """运行所有基准测试"""
        print("=== 优化渲染器性能基准测试 ===")
        
        self.benchmark_texture_cache()
        self.benchmark_font_cache()
        self.benchmark_renderer()
        
        print("\n基准测试完成！")


def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "benchmark":
        # 运行基准测试
        benchmark = PerformanceBenchmark()
        benchmark.run_all_benchmarks()
    else:
        # 运行单元测试
        unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    main()
