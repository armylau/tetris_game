#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能监控器 - 监控游戏性能和渲染统计
"""

import time
import psutil
import pygame
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class PerformanceMetrics:
    """性能指标数据类"""
    fps: float
    render_time: float
    cpu_usage: float
    memory_usage: float
    frame_count: int
    timestamp: float


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.max_history_size = 1000
        
        # 性能统计
        self.frame_count = 0
        self.last_fps_update = time.time()
        self.fps_history: List[float] = []
        self.render_times: List[float] = []
        
        # 进程信息
        self.process = psutil.Process()
        
        # 显示设置
        self.show_metrics = False
        self.font = pygame.font.Font(None, 24)
    
    def start_frame(self) -> float:
        """开始帧计时"""
        return time.time()
    
    def end_frame(self, start_time: float) -> float:
        """结束帧计时并记录性能数据"""
        end_time = time.time()
        render_time = end_time - start_time
        
        # 记录渲染时间
        self.render_times.append(render_time)
        if len(self.render_times) > 100:
            self.render_times.pop(0)
        
        # 更新帧计数
        self.frame_count += 1
        
        # 每秒更新一次FPS
        if end_time - self.last_fps_update >= 1.0:
            current_fps = self.frame_count / (end_time - self.last_fps_update)
            self.fps_history.append(current_fps)
            if len(self.fps_history) > 100:
                self.fps_history.pop(0)
            
            self.frame_count = 0
            self.last_fps_update = end_time
        
        # 记录性能指标
        metrics = PerformanceMetrics(
            fps=self.get_current_fps(),
            render_time=render_time,
            cpu_usage=self.get_cpu_usage(),
            memory_usage=self.get_memory_usage(),
            frame_count=self.frame_count,
            timestamp=end_time
        )
        
        self.metrics_history.append(metrics)
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history.pop(0)
        
        return render_time
    
    def get_current_fps(self) -> float:
        """获取当前FPS"""
        if self.fps_history:
            return self.fps_history[-1]
        return 0.0
    
    def get_average_fps(self) -> float:
        """获取平均FPS"""
        if self.fps_history:
            return sum(self.fps_history) / len(self.fps_history)
        return 0.0
    
    def get_average_render_time(self) -> float:
        """获取平均渲染时间"""
        if self.render_times:
            return sum(self.render_times) / len(self.render_times)
        return 0.0
    
    def get_cpu_usage(self) -> float:
        """获取CPU使用率"""
        try:
            return self.process.cpu_percent()
        except:
            return 0.0
    
    def get_memory_usage(self) -> float:
        """获取内存使用率"""
        try:
            memory_info = self.process.memory_info()
            return memory_info.rss / 1024 / 1024  # MB
        except:
            return 0.0
    
    def get_performance_summary(self) -> Dict[str, float]:
        """获取性能摘要"""
        return {
            'current_fps': self.get_current_fps(),
            'average_fps': self.get_average_fps(),
            'average_render_time': self.get_average_render_time(),
            'cpu_usage': self.get_cpu_usage(),
            'memory_usage_mb': self.get_memory_usage(),
            'min_fps': min(self.fps_history) if self.fps_history else 0.0,
            'max_fps': max(self.fps_history) if self.fps_history else 0.0,
            'min_render_time': min(self.render_times) if self.render_times else 0.0,
            'max_render_time': max(self.render_times) if self.render_times else 0.0
        }
    
    def render_metrics(self, surface: pygame.Surface, x: int = 10, y: int = 10):
        """渲染性能指标到屏幕"""
        if not self.show_metrics:
            return
        
        summary = self.get_performance_summary()
        
        metrics_texts = [
            f"FPS: {summary['current_fps']:.1f}",
            f"Avg FPS: {summary['average_fps']:.1f}",
            f"Render Time: {summary['average_render_time']*1000:.2f}ms",
            f"CPU: {summary['cpu_usage']:.1f}%",
            f"Memory: {summary['memory_usage_mb']:.1f}MB",
            f"Min FPS: {summary['min_fps']:.1f}",
            f"Max FPS: {summary['max_fps']:.1f}"
        ]
        
        # 绘制背景
        bg_rect = pygame.Rect(x, y, 200, len(metrics_texts) * 25 + 10)
        pygame.draw.rect(surface, (0, 0, 0, 128), bg_rect)
        pygame.draw.rect(surface, (255, 255, 255), bg_rect, 1)
        
        # 绘制文本
        for i, text in enumerate(metrics_texts):
            text_surface = self.font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (x + 5, y + 5 + i * 25))
    
    def toggle_metrics_display(self):
        """切换性能指标显示"""
        self.show_metrics = not self.show_metrics
    
    def export_metrics(self, filename: str):
        """导出性能指标到文件"""
        try:
            with open(filename, 'w') as f:
                f.write("Timestamp,FPS,RenderTime,CPU,Memory\n")
                for metrics in self.metrics_history:
                    f.write(f"{metrics.timestamp},{metrics.fps},{metrics.render_time},{metrics.cpu_usage},{metrics.memory_usage}\n")
        except Exception as e:
            print(f"导出性能指标失败: {e}")
    
    def get_recent_metrics(self, count: int = 100) -> List[PerformanceMetrics]:
        """获取最近的性能指标"""
        return self.metrics_history[-count:] if self.metrics_history else []
    
    def clear_history(self):
        """清除历史数据"""
        self.metrics_history.clear()
        self.fps_history.clear()
        self.render_times.clear()


class RenderProfiler:
    """渲染性能分析器"""
    
    def __init__(self):
        self.render_calls: Dict[str, List[float]] = {}
        self.current_frame_calls: Dict[str, float] = {}
    
    def start_render_call(self, call_name: str) -> float:
        """开始渲染调用计时"""
        return time.time()
    
    def end_render_call(self, call_name: str, start_time: float):
        """结束渲染调用计时"""
        duration = time.time() - start_time
        
        if call_name not in self.render_calls:
            self.render_calls[call_name] = []
        
        self.render_calls[call_name].append(duration)
        
        # 保持最近100次调用
        if len(self.render_calls[call_name]) > 100:
            self.render_calls[call_name].pop(0)
    
    def get_render_call_stats(self, call_name: str) -> Dict[str, float]:
        """获取渲染调用统计"""
        if call_name not in self.render_calls:
            return {}
        
        times = self.render_calls[call_name]
        if not times:
            return {}
        
        return {
            'average': sum(times) / len(times),
            'min': min(times),
            'max': max(times),
            'count': len(times)
        }
    
    def get_all_render_stats(self) -> Dict[str, Dict[str, float]]:
        """获取所有渲染调用统计"""
        stats = {}
        for call_name in self.render_calls:
            stats[call_name] = self.get_render_call_stats(call_name)
        return stats
    
    def render_profiler_info(self, surface: pygame.Surface, x: int = 10, y: int = 200):
        """渲染性能分析信息"""
        stats = self.get_all_render_stats()
        if not stats:
            return
        
        font = pygame.font.Font(None, 20)
        
        # 绘制背景
        bg_height = len(stats) * 30 + 20
        bg_rect = pygame.Rect(x, y, 300, bg_height)
        pygame.draw.rect(surface, (0, 0, 0, 128), bg_rect)
        pygame.draw.rect(surface, (255, 255, 255), bg_rect, 1)
        
        # 绘制标题
        title = font.render("Render Profiler", True, (255, 255, 255))
        surface.blit(title, (x + 5, y + 5))
        
        # 绘制统计信息
        y_offset = 30
        for call_name, call_stats in stats.items():
            text = f"{call_name}: {call_stats['average']*1000:.2f}ms"
            text_surface = font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (x + 5, y + y_offset))
            y_offset += 25
