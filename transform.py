#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jupyter Notebook to Python 转换工具
适用于Windows/Linux/Mac
"""

import os
import sys
import subprocess

def convert_notebook(notebook_path):
    """
    智能转换notebook到Python脚本
    自动选择最佳方法
    """
    
    if not os.path.exists(notebook_path):
        print(f"❌ 错误: 找不到文件 '{notebook_path}'")
        return False
    
    print(f"📓 正在转换: {notebook_path}")
    
    # 方法1: 使用 python -m nbconvert
    print("尝试方法1: 使用 python -m nbconvert...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'nbconvert', notebook_path, '--to', 'python', '--no-prompt'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            output_file = notebook_path.replace('.ipynb', '.py')
            print(f"✅ 转换成功: {output_file}")
            return True
        else:
            print(f"⚠️  方法1失败: {result.stderr}")
    except Exception as e:
        print(f"⚠️  方法1失败: {e}")
    
    # 方法2: 使用 nbconvert API
    print("尝试方法2: 使用 nbconvert API...")
    try:
        import nbformat
        from nbconvert import PythonExporter
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        exporter = PythonExporter()
        python_code, _ = exporter.from_notebook_node(notebook)
        
        output_file = notebook_path.replace('.ipynb', '.py')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(python_code)
        
        print(f"✅ 转换成功: {output_file}")
        return True
        
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("   请运行: pip install nbformat nbconvert")
        return False
    except Exception as e:
        print(f"❌ API转换失败: {e}")
        return False

# 主程序
if __name__ == "__main__":
    # 转换你的文件
    notebook_files = [
        'amazon-e-commerce-universe-analysis.ipynb',
        # 可以添加更多文件
    ]
    
    success_count = 0
    for notebook in notebook_files:
        if convert_notebook(notebook):
            success_count += 1
        print("-" * 50)
    
    print(f"\n📊 总结: {success_count}/{len(notebook_files)} 个文件转换成功")