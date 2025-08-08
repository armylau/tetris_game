# Python Import 优化方案

## 当前问题分析

通过分析项目代码，发现以下import相关问题：

### 1. 相对导入不一致
- 有些文件使用相对导入 (`from ..config.game_config import GameConfig`)
- 有些文件使用绝对导入 (`from core.board import Board`)
- 测试文件中混合使用两种方式

### 2. 路径管理混乱
- 测试文件需要手动添加路径：`sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))`
- 不同目录下的文件导入方式不一致

### 3. 异常处理不当
- 使用try-except处理可选导入，但fallback方案不完善
- 字体管理器导入失败时的处理方式不够优雅

### 4. 循环导入风险
- 模块间可能存在循环依赖
- 缺少清晰的依赖层次结构

## 优化方案

### 1. 统一导入规范

#### 1.1 创建 `__init__.py` 文件
确保每个包目录都有 `__init__.py` 文件，明确包的边界：

```python
# src/__init__.py
"""
俄罗斯方块游戏主包
"""

# src/core/__init__.py
"""
游戏核心逻辑包
"""
from .board import Board
from .piece import Piece
from .game_state import GameState
from .game_engine import GameEngine
from .collision import CollisionDetector

__all__ = [
    'Board',
    'Piece', 
    'GameState',
    'GameEngine',
    'CollisionDetector'
]

# src/config/__init__.py
"""
配置管理包
"""
from .game_config import GameConfig
from .level_config import LevelConfig

__all__ = ['GameConfig', 'LevelConfig']

# src/ui/__init__.py
"""
用户界面包
"""
from .renderer import Renderer
from .input_handler import InputHandler
from .main_menu import MainMenu

__all__ = ['Renderer', 'InputHandler', 'MainMenu']

# src/utils/__init__.py
"""
工具包
"""
from .constants import *
from .font_utils import FontManager

__all__ = ['FontManager']
```

#### 1.2 统一使用绝对导入
所有模块内部使用绝对导入，避免相对导入的复杂性：

```python
# 推荐方式
from src.core.board import Board
from src.core.piece import Piece
from src.config.game_config import GameConfig
from src.utils.constants import PIECE_SHAPES

# 避免使用
from ..config.game_config import GameConfig  # 不推荐
from core.board import Board  # 不推荐
```

### 2. 路径管理优化

#### 2.1 创建 `setup.py`
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="tetris_game",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
        ]
    }
)
```

#### 2.2 创建 `conftest.py`
```python
# test/conftest.py
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

#### 2.3 更新测试文件
移除所有测试文件中的手动路径添加：

```python
# test/test_board.py (优化后)
import unittest
from src.core.board import Board
from src.core.piece import Piece

class TestBoard(unittest.TestCase):
    # 测试代码...
```

### 3. 依赖注入和延迟导入

#### 3.1 使用依赖注入
```python
# src/core/game_engine.py (优化后)
import time
import random
from typing import Optional, List
from src.core.board import Board
from src.core.game_state import GameState
from src.core.piece import Piece
from src.core.collision import CollisionDetector
from src.config.game_config import GameConfig
from src.utils.constants import PIECE_SHAPES

class GameEngine:
    def __init__(self, config: GameConfig, level_manager=None):
        self.config = config
        self.board = Board(config.BOARD_WIDTH, config.BOARD_HEIGHT)
        self.game_state = GameState()
        self.collision_detector = CollisionDetector()
        self.last_drop_time = time.time()
        
        # 通过依赖注入传入，避免循环导入
        self.level_manager = level_manager
```

#### 3.2 延迟导入
```python
# src/ui/renderer.py (优化后)
import pygame
from typing import Tuple
from src.core.board import Board
from src.core.piece import Piece
from src.core.game_state import GameState
from src.config.game_config import GameConfig
from src.utils.constants import BLACK, WHITE, GRAY, RED, GREEN, BLUE, YELLOW

class Renderer:
    def __init__(self, screen: pygame.Surface, config: GameConfig):
        self.screen = screen
        self.config = config
        self._font_manager = None
        self._font = None
        self._small_font = None
    
    @property
    def font_manager(self):
        """延迟加载字体管理器"""
        if self._font_manager is None:
            try:
                from src.utils.font_utils import FontManager
                self._font_manager = FontManager()
            except ImportError:
                # 提供默认实现
                self._font_manager = self._create_default_font_manager()
        return self._font_manager
    
    @property
    def font(self):
        """延迟加载字体"""
        if self._font is None:
            self._font = self.font_manager.get_font(36)
        return self._font
    
    def _create_default_font_manager(self):
        """创建默认字体管理器"""
        class DefaultFontManager:
            @staticmethod
            def get_font(size, bold=False):
                return pygame.font.Font(None, size)
        return DefaultFontManager()
```

### 4. 环境配置优化

#### 4.1 创建 `.env` 文件
```bash
# .env
PYTHONPATH=src
PYGAME_HIDE_SUPPORT_PROMPT=1
```

#### 4.2 创建启动脚本
```python
# run_game.py
#!/usr/bin/env python3
"""
游戏启动脚本
"""
import sys
import os
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from main import TetrisGame

if __name__ == "__main__":
    game = TetrisGame()
    game.run()
```

### 5. 导入检查工具

#### 5.1 创建导入检查脚本
```python
# tools/check_imports.py
#!/usr/bin/env python3
"""
检查项目中的导入问题
"""
import ast
import os
from pathlib import Path
from typing import List, Dict

class ImportChecker:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.issues = []
    
    def check_file(self, file_path: Path):
        """检查单个文件的导入"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._check_import(alias.name, file_path)
                elif isinstance(node, ast.ImportFrom):
                    self._check_import_from(node, file_path)
        
        except Exception as e:
            self.issues.append(f"解析文件 {file_path} 时出错: {e}")
    
    def _check_import(self, module_name: str, file_path: Path):
        """检查import语句"""
        if module_name.startswith('.'):
            self.issues.append(f"相对导入: {file_path} -> {module_name}")
    
    def _check_import_from(self, node: ast.ImportFrom, file_path: Path):
        """检查from import语句"""
        if node.module and node.module.startswith('.'):
            self.issues.append(f"相对导入: {file_path} -> {node.module}")
    
    def run(self):
        """运行检查"""
        for py_file in self.project_root.rglob("*.py"):
            if "test" in py_file.parts or "tools" in py_file.parts:
                continue
            self.check_file(py_file)
        
        return self.issues

if __name__ == "__main__":
    checker = ImportChecker(Path("."))
    issues = checker.run()
    
    if issues:
        print("发现导入问题:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("未发现导入问题")
```

### 6. 实施步骤

1. **创建必要的 `__init__.py` 文件**
2. **更新所有导入语句为绝对导入**
3. **创建 `setup.py` 和 `conftest.py`**
4. **更新测试文件，移除手动路径管理**
5. **实施依赖注入模式**
6. **运行导入检查工具验证**

### 7. 最佳实践

1. **统一使用绝对导入**
2. **避免循环依赖**
3. **使用依赖注入**
4. **延迟加载可选依赖**
5. **提供合理的fallback方案**
6. **定期运行导入检查**

### 8. 验证方法

```bash
# 安装开发依赖
pip install -e .[dev]

# 运行导入检查
python tools/check_imports.py

# 运行测试
pytest test/

# 运行游戏
python run_game.py
```

这个方案将显著改善项目的import结构，提高代码的可维护性和可读性。
