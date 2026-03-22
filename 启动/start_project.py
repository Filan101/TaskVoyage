#!/usr/bin/env python3
"""
TaskVoyage 项目启动脚本
功能：启动后端服务和Vue 3前端服务，并自动打开浏览器访问项目主页面
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading

# 项目根目录（因为脚本在"启动"子文件夹中，所以需要向上一级）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 前端Vue 3目录
FRONTEND_VUE_DIR = os.path.join(PROJECT_ROOT, "frontend-vue")
# 后端服务地址
BACKEND_URL = "http://127.0.0.1:8000"
# 前端Vue 3服务地址
FRONTEND_URL = "http://127.0.0.1:3000"


def start_backend():
    """启动后端服务"""
    print("=" * 50)
    print("正在启动后端服务...")
    print("=" * 50)
    
    # 切换到项目根目录
    os.chdir(PROJECT_ROOT)
    
    # 启动后端服务
    try:
        subprocess.run([sys.executable, "manage.py", "runserver"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"后端服务启动失败: {e}")
        sys.exit(1)


def start_frontend():
    """启动前端Vue 3服务"""
    print("=" * 50)
    print("正在启动前端Vue 3服务...")
    print("=" * 50)
    
    # 切换到前端Vue 3目录
    os.chdir(FRONTEND_VUE_DIR)
    
    # 启动前端服务
    try:
        # 检查npm是否安装
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        # 启动前端服务
        subprocess.run(["npm", "run", "dev"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"前端服务启动失败: {e}")
        sys.exit(1)


def open_browser():
    """打开浏览器访问项目主页面"""
    print("等待服务启动...")
    # 等待10秒，确保服务有足够的启动时间
    for i in range(10):
        time.sleep(1)
        print(f"服务启动中... ({i+1}/10)")
    
    print(f"正在打开浏览器访问: {FRONTEND_URL}")
    webbrowser.open(FRONTEND_URL)
    print("浏览器已打开，请稍候...")


def main():
    """主函数"""
    print("TaskVoyage 项目启动脚本")
    print("=" * 50)
    
    # 检查Python环境
    print("检查Python环境...")
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print()
    
    # 检查项目目录
    print("检查项目目录...")
    print(f"项目根目录: {PROJECT_ROOT}")
    if not os.path.exists(os.path.join(PROJECT_ROOT, "manage.py")):
        print("错误: 未找到manage.py文件，请确保在项目根目录运行此脚本")
        sys.exit(1)
    print()
    
    # 检查前端Vue 3目录
    print("检查前端Vue 3目录...")
    print(f"前端Vue 3目录: {FRONTEND_VUE_DIR}")
    if not os.path.exists(FRONTEND_VUE_DIR):
        print("错误: 未找到frontend-vue目录，请确保Vue 3前端项目已创建")
        sys.exit(1)
    print()
    
    # 启动后端服务（在后台线程）
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # 启动前端Vue 3服务（在后台线程）
    frontend_thread = threading.Thread(target=start_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()
    
    # 打开浏览器
    open_browser()
    
    print("\n启动完成！")
    print(f"后端服务地址: {BACKEND_URL}")
    print(f"前端访问地址: {FRONTEND_URL}")
    print("\n按 Ctrl+C 停止服务")
    
    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        sys.exit(0)


if __name__ == "__main__":
    main()
