# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import logging
from typing import Dict, List, Optional

class GameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.current_frame = None
        self.log_messages = []
        
        # 设置窗口
        self.setup_window()
        
    def setup_window(self):
        """设置窗口属性"""
        self.root.title("末日生存者")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # 设置样式
        self.setup_styles()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.game.on_closing)
    
    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        
        # 配置不同样式
        style.configure("Title.TLabel", 
                       font=("Arial", 16, "bold"),
                       foreground="#2C3E50")
        
        style.configure("Subtitle.TLabel",
                       font=("Arial", 12, "bold"),
                       foreground="#34495E")
        
        style.configure("Normal.TLabel",
                       font=("Arial", 10),
                       foreground="#2C3E50")
        
        style.configure("Status.TLabel",
                       font=("Arial", 9),
                       foreground="#7F8C8D")
        
        style.configure("Action.TButton",
                       font=("Arial", 10, "bold"),
                       padding=(10, 5))
        
        style.configure("Danger.TButton",
                       font=("Arial", 10, "bold"),
                       foreground="white",
                       background="#E74C3C")
    
    def clear_interface(self):
        """清除当前界面"""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_main_menu(self):
        """创建主菜单界面"""
        self.clear_interface()
        
        # 标题
        title_label = ttk.Label(self.current_frame, 
                               text="末日生存者", 
                               style="Title.TLabel")
        title_label.pack(pady=30)
        
        # 版本信息
        version_label = ttk.Label(self.current_frame,
                                 text="版本 1.0.0",
                                 style="Status.TLabel")
        version_label.pack(pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(self.current_frame)
        button_frame.pack(pady=30)
        
        # 开始游戏按钮
        start_button = ttk.Button(button_frame,
                                 text="开始游戏",
                                 command=self.show_save_slots,
                                 style="Action.TButton",
                                 width=20)
        start_button.pack(pady=10)
        
        # 游戏背景按钮
        background_button = ttk.Button(button_frame,
                                      text="游戏背景",
                                      command=self.show_game_background,
                                      style="Action.TButton",
                                      width=20)
        background_button.pack(pady=10)
        
        # 图鉴按钮
        codex_button = ttk.Button(button_frame,
                                 text="图鉴",
                                 command=self.show_codex,
                                 style="Action.TButton",
                                 width=20)
        codex_button.pack(pady=10)
        
        # 故事书按钮
        story_button = ttk.Button(button_frame,
                                 text="故事书",
                                 command=self.show_story_book,
                                 style="Action.TButton",
                                 width=20)
        story_button.pack(pady=10)
        
        # 游戏玩法按钮
        gameplay_button = ttk.Button(button_frame,
                                    text="游戏玩法",
                                    command=self.show_gameplay_help,
                                    style="Action.TButton",
                                    width=20)
        gameplay_button.pack(pady=10)
        
        # 退出游戏按钮
        exit_button = ttk.Button(button_frame,
                                text="退出游戏",
                                command=self.game.on_closing,
                                style="Danger.TButton",
                                width=20)
        exit_button.pack(pady=20)
    
    def show_save_slots(self):
        """显示存档槽选择界面"""
        self.clear_interface()
        
        # 返回按钮
        back_button = ttk.Button(self.current_frame,
                                text="返回主菜单",
                                command=self.create_main_menu)
        back_button.pack(anchor="nw", pady=5)
        
        # 标题
        title_label = ttk.Label(self.current_frame,
                               text="选择存档槽",
                               style="Title.TLabel")
        title_label.pack(pady=20)
        
        # 存档槽框架
        slots_frame = ttk.Frame(self.current_frame)
        slots_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        for i in range(1, 6):
            slot_frame = ttk.Frame(slots_frame, relief="solid", padding=10)
            slot_frame.pack(fill="x", pady=5)
            
            save_file = f"saves/save_slot_{i}.json"
            
            try:
                import os
                import json
                if os.path.exists(save_file):
                    with open(save_file, 'r', encoding='utf-8') as f:
                        save_data = json.load(f)
                    
                    player_name = save_data.get('player', {}).get('name', '未知')
                    day_count = save_data.get('day_count', 1)
                    save_time = save_data.get('save_time', '未知时间')
                    
                    slot_text = f"存档 {i}: {player_name} - 第{day_count}天 - {save_time}"
                    
                    # 存档信息
                    info_label = ttk.Label(slot_frame,
                                          text=slot_text,
                                          style="Normal.TLabel")
                    info_label.pack(side="left", padx=10)
                    
                    # 加载按钮
                    load_button = ttk.Button(slot_frame,
                                            text="加载",
                                            command=lambda slot=i: self.game.load_game(slot))
                    load_button.pack(side="right", padx=5)
                    
                    # 删除按钮
                    delete_button = ttk.Button(slot_frame,
                                              text="删除",
                                              command=lambda slot=i: self.delete_save_confirm(slot))
                    delete_button.pack(side="right", padx=5)
                    
                else:
                    # 空存档槽
                    info_label = ttk.Label(slot_frame,
                                          text=f"存档 {i}: 空",
                                          style="Normal.TLabel")
                    info_label.pack(side="left", padx=10)
                    
                    # 新游戏按钮
                    new_game_button = ttk.Button(slot_frame,
                                                text="新游戏",
                                                command=lambda slot=i: self.show_character_selection(slot))
                    new_game_button.pack(side="right", padx=5)
                    
            except Exception as e:
                logging.error(f"读取存档信息失败: {e}")
                error_label = ttk.Label(slot_frame,
                                       text=f"存档 {i}: 损坏",
                                       style="Normal.TLabel")
                error_label.pack(side="left", padx=10)
    
    def delete_save_confirm(self, save_slot):
        """确认删除存档"""
        result = messagebox.askyesno("确认删除", f"确定要删除存档 {save_slot} 吗？")
        if result:
            import os
            save_file = f"saves/save_slot_{save_slot}.json"
            if os.path.exists(save_file):
                os.remove(save_file)
            self.show_save_slots()
    
    def show_character_selection(self, save_slot):
        """显示角色选择界面"""
        self.clear_interface()
        
        # 返回按钮
        back_button = ttk.Button(self.current_frame,
                                text="返回存档选择",
                                command=self.show_save_slots)
        back_button.pack(anchor="nw", pady=5)
        
        # 标题
        title_label = ttk.Label(self.current_frame,
                               text="选择你的角色",
                               style="Title.TLabel")
        title_label.pack(pady=20)
        
        # 角色信息
        characters = [
            {
                "name": "生存专家",
                "class": "survival_expert",
                "description": "精通生存技巧，擅长寻找资源和建造庇护所",
                "health": 100,
                "max_health": 100,
                "stamina": 80,
                "max_stamina": 80,
                "strength": 7,
                "agility": 6,
                "intelligence": 8,
                "luck": 5
            },
            {
                "name": "战斗精英",
                "class": "combat_elite", 
                "description": "前特种部队成员，精通各种战斗技巧",
                "health": 120,
                "max_health": 120,
                "stamina": 70,
                "max_stamina": 70,
                "strength": 9,
                "agility": 8,
                "intelligence": 6,
                "luck": 4
            },
            {
                "name": "敏捷猎手",
                "class": "agile_hunter",
                "description": "擅长潜行和追踪，能够轻易避开危险",
                "health": 90,
                "max_health": 90,
                "stamina": 100,
                "max_stamina": 100,
                "strength": 6,
                "agility": 9,
                "intelligence": 7,
                "luck": 6
            },
            {
                "name": "幸运探索者",
                "class": "lucky_explorer",
                "description": "天生幸运，总能找到稀有物品和避开危险",
                "health": 80,
                "max_health": 80,
                "stamina": 80,
                "max_stamina": 80,
                "strength": 5,
                "agility": 7,
                "intelligence": 6,
                "luck": 10
            }
        ]
        
        # 创建角色选择卡片
        for char in characters:
            char_frame = ttk.Frame(self.current_frame, relief="solid", padding=15)
            char_frame.pack(fill="x", padx=50, pady=10)
            
            # 角色名称和描述
            name_label = ttk.Label(char_frame,
                                  text=char["name"],
                                  style="Subtitle.TLabel")
            name_label.pack(anchor="w")
            
            desc_label = ttk.Label(char_frame,
                                  text=char["description"],
                                  style="Normal.TLabel")
            desc_label.pack(anchor="w", pady=5)
            
            # 角色属性
            stats_text = (f"生命: {char['health']}/{char['max_health']} | "
                         f"体力: {char['stamina']}/{char['max_stamina']} | "
                         f"力量: {char['strength']} | 敏捷: {char['agility']} | "
                         f"智力: {char['intelligence']} | 幸运: {char['luck']}")
            
            stats_label = ttk.Label(char_frame,
                                   text=stats_text,
                                   style="Status.TLabel")
            stats_label.pack(anchor="w")
            
            # 选择按钮
            select_button = ttk.Button(char_frame,
                                      text="选择角色",
                                      command=lambda c=char, s=save_slot: self.start_with_character(c, s),
                                      style="Action.TButton")
            select_button.pack(anchor="e", pady=5)
    
    def start_with_character(self, character_data, save_slot):
        """使用选定角色开始游戏"""
        self.game.start_new_game(save_slot, character_data)
    
    def create_game_interface(self):
        """创建游戏主界面"""
        self.clear_interface()
        
        # 顶部状态栏
        self.create_status_bar()
        
        # 主内容区域
        main_frame = ttk.Frame(self.current_frame)
        main_frame.pack(fill="both", expand=True, pady=10)
        
        # 左侧游戏日志
        self.create_game_log(main_frame)
        
        # 右侧控制面板
        self.create_control_panel(main_frame)
        
        # 底部操作栏
        self.create_action_bar()
    
    def create_status_bar(self):
        """创建状态栏"""
        status_frame = ttk.Frame(self.current_frame, relief="solid", padding=5)
        status_frame.pack(fill="x", pady=5)
        
        # 玩家状态信息
        self.status_label = ttk.Label(status_frame,
                                     text="初始化中...",
                                     style="Normal.TLabel")
        self.status_label.pack(side="left")
        
        # 暂停按钮
        pause_button = ttk.Button(status_frame,
                                 text="暂停",
                                 command=self.game.pause_game)
        pause_button.pack(side="right", padx=5)
        
        # 保存按钮
        save_button = ttk.Button(status_frame,
                                text="保存",
                                command=self.game.save_game)
        save_button.pack(side="right", padx=5)
    
    def create_game_log(self, parent):
        """创建游戏日志区域"""
        log_frame = ttk.Frame(parent)
        log_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # 日志标题
        log_label = ttk.Label(log_frame,
                             text="游戏日志",
                             style="Subtitle.TLabel")
        log_label.pack(anchor="w", pady=5)
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                 wrap=tk.WORD,
                                                 width=60,
                                                 height=25,
                                                 font=("Arial", 9))
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state="disabled")
    
    def create_control_panel(self, parent):
        """创建控制面板"""
        control_frame = ttk.Frame(parent, width=300)
        control_frame.pack(side="right", fill="y")
        control_frame.pack_propagate(False)
        
        # 位置信息
        self.create_location_info(control_frame)
        
        # 快捷操作
        self.create_quick_actions(control_frame)
        
        # 任务信息
        self.create_quest_info(control_frame)
    
    def create_location_info(self, parent):
        """创建位置信息面板"""
        loc_frame = ttk.LabelFrame(parent, text="当前位置", padding=10)
        loc_frame.pack(fill="x", pady=10)
        
        self.location_label = ttk.Label(loc_frame,
                                       text="加载中...",
                                       style="Normal.TLabel")
        self.location_label.pack(anchor="w")
        
        self.terrain_label = ttk.Label(loc_frame,
                                      text="",
                                      style="Status.TLabel")
        self.terrain_label.pack(anchor="w")
        
        self.danger_label = ttk.Label(loc_frame,
                                     text="",
                                      style="Status.TLabel")
        self.danger_label.pack(anchor="w")
    
    def create_quick_actions(self, parent):
        """创建快捷操作面板"""
        action_frame = ttk.LabelFrame(parent, text="快捷操作", padding=10)
        action_frame.pack(fill="x", pady=10)
        
        actions = [
            ("探索", lambda: self.game.perform_action("explore")),
            ("休息", lambda: self.game.perform_action("rest")),
            ("睡觉", lambda: self.show_sleep_dialog()),
            ("进食", lambda: self.show_eat_dialog()),
            ("喝水", lambda: self.show_drink_dialog()),
            ("查看背包", self.show_inventory),
            ("查看地图", self.show_map),
            ("制作物品", self.show_crafting),
            ("农业", self.show_farming),
            ("任务", self.show_quests)
        ]
        
        for action_text, action_command in actions:
            action_button = ttk.Button(action_frame,
                                      text=action_text,
                                      command=action_command,
                                      style="Action.TButton",
                                      width=15)
            action_button.pack(fill="x", pady=2)
    
    def create_quest_info(self, parent):
        """创建任务信息面板"""
        quest_frame = ttk.LabelFrame(parent, text="当前任务", padding=10)
        quest_frame.pack(fill="both", expand=True, pady=10)
        
        self.quest_text = scrolledtext.ScrolledText(quest_frame,
                                                   wrap=tk.WORD,
                                                   height=8,
                                                   font=("Arial", 8))
        self.quest_text.pack(fill="both", expand=True)
        self.quest_text.config(state="disabled")
    
    def create_action_bar(self):
        """创建底部操作栏"""
        action_frame = ttk.Frame(self.current_frame)
        action_frame.pack(fill="x", pady=10)
        
        # 这里可以添加更多专业操作按钮
        professional_actions = [
            ("医疗", self.show_medical),
            ("建造", self.show_construction),
            ("研究", self.show_research),
            ("社交", self.show_social)
        ]
        
        for action_text, action_command in professional_actions:
            button = ttk.Button(action_frame,
                               text=action_text,
                               command=action_command)
            button.pack(side="left", padx=5)
    
    def update_status_display(self):
        """更新状态显示"""
        if not self.game.player.initialized:
            return
        
        player = self.game.player
        status_text = (f"{player.name} | "
                      f"生命: {player.health}/{player.max_health} | "
                      f"体力: {player.stamina}/{player.max_stamina} | "
                      f"精神: {player.mental}/{player.max_mental} | "
                      f"第{self.game.day_count}天 {self.game.format_time()} | "
                      f"{self.game.get_weather_name()} | {self.game.get_season_name()}")
        
        self.status_label.config(text=status_text)
        
        # 更新位置信息
        location = self.game.world.get_current_location()
        if location:
            danger_desc = self.game.world.get_location_danger_description(location.safety_level)
            self.location_label.config(text=location.name)
            self.terrain_label.config(text=f"地形: {location.terrain}")
            self.danger_label.config(text=f"危险程度: {danger_desc}")
        
        # 更新任务信息
        self.update_quest_display()
    
    def update_quest_display(self):
        """更新任务显示"""
        active_quests = self.game.quests.active_quests
        if not active_quests:
            quest_text = "没有进行中的任务"
        else:
            quest_text = ""
            for quest_id in active_quests[:3]:  # 只显示前3个任务
                progress = self.game.quests.get_quest_progress(quest_id)
                if progress:
                    quest_text += f"● {progress['quest']['name']}\n"
                    for obj in progress['objectives']:
                        status = "✓" if obj['completed'] else "○"
                        quest_text += f"  {status} {obj['description']} ({obj['current']}/{obj['required']})\n"
                    quest_text += "\n"
        
        self.quest_text.config(state="normal")
        self.quest_text.delete(1.0, tk.END)
        self.quest_text.insert(1.0, quest_text)
        self.quest_text.config(state="disabled")
    
    def add_log_message(self, message):
        """添加日志消息"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        
        # 限制日志长度
        lines = self.log_text.get(1.0, tk.END).split('\n')
        if len(lines) > 100:
            self.log_text.delete(1.0, f"{len(lines)-100}.0")
    
    def show_sleep_dialog(self):
        """显示睡觉对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("睡觉")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="选择睡眠时间:").pack(pady=10)
        
        hours_var = tk.IntVar(value=8)
        
        hours_frame = ttk.Frame(dialog)
        hours_frame.pack(pady=10)
        
        for hours in [2, 4, 6, 8, 10]:
            ttk.Radiobutton(hours_frame, 
                           text=f"{hours}小时", 
                           variable=hours_var, 
                           value=hours).pack(side="left", padx=5)
        
        def confirm_sleep():
            self.game.perform_action("sleep", hours=hours_var.get())
            dialog.destroy()
        
        ttk.Button(dialog, text="睡觉", command=confirm_sleep).pack(pady=10)
        ttk.Button(dialog, text="取消", command=dialog.destroy).pack(pady=5)
    
    def show_eat_dialog(self):
        """显示进食对话框"""
        # 实现食物选择逻辑
        dialog = tk.Toplevel(self.root)
        dialog.title("进食")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()
    
        ttk.Label(dialog, text="选择要食用的食物:", style="Subtitle.TLabel").pack(pady=10)
    
        # 获取可食用的物品
        food_items = []
        for item_id, quantity in self.game.player.inventory.items():
           item_data = self.game.items.get_item_data(item_id)
           if item_data and item_data.get('type') == 'food' and quantity > 0:
               food_items.append((item_id, item_data, quantity))
    
        if not food_items:
          ttk.Label(dialog, text="没有可食用的食物", style="Normal.TLabel").pack(pady=20)
          ttk.Button(dialog, text="关闭", command=dialog.destroy).pack(pady=10)
          return
    
        # 创建食物列表
        container = ttk.Frame(dialog)
        container.pack(fill="both", expand=True, padx=10, pady=10)
    
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
    
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        for item_id, item_data, quantity in food_items:
            item_frame = ttk.Frame(scrollable_frame, relief="solid", padding=8)
            item_frame.pack(fill="x", pady=2, padx=5)
        
            # 物品信息
            info_text = f"{item_data['name']} x{quantity}\n{item_data['description']}"
            if item_data.get('health_restore', 0) > 0:
              info_text += f"\n恢复生命: {item_data['health_restore']}"
            if item_data.get('stamina_restore', 0) > 0:
              info_text += f" | 恢复体力: {item_data['stamina_restore']}"
        
            ttk.Label(item_frame, text=info_text, style="Normal.TLabel").pack(side="left", anchor="w")
        
            # 食用按钮
            ttk.Button(item_frame, text="食用", 
            command=lambda iid=item_id: self.eat_food(iid, dialog)).pack(side="right", padx=5)
    
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            ttk.Button(dialog, text="取消", command=dialog.destroy).pack(pady=10)

    def eat_food(self, item_id, dialog):
        """食用食物"""
        result = self.game.perform_action("eat", food_type=item_id)
        if result:
          self.add_log_message(result.get('message', '食用了食物'))
          dialog.destroy()

    def show_drink_dialog(self):
        """显示喝水对话框"""
        # 实现饮水选择逻辑
        dialog = tk.Toplevel(self.root)
        dialog.title("喝水")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
    
        # 标题
        title_frame = ttk.Frame(dialog)
        title_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(title_frame, text="选择要饮用的饮品", style="Subtitle.TLabel").pack()
    
        # 获取可饮用的物品
        drink_items = []
        for item_id, quantity in self.game.player.inventory.items():
            item_data = self.game.items.get_item_data(item_id)
            if item_data and item_data.get('type') == 'drink' and quantity > 0:
               drink_items.append((item_id, item_data, quantity))
    
        if not drink_items:
            # 没有饮品的情况
            no_drink_frame = ttk.Frame(dialog)
            no_drink_frame.pack(fill="both", expand=True, padx=20, pady=50)
            ttk.Label(no_drink_frame, text="没有可饮用的饮品", style="Normal.TLabel").pack(pady=10)
            ttk.Label(no_drink_frame, text="去探索或交易获取饮品", style="Status.TLabel").pack()
            ttk.Button(dialog, text="关闭", command=dialog.destroy, width=15).pack(pady=20)
            return
    
        # 饮品列表容器
        container = ttk.Frame(dialog)
        container.pack(fill="both", expand=True, padx=10, pady=10)
    
        # 创建滚动框架
        canvas = tk.Canvas(container, bg="white")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
    
        scrollable_frame.bind(
             "<Configure>",
             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
    
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        # 显示饮品列表
        for item_id, item_data, quantity in drink_items:
            item_frame = ttk.Frame(scrollable_frame, relief="solid", padding=12)
            item_frame.pack(fill="x", pady=3, padx=5)
        
            # 左侧信息区域
            info_frame = ttk.Frame(item_frame)
            info_frame.pack(side="left", fill="x", expand=True)
        
            # 饮品名称和数量
            name_label = ttk.Label(info_frame,
                                                   text=f"{item_data['name']} x{quantity}",
                                                   style="Subtitle.TLabel")
            name_label.pack(anchor="w")
        
            # 饮品描述
            desc_label = ttk.Label(info_frame, 
            text=item_data['description'], 
            style="Normal.TLabel")
            desc_label.pack(anchor="w", pady=2)
        
            # 饮品效果
            effects = []
            if item_data.get('health_restore', 0) > 0:
            	effects.append(f"💗 生命+{item_data['health_restore']}")
            if item_data.get('stamina_restore', 0) > 0:
                effects.append(f"⚡ 体力+{item_data['stamina_restore']}")
            if item_data.get('mental_restore', 0) > 0:
                effects.append(f"🧠 精神+{item_data['mental_restore']}")
            if item_data.get('caffeine', 0) > 0:
                effects.append(f"☕ 咖啡因+{item_data['caffeine']}")
        
            if effects:
                effects_label = ttk.Label(info_frame,
                                                         text=" | ".join(effects),
                                                         style="Status.TLabel")
                effects_label.pack(anchor="w")
        
            # 成瘾警告
            if item_data.get('addictive', False):
                 warning_label = ttk.Label(info_frame, 
                                                            text="⚠ 注意：长期使用可能成瘾",
                                                            style="Status.TLabel",
                                                            foreground="orange")
                 warning_label.pack(anchor="w")

            # 右侧按钮区域
            button_frame = ttk.Frame(item_frame)
            button_frame.pack(side="right")
        
            # 饮用按钮
            drink_button = ttk.Button(button_frame, 
                                                       text="饮用",
                                                       command=lambda iid=item_id: self.drink_item(iid, dialog),
                                                       style="Action.TButton")
            drink_button.pack(pady=5)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # 底部按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
    
        ttk.Button(button_frame, text="关闭", 
              command=dialog.destroy, 
              width=15).pack()

    def drink_item(self, item_id, dialog):
    	"""饮用饮品"""
    	result = self.game.perform_action("drink", drink_type=item_id)
    	if result:
            if result.get('success'):
            	self.add_log_message(result['message'])
            	# 关闭对话框
            	dialog.destroy()
            	# 刷新状态显示
            	self.update_status_display()
            else:
            	messagebox.showwarning("饮用失败", result['message'])
    
    def show_inventory(self):
        """显示背包"""
        window = tk.Toplevel(self.root)
        window.title("背包")
        window.geometry("900x600")
    
        # 创建标签页
        notebook = ttk.Notebook(window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
        # 物品标签页
        items_frame = ttk.Frame(notebook)
        notebook.add(items_frame, text="物品")
    
        # 装备标签页
        equipment_frame = ttk.Frame(notebook)
        notebook.add(equipment_frame, text="装备")
    
        self.create_inventory_tab(items_frame)
        self.create_equipment_tab_redesign(equipment_frame)  # 重新设计的装备页
    
    def create_inventory_tab(self, parent):
        """创建物品标签页"""
        # 分类筛选
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill="x", pady=5)
    
        categories = ["全部", "食物", "饮品", "材料", "医疗", "种子", "特殊"]
        category_var = tk.StringVar(value="全部")
    
        for category in categories:
                       ttk.Radiobutton(filter_frame, 
                       text=category,
                       variable=category_var,
                       value=category,
                       command=lambda: self.refresh_inventory()).pack(side="left", padx=5)
    
        # 物品列表
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)
    
        columns = ("名称", "数量", "类型", "描述")
        self.inventory_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    
        for col in columns:
        	self.inventory_tree.heading(col, text=col)
        	self.inventory_tree.column(col, width=100)
    
        self.inventory_tree.pack(fill="both", expand=True, side="left")
    
        # 滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.inventory_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
    
        # 操作按钮
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=5)
        
        ttk.Button(button_frame, text="使用", command=self.use_selected_item).pack(side="left", padx=5)
        ttk.Button(button_frame, text="丢弃", command=self.drop_selected_item).pack(side="left", padx=5)
        ttk.Button(button_frame, text="关闭", command=window.destroy).pack(side="right", padx=5)
    
        self.refresh_inventory()

    def create_equipment_tab_redesign(self, parent):
    	"""创建装备标签页 - 根据战斗系统重新设计"""
    	# 装备栏位布局
    	equipment_slots = {'头部': ['head', '头盔类装备'],'眼部': ['eyes', '战术目镜'],'胸甲': ['chest', '防护服'], '弹褂': ['vest', '战术背心'],'主武器': ['primary', '长枪'],'副武器': ['secondary', '手枪'],'近战武器': ['melee', '刀、斧等'],'手套': ['gloves', '影响攻速'],'裤子': ['legs', '护腿'],'鞋子': ['boots', '影响闪避']}
    	
    	# 创建两列布局
    	left_frame = ttk.Frame(parent)
    	left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    	
    	right_frame = ttk.Frame(parent)
    	right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    	
    	# 左侧：上半身装备
    	upper_frame = ttk.LabelFrame(left_frame, text="上半身装备", padding=10)
    	upper_frame.pack(fill="x", pady=5)
    	
    	upper_slots = ['头部', '眼部', '胸甲', '弹褂', '手套']
    	
    	for slot_name in upper_slots:
    		self.create_equipment_slot(upper_frame, slot_name, equipment_slots[slot_name])
    	
    	# 左侧：武器
    	weapons_frame = ttk.LabelFrame(left_frame, text="武器", padding=10)
    	weapons_frame.pack(fill="x", pady=5)
    	
    	weapon_slots = ['主武器', '副武器', '近战武器']
    	for slot_name in weapon_slots:
    		self.create_equipment_slot(weapons_frame, slot_name, equipment_slots[slot_name])
    	
    	# 右侧：下半身装备
    	lower_frame = ttk.LabelFrame(right_frame, text="下半身装备", padding=10)
    	lower_frame.pack(fill="x", pady=5)
    	lower_slots = ['裤子', '鞋子']
    	for slot_name in lower_slots:
    		self.create_equipment_slot(lower_frame, slot_name, equipment_slots[slot_name])
    	
    	# 右侧：属性显示
    	stats_frame = ttk.LabelFrame(right_frame, text="属性加成", padding=10)
    	stats_frame.pack(fill="both", expand=True, pady=5)
    	
    	self.create_equipment_stats(stats_frame)

    def create_equipment_slot(self, parent, slot_name, slot_info):
    	"""创建单个装备槽位"""
    	slot_frame = ttk.Frame(parent)
    	slot_frame.pack(fill="x", pady=3)
    	
    	# 槽位名称和说明
    	info_frame = ttk.Frame(slot_frame)
    	info_frame.pack(fill="x")
    	
    	ttk.Label(info_frame, text=slot_name, width=10, style="Subtitle.TLabel").pack(side="left")
    	ttk.Label(info_frame, text=slot_info[1], style="Status.TLabel").pack(side="left", padx=10)
    	
    	# 当前装备显示
    	item_frame = ttk.Frame(slot_frame)
    	item_frame.pack(fill="x", pady=2)
    	
    	slot_id = slot_info[0]
    	item_id = self.game.player.equipment.get(slot_id)
    	
    	if item_id:
    	   item_data = self.game.items.get_item_data(item_id)
    	   if item_data:
    	       # 显示装备信息
    	       item_text = f"{item_data['name']}"
    	       if 'durability' in item_data:
            	item_text += f" (耐久: {item_data['durability']})"
            	
            	ttk.Label(item_frame, text=item_text).pack(side="left")
            	
            	# 装备属性
            	effects_text = self.get_equipment_effects(item_data)
            	if effects_text:
            		ttk.Label(item_frame, text=effects_text, style="Status.TLabel").pack(side="left", padx=10)
            	
            	# 卸下按钮
            	ttk.Button(item_frame, text="卸下",command=lambda s=slot_id: self.unequip_item_ui(s)).pack(side="right")
    	   
    	   else:
            	ttk.Label(item_frame, text="未知装备").pack(side="left")
            	ttk.Button(item_frame, text="卸下",command=lambda s=slot_id: self.unequip_item_ui(s)).pack(side="right")
    	
    	else:
        	ttk.Label(item_frame, text="空").pack(side="left")
        	ttk.Button(item_frame, text="装备",
                  command=lambda s=slot_id: self.show_equipable_items(s)).pack(side="right")

    def get_equipment_effects(self, item_data):
    	"""获取装备效果描述"""
    	effects = []
    	
    	if 'effects' in item_data:
    	       for effect in item_data['effects']:
    	           if effect['type'] == 'stat_bonus':
    	           	effects.append(f"{effect['stat']}+{effect['value']}")
    	           elif effect['type'] == 'carry_capacity':
    	           	effects.append(f"容量+{effect['value']}")
    	           elif effect['type'] == 'damage_bonus':
    	           	effects.append(f"伤害+{effect['value']}")
    	           elif effect['type'] == 'defense_bonus':
    	           	effects.append(f"防御+{effect['value']}")
    	
    	return ", ".join(effects) if effects else ""

    def create_equipment_stats(self, parent):
    	"""创建装备属性显示"""
    	# 获取玩家战斗属性
    	combat_stats = self.game.player.get_combat_stats()
    	total_stats = self.game.player.get_total_stats()
    	
    	stats_text = f"""
	攻击力: {combat_stats['attack']}
	防御力: {combat_stats['defense']} 
	命中率: {combat_stats['accuracy']}%
	闪避率: {combat_stats['dodge']}%
	暴击率: {combat_stats['critical']}%
	
	力量: {total_stats['strength']}
	敏捷: {total_stats['agility']}
	耐力: {total_stats['endurance']}
	幸运: {total_stats['luck']}
	"""
    	
    	text_widget = tk.Text(parent, wrap=tk.WORD, height=12, font=("Arial", 9))
    	text_widget.pack(fill="both", expand=True)
    	text_widget.insert(1.0, stats_text)
    	text_widget.config(state="disabled")

    def show_equipable_items(self, slot):
    	"""显示可装备物品列表"""
    	# 获取可以装备到该槽位的物品
    	equipable_items = []
    	for item_id, quantity in self.game.player.inventory.items():
    	       if quantity > 0:
    	       	item_data = self.game.items.get_item_data(item_id)
    	       	if item_data and item_data.get('equip_slot') == slot:
    	       		equipable_items.append((item_id, item_data, quantity))
    	
    	if not equipable_items:
    	   messagebox.showinfo("提示", f"背包中没有可以装备到{slot}的物品")
    	   return
    	
    	# 创建选择窗口
    	window = tk.Toplevel(self.root)
    	window.title(f"装备选择 - {self.get_slot_display_name(slot)}")
    	window.geometry("600x400")
    	
    	ttk.Label(window, text=f"选择要装备到{self.get_slot_display_name(slot)}的物品:").pack(pady=10)
    	
    	# 创建物品列表
    	tree_frame = ttk.Frame(window)
    	tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
    	
    	columns = ("名称", "类型", "数量", "属性", "耐久")
    	tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
    	
    	for col in columns:
    		tree.heading(col, text=col)
    	
    	tree.column("名称", width=120)
    	tree.column("类型", width=80)
    	tree.column("数量", width=60)
    	tree.column("属性", width=150)
    	tree.column("耐久", width=80)
    	
    	# 添加物品到列表
    	for item_id, item_data, quantity in equipable_items:
    	   effects = self.get_equipment_effects(item_data)
    	   durability = item_data.get('durability', '无限')
    	   
    	   tree.insert("", "end", values=(item_data['name'],item_data.get('type', '未知'),quantity,effects,durability), tags=(item_id,))
    	   
    	tree.pack(fill="both", expand=True, side="left")
    	# 滚动条
    	scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    	scrollbar.pack(side="right", fill="y")
    	tree.configure(yscrollcommand=scrollbar.set)
    	
    	def equip_selected():
    	   """装备选中的物品"""
    	   selection = tree.selection()
    	   if not selection:
    	       messagebox.showinfo("提示", "请选择一个物品")
    	       return
    	   
    	   item_id = tree.item(selection[0])['tags'][0]
    	   success = self.game.player.equip_item(item_id, slot)
    	   
    	   if success:
    	       messagebox.showinfo("成功", "装备成功")
    	       window.destroy()
    	       # 刷新背包界面
    	   else:
    	   	messagebox.showerror("错误", "装备失败")
    	   	
    	# 按钮区域
    	button_frame = ttk.Frame(window)
    	button_frame.pack(fill="x", pady=10)
    	
    	ttk.Button(button_frame, text="装备", command=equip_selected).pack(side="left", padx=5)
    	ttk.Button(button_frame, text="取消", command=window.destroy).pack(side="right", padx=5)
    	
    	# 双击装备
    	tree.bind("<Double-1>", lambda e: equip_selected())

    def get_slot_display_name(self, slot_id):
    	"""获取装备槽位显示名称"""
    	slot_names = {'head': '头部','eyes': '眼部', 'chest': '胸甲','vest': '弹褂','primary': '主武器','secondary': '副武器','melee': '近战武器','gloves': '手套','legs': '裤子','boots': '鞋子'
    	}
    	
    	return slot_names.get(slot_id, slot_id)

    def unequip_item_ui(self, slot):
    	"""卸下装备"""
    	try:
    	   success = self.game.player.unequip_item(slot)
    	   if success:
    	       self.game.add_game_log(f"卸下了{self.get_slot_display_name(slot)}的装备")
    	       messagebox.showinfo("成功", "装备卸下成功")
    	   else:
    	   	messagebox.showinfo("提示", "卸下装备失败")
    	except Exception as e:
    	   logging.error(f"卸下装备时出错: {e}")
    	   messagebox.showerror("错误", f"卸下装备时出错: {e}")

    def show_map(self):
        """显示地图"""
        window = tk.Toplevel(self.root)
        window.title("世界地图")
        window.geometry("600x500")
    
        # 地图画布
        canvas_frame = ttk.Frame(window)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
        # 简单的地图显示
        text_widget = scrolledtext.ScrolledText(canvas_frame, wrap=tk.WORD, font=("Arial", 9))
        text_widget.pack(fill="both", expand=True)
    
        # 生成地图文本
        map_text = "=== 世界地图 ===\n\n"
        current_location = self.game.world.get_current_location()
    
        for location in self.game.world.locations.values():
            if location.discovered:
            	prefix = "★ " if location.id == current_location.id else "  "
            	danger_desc = self.game.world.get_location_danger_description(location.safety_level)
            	map_text += f"{prefix}{location.name} - {location.terrain} ({danger_desc})\n"
            	map_text += f"     {location.description}\n\n"
            else:
            	map_text += f"  ??? - 未探索区域\n\n"
            	
            	text_widget.insert(1.0, map_text)
            	text_widget.config(state="disabled")
            	
            	ttk.Button(window, text="关闭", command=window.destroy).pack(pady=10)
    
    def show_crafting(self):
        """显示制作界面"""
        window = tk.Toplevel(self.root)
        window.title("制作")
        window.geometry("700x500")
    
        notebook = ttk.Notebook(window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
        # 按分类创建标签页
        categories = {'tools': '工具','weapons': '武器', 'armor': '防具','medical': '医疗','food': '食物','construction': '建筑'}
        
        for category, name in categories.items():
        	frame = ttk.Frame(notebook)
        	notebook.add(frame, text=name)
        	self.create_crafting_category_tab(frame, category)

    def create_crafting_category_tab(self, parent, category):
    	"""创建制作分类标签页"""
    	# 获取该分类的所有配方
    	recipes = self.game.items.get_recipes_by_category(category)
    	
    	if not recipes:
    	   ttk.Label(parent, text="没有可制作的配方").pack(pady=20)
    	   return
    	# 配方列表
    	tree_frame = ttk.Frame(parent)
    	tree_frame.pack(fill="both", expand=True)
    	columns = ("名称", "材料", "产品", "难度")
    	tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
    	for col in columns:
    		tree.heading(col, text=col)
    	tree.column("名称", width=150)
    	tree.column("材料", width=200)
    	tree.column("产品", width=150)
    	tree.column("难度", width=80)
    	
    	for recipe in recipes:
        	# 格式化材料
        	materials = ", ".join([f"{self.game.items.get_item_name(mat)}x{amt}"
        	for mat, amt in recipe['materials'].items()])
        	
        	# 格式化产品
        	products = ", ".join([f"{self.game.items.get_item_name(prod)}x{amt}"
        	for prod, amt in recipe['products'].items()])
        	
        	tree.insert("", "end", values=(recipe['name'],materials,products,recipe['difficulty']))
        	tree.pack(fill="both", expand=True, side="left")
        	
        	# 滚动条
        	scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        	scrollbar.pack(side="right", fill="y")
        	tree.configure(yscrollcommand=scrollbar.set)
        	
        	# 制作按钮
        	def craft_selected():
        	   	selection = tree.selection()
        	   	if selection:
        	   		recipe_index = tree.index(selection[0])
        	   		recipe = recipes[recipe_index]
        	   		result = self.game.player.craft_item(recipe)
        	   		messagebox.showinfo("制作结果", result['message'])
        	
        	button_frame = ttk.Frame(parent)
        	button_frame.pack(fill="x", pady=5)
        	ttk.Button(button_frame, text="制作", command=craft_selected).pack(side="left", padx=5)
        	ttk.Button(button_frame, text="关闭", command=window.destroy).pack(side="right", padx=5)
    
    def show_farming(self):
        """显示农业界面"""
        window = tk.Toplevel(self.root)
        window.title("农业")
        window.geometry("600x500")
        
        # 检查当前位置是否可以种植
        current_loc = self.game.player.location
        if not self.game.farming.can_plant(current_loc):
        	ttk.Label(window, text="当前位置不能种植").pack(pady=20)
        	ttk.Button(window, text="关闭", command=window.destroy).pack(pady=10)
        	return
        
        # 获取农田状态
        status = self.game.farming.get_farmland_status(current_loc)
        
        notebook = ttk.Notebook(window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 种植标签页
        planting_frame = ttk.Frame(notebook)
        notebook.add(planting_frame, text="种植")
        
        # 管理标签页
        management_frame = ttk.Frame(notebook)
        notebook.add(management_frame, text="管理")
        
        self.create_planting_tab(planting_frame, status)
        self.create_management_tab(management_frame, status)

    def create_planting_tab(self, parent, status):
    	"""创建种植标签页"""
    	ttk.Label(parent, text=f"可用地块: {status['empty_plots']}/{status['total_plots']}").pack(pady=5)
    	
    	# 季节适宜的作物
    	seasonal_crops = self.game.farming.get_seasonal_crops()
    	
    	if not seasonal_crops:
    	   ttk.Label(parent, text="当前季节没有适宜的作物").pack(pady=20)
    	   return
    	   
    	# 作物列表
    	tree_frame = ttk.Frame(parent)
    	tree_frame.pack(fill="both", expand=True, pady=10)
    	
    	columns = ("名称", "类型", "生长时间", "产量", "描述")
    	tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
    	
    	for col in columns:
    		tree.heading(col, text=col)
    		
    	for crop in seasonal_crops:
    	   growth_days = crop['growth_stages'] * crop['growth_days_per_stage']
    	   yield_range = f"{crop['yield_amount'][0]}-{crop['yield_amount'][1]}"
    	   
    	   tree.insert("", "end", values=(crop['name'],crop['type'],f"{growth_days}天",yield_range,crop['description']))
    	   
    	tree.pack(fill="both", expand=True, side="left")
    	
    	scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    	scrollbar.pack(side="right", fill="y")
    	tree.configure(yscrollcommand=scrollbar.set)
    	
    	# 种植按钮
    	def plant_selected():
    	   selection = tree.selection()
    	   if selection:
    	       crop_index = tree.index(selection[0])
    	       crop = seasonal_crops[crop_index]
    	       result = self.game.farming.plant_crop(crop['id'], self.game.player.location)
    	       messagebox.showinfo("种植结果", result['message'])
    	       
    	ttk.Button(parent, text="种植选中作物", command=plant_selected).pack(pady=5)
    
    def show_quests(self):
        """显示任务界面"""
        window = tk.Toplevel(self.root)
        window.title("任务")
        window.geometry("700x500")
        
        notebook = ttk.Notebook(window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 进行中任务
        active_frame = ttk.Frame(notebook)
        notebook.add(active_frame, text="进行中")
        
        # 可用任务
        available_frame = ttk.Frame(notebook)
        notebook.add(available_frame, text="可接受")
        
        # 已完成任务
        completed_frame = ttk.Frame(notebook)
        notebook.add(completed_frame, text="已完成")
        
        self.create_active_quests_tab(active_frame)
        
        self.create_available_quests_tab(available_frame)
        self.create_completed_quests_tab(completed_frame)
        
        def create_active_quests_tab(self, parent):
        	"""创建进行中任务标签页"""
        	active_quests = self.game.quests.active_quests
        	
        	if not active_quests:
        		ttk.Label(parent, text="没有进行中的任务").pack(pady=20)
        		return
        		
        	text_widget = scrolledtext.ScrolledText(parent, wrap=tk.WORD, font=("Arial", 9))
        	text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        	
        	for quest_id in active_quests:
        		progress = self.game.quests.get_quest_progress(quest_id)
        		if progress:
        		  quest = progress['quest']
        		  text_widget.insert(tk.END, f"【{quest['name']}】\n")
        		  text_widget.insert(tk.END, f"描述: {quest['description']}\n")
        		  text_widget.insert(tk.END, "目标:\n")
        		  
        		  for obj in progress['objectives']:
        		      status = "✓" if obj['completed'] else "○"
        		      text_widget.insert(tk.END, f"  {status} {obj['description']} ({obj['current']}/{obj['required']})\n")
        		  text_widget.insert(tk.END, "\n" + "="*50 + "\n\n")
        	
        	text_widget.config(state="disabled")
    
    def show_medical(self):
        """显示医疗界面"""
        window = tk.Toplevel(self.root)
        window.title("医疗")
        window.geometry("500x400")
        
        # 显示玩家状态
        status_frame = ttk.LabelFrame(window, text="健康状况", padding=10)
        status_frame.pack(fill="x", padx=10, pady=10)
        
        player = self.game.player
        ttk.Label(status_frame, text=f"生命值: {player.health}/{player.max_health}").pack(anchor="w")
        ttk.Label(status_frame, text=f"精神状态: {player.mental}/{player.max_mental}").pack(anchor="w")
        
        # 显示可用的医疗物品
        medical_frame = ttk.LabelFrame(window, text="医疗物品", padding=10)
        medical_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        medical_items = []
        for item_id, quantity in player.inventory.items():
        	item_data = self.game.items.get_item_data(item_id)
        	if item_data and item_data.get('type') == 'medicine' and quantity > 0:
        		medical_items.append((item_id, item_data, quantity))
        		
        if medical_items:
        	   	for item_id, item_data, quantity in medical_items:
        	   		item_frame = ttk.Frame(medical_frame)
        	   		item_frame.pack(fill="x", pady=2)
        	   		
        	   		ttk.Label(item_frame, text=f"{item_data['name']} x{quantity}").pack(side="left")
        	   		ttk.Button(item_frame, text="使用",
        	   		command=lambda iid=item_id: self.use_medical_item(iid, window)).pack(side="right")
        
        else:
        	ttk.Label(medical_frame, text="没有医疗物品").pack(pady=20)
        ttk.Button(window, text="关闭", command=window.destroy).pack(pady=10)

    def use_medical_item(self, item_id, window):
    	"""使用医疗物品"""
    	result = self.game.player.use_item(item_id)
    	messagebox.showinfo("使用物品", result['message'])
    	window.destroy()
    	self.show_medical()  # 刷新界面
    
    def show_construction(self):
        """显示建造界面"""
        window = tk.Toplevel(self.root)
        window.title("建造")
        window.geometry("600x400")
        
        # 显示可建造的结构
        structures = [
        {"name": "简易庇护所", "materials": {"wood": 10, "cloth": 5}, "description": "提供基本防护"},
        {"name": "储物箱", "materials": {"wood": 5, "metal": 2}, "description": "增加存储空间"},
        {"name": "工作台", "materials": {"wood": 8, "metal": 3}, "description": "便于制作物品"},
        {"name": "农田围栏", "materials": {"wood": 15, "materials": 5}, "description": "保护农作物"}
        ]
        
        for structure in structures:
        	frame = ttk.Frame(window, relief="solid", padding=10)
        	frame.pack(fill="x", padx=10, pady=5)
        	
        	ttk.Label(frame, text=structure["name"], style="Subtitle.TLabel").pack(anchor="w")
        	ttk.Label(frame, text=structure["description"]).pack(anchor="w")
        	
        	# 材料需求
        	materials_text = "需要: " + ", ".join([f"{self.game.items.get_item_name(mat)}x{amt}" 
                                              for mat, amt in structure["materials"].items()])
        	
        	ttk.Label(frame, text=materials_text, style="Status.TLabel").pack(anchor="w")
        	
        	# 检查是否可以建造
        	can_build = all(self.game.player.has_item(mat, amt) 
                    	for mat, amt in structure["materials"].items())
        	
        	button_text = "建造" if can_build else "材料不足"
        	button_state = "normal" if can_build else "disabled"
        	ttk.Button(frame, text=button_text, state=button_state,command=lambda s=structure: self.build_structure(s)).pack(anchor="e")
        	ttk.Button(window, text="关闭", command=window.destroy).pack(pady=10)

    def build_structure(self, structure):
    	"""建造结构"""
    	# 消耗材料
    	for material, amount in structure["materials"].items():
    		self.game.player.remove_item(material, amount)
    		
    		messagebox.showinfo("建造完成", f"成功建造了{structure['name']}！")
    		# 这里可以添加建造完成后的效果
    
    def show_research(self):
        """显示研究界面"""
        window = tk.Toplevel(self.root)
        window.title("研究")
        window.geometry("500x300")
    
        # 显示研究项目
        research_projects = [
        {"name": "基础农业技术", "cost": {"research_data": 5}, "description": "提高农作物产量"},
        {"name": "简易医疗知识", "cost": {"research_data": 3}, "description": "解锁新的医疗配方"},
        {"name": "武器改良技术", "cost": {"research_data": 8}, "description": "提高武器伤害"},
        {"name": "能源利用技术", "cost": {"research_data": 10}, "description": "解锁新的能源设备"}
        ]
    
        for project in research_projects:
        	frame = ttk.Frame(window, relief="solid", padding=10)
        	frame.pack(fill="x", padx=10, pady=5)
        	
        	ttk.Label(frame, text=project["name"], style="Subtitle.TLabel").pack(anchor="w")
        	ttk.Label(frame, text=project["description"]).pack(anchor="w")
        	
        	# 研究需求
        	cost_text = "需要研究资料: " + ", ".join([f"{amt}个" for amt in project["cost"].values()])
        	ttk.Label(frame, text=cost_text, style="Status.TLabel").pack(anchor="w")
        	
        	# 检查是否可以研究
        	can_research = all(self.game.player.has_item(mat, amt) for mat, amt in project["cost"].items())
        	
        	button_text = "研究" if can_research else "资料不足"
        	button_state = "normal" if can_research else "disabled"
        	
        	ttk.Button(frame, text=button_text, state=button_state,
                  command=lambda p=project: self.start_research(p)).pack(anchor="e")
        
        ttk.Button(window, text="关闭", command=window.destroy).pack(pady=10)

    def start_research(self, project):
    	"""开始研究"""
    	# 消耗研究资料
    	for material, amount in project["cost"].items():
        	self.game.player.remove_item(material, amount)
        	
    	messagebox.showinfo("研究开始", f"开始研究{project['name']}！")
    	# 这里可以添加研究完成后的效果
    
    def show_social(self):
        """显示社交界面"""
        window = tk.Toplevel(self.root)
        window.title("社交")
        window.geometry("600x400")
    
        notebook = ttk.Notebook(window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
        # NPC列表
        npc_frame = ttk.Frame(notebook)
        notebook.add(npc_frame, text="NPC")
    
        # 阵营关系
        faction_frame = ttk.Frame(notebook)
        notebook.add(faction_frame, text="阵营")
        
        self.create_npc_tab(npc_frame)
        self.create_faction_tab(faction_frame)

    def create_npc_tab(self, parent):
    	"""创建NPC标签页"""
    	# 获取当前位置的NPC
    	current_npcs = self.game.npcs.get_npcs_at_location(self.game.player.location)
    	
    	if not current_npcs:
         	ttk.Label(parent, text="当前位置没有NPC").pack(pady=20)
         	return
         	
    	for npc in current_npcs:
         	frame = ttk.Frame(parent, relief="solid", padding=10)
         	frame.pack(fill="x", padx=10, pady=5)
         	
         	ttk.Label(frame, text=npc["name"], style="Subtitle.TLabel").pack(anchor="w")
         	ttk.Label(frame, text=npc["description"]).pack(anchor="w")
         	
         	# 显示服务
         	services_text = "服务: " + ", ".join(npc.get("services", []))
         	ttk.Label(frame, text=services_text, style="Status.TLabel").pack(anchor="w")
         	
         	ttk.Button(frame, text="对话",
         	command=lambda n=npc: self.show_dialogue_window(n, n["dialogue"]["greeting"])).pack(anchor="e")

    def create_faction_tab(self, parent):
    	"""创建阵营标签页"""
    	relationships = self.game.npcs.get_player_relationships()
    	
    	if not relationships:
        	ttk.Label(parent, text="暂无阵营关系信息").pack(pady=20)
        	return
        	
    	text_widget = scrolledtext.ScrolledText(parent, wrap=tk.WORD, font=("Arial", 9))
    	text_widget.pack(fill="both", expand=True, padx=10, pady=10)
    	
    	for faction_id, info in relationships.items():
        	faction = info['faction']
        	text_widget.insert(tk.END, f"【{faction['name']}】\n")
        	text_widget.insert(tk.END, f"描述: {faction['description']}\n")
        	text_widget.insert(tk.END, f"声望: {info['reputation']} ({info['level']})\n")
        	text_widget.insert(tk.END, f"阵营倾向: {faction['alignment']}\n")
        	text_widget.insert(tk.END, "\n" + "-"*40 + "\n\n")
    
    	text_widget.config(state="disabled")
    
    def show_pause_menu(self):
        """显示暂停菜单"""
        # 实现暂停菜单逻辑
        # 如果已有暂停窗口，先关闭
        if hasattr(self, 'pause_window') and self.pause_window:
            self.pause_window.destroy()
    
        # 创建暂停菜单窗口
        self.pause_window = tk.Toplevel(self.root)
        self.pause_window.title("游戏暂停")
        self.pause_window.geometry("300x400")
        self.pause_window.transient(self.root)
        self.pause_window.grab_set()
    
        # 居中显示
        self.pause_window.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.pause_window.winfo_width()) // 2
        y = (self.root.winfo_screenheight() - self.pause_window.winfo_height()) // 2
        self.pause_window.geometry(f"+{x}+{y}")
    
        # 标题
        ttk.Label(self.pause_window, text="游戏暂停", style="Title.TLabel").pack(pady=20)
    
        # 暂停菜单选项
        options = [
            ("继续游戏", self.game.resume_game),
            ("保存游戏", self.game.save_game),
            ("游戏设置", self.show_settings_dialog),
            ("返回主菜单", self.return_to_main_menu),
            ("退出游戏", self.game.on_closing)
        ]
    
        for text, command in options:
          ttk.Button(self.pause_window, text=text, 
          command=lambda cmd=command: self.execute_pause_command(cmd),
          style="Action.TButton", width=20).pack(pady=5)
    
    def hide_pause_menu(self):
        """隐藏暂停菜单"""
        # 实现隐藏暂停菜单逻辑
        if hasattr(self, 'pause_window') and self.pause_window:
            self.pause_window.destroy()
            self.pause_window = None
    
    def execute_pause_command(self, command):
        """执行暂停菜单命令"""
        self.hide_pause_menu()
        command()

    def show_settings_dialog(self):
        """显示游戏设置对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("游戏设置")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
    
        ttk.Label(dialog, text="游戏设置", style="Title.TLabel").pack(pady=10)
    
        # 游戏速度设置
        speed_frame = ttk.Frame(dialog)
        speed_frame.pack(fill="x", padx=20, pady=10)
    
        ttk.Label(speed_frame, text="游戏速度:").pack(side="left")
    
        speed_var = tk.DoubleVar(value=self.game.game_speed)
        speed_scale = ttk.Scale(speed_frame, from_=0.5, to=3.0, variable=speed_var, 
        orient="horizontal", length=200)
        speed_scale.pack(side="left", padx=10)
    
        speed_label = ttk.Label(speed_frame, text=f"{speed_var.get():.1f}x")
        speed_label.pack(side="left")
    
        def update_speed_label(*args):
        	speed_label.config(text=f"{speed_var.get():.1f}x")
    	
        speed_var.trace('w', update_speed_label)
    
        # 确认按钮
        def apply_settings():
        	self.game.game_speed = speed_var.get()
        	self.add_log_message(f"游戏速度设置为 {speed_var.get():.1f} 倍")
        	dialog.destroy()
    
        ttk.Button(dialog, text="应用", command=apply_settings).pack(pady=10)
        ttk.Button(dialog, text="取消", command=dialog.destroy).pack(pady=5)

    def return_to_main_menu(self):
        """返回主菜单"""
        result = messagebox.askyesno("确认", "确定要返回主菜单吗？未保存的进度将会丢失。")
        if result:
            self.game.return_to_main_menu()
    
    def show_game_over(self, reason, days_survived):
        """显示游戏结束画面"""
        messagebox.showinfo("游戏结束", 
                          f"你死了！\n原因: {reason}\n生存天数: {days_survived}")
        self.create_main_menu()
    
    def show_game_background(self):
        """显示游戏背景"""
        self.show_info_window("游戏背景", self.game.story_book.get_background_story())
    
    def show_codex(self):
        """显示图鉴"""
        self.show_info_window("图鉴", self.game.story_book.get_codex_content())
    
    def show_story_book(self):
        """显示故事书"""
        self.show_info_window("故事书", self.game.story_book.get_all_stories())
    
    def show_gameplay_help(self):
        """显示游戏玩法帮助"""
        self.show_info_window("游戏玩法", self.game.story_book.get_gameplay_help())
    
    def show_info_window(self, title, content):
        """显示信息窗口"""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("600x500")
        
        text_widget = scrolledtext.ScrolledText(window,
                                              wrap=tk.WORD,
                                              font=("Arial", 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert(1.0, content)
        text_widget.config(state="disabled")
        
        ttk.Button(window, text="关闭", command=window.destroy).pack(pady=10)
    
    def show_dialogue_window(self, npc, dialogue):
        """显示对话窗口"""
        window = tk.Toplevel(self.root)
        window.title(f"与 {npc['name']} 对话")
        window.geometry("500x400")
        
        # NPC信息
        info_frame = ttk.Frame(window)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(info_frame, text=npc['name'], style="Subtitle.TLabel").pack(anchor="w")
        ttk.Label(info_frame, text=npc['description'], style="Status.TLabel").pack(anchor="w")
        
        # 对话内容
        dialogue_text = scrolledtext.ScrolledText(window,
                                                 wrap=tk.WORD,
                                                 height=15)
        dialogue_text.pack(fill="both", expand=True, padx=10, pady=5)
        dialogue_text.insert(1.0, dialogue)
        dialogue_text.config(state="disabled")
        
        # 对话选项
        options_frame = ttk.Frame(window)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        topics = list(npc['dialogue']['topics'].keys())
        for topic in topics:
            ttk.Button(options_frame,
                      text=topic,
                      command=lambda t=topic: self.show_topic_dialogue(npc, t, dialogue_text)).pack(side="left", padx=5)
        
        ttk.Button(options_frame, text="再见", command=window.destroy).pack(side="right")
    
    
    def show_topic_dialogue(self, npc, topic, text_widget):
        """显示特定话题的对话"""
        dialogue = self.game.npcs.get_dialogue(npc['id'], topic)
        text_widget.config(state="normal")
        text_widget.insert(tk.END, f"\n\n你: 关于{topic}...\n{npc['name']}: {dialogue}")
        text_widget.see(tk.END)
        text_widget.config(state="disabled")
    
        # 记录交互
        self.game.npcs.record_interaction(npc['id'])
    
        # 增加社交技能经验
        self.game.player.gain_skill_exp('social', 5)

#版权归 乐观的兔子/研究员要加钱 所有