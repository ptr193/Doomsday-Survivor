# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import logging
import os
import json

class GameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.current_frame = None
        self.log_messages = []
        self.inventory_tree = None
        
        # 设置窗口
        self.setup_window()
        
    def setup_window(self):
        """设置窗口属性"""
        self.root.title(f"末日生存者 v{self.game.version}")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        win_width = int(screen_width * 0.8)
        win_height = int(screen_height * 0.8)
        self.root.geometry(f"{win_width}x{win_height}")
        self.root.minsize(800, 600)
        self.root.resizable(True, True)

        self.setup_styles()
        self.root.protocol("WM_DELETE_WINDOW", self.game.on_closing)
    
    def setup_styles(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), foreground="#2C3E50")
        style.configure("Subtitle.TLabel", font=("Arial", 12, "bold"), foreground="#34495E")
        style.configure("Normal.TLabel", font=("Arial", 10), foreground="#2C3E50")
        style.configure("Status.TLabel", font=("Arial", 9), foreground="#7F8C8D")
        style.configure("Action.TButton", font=("Arial", 10, "bold"), padding=(10, 5))
        style.configure("Danger.TButton", font=("Arial", 10, "bold"), foreground="white", background="#E74C3C")
    
    def clear_interface(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_main_menu(self):
        self.clear_interface()
        title_label = ttk.Label(self.current_frame, text="末日生存者", style="Title.TLabel")
        title_label.pack(pady=30)
        version_label = ttk.Label(self.current_frame, text=f"版本 {self.game.version}", style="Status.TLabel")
        version_label.pack(pady=5)
        button_frame = ttk.Frame(self.current_frame)
        button_frame.pack(pady=30)
        start_button = ttk.Button(button_frame, text="开始游戏", command=self.show_save_slots, style="Action.TButton", width=20)
        start_button.pack(pady=10)
        background_button = ttk.Button(button_frame, text="游戏背景", command=self.show_game_background, style="Action.TButton", width=20)
        background_button.pack(pady=10)
        codex_button = ttk.Button(button_frame, text="图鉴", command=self.show_codex, style="Action.TButton", width=20)
        codex_button.pack(pady=10)
        story_button = ttk.Button(button_frame, text="故事书", command=self.show_story_book, style="Action.TButton", width=20)
        story_button.pack(pady=10)
        gameplay_button = ttk.Button(button_frame, text="游戏玩法", command=self.show_gameplay_help, style="Action.TButton", width=20)
        gameplay_button.pack(pady=10)
        exit_button = ttk.Button(button_frame, text="退出游戏", command=self.game.on_closing, style="Danger.TButton", width=20)
        exit_button.pack(pady=20)
    
    def show_save_slots(self):
        self.clear_interface()
        back_button = ttk.Button(self.current_frame, text="返回主菜单", command=self.create_main_menu)
        back_button.pack(anchor="nw", pady=5)
        title_label = ttk.Label(self.current_frame, text="选择存档槽", style="Title.TLabel")
        title_label.pack(pady=20)
        slots_frame = ttk.Frame(self.current_frame)
        slots_frame.pack(fill="both", expand=True, padx=50, pady=20)
        for i in range(1, 6):
            slot_frame = ttk.Frame(slots_frame, relief="solid", padding=10)
            slot_frame.pack(fill="x", pady=5)
            save_file = f"saves/save_slot_{i}.json"
            try:
                if os.path.exists(save_file):
                    with open(save_file, 'r', encoding='utf-8') as f:
                        save_data = json.load(f)
                    player_name = save_data.get('player', {}).get('name', '未知')
                    day_count = save_data.get('day_count', 1)
                    save_time = save_data.get('save_time', '未知时间')
                    slot_text = f"存档 {i}: {player_name} - 第{day_count}天 - {save_time}"
                    info_label = ttk.Label(slot_frame, text=slot_text, style="Normal.TLabel")
                    info_label.pack(side="left", padx=10)
                    load_button = ttk.Button(slot_frame, text="加载", command=lambda slot=i: self.game.load_game(slot))
                    load_button.pack(side="right", padx=5)
                    delete_button = ttk.Button(slot_frame, text="删除", command=lambda slot=i: self.delete_save_confirm(slot))
                    delete_button.pack(side="right", padx=5)
                else:
                    info_label = ttk.Label(slot_frame, text=f"存档 {i}: 空", style="Normal.TLabel")
                    info_label.pack(side="left", padx=10)
                    new_game_button = ttk.Button(slot_frame, text="新游戏", command=lambda slot=i: self.show_character_selection(slot))
                    new_game_button.pack(side="right", padx=5)
            except Exception as e:
                logging.error(f"读取存档信息失败: {e}")
                error_label = ttk.Label(slot_frame, text=f"存档 {i}: 损坏", style="Normal.TLabel")
                error_label.pack(side="left", padx=10)
    
    def delete_save_confirm(self, save_slot):
        result = messagebox.askyesno("确认删除", f"确定要删除存档 {save_slot} 吗？")
        if result:
            save_file = f"saves/save_slot_{save_slot}.json"
            if os.path.exists(save_file):
                os.remove(save_file)
            self.show_save_slots()
    
    def show_character_selection(self, save_slot):
        self.clear_interface()
        back_button = ttk.Button(self.current_frame, text="返回存档选择", command=self.show_save_slots)
        back_button.pack(anchor="nw", pady=5)
        title_label = ttk.Label(self.current_frame, text="选择你的角色", style="Title.TLabel")
        title_label.pack(pady=20)
        characters = [
            {"name": "生存专家", "class": "survival_expert", "description": "精通生存技巧，擅长寻找资源和建造庇护所",
             "health": 100, "max_health": 100, "stamina": 80, "max_stamina": 80,
             "strength": 7, "agility": 6, "intelligence": 8, "luck": 5},
            {"name": "战斗精英", "class": "combat_elite", "description": "前特种部队成员，精通各种战斗技巧",
             "health": 120, "max_health": 120, "stamina": 70, "max_stamina": 70,
             "strength": 9, "agility": 8, "intelligence": 6, "luck": 4},
            {"name": "敏捷猎手", "class": "agile_hunter", "description": "擅长潜行和追踪，能够轻易避开危险",
             "health": 90, "max_health": 90, "stamina": 100, "max_stamina": 100,
             "strength": 6, "agility": 9, "intelligence": 7, "luck": 6},
            {"name": "幸运探索者", "class": "lucky_explorer", "description": "天生幸运，总能找到稀有物品和避开危险",
             "health": 80, "max_health": 80, "stamina": 80, "max_stamina": 80,
             "strength": 5, "agility": 7, "intelligence": 6, "luck": 10}
        ]
        for char in characters:
            char_frame = ttk.Frame(self.current_frame, relief="solid", padding=15)
            char_frame.pack(fill="x", padx=50, pady=10)
            name_label = ttk.Label(char_frame, text=char["name"], style="Subtitle.TLabel")
            name_label.pack(anchor="w")
            desc_label = ttk.Label(char_frame, text=char["description"], style="Normal.TLabel")
            desc_label.pack(anchor="w", pady=5)
            stats_text = (f"生命: {char['health']}/{char['max_health']} | 体力: {char['stamina']}/{char['max_stamina']} | "
                          f"力量: {char['strength']} | 敏捷: {char['agility']} | 智力: {char['intelligence']} | 幸运: {char['luck']}")
            stats_label = ttk.Label(char_frame, text=stats_text, style="Status.TLabel")
            stats_label.pack(anchor="w")
            select_button = ttk.Button(char_frame, text="选择角色", command=lambda c=char, s=save_slot: self.game.start_new_game(s, c), style="Action.TButton")
            select_button.pack(anchor="e", pady=5)
    
    def create_game_interface(self):
        self.clear_interface()
        self.create_status_bar()
        self.status_bar_frame.pack(fill="x", pady=5)
        main_frame = ttk.Frame(self.current_frame)
        main_frame.pack(fill="both", expand=True, pady=10)
        self.create_game_log(main_frame)
        self.create_control_panel(main_frame)
        self.create_action_bar()
    
    def create_status_bar(self):
        self.status_bar_frame = ttk.Frame(self.current_frame, relief="solid", padding=5)
        self.status_label = ttk.Label(self.status_bar_frame, text="初始化中...", style="Normal.TLabel")
        self.status_label.pack(side="left")
        pause_button = ttk.Button(self.status_bar_frame, text="暂停", command=self.game.pause_game)
        pause_button.pack(side="right", padx=5)
        save_button = ttk.Button(self.status_bar_frame, text="保存", command=self.game.save_game)
        save_button.pack(side="right", padx=5)
    
    def create_game_log(self, parent):
        log_frame = ttk.Frame(parent)
        log_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        log_label = ttk.Label(log_frame, text="游戏日志", style="Subtitle.TLabel")
        log_label.pack(anchor="w", pady=5)
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=60, height=25, font=("Arial", 9))
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state="disabled")
    
    def create_control_panel(self, parent):
        control_frame = ttk.Frame(parent, width=300)
        control_frame.pack(side="right", fill="y")
        control_frame.pack_propagate(False)
        self.create_location_info(control_frame)
        self.create_quick_actions(control_frame)
        self.create_quest_info(control_frame)
    
    def create_location_info(self, parent):
        loc_frame = ttk.LabelFrame(parent, text="当前位置", padding=10)
        loc_frame.pack(fill="x", pady=10)
        self.location_label = ttk.Label(loc_frame, text="加载中...", style="Normal.TLabel")
        self.location_label.pack(anchor="w")
        self.terrain_label = ttk.Label(loc_frame, text="", style="Status.TLabel")
        self.terrain_label.pack(anchor="w")
        self.danger_label = ttk.Label(loc_frame, text="", style="Status.TLabel")
        self.danger_label.pack(anchor="w")
    
    def create_quick_actions(self, parent):
        action_frame = ttk.LabelFrame(parent, text="快捷操作", padding=10)
        action_frame.pack(fill="x", pady=10)
        action_map = {
            "explore": self.game.perform_action, "rest": self.game.perform_action, "sleep": self.show_sleep_dialog,
            "eat": self.show_eat_dialog, "drink": self.show_drink_dialog, "fish": self.game.perform_action,
            "hunt": self.game.perform_action, "chop_wood": self.game.perform_action, "gather_herbs": self.game.perform_action,
            "craft": self.show_crafting, "farm": self.show_farming, "trade": self.show_trade_dialog,
            "repair": self.show_repair_dialog, "research": self.game.perform_action, "meditate": self.game.perform_action,
            "inventory": self.show_inventory, "map": self.show_map, "quests": self.show_quests
        }
        action_order = ["explore", "rest", "sleep", "eat", "drink", "fish", "hunt",
                        "chop_wood", "gather_herbs", "craft", "farm", "trade",
                        "repair", "research", "meditate", "inventory", "map", "quests"]
        for action_id in action_order:
            if action_id in self.game.actions:
                action_data = self.game.actions[action_id]
                btn_text = action_data.get("name", action_id)
                command = action_map.get(action_id)
                if command:
                    if action_id in ["explore", "rest", "fish", "hunt", "chop_wood", "gather_herbs", "research", "meditate"]:
                        btn = ttk.Button(action_frame, text=btn_text, command=lambda a=action_id: command(a), style="Action.TButton", width=15)
                    elif action_id in ["craft", "farm", "trade", "repair", "inventory", "map", "quests"]:
                        btn = ttk.Button(action_frame, text=btn_text, command=command, style="Action.TButton", width=15)
                    else:
                        btn = ttk.Button(action_frame, text=btn_text, command=command, style="Action.TButton", width=15)
                    btn.pack(fill="x", pady=2)
    
    def create_quest_info(self, parent):
        quest_frame = ttk.LabelFrame(parent, text="当前任务", padding=10)
        quest_frame.pack(fill="both", expand=True, pady=10)
        self.quest_text = scrolledtext.ScrolledText(quest_frame, wrap=tk.WORD, height=8, font=("Arial", 8))
        self.quest_text.pack(fill="both", expand=True)
        self.quest_text.config(state="disabled")
    
    def create_action_bar(self):
        action_frame = ttk.Frame(self.current_frame)
        action_frame.pack(fill="x", pady=10)
        professional_actions = [("医疗", self.show_medical), ("建造", self.show_construction), ("研究", self.show_research), ("社交", self.show_social)]
        for action_text, action_command in professional_actions:
            button = ttk.Button(action_frame, text=action_text, command=action_command)
            button.pack(side="left", padx=5)
    
    def update_status_display(self):
        if not self.game.player.initialized:
            return
        player = self.game.player
        status_text = (f"{player.name} | 生命: {player.health}/{player.max_health} | 体力: {player.stamina}/{player.max_stamina} | "
                       f"精神: {player.mental}/{player.max_mental} | 疲劳: {player.fatigue}/{player.max_fatigue} | "
                       f"辐射: {self.game.radiation_level}% | 第{self.game.day_count}天 {self.game.format_time()} | "
                       f"{self.game.get_weather_name()} | {self.game.get_season_name()}")
        self.status_label.config(text=status_text)
        location = self.game.world.get_current_location()
        if location:
            danger_desc = self.game.world.get_location_danger_description(location.safety_level)
            self.location_label.config(text=location.name)
            self.terrain_label.config(text=f"地形: {location.terrain}")
            self.danger_label.config(text=f"危险程度: {danger_desc}")
        self.update_quest_display()
    
    def update_quest_display(self):
        active_quests = self.game.quests.active_quests
        if not active_quests:
            quest_text = "没有进行中的任务"
        else:
            quest_text = ""
            for quest_id in active_quests[:3]:
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
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        lines = self.log_text.get(1.0, tk.END).split('\n')
        if len(lines) > 100:
            self.log_text.delete(1.0, f"{len(lines)-100}.0")
    
    # ========== 对话框 ==========
    def show_sleep_dialog(self):
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
            ttk.Radiobutton(hours_frame, text=f"{hours}小时", variable=hours_var, value=hours).pack(side="left", padx=5)
        def confirm_sleep():
            self.game.perform_action("sleep", hours=hours_var.get())
            dialog.destroy()
        ttk.Button(dialog, text="睡觉", command=confirm_sleep).pack(pady=10)
        ttk.Button(dialog, text="取消", command=dialog.destroy).pack(pady=5)
    
    def show_eat_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("进食")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        ttk.Label(dialog, text="选择要食用的食物:", style="Subtitle.TLabel").pack(pady=10)
        food_items = []
        for item_id, quantity in self.game.player.inventory.items():
            item_data = self.game.items.get_item_data(item_id)
            if item_data and item_data.get('type') == 'food' and quantity > 0:
                food_items.append((item_id, item_data, quantity))
        if not food_items:
            ttk.Label(dialog, text="没有可食用的食物", style="Normal.TLabel").pack(pady=20)
            ttk.Button(dialog, text="关闭", command=dialog.destroy).pack(pady=10)
            return
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
            info_text = f"{item_data['name']} x{quantity}\n{item_data['description']}"
            if item_data.get('health_restore', 0) > 0:
                info_text += f"\n恢复生命: {item_data['health_restore']}"
            if item_data.get('stamina_restore', 0) > 0:
                info_text += f" | 恢复体力: {item_data['stamina_restore']}"
            ttk.Label(item_frame, text=info_text, style="Normal.TLabel").pack(side="left", anchor="w")
            ttk.Button(item_frame, text="食用", command=lambda iid=item_id: self.eat_food(iid, dialog)).pack(side="right", padx=5)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        ttk.Button(dialog, text="取消", command=dialog.destroy).pack(pady=10)
    
    def eat_food(self, item_id, dialog):
        self.game.perform_action("eat", food_type=item_id)
        dialog.destroy()
    
    def show_drink_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("喝水")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        ttk.Label(dialog, text="选择要饮用的饮品", style="Subtitle.TLabel").pack(pady=10)
        drink_items = []
        for item_id, quantity in self.game.player.inventory.items():
            item_data = self.game.items.get_item_data(item_id)
            if item_data and item_data.get('type') == 'drink' and quantity > 0:
                drink_items.append((item_id, item_data, quantity))
        if not drink_items:
            ttk.Label(dialog, text="没有可饮用的饮品", style="Normal.TLabel").pack(pady=20)
            ttk.Button(dialog, text="关闭", command=dialog.destroy).pack(pady=10)
            return
        container = ttk.Frame(dialog)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        for item_id, item_data, quantity in drink_items:
            item_frame = ttk.Frame(scrollable_frame, relief="solid", padding=12)
            item_frame.pack(fill="x", pady=3, padx=5)
            info_frame = ttk.Frame(item_frame)
            info_frame.pack(side="left", fill="x", expand=True)
            name_label = ttk.Label(info_frame, text=f"{item_data['name']} x{quantity}", style="Subtitle.TLabel")
            name_label.pack(anchor="w")
            desc_label = ttk.Label(info_frame, text=item_data['description'], style="Normal.TLabel")
            desc_label.pack(anchor="w", pady=2)
            effects = []
            if item_data.get('health_restore', 0) > 0:
                effects.append(f"💗 生命+{item_data['health_restore']}")
            if item_data.get('stamina_restore', 0) > 0:
                effects.append(f"⚡ 体力+{item_data['stamina_restore']}")
            if item_data.get('mental_restore', 0) > 0:
                effects.append(f"🧠 精神+{item_data['mental_restore']}")
            if effects:
                effects_label = ttk.Label(info_frame, text=" | ".join(effects), style="Status.TLabel")
                effects_label.pack(anchor="w")
            ttk.Button(item_frame, text="饮用", command=lambda iid=item_id: self.drink_item(iid, dialog)).pack(side="right", padx=5)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        ttk.Button(dialog, text="取消", command=dialog.destroy).pack(pady=10)
    
    def drink_item(self, item_id, dialog):
        self.game.perform_action("drink", drink_type=item_id)
        dialog.destroy()
    
    def show_inventory(self):
        inv_win = tk.Toplevel(self.root)
        inv_win.title("背包")
        inv_win.geometry("700x500")
        inv_win.minsize(500, 400)
        notebook = ttk.Notebook(inv_win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        items_frame = ttk.Frame(notebook)
        notebook.add(items_frame, text="物品")
        equipment_frame = ttk.Frame(notebook)
        notebook.add(equipment_frame, text="装备")
        self.create_inventory_tab(items_frame, inv_win)
        self.create_equipment_tab(equipment_frame, inv_win)
    
    def create_inventory_tab(self, parent, win):
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill="x", pady=5)
        categories = ["全部", "食物", "饮品", "材料", "医疗", "种子", "武器", "防具", "特殊"]
        category_var = tk.StringVar(value="全部")
        for cat in categories:
            ttk.Radiobutton(filter_frame, text=cat, variable=category_var, value=cat,
                            command=lambda: self.refresh_inventory()).pack(side="left", padx=5)
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)
        columns = ("名称", "数量", "类型", "描述")
        self.inventory_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=100)
        self.inventory_tree.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.inventory_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=5)
        ttk.Button(button_frame, text="使用", command=self.use_selected_item).pack(side="left", padx=5)
        ttk.Button(button_frame, text="丢弃", command=self.drop_selected_item).pack(side="left", padx=5)
        ttk.Button(button_frame, text="关闭", command=win.destroy).pack(side="right", padx=5)
        self.refresh_inventory()
    
    def refresh_inventory(self):
        if hasattr(self, 'inventory_tree'):
            for item in self.inventory_tree.get_children():
                self.inventory_tree.delete(item)
            for item_id, quantity in self.game.player.inventory.items():
                if quantity > 0:
                    item_data = self.game.items.get_item_data(item_id)
                    if item_data:
                        self.inventory_tree.insert("", "end", values=(
                            item_data['name'], quantity, item_data.get('type', '未知'), item_data.get('description', '')
                        ))
    
    def use_selected_item(self):
        selection = self.inventory_tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请选择一个物品")
            return
        item_values = self.inventory_tree.item(selection[0])['values']
        item_name = item_values[0]
        item_id = None
        for iid, data in self.game.items.items.items():
            if data['name'] == item_name:
                item_id = iid
                break
        if item_id:
            self.game.perform_action("use_item", item_id=item_id)
            self.refresh_inventory()
    
    def drop_selected_item(self):
        selection = self.inventory_tree.selection()
        if not selection:
            return
        item_values = self.inventory_tree.item(selection[0])['values']
        item_name = item_values[0]
        result = messagebox.askyesno("确认丢弃", f"确定要丢弃 {item_name} 吗？")
        if result:
            for iid, data in self.game.items.items.items():
                if data['name'] == item_name:
                    self.game.player.remove_item(iid, 1)
                    break
            self.refresh_inventory()
    
    def create_equipment_tab(self, parent, win):
        slots = {'weapon': '武器', 'head': '头部', 'chest': '胸部', 'legs': '腿部', 'backpack': '背包',
                 'accessory1': '饰品1', 'accessory2': '饰品2'}
        for slot, slot_name in slots.items():
            slot_frame = ttk.Frame(parent)
            slot_frame.pack(fill="x", padx=10, pady=2)
            ttk.Label(slot_frame, text=slot_name, width=10).pack(side="left")
            item_id = self.game.player.equipment.get(slot)
            if item_id:
                item_data = self.game.items.get_item_data(item_id)
                item_text = f"{item_data['name']}" if item_data else "未知装备"
            else:
                item_text = "空"
            item_label = ttk.Label(slot_frame, text=item_text)
            item_label.pack(side="left", padx=10)
            if item_id:
                ttk.Button(slot_frame, text="卸下", command=lambda s=slot: self.unequip_item(s)).pack(side="right")
            else:
                ttk.Button(slot_frame, text="装备", command=lambda s=slot: self.show_equip_dialog(s)).pack(side="right")
    
    def unequip_item(self, slot):
        self.game.player.unequip_item(slot)
        self.show_inventory()
    
    def show_equip_dialog(self, slot):
        equipable_items = []
        for item_id, quantity in self.game.player.inventory.items():
            if quantity > 0:
                item_data = self.game.items.get_item_data(item_id)
                if item_data and item_data.get('equip_slot') == slot:
                    equipable_items.append((item_id, item_data))
        if not equipable_items:
            messagebox.showinfo("提示", "没有可装备的物品")
            return
        dialog = tk.Toplevel(self.root)
        dialog.title(f"装备 {slot}")
        dialog.geometry("400x300")
        for item_id, item_data in equipable_items:
            frame = ttk.Frame(dialog, relief="solid", padding=5)
            frame.pack(fill="x", padx=10, pady=2)
            ttk.Label(frame, text=item_data['name']).pack(side="left")
            ttk.Button(frame, text="装备", command=lambda iid=item_id: self.equip_item(iid, slot, dialog)).pack(side="right")
    
    def equip_item(self, item_id, slot, dialog):
        self.game.player.equip_item(item_id, slot)
        dialog.destroy()
        self.show_inventory()
    
    def show_map(self):
        map_win = tk.Toplevel(self.root)
        map_win.title("世界地图")
        map_win.geometry("800x600")
        map_win.minsize(500, 400)
        canvas = tk.Canvas(map_win, bg="#2e2e2e", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        locations = self.game.world.locations
        discovered = [loc for loc in locations.values() if loc.discovered]
        for loc in discovered:
            for conn_id in loc.connected_locations:
                if conn_id in locations and locations[conn_id].discovered:
                    conn = locations[conn_id]
                    canvas.create_line(loc.x, loc.y, conn.x, conn.y, fill="#888", width=2, tags="line")
        for loc in discovered:
            terrain_color = {
                "森林": "#2d6a4f", "平原": "#a7c5a3", "山地": "#8d6b63", "河流": "#4ea8de",
                "农田": "#b7b16b", "道路": "#b5838a", "遗迹": "#6c4e3e", "建筑": "#4a6e8c", "营地": "#c77dff"
            }.get(loc.terrain, "#cccccc")
            has_building = any(kw in loc.name for kw in ["农场", "农舍", "贸易站", "营地", "遗迹"])
            has_npc = loc.id in ["trading_post", "survivor_camp", "farmhouse"]
            if has_building and has_npc:
                size = 16
                x1, y1 = loc.x - size//2, loc.y - size//2
                x2, y2 = loc.x + size//2, loc.y + size//2
                canvas.create_rectangle(x1, y1, x2, y2, fill=terrain_color, outline="gold", width=2, tags=loc.id)
                canvas.create_text(loc.x, loc.y, text="★", fill="gold", font=("Arial", 12), tags=loc.id)
            elif has_building:
                size = 14
                x1, y1 = loc.x - size//2, loc.y - size//2
                x2, y2 = loc.x + size//2, loc.y + size//2
                canvas.create_rectangle(x1, y1, x2, y2, fill=terrain_color, outline="white", width=1, tags=loc.id)
            elif has_npc:
                canvas.create_oval(loc.x-8, loc.y-8, loc.x+8, loc.y+8, fill=terrain_color, outline="cyan", width=2, tags=loc.id)
                canvas.create_text(loc.x, loc.y, text="●", fill="cyan", font=("Arial", 10), tags=loc.id)
            else:
                canvas.create_oval(loc.x-8, loc.y-8, loc.x+8, loc.y+8, fill=terrain_color, outline="white", width=1, tags=loc.id)
            canvas.create_text(loc.x, loc.y-12, text=loc.name, fill="white", font=("Arial", 9), tags=loc.id)
        def on_map_click(event):
            items = canvas.find_withtag("current")
            if items:
                loc_id = canvas.gettags(items[0])[0]
                if loc_id in locations:
                    self.game.perform_action("move", location_id=loc_id)
                    map_win.destroy()
        canvas.tag_bind("all", "<Button-1>", on_map_click)
        ttk.Button(map_win, text="关闭", command=map_win.destroy).pack(pady=5)
    
    def show_crafting(self):
        win = tk.Toplevel(self.root)
        win.title("制作")
        win.geometry("700x500")
        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        categories = {'tools': '工具', 'weapons': '武器', 'armor': '防具', 'medical': '医疗', 'food': '食物', 'construction': '建筑'}
        for cat, name in categories.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=name)
            self.create_crafting_category_tab(frame, cat, win)
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=5)
    
    def create_crafting_category_tab(self, parent, category, win):
        recipes = self.game.items.get_recipes_by_category(category)
        if not recipes:
            ttk.Label(parent, text="没有可制作的配方").pack(pady=20)
            return
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
            materials = ", ".join([f"{self.game.items.get_item_name(mat)}x{amt}" for mat, amt in recipe['materials'].items()])
            products = ", ".join([f"{self.game.items.get_item_name(prod)}x{amt}" for prod, amt in recipe['products'].items()])
            tree.insert("", "end", values=(recipe['name'], materials, products, recipe['difficulty']))
        tree.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        def craft_selected():
            selection = tree.selection()
            if selection:
                recipe_index = tree.index(selection[0])
                recipe = recipes[recipe_index]
                self.game.perform_action("craft", recipe_id=recipe['id'])
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=5)
        ttk.Button(button_frame, text="制作", command=craft_selected).pack(side="left", padx=5)
    
    def show_farming(self):
        win = tk.Toplevel(self.root)
        win.title("农业")
        win.geometry("600x500")
        current_loc = self.game.player.location
        if not self.game.farming.can_plant(current_loc):
            ttk.Label(win, text="当前位置不能种植").pack(pady=20)
            ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
            return
        status = self.game.farming.get_farmland_status(current_loc)
        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        planting_frame = ttk.Frame(notebook)
        notebook.add(planting_frame, text="种植")
        management_frame = ttk.Frame(notebook)
        notebook.add(management_frame, text="管理")
        self.create_planting_tab(planting_frame, status)
        self.create_management_tab(management_frame, status)
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
    def create_planting_tab(self, parent, status):
        ttk.Label(parent, text=f"可用地块: {status['empty_plots']}/{status['total_plots']}").pack(pady=5)
        seasonal_crops = self.game.farming.get_seasonal_crops()
        if not seasonal_crops:
            ttk.Label(parent, text="当前季节没有适宜的作物").pack(pady=20)
            return
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, pady=10)
        columns = ("名称", "类型", "生长时间", "产量", "描述")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
        for crop in seasonal_crops:
            growth_days = crop['growth_stages'] * crop['growth_days_per_stage']
            yield_range = f"{crop['yield_amount'][0]}-{crop['yield_amount'][1]}"
            tree.insert("", "end", values=(crop['name'], crop['type'], f"{growth_days}天", yield_range, crop['description']))
        tree.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        def plant_selected():
            selection = tree.selection()
            if selection:
                crop_index = tree.index(selection[0])
                crop = seasonal_crops[crop_index]
                self.game.perform_action("farm", crop_type=crop['id'])
        ttk.Button(parent, text="种植选中作物", command=plant_selected).pack(pady=5)
    
    def create_management_tab(self, parent, status):
        text = scrolledtext.ScrolledText(parent, wrap=tk.WORD, font=("Arial", 9))
        text.pack(fill="both", expand=True, padx=10, pady=10)
        for plot in status.get('plots_details', []):
            if plot.get('crop_type'):
                text.insert(tk.END, f"地块 {plot['id']}: {plot.get('crop_name', '未知')}\n")
                text.insert(tk.END, f"  生长阶段: {plot.get('growth_description', '未知')}\n")
                text.insert(tk.END, f"  健康: {plot.get('health', 0)}% | 水分: {plot.get('water_level', 0)}% | 害虫: {plot.get('pest_infestation', 0)}% | 杂草: {plot.get('weeds', 0)}%\n\n")
        text.config(state="disabled")
    
    def show_quests(self):
        win = tk.Toplevel(self.root)
        win.title("任务")
        win.geometry("700x500")
        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        active_frame = ttk.Frame(notebook)
        notebook.add(active_frame, text="进行中")
        available_frame = ttk.Frame(notebook)
        notebook.add(available_frame, text="可接受")
        completed_frame = ttk.Frame(notebook)
        notebook.add(completed_frame, text="已完成")
        self.create_active_quests_tab(active_frame)
        self.create_available_quests_tab(available_frame)
        self.create_completed_quests_tab(completed_frame)
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
    def create_active_quests_tab(self, parent):
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
    
    def create_available_quests_tab(self, parent):
        available = self.game.quests.get_available_quests()
        if not available:
            ttk.Label(parent, text="没有可接受的任务").pack(pady=20)
            return
        for quest in available:
            frame = ttk.Frame(parent, relief="solid", padding=10)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=quest['name'], style="Subtitle.TLabel").pack(anchor="w")
            ttk.Label(frame, text=quest['description']).pack(anchor="w")
            ttk.Button(frame, text="接受任务", command=lambda qid=quest['id']: self.accept_quest(qid)).pack(anchor="e")
    
    def accept_quest(self, quest_id):
        result = self.game.quests.start_quest(quest_id)
        if result['success']:
            self.show_quests()
        else:
            messagebox.showwarning("接受失败", result['message'])
    
    def create_completed_quests_tab(self, parent):
        completed = self.game.quests.completed_quests
        if not completed:
            ttk.Label(parent, text="没有已完成的任务").pack(pady=20)
            return
        text_widget = scrolledtext.ScrolledText(parent, wrap=tk.WORD, font=("Arial", 9))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        for quest_id in completed:
            quest = self.game.quests.quests.get(quest_id)
            if quest:
                text_widget.insert(tk.END, f"✓ {quest['name']}\n")
        text_widget.config(state="disabled")
    
    def show_medical(self):
        win = tk.Toplevel(self.root)
        win.title("医疗")
        win.geometry("500x400")
        status_frame = ttk.LabelFrame(win, text="健康状况", padding=10)
        status_frame.pack(fill="x", padx=10, pady=10)
        player = self.game.player
        ttk.Label(status_frame, text=f"生命值: {player.health}/{player.max_health}").pack(anchor="w")
        ttk.Label(status_frame, text=f"精神状态: {player.mental}/{player.max_mental}").pack(anchor="w")
        ttk.Label(status_frame, text=f"疲劳值: {player.fatigue}/{player.max_fatigue}").pack(anchor="w")
        medical_frame = ttk.LabelFrame(win, text="医疗物品", padding=10)
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
                ttk.Button(item_frame, text="使用", command=lambda iid=item_id: self.use_medical_item(iid, win)).pack(side="right")
        else:
            ttk.Label(medical_frame, text="没有医疗物品").pack(pady=20)
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
    def use_medical_item(self, item_id, win):
        self.game.perform_action("use_item", item_id=item_id)
        win.destroy()
        self.show_medical()
    
    def show_construction(self):
        win = tk.Toplevel(self.root)
        win.title("建造")
        win.geometry("600x400")
        structures = [
            {"name": "简易庇护所", "materials": {"wood": 10, "cloth": 5}, "description": "提供基本防护"},
            {"name": "储物箱", "materials": {"wood": 5, "metal": 2}, "description": "增加存储空间"},
            {"name": "工作台", "materials": {"wood": 8, "metal": 3}, "description": "便于制作物品"},
            {"name": "农田围栏", "materials": {"wood": 15, "materials": 5}, "description": "保护农作物"}
        ]
        for structure in structures:
            frame = ttk.Frame(win, relief="solid", padding=10)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=structure["name"], style="Subtitle.TLabel").pack(anchor="w")
            ttk.Label(frame, text=structure["description"]).pack(anchor="w")
            materials_text = "需要: " + ", ".join([f"{self.game.items.get_item_name(mat)}x{amt}" for mat, amt in structure["materials"].items()])
            ttk.Label(frame, text=materials_text, style="Status.TLabel").pack(anchor="w")
            can_build = all(self.game.player.has_item(mat, amt) for mat, amt in structure["materials"].items())
            button_text = "建造" if can_build else "材料不足"
            button_state = "normal" if can_build else "disabled"
            ttk.Button(frame, text=button_text, state=button_state, command=lambda s=structure: self.build_structure(s)).pack(anchor="e")
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
    def build_structure(self, structure):
        for material, amount in structure["materials"].items():
            self.game.player.remove_item(material, amount)
        messagebox.showinfo("建造完成", f"成功建造了{structure['name']}！")
    
    def show_research(self):
        win = tk.Toplevel(self.root)
        win.title("研究")
        win.geometry("500x300")
        research_projects = [
            {"name": "基础农业技术", "cost": {"research_data": 5}, "description": "提高农作物产量"},
            {"name": "简易医疗知识", "cost": {"research_data": 3}, "description": "解锁新的医疗配方"},
            {"name": "武器改良技术", "cost": {"research_data": 8}, "description": "提高武器伤害"},
            {"name": "能源利用技术", "cost": {"research_data": 10}, "description": "解锁新的能源设备"}
        ]
        for project in research_projects:
            frame = ttk.Frame(win, relief="solid", padding=10)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=project["name"], style="Subtitle.TLabel").pack(anchor="w")
            ttk.Label(frame, text=project["description"]).pack(anchor="w")
            cost_text = "需要研究资料: " + ", ".join([f"{amt}个" for amt in project["cost"].values()])
            ttk.Label(frame, text=cost_text, style="Status.TLabel").pack(anchor="w")
            can_research = all(self.game.player.has_item(mat, amt) for mat, amt in project["cost"].items())
            button_text = "研究" if can_research else "资料不足"
            button_state = "normal" if can_research else "disabled"
            ttk.Button(frame, text=button_text, state=button_state, command=lambda p=project: self.start_research(p)).pack(anchor="e")
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
    def start_research(self, project):
        for material, amount in project["cost"].items():
            self.game.player.remove_item(material, amount)
        self.game.perform_action("research")
        messagebox.showinfo("研究开始", f"开始研究{project['name']}！")
    
    def show_social(self):
        win = tk.Toplevel(self.root)
        win.title("社交")
        win.geometry("600x400")
        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        npc_frame = ttk.Frame(notebook)
        notebook.add(npc_frame, text="NPC")
        faction_frame = ttk.Frame(notebook)
        notebook.add(faction_frame, text="阵营")
        self.create_npc_tab(npc_frame)
        self.create_faction_tab(faction_frame)
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
    def create_npc_tab(self, parent):
        current_npcs = self.game.npcs.get_npcs_at_location(self.game.player.location)
        if not current_npcs:
            ttk.Label(parent, text="当前位置没有NPC").pack(pady=20)
            return
        for npc in current_npcs:
            frame = ttk.Frame(parent, relief="solid", padding=10)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=npc["name"], style="Subtitle.TLabel").pack(anchor="w")
            ttk.Label(frame, text=npc["description"]).pack(anchor="w")
            services_text = "服务: " + ", ".join(npc.get("services", []))
            ttk.Label(frame, text=services_text, style="Status.TLabel").pack(anchor="w")
            ttk.Button(frame, text="对话", command=lambda n=npc: self.show_dialogue_window(n, n["dialogue"]["greeting"])).pack(anchor="e")
    
    def create_faction_tab(self, parent):
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
    
    def show_trade_dialog(self):
        npcs = self.game.npcs.get_npcs_at_location(self.game.player.location)
        merchants = [n for n in npcs if 'trade' in n.get('services', [])]
        if not merchants:
            messagebox.showinfo("提示", "当前位置没有可交易的商人")
            return
        merchant = merchants[0]
        shop_id = merchant.get('shop')
        if not shop_id:
            messagebox.showinfo("提示", f"{merchant['name']} 没有商店")
            return
        shop = self.game.npcs.get_shop_inventory(shop_id)
        if not shop:
            return
        win = tk.Toplevel(self.root)
        win.title(f"与 {merchant['name']} 交易")
        win.geometry("600x400")
        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        buy_frame = ttk.Frame(notebook)
        notebook.add(buy_frame, text="购买")
        sell_frame = ttk.Frame(notebook)
        notebook.add(sell_frame, text="出售")
        self.create_buy_tab(buy_frame, shop, shop_id)
        self.create_sell_tab(sell_frame, shop, shop_id)
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
    def create_buy_tab(self, parent, shop, shop_id):
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)
        columns = ("物品", "价格", "库存")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
        for item_id, item_info in shop['items'].items():
            item_data = self.game.items.get_item_data(item_id)
            if item_data:
                tree.insert("", "end", values=(item_data['name'], item_info['price'], item_info['stock']), tags=(item_id,))
        tree.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        def buy_selected():
            selection = tree.selection()
            if selection:
                item_id = tree.item(selection[0])['tags'][0]
                result = self.game.npcs.buy_item(shop_id, item_id, 1)
                if result['success']:
                    messagebox.showinfo("购买成功", result['message'])
                    self.show_trade_dialog()
                else:
                    messagebox.showwarning("购买失败", result['message'])
        ttk.Button(parent, text="购买", command=buy_selected).pack(pady=5)
    
    def create_sell_tab(self, parent, shop, shop_id):
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)
        columns = ("物品", "数量", "估算价格")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
        for item_id, quantity in self.game.player.inventory.items():
            if item_id in shop.get('buys', []):
                item_data = self.game.items.get_item_data(item_id)
                if item_data:
                    price = int(item_data.get('value', 1) * 0.6)
                    tree.insert("", "end", values=(item_data['name'], quantity, price), tags=(item_id,))
        tree.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        def sell_selected():
            selection = tree.selection()
            if selection:
                item_id = tree.item(selection[0])['tags'][0]
                result = self.game.npcs.sell_item(shop_id, item_id, 1)
                if result['success']:
                    messagebox.showinfo("出售成功", result['message'])
                    self.show_trade_dialog()
                else:
                    messagebox.showwarning("出售失败", result['message'])
        ttk.Button(parent, text="出售", command=sell_selected).pack(pady=5)
    
    def show_repair_dialog(self):
        messagebox.showinfo("修理", "修理功能将在后续版本完善")
    
    def show_pause_menu(self):
        if hasattr(self, 'pause_window') and self.pause_window:
            self.pause_window.destroy()
        self.pause_window = tk.Toplevel(self.root)
        self.pause_window.title("游戏暂停")
        self.pause_window.geometry("300x400")
        self.pause_window.transient(self.root)
        self.pause_window.grab_set()
        x = (self.root.winfo_screenwidth() - 300) // 2
        y = (self.root.winfo_screenheight() - 400) // 2
        self.pause_window.geometry(f"+{x}+{y}")
        ttk.Label(self.pause_window, text="游戏暂停", style="Title.TLabel").pack(pady=20)
        options = [
            ("继续游戏", self.game.resume_game),
            ("保存游戏", self.game.save_game),
            ("游戏设置", self.show_settings_dialog),
            ("返回主菜单", self.return_to_main_menu),
            ("退出游戏", self.game.on_closing)
        ]
        for text, command in options:
            ttk.Button(self.pause_window, text=text, command=command, style="Action.TButton", width=20).pack(pady=5)
    
    def hide_pause_menu(self):
        if hasattr(self, 'pause_window') and self.pause_window:
            self.pause_window.destroy()
            self.pause_window = None
    
    def show_settings_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("游戏设置")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        ttk.Label(dialog, text="游戏设置", style="Title.TLabel").pack(pady=10)
        speed_frame = ttk.Frame(dialog)
        speed_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(speed_frame, text="游戏速度:").pack(side="left")
        speed_var = tk.DoubleVar(value=self.game.game_speed)
        speed_scale = ttk.Scale(speed_frame, from_=0.5, to=3.0, variable=speed_var, orient="horizontal", length=200)
        speed_scale.pack(side="left", padx=10)
        speed_label = ttk.Label(speed_frame, text=f"{speed_var.get():.1f}x")
        speed_label.pack(side="left")
        def update_speed_label(*args):
            speed_label.config(text=f"{speed_var.get():.1f}x")
        speed_var.trace('w', update_speed_label)
        def apply_settings():
            self.game.change_game_speed(speed_var.get())
            dialog.destroy()
        ttk.Button(dialog, text="应用", command=apply_settings).pack(pady=10)
        ttk.Button(dialog, text="取消", command=dialog.destroy).pack(pady=5)
    
    def return_to_main_menu(self):
        result = messagebox.askyesno("确认", "确定要返回主菜单吗？未保存的进度将会丢失。")
        if result:
            self.game.return_to_main_menu()
    
    def show_game_over(self, reason, days_survived):
        messagebox.showinfo("游戏结束", f"你死了！\n原因: {reason}\n生存天数: {days_survived}")
        self.create_main_menu()
    
    def show_game_background(self):
        self.show_info_window("游戏背景", self.game.story_book.get_background_story())
    
    def show_codex(self):
        self.show_info_window("图鉴", self.game.story_book.get_codex_content())
    
    def show_story_book(self):
        self.show_info_window("故事书", self.game.story_book.get_all_stories())
    
    def show_gameplay_help(self):
        self.show_info_window("游戏玩法", self.game.story_book.get_gameplay_help())
    
    def show_info_window(self, title, content):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("600x500")
        text_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert(1.0, content)
        text_widget.config(state="disabled")
        ttk.Button(window, text="关闭", command=window.destroy).pack(pady=10)
    
    def show_dialogue_window(self, npc, initial_dialogue):
        win = tk.Toplevel(self.root)
        win.title(f"与 {npc['name']} 对话")
        win.geometry("500x400")
        info_frame = ttk.Frame(win)
        info_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(info_frame, text=npc['name'], style="Subtitle.TLabel").pack(anchor="w")
        ttk.Label(info_frame, text=npc['description'], style="Status.TLabel").pack(anchor="w")
        dialogue_text = scrolledtext.ScrolledText(win, wrap=tk.WORD, height=15)
        dialogue_text.pack(fill="both", expand=True, padx=10, pady=5)
        dialogue_text.insert(1.0, initial_dialogue)
        dialogue_text.config(state="disabled")
        options_frame = ttk.Frame(win)
        options_frame.pack(fill="x", padx=10, pady=10)
        topics = list(npc['dialogue'].get('topics', {}).keys())
        for topic in topics:
            ttk.Button(options_frame, text=topic, command=lambda t=topic: self.show_topic_dialogue(npc, t, dialogue_text)).pack(side="left", padx=5)
        ttk.Button(options_frame, text="再见", command=win.destroy).pack(side="right")
    
    def show_topic_dialogue(self, npc, topic, text_widget):
        dialogue = self.game.npcs.get_dialogue(npc['id'], topic)
        text_widget.config(state="normal")
        text_widget.insert(tk.END, f"\n\n你: 关于{topic}...\n{npc['name']}: {dialogue}")
        text_widget.see(tk.END)
        text_widget.config(state="disabled")
        self.game.npcs.record_interaction(npc['id'])
        self.game.player.gain_skill_exp('social', 5)