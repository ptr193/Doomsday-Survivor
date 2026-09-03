#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from game import TextAdventureGame
import os
import sys
import logging
import random

VERSION = "1.7.0-Alpha"

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def check_directories():
    directories = ['saves', 'data', 'logs', 'mods/system', 'mods/global']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"创建目录: {directory}")

def show_loading():
    """显示加载进度条窗口"""
    loading = tk.Tk()
    loading.title("加载中")
    loading.geometry("400x200")
    loading.resizable(False, False)
    # 居中
    screen_width = loading.winfo_screenwidth()
    screen_height = loading.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 200) // 2
    loading.geometry(f"+{x}+{y}")
    ttk.Label(loading, text="末日生存者", font=("Arial", 16, "bold")).pack(pady=10)
    ttk.Label(loading, text=f"版本 {VERSION}", font=("Arial", 10)).pack(pady=5)
    progress = ttk.Progressbar(loading, mode='indeterminate', length=300)
    progress.pack(pady=20)
    progress.start(10)
    # 随机提示语
    tips = [
        "提示：记得每天补充食物和水。",
        "提示：不同地形有不同的资源。",
        "提示：夜晚行动会更危险。",
        "提示：与NPC建立良好关系可以获取帮助。",
        "提示：制作工具可以提高生存效率。",
        "提示：保持精神健康，避免崩溃。"
    ]
    tip_label = ttk.Label(loading, text=random.choice(tips), font=("Arial", 9), foreground="#7F8C8D")
    tip_label.pack(pady=10)
    loading.update()
    return loading

def main():
    try:
        loading = show_loading()
        # 模拟加载各系统（实际加载在game初始化中完成）
        logging.info(f"启动末日生存者游戏 v{VERSION}...")
        check_directories()
        # 隐藏根窗口，先显示进度条
        root = tk.Tk()
        root.withdraw()
        app = TextAdventureGame(root)
        # 加载完成后关闭进度条，显示主窗口
        def finish_loading():
        	loading.destroy()
        	root.deiconify()
        loading.after(1000, finish_loading)
        root.mainloop()
    except Exception as e:
        logging.error(f"游戏启动错误: {e}", exc_info=True)
        tk.messagebox.showerror("启动错误", f"游戏启动时发生错误:\n{e}")
    finally:
        logging.info("游戏退出")

if __name__ == "__main__":
    main()