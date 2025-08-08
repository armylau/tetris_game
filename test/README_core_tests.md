# Core组件单元测试

本目录包含了俄罗斯方块游戏核心组件的完整单元测试。

## 测试文件说明

### 1. test_board.py
测试 `Board` 类的功能：
- 游戏板初始化
- 方块位置有效性检查
- 方块放置
- 行消除
- 游戏结束检测
- 边界情况处理

### 2. test_piece.py
测试 `Piece` 类的功能：
- 方块初始化
- 方块旋转
- 形状和尺寸获取
- 颜色验证
- 不同方块类型的旋转一致性

### 3. test_collision.py
测试 `CollisionDetector` 类的功能：
- 碰撞检测
- 墙踢算法
- 旋转检查
- 边界情况处理
- 不同方块的碰撞检测

### 4. test_game_state.py
测试 `GameState` 类的功能：
- 游戏状态初始化
- 分数计算和更新
- 等级计算和更新
- 方块生成和管理
- 游戏状态重置

### 5. test_game_engine.py
测试 `GameEngine` 类的功能：
- 游戏引擎初始化
- 方块生成和移动
- 方块旋转
- 自动下落
- 游戏状态更新
- 游戏重置

## 运行测试

### 运行所有测试
```bash
cd test
python run_core_tests.py
```

### 运行特定测试
```bash
# 运行Board测试
python run_core_tests.py --test board

# 运行Piece测试
python run_core_tests.py --test piece

# 运行Collision测试
python run_core_tests.py --test collision

# 运行GameState测试
python run_core_tests.py --test game_state

# 运行GameEngine测试
python run_core_tests.py --test game_engine
```

### 直接运行单个测试文件
```bash
# 运行Board测试
python test_board.py

# 运行Piece测试
python test_piece.py

# 运行Collision测试
python test_collision.py

# 运行GameState测试
python test_game_state.py

# 运行GameEngine测试
python test_game_engine.py
```

## 测试覆盖范围

### Board类测试覆盖
- ✅ 游戏板初始化
- ✅ 有效位置检查（边界、碰撞）
- ✅ 方块放置（成功/失败）
- ✅ 行消除（单行/多行）
- ✅ 游戏结束检测
- ✅ 边界情况处理

### Piece类测试覆盖
- ✅ 方块初始化
- ✅ 所有方块类型的旋转
- ✅ 形状和尺寸获取
- ✅ 颜色验证
- ✅ 旋转一致性检查

### CollisionDetector类测试覆盖
- ✅ 碰撞检测
- ✅ 墙踢算法
- ✅ 旋转检查（成功/失败）
- ✅ 边界情况处理
- ✅ 状态保持一致性

### GameState类测试覆盖
- ✅ 游戏状态初始化
- ✅ 分数计算（不同等级）
- ✅ 等级更新
- ✅ 方块管理
- ✅ 游戏状态重置

### GameEngine类测试覆盖
- ✅ 游戏引擎初始化
- ✅ 方块生成和移动
- ✅ 方块旋转（包括墙踢）
- ✅ 自动下落
- ✅ 游戏状态更新
- ✅ 游戏重置

## 测试特点

1. **全面性**: 覆盖了所有核心组件的所有主要功能
2. **边界测试**: 包含各种边界情况和异常情况
3. **一致性测试**: 验证组件间的交互和状态一致性
4. **性能测试**: 测试大量数据和长时间运行的情况
5. **隔离性**: 每个测试都是独立的，不依赖其他测试

## 测试结果解读

测试运行后会显示：
- 运行的测试数量
- 失败的测试数量
- 错误的测试数量
- 跳过的测试数量
- 详细的失败和错误信息

## 注意事项

1. 确保在运行测试前已安装所有依赖
2. 测试需要访问 `src` 目录中的模块
3. 某些测试可能需要较长时间运行
4. 如果测试失败，请检查相关的核心组件代码

## 扩展测试

如需添加新的测试用例：
1. 在相应的测试文件中添加新的测试方法
2. 确保测试方法以 `test_` 开头
3. 使用适当的断言方法验证结果
4. 运行测试确保新测试通过
