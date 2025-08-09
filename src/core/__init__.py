"""
游戏核心逻辑包
"""
from .board import Board
from .piece import Piece
from .game_state import GameState
from .collision import CollisionDetector
from .score_manager import ScoreManager

# 延迟导入GameEngine避免循环导入
def get_game_engine():
    from .game_engine import GameEngine
    return GameEngine

__all__ = [
    'Board',
    'Piece', 
    'GameState',
    'CollisionDetector',
    'ScoreManager',
    'get_game_engine'
]
