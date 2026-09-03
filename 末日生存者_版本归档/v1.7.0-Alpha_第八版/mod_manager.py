# -*- coding: utf-8 -*-
import os
import json
import logging
from typing import Dict, Any, Optional, List

class ModManager:
    """MOD管理器，负责加载和管理所有外部数据"""
    def __init__(self, game):
        self.game = game
        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.join(root_dir, "data")
        self.system_mods_path = os.path.join(root_dir, "mods", "system")
        self.global_mods_path = os.path.join(root_dir, "mods", "global")
        self.active_global_mods = set()
        self.enabled_global_mods = {}  # mod_id -> bool
        self.loaded_data = {
            'items': {},
            'enemies': {},
            'npcs': {},
            'quests': {},
            'actions': {},
            'terrains': {},
            'commands': {},
            'recipes': {},
            'stories': {}
        }

    def initialize(self):
        """初始化MOD管理器，加载系统资源和启用全局MOD"""
        self.load_system_resources()
        self.load_enabled_global_mods()
        self.apply_global_mods()
        logging.info("MOD管理器初始化完成")

    def load_system_resources(self):
        """加载系统资源（内置数据）"""
        # 加载 items.json
        self._load_json_file(os.path.join(self.base_path, 'items.json'), 'items')
        # 加载 enemies.json
        self._load_json_file(os.path.join(self.base_path, 'enemies.json'), 'enemies')
        # 加载 npcs.json
        self._load_json_file(os.path.join(self.base_path, 'npcs.json'), 'npcs')
        # 加载 quests.json
        self._load_json_file(os.path.join(self.base_path, 'quests.json'), 'quests')
        # 加载 actions.json
        self._load_json_file(os.path.join(self.base_path, 'actions.json'), 'actions')
        # 加载 terrains.json
        self._load_json_file(os.path.join(self.base_path, 'terrains.json'), 'terrains')
        # 加载 commands.json
        self._load_json_file(os.path.join(self.base_path, 'commands.json'), 'commands')
        # 加载 recipes.json（可选，可合并到items.json）
        self._load_json_file(os.path.join(self.base_path, 'recipes.json'), 'recipes')
        # 加载 stories（从data/stories/*.txt）
        self._load_stories_from_dir(os.path.join(self.base_path, 'stories'))

    def _load_json_file(self, path: str, category: str):
        if not os.path.exists(path):
            logging.warning(f"系统资源文件不存在: {path}")
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                logging.warning(f"系统资源格式无效: {path}")
                return
            if category == 'items' and 'items' in data and isinstance(data.get('items'), dict):
                self.loaded_data['items'].update(data['items'])
                nested_recipes = data.get('recipes', {})
                if isinstance(nested_recipes, dict):
                    self.loaded_data['recipes'].update(nested_recipes)
                logging.info(f"加载系统资源 items: {len(data['items'])} 项")
                return
            self.loaded_data[category].update(data)
            logging.info(f"加载系统资源 {category}: {len(data)} 项")
        except Exception as e:
            logging.error(f"加载系统资源失败 {path}: {e}")

    def _load_stories_from_dir(self, dir_path: str):
        """从目录加载故事文本文件"""
        logging.info(f"尝试加载故事目录: {dir_path}")
        if not os.path.exists(dir_path):
            logging.warning(f"故事目录不存在: {dir_path}")
            return
        count = 0
        for filename in os.listdir(dir_path):
            if filename.endswith('.txt'):
                try:
                    file_path = os.path.join(dir_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                    	lines = f.readlines()
                    	# 提取标题：如果第一行以 '# ' 开头，则去除前缀并作为标题，否则用文件名
                    	if lines and lines[0].strip().startswith('# '):
                    		title = lines[0].strip()[2:].strip()  # 去掉 '# ' 和首尾空格
                    		content = ''.join(lines[1:])  # 剩余内容
                    	else:
                    		title = filename[:-4]  # 文件名（不含扩展名）
                    		content = ''.join(lines)
                        
                        
                    story_id = filename[:-4]  # 去掉.txt
                    self.loaded_data['stories'][story_id] = {'title': title, 'content': content}
                    count += 1
                    logging.info(f"加载故事文件: {filename} -> {story_id}(标题:{title})")
                
                
                except Exception as e:
                    logging.error(f"加载故事文件失败 {filename}: {e}")
        logging.info(f"从 {dir_path} 加载了 {count} 个故事")

    def load_enabled_global_mods(self):
        """加载全局MOD列表（从配置文件读取已启用列表）"""
        config_file = os.path.join(self.global_mods_path, "enabled.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    self.enabled_global_mods = json.load(f)
            except:
                pass

    def apply_global_mods(self):
        """应用所有启用的全局MOD（按顺序）"""
        if not os.path.exists(self.global_mods_path):
            return
        for mod_id in os.listdir(self.global_mods_path):
            mod_path = os.path.join(self.global_mods_path, mod_id)
            if not os.path.isdir(mod_path):
                continue
            if mod_id in self.enabled_global_mods and self.enabled_global_mods[mod_id]:
                self.apply_mod(mod_path)

    def apply_mod(self, mod_path: str):
        """应用一个MOD（合并数据）"""
        # 读取 mod_info.json
        info_file = os.path.join(mod_path, 'mod_info.json')
        mod_name = mod_path
        if os.path.exists(info_file):
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    mod_name = info.get('name', mod_path)
                    logging.info(f"加载MOD: {mod_name} v{info.get('version', '?')}")
            except:
                pass
        # 遍历数据文件
        for category in self.loaded_data.keys():
            file_path = os.path.join(mod_path, f"{category}.json")
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        mod_data = json.load(f)
                    self.loaded_data[category].update(mod_data)
                    logging.info(f"  {category}: 添加 {len(mod_data)} 项")
                except Exception as e:
                    logging.error(f"加载MOD文件 {file_path} 失败: {e}")
        # 故事文件
        stories_dir = os.path.join(mod_path, 'stories')
        if os.path.exists(stories_dir):
            self._load_stories_from_dir(stories_dir)

    def get_data(self, category: str, key: str = None):
        """获取指定类别的数据，如果key为None则返回整个字典"""
        data = self.loaded_data.get(category, {})
        if key is None:
            return data
        return data.get(key)

    def get_all_data(self):
        return self.loaded_data