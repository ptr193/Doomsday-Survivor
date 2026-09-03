# -*- coding: utf-8 -*-
import os
import logging
from datetime import datetime

class DiarySystem:
    def __init__(self, game):
        self.game = game
        self.diary_path = None
        self.content = ""
        self.initialized = False

    def initialize(self, save_slot):
        """初始化日记系统，关联存档目录"""
        self.diary_path = os.path.join("saves", f"save_slot_{save_slot}", "diary.txt")
        self.load()
        self.initialized = True
        logging.info(f"日记系统初始化: {self.diary_path}")

    def load(self):
        """加载日记内容"""
        if os.path.exists(self.diary_path):
            try:
                with open(self.diary_path, 'r', encoding='utf-8') as f:
                    self.content = f.read()
            except Exception as e:
                logging.error(f"加载日记失败: {e}")
        else:
            self.content = ""

    def save(self):
        """保存日记内容"""
        if not self.diary_path:
            return
        try:
            os.makedirs(os.path.dirname(self.diary_path), exist_ok=True)
            with open(self.diary_path, 'w', encoding='utf-8') as f:
                f.write(self.content)
            logging.info("日记已保存")
        except Exception as e:
            logging.error(f"保存日记失败: {e}")

    def add_entry(self, text: str):
        """添加日记条目（自动添加时间戳）"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.content += f"\n[{timestamp}] {text}\n"
        self.save()
        self.game.add_game_log("日记已更新")

    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content
        self.save()