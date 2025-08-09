#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接启动优化版本的游戏
"""

import sys
import os

def main():
    """主函数"""
    print("🚀 启动优化版俄罗斯方块游戏...")
    print("使用优化渲染系统，性能提升显著！")
    print("快捷键:")
    print("  F3: 切换性能指标显示")
    print("  F4: 导出性能指标")
    print("  ESC: 返回主菜单")
    print("  P: 暂停/继续游戏")
    print("  R: 重置游戏")
    print()
    
    try:
        # 添加src目录到Python路径
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        # 导入并运行优化版本
        from main_optimized import main
        main()
    except ImportError as e:
        print(f"❌ 导入优化版本失败: {e}")
        print("请确保所有依赖已正确安装")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 运行优化版本时出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
