#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块游戏启动脚本
让用户选择使用传统版本还是优化版本
"""

import sys
import os

def print_banner():
    """打印游戏横幅"""
    print("=" * 60)
    print("🎮 俄罗斯方块游戏 🎮")
    print("=" * 60)
    print()

def print_version_info():
    """打印版本信息"""
    print("可用版本:")
    print("  1. 传统版本 (src/main.py)")
    print("     - 使用传统渲染系统")
    print("     - 兼容性好，稳定可靠")
    print("     - 适合所有设备")
    print()
    print("  2. 优化版本 (src/main_optimized.py)")
    print("     - 使用优化渲染系统")
    print("     - 性能提升显著 (FPS +105%)")
    print("     - 支持性能监控")
    print("     - 推荐用于现代设备")
    print()

def get_user_choice():
    """获取用户选择"""
    while True:
        try:
            choice = input("请选择版本 (1/2): ").strip()
            if choice == "1":
                return "traditional"
            elif choice == "2":
                return "optimized"
            else:
                print("❌ 无效选择，请输入 1 或 2")
        except KeyboardInterrupt:
            print("\n👋 再见！")
            sys.exit(0)

def run_traditional_version():
    """运行传统版本"""
    print("🚀 启动传统版本...")
    print("正在导入传统渲染系统...")
    
    try:
        # 添加src目录到Python路径
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        # 导入并运行传统版本
        from main import main
        main()
    except ImportError as e:
        print(f"❌ 导入传统版本失败: {e}")
        print("请确保所有依赖已正确安装")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 运行传统版本时出错: {e}")
        sys.exit(1)

def run_optimized_version():
    """运行优化版本"""
    print("🚀 启动优化版本...")
    print("正在导入优化渲染系统...")
    
    try:
        # 添加src目录到Python路径
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        # 导入并运行优化版本
        from main_optimized import main
        main()
    except ImportError as e:
        print(f"❌ 导入优化版本失败: {e}")
        print("请确保所有依赖已正确安装")
        print("如果问题持续，请尝试运行传统版本")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 运行优化版本时出错: {e}")
        print("建议尝试运行传统版本")
        sys.exit(1)

def main():
    """主函数"""
    print_banner()
    print_version_info()
    
    choice = get_user_choice()
    
    if choice == "traditional":
        run_traditional_version()
    elif choice == "optimized":
        run_optimized_version()

if __name__ == "__main__":
    main()
