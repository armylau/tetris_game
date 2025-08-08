#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行core组件单元测试的脚本
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# 导入所有测试模块
from test_board import TestBoard
from test_piece import TestPiece
from test_collision import TestCollisionDetector
from test_game_state import TestGameState
from test_game_engine import TestGameEngine


def run_all_tests():
    """运行所有core组件的测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestBoard,
        TestPiece,
        TestCollisionDetector,
        TestGameState,
        TestGameEngine
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 打印测试结果摘要
    print("\n" + "="*50)
    print("测试结果摘要:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    return result.wasSuccessful()


def run_specific_test(test_name):
    """运行特定的测试"""
    test_suite = unittest.TestSuite()
    
    # 根据测试名称选择测试类
    test_map = {
        'board': TestBoard,
        'piece': TestPiece,
        'collision': TestCollisionDetector,
        'game_state': TestGameState,
        'game_engine': TestGameEngine
    }
    
    if test_name in test_map:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_map[test_name])
        test_suite.addTests(tests)
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(test_suite)
        
        print(f"\n{test_name} 测试结果:")
        print(f"运行测试: {result.testsRun}")
        print(f"失败: {len(result.failures)}")
        print(f"错误: {len(result.errors)}")
        
        return result.wasSuccessful()
    else:
        print(f"未知的测试: {test_name}")
        print("可用的测试: board, piece, collision, game_state, game_engine")
        return False


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='运行core组件单元测试')
    parser.add_argument('--test', '-t', 
                       choices=['board', 'piece', 'collision', 'game_state', 'game_engine'],
                       help='运行特定的测试')
    
    args = parser.parse_args()
    
    if args.test:
        success = run_specific_test(args.test)
    else:
        success = run_all_tests()
    
    # 设置退出码
    sys.exit(0 if success else 1)
