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
