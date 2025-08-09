#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渲染性能测试脚本
对比原始复杂渲染器和当前简化渲染器的性能
"""

import pygame
import time
import statistics
from typing import List, Dict, Tuple
from src.config.game_config import GameConfig
from src.core.board import Board
from src.core.piece import Piece
from src.core.game_state import GameState
from src.utils.constants import BLACK, WHITE, GRAY, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE


class OriginalComplexRenderer:
    """原始复杂渲染器 - 使用层系统和双缓冲"""
    
    def __init__(self, screen: pygame.Surface, config: GameConfig):
        self.screen = screen
        self.config = config
        
        # 创建后缓冲
        self.back_buffer = pygame.Surface(screen.get_size())
        
        # 创建层系统
        self.layers = {
            'background': pygame.Surface(screen.get_size()),
            'board': pygame.Surface(screen.get_size()),
            'pieces': pygame.Surface(screen.get_size()),
            'ui': pygame.Surface(screen.get_size())
        }
        
        # 设置层属性
        for layer in self.layers.values():
            layer.set_alpha(255)
        
        # 字体缓存
        self.font_cache = {}
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # 性能监控
        self.render_times = []
    
    def get_cached_text(self, text: str, color: Tuple[int, int, int], font_size: int = 36) -> pygame.Surface:
        """获取缓存的文本"""
        font = self.font if font_size == 36 else self.small_font
        key = f"{text}_{color}_{font_size}"
        if key not in self.font_cache:
            self.font_cache[key] = font.render(text, True, color)
        return self.font_cache[key]
    
    def render_board(self, board: Board):
        """渲染游戏板到层"""
        layer = self.layers['board']
        layer.fill((0, 0, 0))  # 清除层
        
        # 绘制游戏板背景
        pygame.draw.rect(layer, GRAY, 
                        (self.config.BOARD_X - 2, self.config.BOARD_Y - 2, 
                         self.config.BOARD_WIDTH * self.config.CELL_SIZE + 4, 
                         self.config.BOARD_HEIGHT * self.config.CELL_SIZE + 4))
        
        # 绘制网格
        for row in range(board.height):
            for col in range(board.width):
                x = self.config.BOARD_X + col * self.config.CELL_SIZE
                y = self.config.BOARD_Y + row * self.config.CELL_SIZE
                
                if board.grid[row][col]:
                    pygame.draw.rect(layer, board.grid[row][col],
                                   (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE))
                    pygame.draw.rect(layer, BLACK,
                                   (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE), 1)
                else:
                    pygame.draw.rect(layer, BLACK,
                                   (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE), 1)
    
    def render_piece(self, piece: Piece, position: Tuple[int, int]):
        """渲染方块到层"""
        if not piece:
            return
        
        layer = self.layers['pieces']
        layer.fill((0, 0, 0))  # 清除层
        
        x, y = position
        
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[0])):
                if piece.shape[row][col]:
                    screen_x = self.config.BOARD_X + (x + col) * self.config.CELL_SIZE
                    screen_y = self.config.BOARD_Y + (y + row) * self.config.CELL_SIZE
                    pygame.draw.rect(layer, piece.color,
                                   (screen_x, screen_y, self.config.CELL_SIZE, self.config.CELL_SIZE))
                    pygame.draw.rect(layer, BLACK,
                                   (screen_x, screen_y, self.config.CELL_SIZE, self.config.CELL_SIZE), 1)
    
    def render_ui(self, game_state: GameState):
        """渲染UI到层"""
        layer = self.layers['ui']
        layer.fill((0, 0, 0))  # 清除层
        
        # 绘制分数
        score_text = self.get_cached_text(f"Score: {game_state.score}", WHITE)
        layer.blit(score_text, (50, 50))
        
        # 绘制等级
        level_text = self.get_cached_text(f"Level: {game_state.level}", WHITE)
        layer.blit(level_text, (50, 100))
        
        # 绘制已消除行数
        lines_text = self.get_cached_text(f"Lines: {game_state.lines_cleared}", WHITE)
        layer.blit(lines_text, (50, 150))
        
        # 绘制下一个方块预览
        if game_state.next_piece:
            next_text = self.get_cached_text("Next:", WHITE)
            layer.blit(next_text, (50, 350))
            
            preview_x = 50
            preview_y = 400
            for row in range(len(game_state.next_piece.shape)):
                for col in range(len(game_state.next_piece.shape[0])):
                    if game_state.next_piece.shape[row][col]:
                        x = preview_x + col * 20
                        y = preview_y + row * 20
                        pygame.draw.rect(layer, game_state.next_piece.color,
                                       (x, y, 20, 20))
                        pygame.draw.rect(layer, BLACK, (x, y, 20, 20), 1)
    
    def render_frame(self):
        """渲染完整帧 - 层合成"""
        start_time = time.time()
        
        # 清除后缓冲
        self.back_buffer.fill(BLACK)
        
        # 合成所有层到后缓冲
        for layer_name in ['background', 'board', 'pieces', 'ui']:
            self.back_buffer.blit(self.layers[layer_name], (0, 0))
        
        # 将后缓冲复制到屏幕
        self.screen.blit(self.back_buffer, (0, 0))
        
        # 更新显示
        pygame.display.flip()
        
        # 记录渲染时间
        render_time = time.time() - start_time
        self.render_times.append(render_time)
        
        if len(self.render_times) > 100:
            self.render_times.pop(0)
    
    def get_average_render_time(self) -> float:
        """获取平均渲染时间"""
        if self.render_times:
            return sum(self.render_times) / len(self.render_times)
        return 0.0
    
    def get_fps(self) -> float:
        """获取当前FPS"""
        if len(self.render_times) >= 2:
            return 1.0 / self.get_average_render_time()
        return 0.0


class CurrentSimpleRenderer:
    """当前简化渲染器 - 直接渲染到屏幕"""
    
    def __init__(self, screen: pygame.Surface, config: GameConfig):
        self.screen = screen
        self.config = config
        
        # 字体缓存
        self.font_cache = {}
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # 性能监控
        self.render_times = []
    
    def get_cached_text(self, text: str, color: Tuple[int, int, int], font_size: int = 36) -> pygame.Surface:
        """获取缓存的文本"""
        font = self.font if font_size == 36 else self.small_font
        key = f"{text}_{color}_{font_size}"
        if key not in self.font_cache:
            self.font_cache[key] = font.render(text, True, color)
        return self.font_cache[key]
    
    def render_board(self, board: Board):
        """渲染游戏板"""
        # 绘制游戏板背景
        pygame.draw.rect(self.screen, GRAY, 
                        (self.config.BOARD_X - 2, self.config.BOARD_Y - 2, 
                         self.config.BOARD_WIDTH * self.config.CELL_SIZE + 4, 
                         self.config.BOARD_HEIGHT * self.config.CELL_SIZE + 4))
        
        # 绘制网格
        for row in range(board.height):
            for col in range(board.width):
                x = self.config.BOARD_X + col * self.config.CELL_SIZE
                y = self.config.BOARD_Y + row * self.config.CELL_SIZE
                
                if board.grid[row][col]:
                    pygame.draw.rect(self.screen, board.grid[row][col],
                                   (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK,
                                   (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE), 1)
                else:
                    pygame.draw.rect(self.screen, BLACK,
                                   (x, y, self.config.CELL_SIZE, self.config.CELL_SIZE), 1)
    
    def render_piece(self, piece: Piece, position: Tuple[int, int]):
        """渲染方块"""
        if not piece:
            return
        
        x, y = position
        
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[0])):
                if piece.shape[row][col]:
                    screen_x = self.config.BOARD_X + (x + col) * self.config.CELL_SIZE
                    screen_y = self.config.BOARD_Y + (y + row) * self.config.CELL_SIZE
                    pygame.draw.rect(self.screen, piece.color,
                                   (screen_x, screen_y, self.config.CELL_SIZE, self.config.CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK,
                                   (screen_x, screen_y, self.config.CELL_SIZE, self.config.CELL_SIZE), 1)
    
    def render_ui(self, game_state: GameState):
        """渲染用户界面"""
        # 绘制分数
        score_text = self.get_cached_text(f"Score: {game_state.score}", WHITE)
        self.screen.blit(score_text, (50, 50))
        
        # 绘制等级
        level_text = self.get_cached_text(f"Level: {game_state.level}", WHITE)
        self.screen.blit(level_text, (50, 100))
        
        # 绘制已消除行数
        lines_text = self.get_cached_text(f"Lines: {game_state.lines_cleared}", WHITE)
        self.screen.blit(lines_text, (50, 150))
        
        # 绘制下一个方块预览
        if game_state.next_piece:
            next_text = self.get_cached_text("Next:", WHITE)
            self.screen.blit(next_text, (50, 350))
            
            preview_x = 50
            preview_y = 400
            for row in range(len(game_state.next_piece.shape)):
                for col in range(len(game_state.next_piece.shape[0])):
                    if game_state.next_piece.shape[row][col]:
                        x = preview_x + col * 20
                        y = preview_y + row * 20
                        pygame.draw.rect(self.screen, game_state.next_piece.color,
                                       (x, y, 20, 20))
                        pygame.draw.rect(self.screen, BLACK, (x, y, 20, 20), 1)
    
    def render_frame(self):
        """渲染完整帧"""
        start_time = time.time()
        
        # 更新显示
        pygame.display.flip()
        
        # 记录渲染时间
        render_time = time.time() - start_time
        self.render_times.append(render_time)
        
        if len(self.render_times) > 100:
            self.render_times.pop(0)
    
    def get_average_render_time(self) -> float:
        """获取平均渲染时间"""
        if self.render_times:
            return sum(self.render_times) / len(self.render_times)
        return 0.0
    
    def get_fps(self) -> float:
        """获取当前FPS"""
        if len(self.render_times) >= 2:
            return 1.0 / self.get_average_render_time()
        return 0.0


def create_test_data():
    """创建测试数据"""
    config = GameConfig()
    board = Board(config.BOARD_WIDTH, config.BOARD_HEIGHT)
    
    # 创建一些测试方块
    piece = Piece('O')  # O型方块
    piece.color = BLUE
    
    next_piece = Piece('T')  # T型方块
    next_piece.color = RED
    
    # 创建游戏状态
    game_state = GameState()
    game_state.score = 1250
    game_state.level = 3
    game_state.lines_cleared = 15
    game_state.next_piece = next_piece
    
    return config, board, piece, game_state


def run_performance_test(renderer_class, renderer_name: str, test_duration: int = 10) -> Dict:
    """运行性能测试"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(f"性能测试 - {renderer_name}")
    
    config, board, piece, game_state = create_test_data()
    renderer = renderer_class(screen, config)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    frame_count = 0
    
    print(f"开始测试 {renderer_name}...")
    
    while time.time() - start_time < test_duration:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        
        # 清除屏幕
        screen.fill(BLACK)
        
        # 渲染测试
        renderer.render_board(board)
        renderer.render_piece(piece, (5, 5))
        renderer.render_ui(game_state)
        renderer.render_frame()
        
        frame_count += 1
        clock.tick(60)
    
    pygame.quit()
    
    # 计算统计数据
    render_times = renderer.render_times
    if render_times:
        avg_render_time = statistics.mean(render_times)
        min_render_time = min(render_times)
        max_render_time = max(render_times)
        std_dev = statistics.stdev(render_times) if len(render_times) > 1 else 0
        fps = frame_count / test_duration
    else:
        avg_render_time = min_render_time = max_render_time = std_dev = fps = 0
    
    return {
        'name': renderer_name,
        'frame_count': frame_count,
        'test_duration': test_duration,
        'avg_render_time': avg_render_time * 1000,  # 转换为毫秒
        'min_render_time': min_render_time * 1000,
        'max_render_time': max_render_time * 1000,
        'std_dev': std_dev * 1000,
        'fps': fps,
        'render_times': render_times
    }


