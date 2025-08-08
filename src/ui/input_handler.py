#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输入处理器 - 负责用户输入处理
"""

import time
import pygame
from typing import List, Set
from src.config.game_config import GameConfig


class GameEvent:
    """游戏事件类"""
    
    def __init__(self, event_type: str, **kwargs):
        self.event_type = event_type
        self.kwargs = kwargs


class InputHandler:
    """输入处理器 - 负责用户输入处理"""
    
    def __init__(self, config: GameConfig):
        self.config = config
        self.keys_pressed: Set[int] = set()
        self.last_key_time = {}
        self.key_repeat_delay = config.KEY_REPEAT_DELAY
        self.key_repeat_interval = config.KEY_REPEAT_INTERVAL
        
        # 向下键加速相关变量
        self.down_key_start_time = 0
        self.down_key_last_move_time = 0
        self.down_key_acceleration_start = config.DOWN_KEY_ACCELERATION_START
        self.down_key_acceleration_max = config.DOWN_KEY_ACCELERATION_MAX
        self.down_key_min_interval = config.DOWN_KEY_MIN_INTERVAL
        self.down_key_max_interval = config.DOWN_KEY_MAX_INTERVAL
    
    def handle_events(self) -> List[GameEvent]:
        """处理输入事件"""
        events = []
        current_time = time.time() * 1000  # 转换为毫秒
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.append(GameEvent("quit"))
            
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.last_key_time[event.key] = current_time
                
                # 处理单次按键事件
                if event.key == pygame.K_LEFT:
                    events.append(GameEvent("move_left"))
                elif event.key == pygame.K_RIGHT:
                    events.append(GameEvent("move_right"))
                elif event.key == pygame.K_DOWN:
                    events.append(GameEvent("move_down"))
                    self.down_key_start_time = current_time
                    self.down_key_last_move_time = current_time
                elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    events.append(GameEvent("rotate"))
                elif event.key == pygame.K_p:
                    events.append(GameEvent("toggle_pause"))
                elif event.key == pygame.K_r:
                    events.append(GameEvent("reset_game"))
                elif event.key == pygame.K_ESCAPE:
                    events.append(GameEvent("return_to_menu"))
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
                if event.key in self.last_key_time:
                    del self.last_key_time[event.key]
                
                # 重置向下键加速相关变量
                if event.key == pygame.K_DOWN:
                    self.down_key_start_time = 0
                    self.down_key_last_move_time = 0
        
        # 处理连续输入
        continuous_events = self.handle_continuous_input(current_time)
        events.extend(continuous_events)
        
        return events
    
    def handle_continuous_input(self, current_time: float) -> List[GameEvent]:
        """处理连续输入"""
        events = []
        
        # 处理左右移动的连续按键
        if pygame.K_LEFT in self.keys_pressed:
            if (current_time - self.last_key_time.get(pygame.K_LEFT, 0) > 
                self.key_repeat_delay):
                if (current_time - self.last_key_time.get(pygame.K_LEFT, 0) > 
                    self.key_repeat_interval):
                    events.append(GameEvent("move_left"))
                    self.last_key_time[pygame.K_LEFT] = current_time
        
        if pygame.K_RIGHT in self.keys_pressed:
            if (current_time - self.last_key_time.get(pygame.K_RIGHT, 0) > 
                self.key_repeat_delay):
                if (current_time - self.last_key_time.get(pygame.K_RIGHT, 0) > 
                    self.key_repeat_interval):
                    events.append(GameEvent("move_right"))
                    self.last_key_time[pygame.K_RIGHT] = current_time
        
        # 处理向下加速的连续按键
        if pygame.K_DOWN in self.keys_pressed:
            # 计算按键持续时间
            hold_duration = current_time - self.down_key_start_time
            
            # 如果超过开始加速的时间
            if hold_duration > self.down_key_acceleration_start:
                # 计算加速后的间隔时间（线性插值）
                if hold_duration >= self.down_key_acceleration_max:
                    # 达到最大加速
                    interval = self.down_key_min_interval
                else:
                    # 线性插值计算间隔
                    progress = (hold_duration - self.down_key_acceleration_start) / (self.down_key_acceleration_max - self.down_key_acceleration_start)
                    interval = self.down_key_max_interval - (self.down_key_max_interval - self.down_key_min_interval) * progress
                
                # 检查是否到了移动时间
                if current_time - self.down_key_last_move_time >= interval:
                    events.append(GameEvent("move_down"))
                    self.down_key_last_move_time = current_time
        
        return events
    
    def is_key_pressed(self, key: int) -> bool:
        """检查按键状态"""
        return key in self.keys_pressed
