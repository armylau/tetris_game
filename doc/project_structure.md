# 俄罗斯方块游戏项目概览

## 项目结构
```
tetris_game/
├── tetris_main.py          # 主游戏文件
├── game/
│   ├── __init__.py
│   ├── board.py            # 游戏板逻辑
│   ├── piece.py            # 方块类
│   ├── game_state.py       # 游戏状态管理
│   └── collision.py        # 碰撞检测
├── ui/
│   ├── __init__.py
│   ├── renderer.py         # 渲染引擎
│   ├── menu.py            # 菜单系统
│   └── hud.py             # 用户界面元素
├── audio/
│   ├── __init__.py
│   ├── sound_manager.py    # 音频管理
│   └── sounds/            # 音频文件
├── data/
│   ├── __init__.py
│   ├── config.py          # 配置文件
│   ├── high_scores.py     # 高分记录
│   └── assets/            # 游戏资源
├── utils/
│   ├── __init__.py
│   ├── constants.py       # 常量定义
│   └── helpers.py         # 工具函数
├── requirements.txt        # 项目依赖
├── README.md              # 项目说明
├── overview.md            # 项目概览
└── requirements.md        # 需求文档
```
