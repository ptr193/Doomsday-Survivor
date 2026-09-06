# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime, timedelta
import random
import logging
import json
import os

class TextAdventureGame:
    def __init__(self, root):
        self.root = root
        self.version = "1.7.0-Alpha"
        self.setup_game()
        
    def setup_game(self):
        logging.info("初始化游戏系统...")
        
        # 游戏状态
        self.game_state = "menu"
        self.current_save_slot = None
        self.game_speed = 1.0
        
        # 游戏数据
        self.game_time = None
        self.day_count = 1
        self.weather = "sunny"
        self.season = "spring"
        self.temperature = 20
        self.radiation_level = 0
        self.fatigue = 0              # 疲劳值 0-100
        self.max_fatigue = 100
        self.completed_research = []
        
        # 天气影响因子
        self.weather_effects = {}
        
        # 系统标志
        self.systems_initialized = False
        
        # 延迟导入以避免循环依赖
        self.initialize_systems()
        
        # 自动保存
        self.autosave_thread = None
        self.autosave_running = True
        self.start_autosave()
        
        # 游戏循环
        self.game_loop_running = True
        self.start_game_loop()
        
        # 显示界面
        self.show_main_menu()
        
        logging.info("游戏系统初始化完成")
    
    def initialize_systems(self):
        """初始化所有游戏系统"""
        try:
            from player import Player
            from world import GameWorld
            from items import ItemSystem
            from combat import CombatSystem
            from farming import FarmingSystem
            from quests import QuestSystem
            from npc import NPCSystem
            from ui import GameUI
            from save_system import SaveSystem
            from achievement import AchievementSystem
            from mod_manager import ModManager
            from diary_system import DiarySystem
            from story_reader import StoryReader
            from terrain_generator import TerrainGenerator
            
            self.mod_manager = ModManager(self)
            self.mod_manager.initialize()
            
            self.player = Player(self)
            self.world = GameWorld(self)
            self.items = ItemSystem(self)
            self.combat = CombatSystem(self)
            self.farming = FarmingSystem(self)
            self.quests = QuestSystem(self)
            self.npcs = NPCSystem(self)
            self.save_system = SaveSystem(self)
            self.achievements = AchievementSystem(self)
            self.diary = DiarySystem(self)
            self.story_reader = StoryReader(self)
            self.terrain_gen = TerrainGenerator(self)
            
            self.terrain_gen.load_from_mods()
            
            self.story_reader.initialize()
            
            self.ui = GameUI(self.root, self)
            
            self.systems_initialized = True
            logging.info("所有游戏系统初始化成功")
        except Exception as e:
            logging.error(f"系统初始化失败: {e}")
            raise
    
    def show_main_menu(self):
        """显示主菜单"""
        self.ui.create_main_menu()
        self.game_state = "menu"
    
    def start_new_game(self, save_slot, character_data):
        """开始新游戏"""
        try:
            logging.info(f"开始新游戏，存档槽: {save_slot}")
            self.current_save_slot = save_slot
            
            # 初始化玩家
            self.player.initialize(character_data)
            
            # 动态生成世界
            world_data = self.terrain_gen.generate_map()
            self.world.generate_world(world_data)
            self.player.location = self.world.current_location_id
            self.player.discovered_locations = [self.world.current_location_id]
            
            # 初始化其他系统
            self.items.initialize()
            self.combat.initialize()
            self.farming.initialize()
            self.quests.initialize()
            self.npcs.initialize()
            self.achievements.initialize()
            self.diary.initialize(save_slot)
            #self.story_reader.initialize()
            
            # 初始化游戏时间
            self.game_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
            self.day_count = 1
            self.weather = "sunny"
            self.season = "spring"
            self.temperature = 20
            self.radiation_level = 0
            self.fatigue = 0
            self.completed_research = []
            
            # 应用初始天气效果
            self.apply_weather_effect()
            
            # 进入游戏界面
            self.ui.create_game_interface()
            self.game_state = "playing"
            
            # 触发初始事件
            self.trigger_initial_events()
            
            logging.info("新游戏开始成功")
        except Exception as e:
            logging.error(f"开始新游戏时出错: {e}")
            messagebox.showerror("错误", f"开始新游戏时出错: {e}")
    
    def load_game(self, save_slot):
        """加载游戏"""
        try:
            logging.info(f"加载游戏，存档槽: {save_slot}")
            save_data = self.save_system.load_game(save_slot)
            if not save_data:
                messagebox.showerror("错误", "存档文件损坏或不存在")
                return
            self.current_save_slot = save_slot
            
            self.items.initialize()
            self.combat.initialize()
            self.farming.initialize()
            self.quests.initialize()
            self.npcs.initialize()
            self.achievements.initialize()
            self.player.load_data(save_data.get('player', {}))
            self.world.load_data(save_data.get('world', {}))
            self.items.load_data(save_data.get('items', {}))
            self.farming.load_data(save_data.get('farming', {}))
            self.quests.load_data(save_data.get('quests', {}))
            self.npcs.load_data(save_data.get('npcs', {}))
            self.achievements.load_data(save_data.get('achievements', {}))
            self.story_reader.load_data(save_data.get('stories', {}))
            self.diary.initialize(save_slot)
            if not self.world.locations:
                world_data = self.terrain_gen.generate_map()
                self.world.generate_world(world_data)
                self.world.load_data(save_data.get('world', {}))
            if self.player.location in self.world.locations:
                self.world.current_location_id = self.player.location
            
            # 加载游戏状态
            self.game_time = datetime.fromisoformat(save_data.get('game_time', datetime.now().isoformat()))
            self.day_count = save_data.get('day_count', 1)
            self.weather = save_data.get('weather', 'sunny')
            self.season = save_data.get('season', 'spring')
            self.temperature = save_data.get('temperature', 20)
            self.radiation_level = save_data.get('radiation_level', 0)
            self.fatigue = save_data.get('fatigue', 0)
            self.completed_research = list(save_data.get('completed_research', []))
            
            # 应用天气效果
            self.apply_weather_effect()
            
            # 进入游戏界面
            self.ui.create_game_interface()
            self.game_state = "playing"
            
            self.add_game_log(f"游戏加载成功！欢迎回来，{self.player.name}。")
            self.add_game_log(f"现在是第{self.day_count}天，{self.format_time()}。")
            logging.info("游戏加载成功")
        except Exception as e:
            logging.error(f"加载游戏时出错: {e}")
            messagebox.showerror("错误", f"加载游戏时出错: {e}")
    
    def save_game(self):
        """保存游戏"""
        logging.info(f"尝试保存游戏，存档槽: {self.current_save_slot}")
        if not self.current_save_slot:
            return
        try:
            save_data = {
                'player': self.player.get_save_data(),
                'world': self.world.get_save_data(),
                'items': self.items.get_save_data(),
                'farming': self.farming.get_save_data(),
                'quests': self.quests.get_save_data(),
                'npcs': self.npcs.get_save_data(),
                'achievements': self.achievements.get_save_data(),
                'stories': self.story_reader.get_save_data(),
                'game_time': self.game_time.isoformat(),
                'day_count': self.day_count,
                'weather': self.weather,
                'season': self.season,
                'temperature': self.temperature,
                'radiation_level': self.radiation_level,
                'fatigue': self.fatigue,
                'completed_research': list(self.completed_research),
                'save_time': datetime.now().isoformat(),
                'version': self.version
            }
            success = self.save_system.save_game(self.current_save_slot, save_data)
            if success:
                self.diary.save()
                logging.info(f"游戏保存成功，存档槽: {self.current_save_slot}")
            else:
                logging.error("游戏保存失败")
        except Exception as e:
            logging.error(f"保存游戏时出错: {e}")
    
    def add_game_log(self, message):
        """添加游戏日志"""
        if hasattr(self, 'ui') and self.ui:
            timestamp = self.game_time.strftime("%H:%M")
            self.ui.add_log_message(f"[{timestamp}] {message}")
    
    def format_time(self):
        """格式化游戏时间"""
        return self.game_time.strftime("%H:%M")
    
    def advance_time(self, hours=1):
        """推进游戏时间"""
        if self.game_state != "playing":
            return
        actual_hours = hours * self.game_speed
        old_day = self.game_time.date()
        self.game_time += timedelta(hours=actual_hours)
        self.handle_time_advancement(actual_hours)
        days_passed = (self.game_time.date() - old_day).days
        for _ in range(max(0, days_passed)):
            self.new_day()
    
    def is_night(self):
        if not self.game_time:
            return False
        hour = self.game_time.hour
        return hour < 6 or hour >= 18

    def get_time_of_day_name(self):
        if not self.game_time:
            return "白天"
        hour = self.game_time.hour
        if 5 <= hour < 8:
            return "清晨"
        if 8 <= hour < 18:
            return "白天"
        if 18 <= hour < 22:
            return "黄昏"
        return "夜晚"

    def handle_time_advancement(self, hours):
        """处理时间推进相关事件"""
        hour = self.game_time.hour
        was_night = self.player.night_penalty
        if 6 <= hour < 18:
            base_temp = 20 if self.season == "spring" else 30 if self.season == "summer" else 15 if self.season == "autumn" else 5
            self.temperature = base_temp + random.randint(-3, 5)
            self.player.night_penalty = False
            if was_night:
                self.add_game_log("天亮了，视野恢复，行动不再受夜间影响。")
        else:
            base_temp = 10 if self.season == "spring" else 20 if self.season == "summer" else 5 if self.season == "autumn" else -5
            self.temperature = base_temp + random.randint(-5, 3)
            self.player.night_penalty = True
            if not was_night:
                self.add_game_log("夜幕降临，体力消耗增加，遭遇敌人的几率上升。")
        
        self.player.handle_time_passage(hours)
        self.farming.update_crops_growth(hours)
        self.quests.check_timed_quests()
    
    def new_day(self):
        """新的一天"""
        self.day_count += 1
        self.add_game_log(f"=== 第{self.day_count}天开始 ===")
        self.player.daily_recovery()
        self.player.daily_consumption()
        self.player.modify_fatigue(-5)
        self.check_season_change()
        self.update_weather()
        self.adjust_seasonal_resources()
        self.quests.check_daily_quests()
        self.npcs.move_wandering_npcs()
        if self.day_count % 3 == 0:
            self.npcs.restock_shops()
        self.trigger_random_event()
        self.achievements.check_daily_achievements()
        self.try_unlock_stories()
        logging.info(f"进入第{self.day_count}天")
    
    def check_season_change(self):
        """检查季节变化"""
        if self.day_count % 30 == 0:  # 每30天换季
            seasons = ["spring", "summer", "autumn", "winter"]
            current_index = seasons.index(self.season)
            new_index = (current_index + 1) % 4
            old_season = self.season
            self.season = seasons[new_index]
            season_names = {"spring": "春季", "summer": "夏季", "autumn": "秋季", "winter": "冬季"}
            self.add_game_log(f"季节变换：从{season_names[old_season]}进入了{season_names[self.season]}。")
    
    def update_weather(self):
        """更新天气"""
        weather_weights = {
            "spring": {"sunny": 30, "rainy": 35, "cloudy": 25, "foggy": 8, "stormy": 2},
            "summer": {"sunny": 50, "rainy": 20, "cloudy": 15, "foggy": 5, "stormy": 10},
            "autumn": {"sunny": 40, "rainy": 25, "cloudy": 25, "foggy": 8, "stormy": 2},
            "winter": {"sunny": 30, "rainy": 10, "cloudy": 40, "foggy": 15, "stormy": 5}
        }
        weights = weather_weights.get(self.season, weather_weights["spring"])
        if self.season == "winter":
            weights["snowstorm"] = 10
        if self.season == "summer":
            weights["sandstorm"] = 5
        if self.radiation_level > 50:
            weights["radiation_dust"] = 15
        weather_types = list(weights.keys())
        weight_values = list(weights.values())
        old_weather = self.weather
        self.weather = random.choices(weather_types, weights=weight_values)[0]
        self.apply_weather_effect()
        if old_weather != self.weather:
            weather_names = {
                "sunny": "晴朗", "rainy": "雨天", "cloudy": "多云", "foggy": "雾天",
                "stormy": "暴风雨", "snowstorm": "暴风雪", "sandstorm": "沙尘暴",
                "radiation_dust": "辐射尘"
            }
            self.add_game_log(f"天气变化：现在是{weather_names.get(self.weather, self.weather)}。")
    
    def apply_weather_effect(self):
        """根据当前天气应用影响"""
        effects = {
            "sunny": {"stamina_mod": 1.0, "health_mod": 1.0, "mental_mod": 1.0, "resource_mod": 1.0, "move_cost_mod": 1.0, "description": "晴朗，适合活动"},
            "rainy": {"stamina_mod": 0.9, "health_mod": 1.0, "mental_mod": 0.95, "resource_mod": 0.8, "move_cost_mod": 1.2, "description": "雨天，路面湿滑"},
            "cloudy": {"stamina_mod": 1.0, "health_mod": 1.0, "mental_mod": 0.9, "resource_mod": 0.9, "move_cost_mod": 1.0, "description": "多云，略显沉闷"},
            "foggy": {"stamina_mod": 0.9, "health_mod": 1.0, "mental_mod": 0.9, "resource_mod": 0.7, "move_cost_mod": 1.1, "description": "浓雾，视野不佳"},
            "stormy": {"stamina_mod": 0.7, "health_mod": 0.9, "mental_mod": 0.8, "resource_mod": 0.5, "move_cost_mod": 1.5, "description": "暴风雨，行动困难"},
            "snowstorm": {"stamina_mod": 0.6, "health_mod": 0.8, "mental_mod": 0.7, "resource_mod": 0.4, "move_cost_mod": 1.8, "description": "暴风雪，极寒"},
            "sandstorm": {"stamina_mod": 0.5, "health_mod": 0.7, "mental_mod": 0.6, "resource_mod": 0.3, "move_cost_mod": 2.0, "description": "沙尘暴，呼吸困难"},
            "radiation_dust": {"stamina_mod": 0.7, "health_mod": 0.5, "mental_mod": 0.5, "resource_mod": 0.4, "move_cost_mod": 1.2, "description": "辐射尘，辐射增加"}
        }
        self.weather_effects = effects.get(self.weather, effects["sunny"])
        if self.weather == "stormy":
            self.player.modify_health(-1)
        elif self.weather == "snowstorm":
            self.player.modify_health(-2)
            self.player.modify_stamina(-3)
        elif self.weather == "sandstorm":
            self.player.modify_health(-2)
            self.player.modify_stamina(-5)
        elif self.weather == "radiation_dust":
            self.radiation_level += 5
            self.player.modify_health(-3)
    
    def adjust_seasonal_resources(self):
        """按季节刷新各地点可再生资源。"""
        if not getattr(self.world, 'locations', None):
            return
        season_mods = {
            "spring": {"food": 1.3, "water": 1.2, "wood": 1.1, "medicine": 1.2, "rare_herbs": 1.3, "materials": 1.0, "stone": 0.9},
            "summer": {"food": 1.1, "water": 0.8, "wood": 1.0, "medicine": 1.0, "rare_herbs": 0.9, "materials": 1.1, "stone": 1.0},
            "autumn": {"food": 1.4, "water": 1.0, "wood": 1.2, "medicine": 0.9, "rare_herbs": 1.1, "materials": 1.0, "stone": 1.0},
            "winter": {"food": 0.6, "water": 0.7, "wood": 0.8, "medicine": 0.7, "rare_herbs": 0.5, "materials": 0.9, "stone": 1.2}
        }
        mods = season_mods.get(self.season, season_mods["spring"])
        weather_mod = self.weather_effects.get("resource_mod", 1.0)
        refreshed = 0
        for location in self.world.locations.values():
            terrain_cfg = None
            if hasattr(self, 'terrain_gen') and self.terrain_gen:
                terrain_cfg = self.terrain_gen.terrain_types.get(location.terrain)
            if terrain_cfg and terrain_cfg.resource_distribution:
                for res_type, prob in terrain_cfg.resource_distribution.items():
                    chance = min(0.95, prob * mods.get(res_type, 1.0) * weather_mod)
                    if random.random() < chance:
                        gain = max(1, int(random.randint(1, 2) * mods.get(res_type, 1.0) * weather_mod))
                        location.resources[res_type] = location.resources.get(res_type, 0) + gain
                        refreshed += gain
            else:
                for res_type in list(location.resources.keys()):
                    current = location.resources.get(res_type, 0)
                    if current <= 0:
                        continue
                    location.resources[res_type] = max(1, int(current * mods.get(res_type, 1.0) * weather_mod))
        if self.day_count % 30 == 0:
            season_names = {"spring": "春季", "summer": "夏季", "autumn": "秋季", "winter": "冬季"}
            self.add_game_log(f"{season_names.get(self.season, self.season)}改变了各地资源分布。")
        if refreshed:
            logging.info(f"季节资源刷新，新增约 {refreshed} 点资源")
    
    def trigger_initial_events(self):
        self.add_game_log(f"欢迎，{self.player.name}！你开始了在末日世界的生存之旅。")
        self.add_game_log(f"现在是第{self.day_count}天，{self.format_time()}，天气{self.get_weather_name()}。")
        self.add_game_log("这个世界充满了危险和机遇，谨慎选择你的每一步行动。")
        self.achievements.unlock("first_step")
        if 'main_01' in self.quests.quests:
            self.quests.start_quest('main_01')
    
    def trigger_random_event(self):
        event_chance = random.randint(1, 100)
        if event_chance <= 10:
            events = [
                self.event_mysterious_traveler,
                self.event_abandoned_supplies,
                self.event_animal_encounter,
                self.event_weather_anomaly,
                self.event_radio_signal
            ]
            random.choice(events)()
    
    def event_mysterious_traveler(self):
        self.add_game_log("你在路上遇到了一位神秘的旅行者，他给了你一些有用的建议。")
        self.player.add_item("food", 2)
        self.player.add_item("water", 2)
    
    def event_abandoned_supplies(self):
        self.add_game_log("你发现了一处废弃的营地，找到了一些有用的物资。")
        loot = random.choice([
            {"materials": 5},
            {"medicine": 2},
            {"food": 3, "water": 3}
        ])
        for item, amount in loot.items():
            self.player.add_item(item, amount)
    
    def event_animal_encounter(self):
        animals = ["温顺的鹿", "警惕的狐狸", "好奇的松鼠"]
        animal = random.choice(animals)
        self.add_game_log(f"你遇到了一只{animal}，它好奇地看了你一眼后跑开了。")
    
    def event_weather_anomaly(self):
        self.add_game_log("你注意到今天的天气有些异常，空气中弥漫着奇怪的能量。")
        self.radiation_level += 5
    
    def event_radio_signal(self):
        self.add_game_log("你的收音机突然接收到一段微弱的信号，但很快就消失了...")
    
    def get_weather_name(self):
        names = {"sunny": "晴朗", "rainy": "雨天", "cloudy": "多云", "foggy": "雾天", "stormy": "暴风雨", "snowstorm": "暴风雪", "sandstorm": "沙尘暴", "radiation_dust": "辐射尘"}
        return names.get(self.weather, self.weather)
    
    def get_season_name(self):
        names = {"spring": "春季", "summer": "夏季", "autumn": "秋季", "winter": "冬季"}
        return names.get(self.season, self.season)
    
    def perform_action(self, action_type, **kwargs):
        """执行游戏动作"""
        if self.game_state != "playing":
            return
        try:
            if action_type == "explore":
                self.action_explore()
            elif action_type == "rest":
                self.action_rest()
            elif action_type == "sleep":
                self.action_sleep(kwargs.get('hours', 8))
            elif action_type == "eat":
                self.action_eat(kwargs.get('food_type'))
            elif action_type == "drink":
                self.action_drink(kwargs.get('drink_type'))
            elif action_type == "craft":
                self.action_craft(kwargs.get('recipe_id'), kwargs.get('tier', 2))
            elif action_type == "farm":
                self.action_farm(kwargs.get('crop_type'))
            elif action_type == "harvest":
                self.action_harvest(kwargs.get('plot_id'))
            elif action_type == "water_crops":
                self.action_water_crops(kwargs.get('plot_id'))
            elif action_type == "remove_weeds":
                self.action_remove_weeds(kwargs.get('plot_id'))
            elif action_type == "clear_farmland":
                self.action_clear_farmland()
            elif action_type == "expand_farmland":
                self.action_expand_farmland()
            elif action_type == "fertilize":
                self.action_fertilize()
            elif action_type == "move":
                self.action_move(kwargs.get('location_id'))
            elif action_type == "use_item":
                self.action_use_item(kwargs.get('item_id'))
            elif action_type == "fish":
                self.action_fish()
            elif action_type == "hunt":
                self.action_hunt()
            elif action_type == "chop_wood":
                self.action_chop_wood()
            elif action_type == "gather_herbs":
                self.action_gather_herbs()
            elif action_type == "trade":
                self.action_trade()
            elif action_type == "repair":
                self.action_repair(kwargs.get('item_id'))
            elif action_type == "build":
                self.action_build(kwargs.get('structure_id'))
            elif action_type == "research":
                self.action_research(kwargs.get('project_id'))
            elif action_type == "meditate":
                self.action_meditate()
            else:
                self.add_game_log(f"未知动作: {action_type}")
        except Exception as e:
            logging.error(f"执行动作时出错: {e}")
            self.add_game_log(f"执行动作时出错: {e}")
    
    def action_explore(self):
        """探索动作"""
        if self.game_state != "playing":
            return
        if self.player.stamina < 10:
            self.add_game_log("体力不足，无法探索。")
            return
        if self.player.is_overencumbered():
            self.add_game_log("负重过高，探索变得更加吃力。")
        current_location = self.world.get_current_location()
        self.add_game_log(f"你在{current_location.name}仔细探索...")
        self.player.modify_stamina(-10)
        self.advance_time(2)
        event_result = self.world.generate_exploration_event()
        if event_result and event_result.get('type') != 'nothing':
            self.handle_exploration_event(event_result)
            event_type = event_result['type']
            exp_rewards = {'resource': 8, 'enemy': 10, 'discovery': 15, 'npc': 12, 'special': 20}
            self.player.gain_skill_exp('survival', exp_rewards.get(event_type, 5))
            self.achievements.check_exploration_achievements()
            self.add_game_log(event_result.get('message', '探索完成'))
        else:
            self.add_game_log("探索完毕，但没有发现特别的东西。")
            self.player.gain_skill_exp('survival', 3)
    
    def action_rest(self):
        if self.player.stamina >= self.player.max_stamina and self.player.health >= self.player.max_health:
            self.add_game_log("你不需要休息。")
            return
        self.add_game_log("你休息了一会儿...")
        self.advance_time(2)
        stamina_recovery = min(30, self.player.max_stamina - self.player.stamina)
        health_recovery = min(15, self.player.max_health - self.player.health)
        self.player.modify_stamina(stamina_recovery)
        self.player.modify_health(health_recovery)
        self.add_game_log(f"休息后，你恢复了{stamina_recovery}点体力和{health_recovery}点生命值。")
    
    def action_sleep(self, hours=8):
        if hours < 2:
            self.add_game_log("睡眠时间太短，无法有效休息。")
            return
        self.add_game_log(f"你睡了{hours}小时...")
        self.advance_time(hours)
        result = self.player.sleep(hours)
        self.add_game_log(f"睡眠后，你恢复了{int(result['stamina_recovery'])}体力、{int(result['health_recovery'])}生命值和{int(result['mental_recovery'])}精神值。")
    
    def action_eat(self, food_type):
        if not food_type:
            self.add_game_log("请指定要吃的食物。")
            return
        if not self.player.has_item(food_type):
            self.add_game_log(f"你没有{self.items.get_item_name(food_type)}。")
            return
        food_data = self.items.get_item_data(food_type)
        if not food_data or food_data.get('type') != 'food':
            self.add_game_log("这不是可食用的物品。")
            return
        self.player.remove_item(food_type, 1)
        health_restore = food_data.get('health_restore', 0)
        stamina_restore = food_data.get('stamina_restore', 0)
        mental_restore = food_data.get('mental_restore', 0)
        self.player.modify_health(health_restore)
        self.player.modify_stamina(stamina_restore)
        self.player.modify_mental(mental_restore)
        self.advance_time(0.5)
        self.add_game_log(f"你吃了{self.items.get_item_name(food_type)}，恢复了{health_restore}生命值、{stamina_restore}体力和{mental_restore}精神值。")
    
    def action_drink(self, drink_type):
        if not drink_type:
            self.add_game_log("请指定要喝的饮品。")
            return
        if not self.player.has_item(drink_type):
            self.add_game_log(f"你没有{self.items.get_item_name(drink_type)}。")
            return
        drink_data = self.items.get_item_data(drink_type)
        if not drink_data or drink_data.get('type') != 'drink':
            self.add_game_log("这不是可饮用的物品。")
            return
        self.player.remove_item(drink_type, 1)
        health_restore = drink_data.get('health_restore', 0)
        stamina_restore = drink_data.get('stamina_restore', 0)
        mental_restore = drink_data.get('mental_restore', 0)
        self.player.modify_health(health_restore)
        self.player.modify_stamina(stamina_restore)
        self.player.modify_mental(mental_restore)
        self.advance_time(0.5)
        self.add_game_log(f"你喝了{self.items.get_item_name(drink_type)}，恢复了{health_restore}生命值、{stamina_restore}体力和{mental_restore}精神值。")
    
    def action_farm(self, crop_type):
        if not self.farming.can_plant(self.player.location):
            self.add_game_log("这里不能种植。")
            return
        planting_result = self.farming.plant_crop(crop_type, self.player.location)
        if planting_result['success']:
            self.add_game_log(planting_result['message'])
            self.advance_time(2)
            self.player.modify_stamina(-15)
        else:
            self.add_game_log(planting_result['message'])

    def action_harvest(self, plot_id):
        result = self.farming.harvest_crop(self.player.location, plot_id)
        self.add_game_log(result['message'])
        if result.get('success'):
            self.advance_time(1)
            self.player.modify_stamina(-8)

    def action_water_crops(self, plot_id=None):
        result = self.farming.water_crops(self.player.location, plot_id)
        self.add_game_log(result['message'])
        if result.get('success'):
            self.advance_time(0.5)

    def action_clear_farmland(self):
        result = self.farming.clear_farmland(self.player.location)
        self.add_game_log(result['message'])
        if result.get('success'):
            self.advance_time(2)
            self.player.modify_stamina(-20)
            self.try_unlock_stories()

    def action_expand_farmland(self):
        result = self.farming.expand_farmland(self.player.location)
        self.add_game_log(result['message'])
        if result.get('success'):
            self.advance_time(1)
            self.player.modify_stamina(-12)

    def action_fertilize(self):
        result = self.farming.fertilize_soil(self.player.location)
        self.add_game_log(result['message'])
        if result.get('success'):
            self.advance_time(0.5)
            self.player.modify_stamina(-6)

    def action_remove_weeds(self, plot_id):
        result = self.farming.remove_weeds(self.player.location, plot_id)
        self.add_game_log(result['message'])
        if result.get('success'):
            self.advance_time(0.5)
    
    def action_craft(self, recipe_id, tier=2):
        if not recipe_id:
            self.add_game_log("请指定要制作的物品。")
            return
        recipe_data = self.items.get_recipe_with_tier(recipe_id, tier)
        if not recipe_data:
            self.add_game_log("未知的制作配方或挡级无效。")
            return
        craft_result = self.player.craft_item_with_tier(recipe_id, tier, recipe_data)
        if craft_result['success']:
            self.add_game_log(craft_result['message'])
            self.advance_time(1)
            self.player.modify_stamina(-5)
        else:
            self.add_game_log(craft_result['message'])
    
    def action_move(self, location_id):
        if not location_id:
            self.add_game_log("请指定要移动到的地点。")
            return
        if self.player.is_overencumbered() and self.player.stamina < 12:
            self.add_game_log("负重过高且体力不足，无法继续赶路。")
            return
        move_result = self.world.move_to_location(location_id)
        if move_result['success']:
            self.add_game_log(move_result['message'])
            hours = 1.0 if self.is_night() else 0.5
            self.advance_time(hours)
            self.player.modify_stamina(-5)
            self.try_unlock_stories()
        else:
            self.add_game_log(move_result['message'])
    
    def action_use_item(self, item_id):
        if not item_id:
            self.add_game_log("请指定要使用的物品。")
            return
        if not self.player.has_item(item_id):
            self.add_game_log(f"你没有{self.items.get_item_name(item_id)}。")
            return
        use_result = self.player.use_item(item_id)
        if use_result['success']:
            self.add_game_log(use_result['message'])
            self.advance_time(0.5)
        else:
            self.add_game_log(use_result['message'])
    
    def action_fish(self):
        loc = self.world.get_current_location()
        if loc.terrain not in ["河流", "湖泊", "river", "lake"]:
            self.add_game_log("只有在水边才能钓鱼。")
            return
        if not self.player.has_item("fishing_rod"):
            self.add_game_log("你需要鱼竿才能钓鱼。")
            return
        if self.player.stamina < 8:
            self.add_game_log("体力不足，无法钓鱼。")
            return
        self.player.modify_stamina(-8)
        self.advance_time(2)
        skill = self.player.skills['survival']
        luck = self.player.luck
        weather_mod = self.weather_effects.get("resource_mod", 1.0)
        catch_chance = 0.3 + skill * 0.05 + luck * 0.01
        if random.random() < catch_chance * weather_mod:
            fish_amount = random.randint(1, 3) + skill // 2
            self.player.add_item("food", fish_amount)
            self.add_game_log(f"你钓到了{fish_amount}条鱼！")
            self.player.gain_skill_exp('survival', 6)
        else:
            self.add_game_log("今天运气不佳，一条鱼也没钓到。")
        self.player.degrade_item("fishing_rod", 1)
    
    def action_hunt(self):
        loc = self.world.get_current_location()
        if loc.terrain not in ["森林", "平原", "forest", "plain"]:
            self.add_game_log("只有在森林或平原才能狩猎。")
            return
        weapon = self.player.equipment.get('weapon')
        if not weapon:
            self.add_game_log("你需要武器才能狩猎。")
            return
        if self.player.stamina < 15:
            self.add_game_log("体力不足，无法狩猎。")
            return
        self.player.modify_stamina(-15)
        self.advance_time(3)
        skill = self.player.skills['combat']
        luck = self.player.luck
        weather_mod = self.weather_effects.get("resource_mod", 1.0)
        success_chance = 0.4 + skill * 0.05 + luck * 0.01
        if random.random() < success_chance * weather_mod:
            meat = random.randint(2, 5) + skill // 3
            leather = random.randint(1, 2) if random.random() < 0.5 else 0
            self.player.add_item("food", meat)
            if leather > 0:
                self.player.add_item("leather", leather)
            self.add_game_log(f"狩猎成功！获得了{meat}份肉" + (f"和{leather}张皮革" if leather else ""))
            self.player.gain_skill_exp('combat', 12)
        else:
            if random.random() < 0.3:
                damage = random.randint(5, 15)
                self.player.modify_health(-damage)
                self.add_game_log(f"狩猎失败，你被动物反击，受到了{damage}点伤害！")
            else:
                self.add_game_log("狩猎失败，什么也没抓到。")
        if weapon:
            self.player.degrade_item(weapon, 1)
    
    def action_chop_wood(self):
        loc = self.world.get_current_location()
        if loc.terrain not in ["森林", "forest"]:
            self.add_game_log("只有在森林才能砍柴。")
            return
        if self.player.stamina < 12:
            self.add_game_log("体力不足，无法砍柴。")
            return
        self.player.modify_stamina(-12)
        self.advance_time(2)
        skill = self.player.skills['survival']
        weather_mod = self.weather_effects.get("resource_mod", 1.0)
        wood_amount = random.randint(3, 6) + skill // 2
        wood_amount = int(wood_amount * weather_mod)
        wood_amount = max(1, wood_amount)
        self.player.add_item("wood", wood_amount)
        self.add_game_log(f"你砍到了{wood_amount}个木材。")
        self.player.gain_skill_exp('survival', 4)
    
    def action_gather_herbs(self):
        loc = self.world.get_current_location()
        if loc.terrain not in ["森林", "山地", "forest", "mountain"]:
            self.add_game_log("只有在森林或山地才能采药。")
            return
        if self.player.stamina < 8:
            self.add_game_log("体力不足，无法采药。")
            return
        self.player.modify_stamina(-8)
        self.advance_time(2)
        skill = self.player.skills['medical']
        weather_mod = self.weather_effects.get("resource_mod", 1.0)
        herb_count = random.randint(1, 3) + skill // 3
        herb_count = int(herb_count * weather_mod)
        herb_count = max(1, herb_count)
        herbs = ["rare_herbs", "medicine"]
        for _ in range(herb_count):
            herb = random.choice(herbs)
            self.player.add_item(herb, 1)
        self.add_game_log(f"你采集到了{herb_count}份草药。")
        self.player.gain_skill_exp('medical', 8)
    
    def action_trade(self):
        self.ui.show_trade_dialog()
    
    def action_repair(self, item_id=None):
        if self.game_state != "playing":
            return
        if not item_id:
            self.ui.show_repair_dialog()
            return
        result = self.player.repair_item(item_id)
        self.add_game_log(result['message'])
        if result.get('success'):
            self.advance_time(2)

    def get_buildable_structures(self):
        return [
            {
                "id": "shelter", "name": "简易庇护所",
                "materials": {"wood": 10, "cloth": 5, "materials": 8},
                "description": "提高当前地点安全性，睡眠恢复更好",
                "effects": {"safety": 2}
            },
            {
                "id": "storage_box", "name": "储物箱",
                "materials": {"wood": 5, "metal": 2},
                "description": "在当前地点存放多余物资",
                "effects": {"storage": True}
            },
            {
                "id": "workbench", "name": "工作台",
                "materials": {"wood": 8, "metal": 3},
                "description": "降低制作消耗，提升修理效果",
                "effects": {"crafting_bonus": 1}
            },
            {
                "id": "farm_fence", "name": "农田围栏",
                "materials": {"wood": 15, "materials": 5},
                "description": "保护农作物，减少野兽破坏",
                "effects": {"farm_fence": True}
            }
        ]

    def action_build(self, structure_id):
        if self.game_state != "playing":
            return {'success': False, 'message': '当前无法建造'}
        structure = next((s for s in self.get_buildable_structures() if s['id'] == structure_id), None)
        if not structure:
            return {'success': False, 'message': '未知建筑'}
        location = self.world.get_current_location()
        if not location:
            return {'success': False, 'message': '未知地点'}
        if structure_id in getattr(location, 'structures', []):
            return {'success': False, 'message': f'{location.name}已经有{structure["name"]}'}
        for material, amount in structure['materials'].items():
            if not self.player.has_item(material, amount):
                return {'success': False, 'message': f"材料不足，需要{self.items.get_item_name(material)}x{amount}"}
        if self.player.stamina < 12:
            return {'success': False, 'message': '体力不足，无法建造'}
        for material, amount in structure['materials'].items():
            self.player.remove_item(material, amount)
        self.player.modify_stamina(-12)
        self.advance_time(2)
        if not hasattr(location, 'structures') or location.structures is None:
            location.structures = []
        location.structures.append(structure_id)
        effects = structure.get('effects', {})
        if effects.get('safety'):
            location.safety_level = min(10, location.safety_level + int(effects['safety']))
        if effects.get('farm_fence') and hasattr(self, 'farming'):
            farmland = self.farming.farmlands.get(location.id)
            if farmland:
                farmland.setdefault('upgrades', {})['fence'] = True
        self.player.gain_skill_exp('crafting', 20)
        self.player.stats['items_crafted'] = self.player.stats.get('items_crafted', 0) + 1
        if hasattr(self, 'quests') and self.quests:
            self.quests.update_quest_progress('item_crafted', item_id=structure_id)
            self.quests.update_quest_progress('structure_built', structure=structure_id)
        message = f"在{location.name}建造了{structure['name']}！"
        self.add_game_log(message)
        return {'success': True, 'message': message}
    
    def get_research_projects(self):
        return [
            {"id": "basic_farming", "name": "基础农业技术", "cost": {"research_data": 5}, "description": "提高农作物产量"},
            {"id": "basic_medical", "name": "简易医疗知识", "cost": {"research_data": 3}, "description": "解锁新的医疗配方"},
            {"id": "weapon_upgrade", "name": "武器改良技术", "cost": {"research_data": 8}, "description": "提高武器伤害"},
            {"id": "energy_tech", "name": "能源利用技术", "cost": {"research_data": 10}, "description": "解锁简易能源设备"}
        ]

    def action_research(self, project_id=None):
        if self.game_state != "playing":
            return {'success': False, 'message': '当前无法研究'}
        if self.player.stamina < 5:
            self.add_game_log("体力不足，无法研究。")
            return {'success': False, 'message': '体力不足，无法研究'}
        if not project_id:
            if not self.player.has_item("research_data"):
                self.add_game_log("你需要研究资料才能进行研究。")
                return {'success': False, 'message': '你需要研究资料才能进行研究'}
            self.player.modify_stamina(-5)
            self.player.remove_item("research_data", 1)
            self.advance_time(3)
            self.player.gain_skill_exp('intelligence', 15)
            self.add_game_log("你花时间研究了科技资料，获得了一些新知识。")
            return {'success': True, 'message': '研究完成'}
        project = next((p for p in self.get_research_projects() if p['id'] == project_id), None)
        if not project:
            return {'success': False, 'message': '未知研究项目'}
        if project_id in self.completed_research:
            return {'success': False, 'message': f'{project["name"]}已经完成'}
        for material, amount in project['cost'].items():
            if not self.player.has_item(material, amount):
                return {'success': False, 'message': f"资料不足，需要{self.items.get_item_name(material)}x{amount}"}
        for material, amount in project['cost'].items():
            self.player.remove_item(material, amount)
        self.player.modify_stamina(-5)
        self.advance_time(3)
        self.player.gain_skill_exp('intelligence', 20)
        self.completed_research.append(project_id)
        message = f"完成研究：{project['name']}！"
        self.add_game_log(message)
        return {'success': True, 'message': message}
    
    def action_meditate(self):
        if self.game_state != "playing":
            return
        if self.player.stamina < 2:
            self.add_game_log("体力不足，无法冥想。")
            return
        self.player.modify_stamina(-2)
        self.advance_time(1)
        mental_recovery = 15
        self.player.modify_mental(mental_recovery)
        self.add_game_log(f"冥想让你平静下来，恢复了{mental_recovery}点精神值。")
        self.player.gain_skill_exp('mental', 3)
    
    def handle_exploration_event(self, event_result):
        event_type = event_result['type']
        if event_type == "resource":
            resource_type = event_result['resource_type']
            amount = event_result['amount']
            item_name = self.items.get_item_name(resource_type)
            if self.player.add_item(resource_type, amount):
                self.add_game_log(f"你找到了{amount}个{item_name}！")
            else:
                self.add_game_log(f"发现了{amount}个{item_name}，但负重已满，无法带走。")
        elif event_type == "enemy":
            enemy_data = event_result['enemy_data']
            combat_result = self.combat.start_combat(self.player, enemy_data)
            self.handle_combat_result(combat_result)
        elif event_type == "discovery":
            new_location = event_result['location']
            self.world.discover_location(new_location)
            self.add_game_log(f"你发现了一个新地点：{new_location.name}！")
            self.try_unlock_stories()
        elif event_type == "npc":
            npc_data = event_result['npc_data']
            self.npcs.add_encountered_npc(npc_data)
            self.add_game_log(f"你遇到了{npc_data['name']}！")
        elif event_type == "nothing":
            self.add_game_log("探索完毕，但没有发现特别的东西。")
        elif event_type == "special":
            self.add_game_log(event_result['message'])
            if event_result.get('reward'):
                for item, amount in event_result['reward'].items():
                    self.player.add_item(item, amount)
    
    def handle_combat_result(self, combat_result):
        if combat_result.get('escaped'):
            self.add_game_log("你逃离了战斗。")
            return
        if combat_result.get('player_won'):
            self.add_game_log(f"你击败了{combat_result['enemy_name']}！")
            if combat_result.get('loot'):
                for item, amount in combat_result['loot'].items():
                    if self.player.add_item(item, amount):
                        self.add_game_log(f"获得了{amount}个{self.items.get_item_name(item)}！")
                    else:
                        self.add_game_log(f"战利品{self.items.get_item_name(item)}x{amount}因负重已满未能带走。")
            self.achievements.check_combat_achievements(combat_result.get('enemy_name', ''))
            self.try_unlock_stories()
        else:
            self.add_game_log("战斗失败！你受了重伤。")
            self.player.modify_health(-20)
            self.player.modify_mental(-15)

    def try_unlock_stories(self):
        if not getattr(self, 'story_reader', None):
            return
        unlocked = self.story_reader.check_unlock_conditions({
            'location': self.player.location,
            'discovered_locations': self.player.discovered_locations,
            'quests_completed': self.quests.completed_quests if getattr(self, 'quests', None) else [],
            'enemies_defeated': self.player.stats.get('enemies_defeated', 0),
            'day_count': self.day_count,
            'farmlands': list(self.farming.farmlands.keys()) if getattr(self, 'farming', None) else [],
        })
        for title in unlocked:
            self.add_game_log(f"解锁故事：{title}")
    
    def start_autosave(self):
        def autosave_loop():
            while self.autosave_running:
                time.sleep(300)
                if self.game_state == "playing" and self.player.initialized:
                    self.save_game()
        self.autosave_thread = threading.Thread(target=autosave_loop, daemon=True)
        self.autosave_thread.start()
    
    def start_game_loop(self):
        def game_loop():
            while self.game_loop_running:
                if self.game_state == "playing" and self.player.initialized:
                    self.ui.update_status_display()
                    self.check_player_status()
                time.sleep(1)
        loop_thread = threading.Thread(target=game_loop, daemon=True)
        loop_thread.start()
    
    def check_player_status(self):
        if self.player.health <= 0:
            self.game_over("生命值耗尽")
        elif self.player.mental <= 0:
            self.game_over("精神崩溃")
        elif self.radiation_level >= 100:
            self.game_over("辐射中毒")
        elif self.player.fatigue >= 100:
            self.game_over("疲劳过度")
    
    def game_over(self, reason):
        self.add_game_log(f"游戏结束！原因：{reason}")
        self.add_game_log(f"你生存了{self.day_count}天。")
        self.achievements.unlock("survival_days", self.day_count)
        self.ui.show_game_over(reason, self.day_count)
        if self.current_save_slot:
            self.save_system.delete_save(self.current_save_slot)
        self.game_state = "menu"
    
    def pause_game(self):
        if self.game_state == "playing":
            self.game_state = "paused"
            self.game_speed = 0
        if hasattr(self, 'ui'):
            self.ui.show_pause_menu()
        logging.info("游戏已暂停")
    
    def resume_game(self):
        if self.game_state == "paused":
            self.game_state = "playing"
            self.game_speed = 1.0
        if hasattr(self, 'ui'):
            self.ui.hide_pause_menu()
        logging.info("游戏已继续")
    
    def show_settings(self):
        if hasattr(self, 'ui'):
            self.ui.show_settings_dialog()
    
    def return_to_main_menu(self):
        if self.game_state == "paused":
            self.resume_game()
        self.show_main_menu()
    
    def change_game_speed(self, speed):
        self.game_speed = speed
        self.add_game_log(f"游戏速度调整为{speed}倍。")
    
    def on_closing(self):
        logging.info("游戏关闭中...")
        self.autosave_running = False
        self.game_loop_running = False
        if self.game_state == "playing" and self.player.initialized:
            self.save_game()
        self.root.destroy()
        logging.info("游戏已关闭")
    
    def execute_command(self, cmd):
        """处理用户输入的指令"""
        cmd = cmd.strip().lower()
        if cmd == "help":
            self.add_game_log("可用指令: help, status, inventory, map, sleep, eat, drink, explore, quit")
        elif cmd == "status":
            self.add_game_log(f"生命: {self.player.health}/{self.player.max_health}, 体力: {self.player.stamina}/{self.player.max_stamina}, 精神: {self.player.mental}/{self.player.max_mental}, 疲劳: {self.player.fatigue}/{self.max_fatigue}, 金钱: {self.player.money}")
        elif cmd == "inventory":
            items = ", ".join([f"{self.items.get_item_name(i)}({q})" for i,q in self.player.inventory.items()])
            self.add_game_log(f"背包: {items}")
        elif cmd == "map":
            self.ui.show_map()
        elif cmd in ("sleep", "eat", "drink", "explore"):
            self.perform_action(cmd)
        elif cmd == "quit":
            self.on_closing()
        else:
            self.add_game_log(f"未知指令: {cmd}")