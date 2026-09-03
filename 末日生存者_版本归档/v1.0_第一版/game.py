# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime, timedelta
import random
import logging

class TextAdventureGame:
    def __init__(self, root):
        self.root = root
        self.setup_game()
        
    def setup_game(self):
        """初始化游戏系统"""
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
            from story_book import StoryBook
            from achievement import AchievementSystem
            
            self.player = Player(self)
            self.world = GameWorld(self)
            self.items = ItemSystem(self)
            self.combat = CombatSystem(self)
            self.farming = FarmingSystem(self)
            self.quests = QuestSystem(self)
            self.npcs = NPCSystem(self)
            self.ui = GameUI(self.root, self)
            self.save_system = SaveSystem(self)
            self.story_book = StoryBook(self)
            self.achievements = AchievementSystem(self)
            
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
            
            # 初始化世界
            self.world.initialize()
            
            # 初始化其他系统
            self.items.initialize()
            self.combat.initialize()
            self.farming.initialize()
            self.quests.initialize()
            self.npcs.initialize()
            self.achievements.initialize()
            
            # 初始化游戏时间
            self.game_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
            self.day_count = 1
            self.weather = "sunny"
            self.season = "spring"
            self.temperature = 20
            self.radiation_level = 0
            
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
            
            # 加载各个系统数据
            self.player.load_data(save_data.get('player', {}))
            self.world.load_data(save_data.get('world', {}))
            self.items.load_data(save_data.get('items', {}))
            self.farming.load_data(save_data.get('farming', {}))
            self.quests.load_data(save_data.get('quests', {}))
            self.npcs.load_data(save_data.get('npcs', {}))
            self.achievements.load_data(save_data.get('achievements', {}))
            
            # 加载游戏状态
            self.game_time = datetime.fromisoformat(save_data.get('game_time', datetime.now().isoformat()))
            self.day_count = save_data.get('day_count', 1)
            self.weather = save_data.get('weather', 'sunny')
            self.season = save_data.get('season', 'spring')
            self.temperature = save_data.get('temperature', 20)
            self.radiation_level = save_data.get('radiation_level', 0)
            
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
        if not self.current_save_slot or self.game_state != "playing":
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
                'game_time': self.game_time.isoformat(),
                'day_count': self.day_count,
                'weather': self.weather,
                'season': self.season,
                'temperature': self.temperature,
                'radiation_level': self.radiation_level,
                'save_time': datetime.now().isoformat(),
                'version': '1.0.0'
            }
            
            success = self.save_system.save_game(self.current_save_slot, save_data)
            if success:
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
        self.game_time += timedelta(hours=actual_hours)
        
        # 处理时间相关事件
        self.handle_time_advancement(actual_hours)
        
        # 检查是否过了一天
        if self.game_time.hour == 0 and actual_hours > 0:
            self.new_day()
    
    def handle_time_advancement(self, hours):
        """处理时间推进相关事件"""
        # 更新温度（日夜变化）
        hour = self.game_time.hour
        if 6 <= hour < 18:  # 白天
            base_temp = 20 if self.season == "spring" else 30 if self.season == "summer" else 15 if self.season == "autumn" else 5
            self.temperature = base_temp + random.randint(-3, 5)
        else:  # 夜晚
            base_temp = 10 if self.season == "spring" else 20 if self.season == "summer" else 5 if self.season == "autumn" else -5
            self.temperature = base_temp + random.randint(-5, 3)
        
        # 玩家自然消耗
        self.player.handle_time_passage(hours)
        
        # 农作物生长
        self.farming.update_crops_growth(hours)
        
        # 任务时间检查
        self.quests.check_timed_quests()
    
    def new_day(self):
        """新的一天"""
        self.day_count += 1
        self.add_game_log(f"=== 第{self.day_count}天开始 ===")
        
        # 每日恢复
        self.player.daily_recovery()
        
        # 每日消耗
        self.player.daily_consumption()
        
        # 检查季节变化
        self.check_season_change()
        
        # 更新天气
        self.update_weather()
        
        # 检查任务
        self.quests.check_daily_quests()
        
        # 随机事件
        self.trigger_random_event()
        
        # 成就检查
        self.achievements.check_daily_achievements()
        
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
        weather_types = list(weights.keys())
        weight_values = list(weights.values())
        
        old_weather = self.weather
        self.weather = random.choices(weather_types, weights=weight_values)[0]
        
        if old_weather != self.weather:
            weather_names = {"sunny": "晴朗", "rainy": "雨天", "cloudy": "多云", "foggy": "雾天", "stormy": "暴风雨"}
            self.add_game_log(f"天气变化：现在是{weather_names[self.weather]}。")
    
    def trigger_initial_events(self):
        """触发初始事件"""
        self.add_game_log(f"欢迎，{self.player.name}！你开始了在末日世界的生存之旅。")
        self.add_game_log(f"现在是第{self.day_count}天，{self.format_time()}，天气{self.get_weather_name()}。")
        self.add_game_log("这个世界充满了危险和机遇，谨慎选择你的每一步行动。")
        
        # 解锁初始成就
        self.achievements.unlock("first_step")
    
    def trigger_random_event(self):
        """触发随机事件"""
        event_chance = random.randint(1, 100)
        
        if event_chance <= 10:  # 10%几率触发事件
            events = [
                self.event_mysterious_traveler,
                self.event_abandoned_supplies,
                self.event_animal_encounter,
                self.event_weather_anomaly,
                self.event_radio_signal
            ]
            random.choice(events)()
    
    def event_mysterious_traveler(self):
        """神秘旅行者事件"""
        self.add_game_log("你在路上遇到了一位神秘的旅行者，他给了你一些有用的建议。")
        self.player.add_item("food", 2)
        self.player.add_item("water", 2)
    
    def event_abandoned_supplies(self):
        """废弃物资事件"""
        self.add_game_log("你发现了一处废弃的营地，找到了一些有用的物资。")
        loot = random.choice([
            {"materials": 5},
            {"medicine": 2},
            {"food": 3, "water": 3}
        ])
        for item, amount in loot.items():
            self.player.add_item(item, amount)
    
    def event_animal_encounter(self):
        """动物遭遇事件"""
        animals = ["温顺的鹿", "警惕的狐狸", "好奇的松鼠"]
        animal = random.choice(animals)
        self.add_game_log(f"你遇到了一只{animal}，它好奇地看了你一眼后跑开了。")
    
    def event_weather_anomaly(self):
        """天气异常事件"""
        self.add_game_log("你注意到今天的天气有些异常，空气中弥漫着奇怪的能量。")
        self.radiation_level += 5
    
    def event_radio_signal(self):
        """无线电信号事件"""
        self.add_game_log("你的收音机突然接收到一段微弱的信号，但很快就消失了...")
    
    def get_weather_name(self):
        """获取天气名称"""
        names = {
            "sunny": "晴朗",
            "rainy": "雨天", 
            "cloudy": "多云",
            "foggy": "雾天",
            "stormy": "暴风雨"
        }
        return names.get(self.weather, self.weather)
    
    def get_season_name(self):
        """获取季节名称"""
        names = {
            "spring": "春季",
            "summer": "夏季",
            "autumn": "秋季", 
            "winter": "冬季"
        }
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
            elif action_type == "farm":
                self.action_farm(kwargs.get.get('crop_type'))
            elif action_type == "craft":
                self.action_craft(kwargs.get('recipe_id'))
            elif action_type == "talk":
                self.action_talk(kwargs.get('npc_id'))
            elif action_type == "sleep":
                self.action_sleep(kwargs.get('hours', 8))
            elif action_type == "eat":
                self.action_eat(kwargs.get('food_type'))
            elif action_type == "drink":
                self.action_drink(kwargs.get('drink_type'))
            elif action_type == "move":
                self.action_move(kwargs.get('location_id'))
            elif action_type == "use_item":
                self.action_use_item(kwargs.get('item_id'))
            else:
                self.add_game_log(f"未知动作: {action_type}")
                
        except Exception as e:
            logging.error(f"执行动作时出错: {e}")
            self.add_game_log(f"执行动作时出错: {e}")
    
    def action_explore(self):
        """探索动作"""
        if self.player.stamina < 10:
            self.add_game_log("体力不足，无法探索。")
            return
            
        # 消耗体力
        self.player.modify_stamina(-10)
        self.advance_time(2)
        
        current_location = self.world.get_current_location()
        self.add_game_log(f"你在{current_location.name}探索...")
        
        # 生成探索事件
        event_result = self.world.generate_exploration_event()
        self.handle_exploration_event(event_result)
        
        # 成就检查
        self.achievements.check_exploration_achievements()
    
    def action_rest(self):
        """休息动作"""
        if self.player.stamina >= self.player.max_stamina and self.player.health >= self.player.max_health:
            self.add_game_log("你不需要休息。")
            return
            
        self.add_game_log("你休息了一会儿...")
        self.advance_time(2)
        
        # 恢复体力和生命值
        stamina_recovery = min(30, self.player.max_stamina - self.player.stamina)
        health_recovery = min(15, self.player.max_health - self.player.health)
        
        self.player.modify_stamina(stamina_recovery)
        self.player.modify_health(health_recovery)
        
        self.add_game_log(f"休息后，你恢复了{stamina_recovery}点体力和{health_recovery}点生命值。")
    
    def action_sleep(self, hours=8):
        """睡觉动作"""
        if hours < 2:
            self.add_game_log("睡眠时间太短，无法有效休息。")
            return
            
        self.add_game_log(f"你睡了{hours}小时...")
        self.advance_time(hours)
        
        # 睡眠恢复
        stamina_recovery = min(50, self.player.max_stamina - self.player.stamina)
        health_recovery = min(25, self.player.max_health - self.player.health)
        mental_recovery = min(40, self.player.max_mental - self.player.mental)
        
        self.player.modify_stamina(stamina_recovery)
        self.player.modify_health(health_recovery)
        self.player.modify_mental(mental_recovery)
        
        self.add_game_log(f"睡眠后，你恢复了{stamina_recovery}体力、{health_recovery}生命值和{mental_recovery}精神值。")
    
    def action_eat(self, food_type):
        """进食动作"""
        if not self.player.has_item(food_type):
            self.add_game_log(f"你没有{self.items.get_item_name(food_type)}。")
            return
            
        food_data = self.items.get_item_data(food_type)
        if not food_data or food_data.get('type') != 'food':
            self.add_game_log("这不是可食用的物品。")
            return
            
        # 消耗食物
        self.player.remove_item(food_type, 1)
        
        # 应用效果
        health_restore = food_data.get('health_restore', 0)
        stamina_restore = food_data.get('stamina_restore', 0)
        mental_restore = food_data.get('mental_restore', 0)
        
        self.player.modify_health(health_restore)
        self.player.modify_stamina(stamina_restore)
        self.player.modify_mental(mental_restore)
        
        self.advance_time(0.5)
        self.add_game_log(f"你吃了{self.items.get_item_name(food_type)}，恢复了{health_restore}生命值、{stamina_restore}体力和{mental_restore}精神值。")
    
    def action_drink(self, drink_type):
        """喝水动作"""
        if not self.player.has_item(drink_type):
            self.add_game_log(f"你没有{self.items.get_item_name(drink_type)}。")
            return
            
        drink_data = self.items.get_item_data(drink_type)
        if not drink_data or drink_data.get('type') != 'drink':
            self.add_game_log("这不是可饮用的物品。")
            return
            
        # 消耗饮品
        self.player.remove_item(drink_type, 1)
        
        # 应用效果
        health_restore = drink_data.get('health_restore', 0)
        stamina_restore = drink_data.get('stamina_restore', 0)
        mental_restore = drink_data.get('mental_restore', 0)
        
        self.player.modify_health(health_restore)
        self.player.modify_stamina(stamina_restore)
        self.player.modify_mental(mental_restore)
        
        self.advance_time(0.5)
        self.add_game_log(f"你喝了{self.items.get_item_name(drink_type)}，恢复了{health_restore}生命值、{stamina_restore}体力和{mental_restore}精神值。")
    
    def action_farm(self, crop_type):
        """农业动作"""
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
    
    def action_craft(self, recipe_id):
        """制作动作"""
        recipe = self.items.get_recipe(recipe_id)
        if not recipe:
            self.add_game_log("未知的制作配方。")
            return
            
        craft_result = self.player.craft_item(recipe)
        if craft_result['success']:
            self.add_game_log(craft_result['message'])
            self.advance_time(1)
            self.player.modify_stamina(-5)
        else:
            self.add_game_log(craft_result['message'])
    
    def action_talk(self, npc_id):
        """对话动作"""
        npc = self.npcs.get_npc(npc_id)
        if not npc:
            self.add_game_log("找不到这个NPC。")
            return
            
        dialogue = npc.get_dialogue()
        self.ui.show_dialogue_window(npc, dialogue)
    
    def action_move(self, location_id):
        """移动动作"""
        move_result = self.world.move_to_location(location_id)
        if move_result['success']:
            self.add_game_log(move_result['message'])
            self.advance_time(0.5)
            self.player.modify_stamina(-5)
        else:
            self.add_game_log(move_result['message'])
    
    def action_use_item(self, item_id):
        """使用物品动作"""
        if not self.player.has_item(item_id):
            self.add_game_log(f"你没有{self.items.get_item_name(item_id)}。")
            return
            
        use_result = self.player.use_item(item_id)
        if use_result['success']:
            self.add_game_log(use_result['message'])
            self.advance_time(0.5)
        else:
            self.add_game_log(use_result['message'])
    
    def handle_exploration_event(self, event_result):
        """处理探索事件"""
        event_type = event_result['type']
        
        if event_type == "resource":
            resource_type = event_result['resource_type']
            amount = event_result['amount']
            self.player.add_item(resource_type, amount)
            item_name = self.items.get_item_name(resource_type)
            self.add_game_log(f"你找到了{amount}个{item_name}！")
            
        elif event_type == "enemy":
            enemy_data = event_result['enemy_data']
            combat_result = self.combat.start_combat(self.player, enemy_data)
            self.handle_combat_result(combat_result)
            
        elif event_type == "discovery":
            new_location = event_result['location']
            self.world.discover_location(new_location)
            self.add_game_log(f"你发现了一个新地点：{new_location.name}！")
            
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
        """处理战斗结果"""
        if combat_result['player_won']:
            self.add_game_log(f"你击败了{combat_result['enemy_name']}！")
            
            # 获得战利品
            if combat_result.get('loot'):
                for item, amount in combat_result['loot'].items():
                    self.player.add_item(item, amount)
                    item_name = self.items.get_item_name(item)
                    self.add_game_log(f"获得了{amount}个{item_name}！")
            
            # 成就检查
            self.achievements.check_combat_achievements(combat_result['enemy_name'])
        else:
            self.add_game_log("战斗失败！你受了重伤。")
            self.player.modify_health(-20)
            self.player.modify_mental(-15)
    
    def start_autosave(self):
        """启动自动保存"""
        self.autosave_thread = threading.Thread(target=self.autosave_loop, daemon=True)
        self.autosave_thread.start()
    
    def autosave_loop(self):
        """自动保存循环"""
        while self.autosave_running:
            time.sleep(300)  # 每5分钟自动保存一次
            if self.game_state == "playing" and self.player.initialized:
                self.save_game()
    
    def start_game_loop(self):
        """启动游戏循环"""
        def game_loop():
            while self.game_loop_running:
                if self.game_state == "playing" and self.player.initialized:
                    # 更新UI
                    self.ui.update_status_display()
                    
                    # 检查玩家状态
                    self.check_player_status()
                
                time.sleep(1)  # 1秒更新一次
        
        loop_thread = threading.Thread(target=game_loop, daemon=True)
        loop_thread.start()
    
    def check_player_status(self):
        """检查玩家状态"""
        # 检查死亡
        if self.player.health <= 0:
            self.game_over("生命值耗尽")
        
        # 检查精神崩溃
        if self.player.mental <= 0:
            self.game_over("精神崩溃")
        
        # 检查辐射中毒
        if self.radiation_level >= 100:
            self.game_over("辐射中毒")
    
    def game_over(self, reason):
        """游戏结束"""
        self.add_game_log(f"游戏结束！原因：{reason}")
        self.add_game_log(f"你生存了{self.day_count}天。")
        
        # 成就检查
        self.achievements.unlock("survival_days", self.day_count)
        
        # 显示游戏结束画面
        self.ui.show_game_over(reason, self.day_count)
        
        # 删除存档
        if self.current_save_slot:
            self.save_system.delete_save(self.current_save_slot)
        
        self.game_state = "menu"
    
    def pause_game(self):
        """暂停游戏"""
        if self.game_state == "playing":
            self.game_state = "paused"
            self.ui.show_pause_menu()
    
    def resume_game(self):
        """继续游戏"""
        if self.game_state == "paused":
            self.game_state = "playing"
            self.ui.hide_pause_menu()
    
    def change_game_speed(self, speed):
        """改变游戏速度"""
        self.game_speed = speed
        self.add_game_log(f"游戏速度调整为{speed}倍。")
    
    def on_closing(self):
        """关闭游戏"""
        logging.info("游戏关闭中...")
        self.autosave_running = False
        self.game_loop_running = False
        
        if self.game_state == "playing" and self.player.initialized:
            self.save_game()
        
        self.root.destroy()
        logging.info("游戏已关闭")