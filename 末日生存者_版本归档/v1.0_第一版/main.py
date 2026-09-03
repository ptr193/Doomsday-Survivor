#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from game import TextAdventureGame
import os
import sys
import logging

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
    """检查并创建必要的目录"""
    directories = ['saves', 'game_data', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"创建目录: {directory}")

def main():
    """主程序入口"""
    try:
        logging.info("启动末日生存者游戏...")
        
        # 检查目录
        check_directories()
        
        # 设置Tkinter外观
        tk.Tk().withdraw()  # 隐藏根窗口
        
        # 启动游戏
        root = tk.Tk()
        app = TextAdventureGame(root)
        
        logging.info("游戏初始化完成")
        root.mainloop()
        
    except Exception as e:
        logging.error(f"游戏启动错误: {e}", exc_info=True)
        tk.messagebox.showerror("启动错误", f"游戏启动时发生错误:\n{e}")
    finally:
        logging.info("游戏退出")

if __name__ == "__main__":
    main()