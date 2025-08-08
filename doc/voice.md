# 俄罗斯方块游戏音效系统需求与设计方案

## 1. 项目概述

为俄罗斯方块游戏添加完整的音效系统，提升游戏体验和用户交互反馈。

## 2. 需求列表

### 2.1 核心音效需求

#### 2.1.1 游戏操作音效
- **方块移动音效**
  - 左移/右移方块时的音效
  - 方块旋转时的音效
  - 方块快速下降时的音效

- **方块放置音效**
  - 方块落地时的音效
  - 方块锁定时的音效

- **行消除音效**
  - 单行消除音效
  - 多行同时消除音效（根据消除行数不同）
  - 四行同时消除（Tetris）特殊音效

#### 2.1.2 游戏状态音效
- **游戏开始音效**
- **游戏暂停音效**
- **游戏结束音效**
- **游戏胜利音效**
- **关卡升级音效**

#### 2.1.3 界面交互音效
- **菜单选择音效**
- **按钮点击音效**
- **设置变更音效**
- **音量调节音效**

#### 2.1.4 背景音乐
- **主菜单背景音乐**
- **游戏进行中背景音乐**
- **游戏结束背景音乐**

### 2.2 音效控制需求

#### 2.2.1 音量控制
- 主音量控制
- 音效音量独立控制
- 背景音乐音量独立控制
- 静音功能

#### 2.2.2 音效开关
- 音效总开关
- 背景音乐开关
- 操作音效开关
- 界面音效开关

## 3. 技术设计方案

### 3.1 音效系统架构

```
音效系统架构图：

┌─────────────────┐
│   音效管理器    │  (VoiceManager)
├─────────────────┤
│ 音效播放器      │  (VoicePlayer)
│ 背景音乐播放器  │  (BGMPlayer)
│ 音量控制器      │  (VolumeController)
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   音效资源      │  (VoiceAssets)
├─────────────────┤
│ 操作音效        │
│ 状态音效        │
│ 界面音效        │
│ 背景音乐        │
└─────────────────┘
```

### 3.2 核心类设计

#### 3.2.1 VoiceManager（音效管理器）
```python
class VoiceManager:
    def __init__(self):
        self.voice_player = VoicePlayer()
        self.bgm_player = BGMPlayer()
        self.volume_controller = VolumeController()
        self.settings = VoiceSettings()
    
    def play_effect(self, effect_type, effect_name):
        """播放指定音效"""
        pass
    
    def play_bgm(self, bgm_name):
        """播放背景音乐"""
        pass
    
    def set_volume(self, volume_type, volume):
        """设置音量"""
        pass
    
    def toggle_mute(self, mute_type):
        """切换静音状态"""
        pass
```

#### 3.2.2 VoicePlayer（音效播放器）
```python
class VoicePlayer:
    def __init__(self):
        self.effects = {}  # 音效资源字典
        self.current_volume = 1.0
    
    def load_effect(self, effect_name, file_path):
        """加载音效文件"""
        pass
    
    def play(self, effect_name):
        """播放音效"""
        pass
    
    def stop(self, effect_name):
        """停止音效"""
        pass
```

#### 3.2.3 BGMPlayer（背景音乐播放器）
```python
class BGMPlayer:
    def __init__(self):
        self.bgm_tracks = {}  # 背景音乐资源字典
        self.current_bgm = None
        self.loop = True
    
    def load_bgm(self, bgm_name, file_path):
        """加载背景音乐"""
        pass
    
    def play(self, bgm_name, loop=True):
        """播放背景音乐"""
        pass
    
    def stop(self):
        """停止背景音乐"""
        pass
    
    def pause(self):
        """暂停背景音乐"""
        pass
    
    def resume(self):
        """恢复背景音乐"""
        pass
```

#### 3.2.4 VolumeController（音量控制器）
```python
class VolumeController:
    def __init__(self):
        self.master_volume = 1.0
        self.effect_volume = 1.0
        self.bgm_volume = 1.0
        self.master_mute = False
        self.effect_mute = False
        self.bgm_mute = False
    
    def set_master_volume(self, volume):
        """设置主音量"""
        pass
    
    def set_effect_volume(self, volume):
        """设置音效音量"""
        pass
    
    def set_bgm_volume(self, volume):
        """设置背景音乐音量"""
        pass
    
    def toggle_master_mute(self):
        """切换主静音"""
        pass
    
    def toggle_effect_mute(self):
        """切换音效静音"""
        pass
    
    def toggle_bgm_mute(self):
        """切换背景音乐静音"""
        pass
```

### 3.3 音效资源管理

#### 3.3.1 音效文件结构
```
assets/
├── sounds/
│   ├── effects/
│   │   ├── move_left.wav
│   │   ├── move_right.wav
│   │   ├── rotate.wav
│   │   ├── drop.wav
│   │   ├── lock.wav
│   │   ├── line_clear.wav
│   │   ├── tetris.wav
│   │   ├── game_start.wav
│   │   ├── game_over.wav
│   │   ├── level_up.wav
│   │   ├── menu_select.wav
│   │   └── button_click.wav
│   └── bgm/
│       ├── main_menu.mp3
│       ├── game_play.mp3
│       └── game_over.mp3
```

