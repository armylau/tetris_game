"""
游戏核心逻辑包
"""
from .board import Board
from .piece import Piece
from .game_state import GameState
from .collision import CollisionDetector

# 延迟导入GameEngine避免循环导入
def get_game_engine():
    from .game_engine import GameEngine
    return GameEngine

__all__ = [
    'Board',
    'Piece', 
    'GameState',
    'CollisionDetector',
    'get_game_engine'
]
