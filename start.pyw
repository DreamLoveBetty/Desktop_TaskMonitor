#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComfyUI Pet Monitor 启动脚本
"""

import sys
import subprocess
import os

def check_python():
    """检查 Python 版本"""
    if sys.version_info < (3, 7):
        print("错误: 需要 Python 3.7 或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    return True

def install_dependencies():
    """安装依赖包"""
    try:
        import PyQt5
        print("✓ PyQt5 已安装")
        return True
    except ImportError:
        print("正在安装依赖包...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✓ 依赖包安装成功")
            return True
        except subprocess.CalledProcessError:
            print("✗ 依赖包安装失败")
            return False

def start_program():
    """启动程序"""
    try:
        print("启动 ComfyUI Pet Monitor...")
        subprocess.run([sys.executable, "comfyui_pet_monitor.py"])
    except Exception as e:
        print(f"程序启动失败: {e}")

def main():
    """主函数"""
    print("ComfyUI Pet Monitor 启动器")
    print("=" * 40)
    
    # 检查 Python 版本
    if not check_python():
        input("按回车键退出...")
        return
    
    # 安装依赖
    if not install_dependencies():
        input("按回车键退出...")
        return
    
    # 启动程序
    start_program()

if __name__ == "__main__":
    main()
