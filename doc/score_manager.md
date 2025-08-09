# ScoreManager 类文档

## 概述

`ScoreManager` 是一个专门用于管理俄罗斯方块游戏分数的Python类。它提供了完整的分数计算、存储、检索和统计功能，遵循PEP 8编码规范。

## 功能特性

- ✅ 分数计算（支持不同消除行数、关卡和连击）
- ✅ 分数存储和加载（JSON格式）
- ✅ 最高分数记录
- ✅ 分数历史记录管理
- ✅ 前N名分数查询
- ✅ 统计信息生成
- ✅ 完全类型注解
- ✅ 完整的文档字符串

## 类结构

### 主要方法

#### `__init__(score_file_path: str = "scores.json")`
初始化分数管理器。

**参数：**
- `score_file_path`: 分数文件保存路径（默认：scores.json）

#### `add_score(points: int, level: int = 1, lines_cleared: int = 0) -> None`
添加分数到当前游戏。

**参数：**
- `points`: 要添加的分数
- `level`: 当前关卡（默认：1）
- `lines_cleared`: 消除的行数（默认：0）

#### `calculate_score(lines_cleared: int, level: int, combo: int = 0) -> int`
根据消除行数、关卡和连击计算分数。

**参数：**
- `lines_cleared`: 消除的行数（1-4）
- `level`: 当前关卡
- `combo`: 连击数（默认：0）

**返回：**
- 计算得到的分数

**分数计算规则：**
- 单行消除：100分 × 关卡倍数
- 双行消除：300分 × 关卡倍数
- 三行消除：500分 × 关卡倍数
- 四行消除：800分 × 关卡倍数
- 连击奖励：50分 × 连击数 × 关卡倍数

#### `reset_current_score() -> None`
重置当前分数（不影响最高分数）。

#### `save_score(player_name: str = "Player", game_mode: str = "classic") -> None`
保存当前分数到历史记录。

**参数：**
- `player_name`: 玩家名称（默认：Player）
- `game_mode`: 游戏模式（默认：classic）

#### `get_high_score() -> int`
获取最高分数。

#### `get_current_score() -> int`
获取当前分数。

#### `get_score_history(limit: Optional[int] = None) -> List[Dict]`
获取分数历史记录。

**参数：**
- `limit`: 限制返回的记录数量（默认：None，返回全部）

#### `get_top_scores(count: int = 10) -> List[Dict]`
获取前N名分数。

**参数：**
- `count`: 返回的分数数量（默认：10）

#### `get_statistics() -> Dict`
获取分数统计信息。

**返回：**
包含以下键的字典：
- `total_games`: 总游戏次数
- `average_score`: 平均分数
- `highest_score`: 最高分数
- `lowest_score`: 最低分数
- `total_score`: 总分数

#### `clear_history() -> None`
清空分数历史记录。

## 使用示例

### 基本使用

```python
from src.core.score_manager import ScoreManager

# 创建分数管理器
score_manager = ScoreManager("my_scores.json")

# 计算分数
score = score_manager.calculate_score(lines_cleared=2, level=3, combo=1)
print(f"得分: {score}")  # 输出: 得分: 1050

# 添加分数
score_manager.add_score(score)

# 保存分数
score_manager.save_score("玩家A", "classic")

# 获取最高分数
high_score = score_manager.get_high_score()
print(f"最高分数: {high_score}")
```

### 分数历史查询

```python
# 获取前5名分数
top_scores = score_manager.get_top_scores(5)
for i, record in enumerate(top_scores, 1):
    print(f"{i}. {record['player_name']}: {record['score']} 分")

# 获取统计信息
stats = score_manager.get_statistics()
print(f"平均分数: {stats['average_score']:.1f}")
```

## 文件格式

分数数据以JSON格式存储，结构如下：

```json
{
  "score_history": [
    {
      "player_name": "玩家A",
      "score": 1000,
      "game_mode": "classic",
      "timestamp": "2025-08-09T13:59:39.123456",
      "date": "2025-08-09 13:59:39"
    }
  ],
  "high_score": 1000,
  "last_updated": "2025-08-09T13:59:39.123456"
}
```

## 测试

运行测试：

```bash
python -m pytest test/test_score_manager.py -v
```

## 代码规范

- 遵循PEP 8编码规范
- 使用类型注解
- 完整的文档字符串
- 中文注释和文档
- 使用f-strings进行字符串格式化

## 依赖

- Python 3.7+
- 标准库：`json`, `os`, `datetime`, `typing`

## 许可证

本项目遵循项目主许可证。