#### 3.3.2 音效配置文件
```json
{
  "effects": {
    "move_left": {
      "file": "sounds/effects/move_left.wav",
      "volume": 0.8,
      "loop": false
    },
    "move_right": {
      "file": "sounds/effects/move_right.wav",
      "volume": 0.8,
      "loop": false
    },
    "rotate": {
      "file": "sounds/effects/rotate.wav",
      "volume": 0.9,
      "loop": false
    },
    "drop": {
      "file": "sounds/effects/drop.wav",
      "volume": 0.7,
      "loop": false
    },
    "lock": {
      "file": "sounds/effects/lock.wav",
      "volume": 0.8,
      "loop": false
    },
    "line_clear": {
      "file": "sounds/effects/line_clear.wav",
      "volume": 1.0,
      "loop": false
    },
    "tetris": {
      "file": "sounds/effects/tetris.wav",
      "volume": 1.0,
      "loop": false
    },
    "game_start": {
      "file": "sounds/effects/game_start.wav",
      "volume": 0.9,
      "loop": false
    },
    "game_over": {
      "file": "sounds/effects/game_over.wav",
      "volume": 0.9,
      "loop": false
    },
    "level_up": {
      "file": "sounds/effects/level_up.wav",
      "volume": 1.0,
      "loop": false
    },
    "menu_select": {
      "file": "sounds/effects/menu_select.wav",
      "volume": 0.7,
      "loop": false
    },
    "button_click": {
      "file": "sounds/effects/button_click.wav",
      "volume": 0.6,
      "loop": false
    }
  },
  "bgm": {
    "main_menu": {
      "file": "sounds/bgm/main_menu.mp3",
      "volume": 0.5,
      "loop": true
    },
    "game_play": {
      "file": "sounds/bgm/game_play.mp3",
      "volume": 0.4,
      "loop": true
    },
    "game_over": {
      "file": "sounds/bgm/game_over.mp3",
      "volume": 0.5,
      "loop": false
    }
  },
  "settings": {
    "master_volume": 1.0,
    "effect_volume": 1.0,
    "bgm_volume": 0.8,
    "master_mute": false,
    "effect_mute": false,
    "bgm_mute": false
  }
}
```

## 4. 实现计划

### 4.1 开发阶段

#### 阶段一：基础音效系统
- [ ] 创建音效管理器基础框架
- [ ] 实现音效播放器
- [ ] 实现音量控制器
- [ ] 添加基础音效文件

#### 阶段二：游戏音效集成
- [ ] 集成方块移动音效
- [ ] 集成方块放置音效
- [ ] 集成行消除音效
- [ ] 集成游戏状态音效

#### 阶段三：背景音乐系统
- [ ] 实现背景音乐播放器
- [ ] 添加背景音乐文件
- [ ] 实现音乐切换逻辑

#### 阶段四：界面音效
- [ ] 集成菜单选择音效
- [ ] 集成按钮点击音效
- [ ] 添加设置界面音效

#### 阶段五：设置与优化
- [ ] 实现音效设置界面
- [ ] 添加音效开关功能
- [ ] 优化音效性能
- [ ] 测试与调试

### 4.2 技术依赖

- **pygame.mixer**: 用于音效播放
- **json**: 用于音效配置管理
- **os**: 用于文件路径处理

### 4.3 文件结构

```
src/
├── voice/
│   ├── __init__.py
│   ├── voice_manager.py
│   ├── voice_player.py
│   ├── bgm_player.py
│   ├── volume_controller.py
│   ├── voice_settings.py
│   └── voice_config.py
├── assets/
│   └── sounds/
│       ├── effects/
│       └── bgm/
└── config/
    └── voice_config.json
```

## 5. 测试计划

### 5.1 功能测试
- [ ] 音效播放功能测试
- [ ] 音量控制功能测试
- [ ] 静音功能测试
- [ ] 背景音乐切换测试

### 5.2 性能测试
- [ ] 音效加载性能测试
- [ ] 内存使用测试
- [ ] CPU使用率测试

### 5.3 兼容性测试
- [ ] 不同操作系统兼容性
- [ ] 不同音频设备兼容性
- [ ] 不同音频格式兼容性

## 6. 注意事项

### 6.1 音效设计原则
- 音效应该简洁明了，不影响游戏体验
- 音量设置要合理，避免过于刺耳
- 音效时长要适中，避免过长影响游戏节奏

### 6.2 性能考虑
- 音效文件大小要控制在合理范围内
- 使用适当的音频格式（WAV用于音效，MP3用于背景音乐）
- 实现音效资源池，避免重复加载

### 6.3 用户体验
- 提供完整的音效设置选项
- 支持音效开关的快速切换
- 保存用户的音效设置偏好

## 7. 后续扩展

### 7.1 高级功能
- 音效3D定位
- 音效混响效果
- 自定义音效包
- 音效录制功能

### 7.2 多平台支持
- 移动端音效优化
- Web端音效支持
- 跨平台音效同步

---

*文档版本：1.0*  
*创建日期：2024年*  
*最后更新：2024年*