def main():
    """主测试函数"""
    print("开始渲染性能对比测试...")
    print("=" * 50)
    
    # 测试参数
    test_duration = 15  # 每个渲染器测试15秒
    
    # 运行测试
    results = []
    
    # 测试原始复杂渲染器
    try:
        original_result = run_performance_test(OriginalComplexRenderer, "原始复杂渲染器", test_duration)
        results.append(original_result)
    except Exception as e:
        print(f"原始渲染器测试失败: {e}")
    
    # 测试当前简化渲染器
    try:
        current_result = run_performance_test(CurrentSimpleRenderer, "当前简化渲染器", test_duration)
        results.append(current_result)
    except Exception as e:
        print(f"当前渲染器测试失败: {e}")
    
    # 输出结果
    print("\n" + "=" * 50)
    print("性能测试结果:")
    print("=" * 50)
    
    for result in results:
        print(f"\n{result['name']}:")
        print(f"  测试时长: {result['test_duration']}秒")
        print(f"  总帧数: {result['frame_count']}")
        print(f"  平均FPS: {result['fps']:.2f}")
        print(f"  平均渲染时间: {result['avg_render_time']:.3f}ms")
        print(f"  最小渲染时间: {result['min_render_time']:.3f}ms")
        print(f"  最大渲染时间: {result['max_render_time']:.3f}ms")
        print(f"  标准差: {result['std_dev']:.3f}ms")
    
    # 性能对比
    if len(results) == 2:
        original = results[0]
        current = results[1]
        
        fps_improvement = ((current['fps'] - original['fps']) / original['fps']) * 100
        render_time_improvement = ((original['avg_render_time'] - current['avg_render_time']) / original['avg_render_time']) * 100
        
        print("\n" + "=" * 50)
        print("性能对比:")
        print("=" * 50)
        print(f"FPS提升: {fps_improvement:+.2f}%")
        print(f"渲染时间减少: {render_time_improvement:+.2f}%")
        
        if fps_improvement > 0:
            print("✅ 简化渲染器性能更优")
        else:
            print("❌ 原始渲染器性能更优")
    
    return results


if __name__ == "__main__":
    main()
