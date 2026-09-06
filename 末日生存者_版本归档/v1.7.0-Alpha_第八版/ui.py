# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import logging,os

class GameUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.current_frame = None
        self.log_text = None
        self.status_label = None
        self.quest_info_text = None
        self.status_summary_label = None
        self.quick_items_frame = None
        self.surroundings_frame = None
        self.action_scrollable = None
        self.selected_surrounding = None
        self.selected_item = None
        self.pause_window = None
        
        self.setup_window()
        
    def setup_window(self):
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
    
    def create_scrollable_frame(self, parent, height=None):
        """创建可滚动容器，返回 scrollable_frame"""
        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        def _configure_canvas(event):
            canvas.itemconfig(1, width=event.width)
        canvas.bind("<Configure>", _configure_canvas)
        if height:
            canvas.config(height=height)
        return scrollable
    
    # ---------- 主菜单 ----------
    def create_main_menu(self):
        self.clear_interface()
        scrollable = self.create_scrollable_frame(self.current_frame)
        title_label = ttk.Label(scrollable, text="末日生存者", style="Title.TLabel")
        title_label.pack(pady=30)
        version_label = ttk.Label(scrollable, text=f"版本 {self.game.version}", style="Status.TLabel")
        version_label.pack(pady=5)
        button_frame = ttk.Frame(scrollable)
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
        mod_button = ttk.Button(button_frame, text="模组管理", command=self.show_mod_manager, style="Action.TButton", width=20)
        mod_button.pack(pady=10)
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
        scrollable = self.create_scrollable_frame(slots_frame)
        for i in range(1, 6):
            slot_frame = ttk.Frame(scrollable, relief="solid", padding=10)
            slot_frame.pack(fill="x", pady=5)
            save_file = f"saves/save_slot_{i}.json"
            try:
                import json, os
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
                error_label = ttk.Label(slot_frame, text=f"存档 {i}: 损坏", style="Normal.TLabel")
                error_label.pack(side="left", padx=10)
    
    def delete_save_confirm(self, save_slot):
        result = messagebox.askyesno("确认删除", f"确定要删除存档 {save_slot} 吗？")
        if result:
            import shutil
            save_dir = f"saves/save_slot_{save_slot}"
            try:
                if os.path.exists(save_dir):
                	shutil.rmtree(save_dir)
                	logging.info(f"删除存档目录: {save_dir}")
                else:
                	logging.warning(f"存档目录不存在:{save_dir}")
            except Exception as e:
            	logging.error(f"删除存档目录失败: {e}")
            
            
            save_file = f"saves/save_slot_{save_slot}.json"
            try:
                  if os.path.exists(save_file):
                  	os.remove(save_file)
                  	logging.info(f"成功删除存档文件: {save_file}")
                  else:
                  	logging.warning(f"存档文件不存在: {save_file}")
            
            except Exception as e:
                logging.error(f"删除存档失败: {e}")
                messagebox.showerror("错误", f"删除存档失败: {e}")
            self.show_save_slots()
    
    def show_character_selection(self, save_slot):
        self.clear_interface()
        back_button = ttk.Button(self.current_frame, text="返回存档选择", command=self.show_save_slots)
        back_button.pack(anchor="nw", pady=5)
        title_label = ttk.Label(self.current_frame, text="选择你的角色", style="Title.TLabel")
        title_label.pack(pady=20)
        scrollable = self.create_scrollable_frame(self.current_frame)
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
        name_frame = ttk.Frame(scrollable)
        name_frame.pack(fill="x", padx=50, pady=10)
        ttk.Label(name_frame, text="角色姓名:", style="Normal.TLabel").pack(side="left")
        name_var = tk.StringVar(value="幸存者")
        name_entry = ttk.Entry(name_frame, textvariable=name_var, width=24)
        name_entry.pack(side="left", padx=8)
        def start_with_character(char, slot):
            data = dict(char)
            custom_name = name_var.get().strip()
            data["name"] = custom_name or char["name"]
            self.game.start_new_game(slot, data)
        for char in characters:
            char_frame = ttk.Frame(scrollable, relief="solid", padding=15)
            char_frame.pack(fill="x", padx=50, pady=10)
            name_label = ttk.Label(char_frame, text=char["name"], style="Subtitle.TLabel")
            name_label.pack(anchor="w")
            desc_label = ttk.Label(char_frame, text=char["description"], style="Normal.TLabel")
            desc_label.pack(anchor="w", pady=5)
            stats_text = (f"生命: {char['health']}/{char['max_health']} | 体力: {char['stamina']}/{char['max_stamina']} | "
                          f"力量: {char['strength']} | 敏捷: {char['agility']} | 智力: {char['intelligence']} | 幸运: {char['luck']}")
            stats_label = ttk.Label(char_frame, text=stats_text, style="Status.TLabel")
            stats_label.pack(anchor="w")
            select_button = ttk.Button(char_frame, text="选择角色", command=lambda c=char, s=save_slot: start_with_character(c, s), style="Action.TButton")
            select_button.pack(anchor="e", pady=5)
    
    # ---------- 游戏主界面 ----------
    def create_game_interface(self):
        self.clear_interface()
        # 上层：状态栏
        self.create_status_bar()
        # 中层：左右分区（左侧包含周围事物和日志，右侧操作按钮）
        middle_frame = ttk.Frame(self.current_frame)
        middle_frame.pack(fill="both", expand=True, pady=5)
        # 左侧分区（包含两个滚动区域）
        left_frame = ttk.Frame(middle_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        # 左侧上层：周围可互动事物
        self.create_surroundings_frame(left_frame)
        # 左侧下层：游戏日志（带滚动）
        self.create_log_frame(left_frame)
        # 右侧分区：操作按钮区（动态）
        self.create_action_buttons_frame(middle_frame)
        # 下层：左右分区（状态简览+指令区）
        bottom_frame = ttk.Frame(self.current_frame)
        bottom_frame.pack(fill="x", pady=5)
        self.create_status_summary(bottom_frame)
        self.create_command_area(bottom_frame)
        # 初始更新
        self.update_surroundings()
        self.update_action_buttons()
    
    def create_status_bar(self):
        frame = ttk.Frame(self.current_frame, relief="solid", padding=5)
        frame.pack(fill="x", pady=5)
        self.status_label = ttk.Label(frame, text="初始化中...", style="Normal.TLabel")
        self.status_label.pack(side="left")
        pause_button = ttk.Button(frame, text="暂停", command=self.game.pause_game)
        pause_button.pack(side="right", padx=5)
        save_button = ttk.Button(frame, text="保存", command=self.game.save_game)
        save_button.pack(side="right", padx=5)
    
    def create_surroundings_frame(self, parent):
        label_frame = ttk.LabelFrame(parent, text="周围可互动事物", padding=5)
        label_frame.pack(fill="both", expand=True, pady=5)
        scrollable = self.create_scrollable_frame(label_frame, height=150)
        self.surroundings_frame = scrollable
    
    def update_surroundings(self):
        for widget in self.surroundings_frame.winfo_children():
            widget.destroy()
        loc = self.game.world.get_current_location()
        if loc:
            ttk.Label(self.surroundings_frame, text=f"地点: {loc.name}", style="Status.TLabel").pack(anchor="w")
            if loc.resources:
                res_text = ", ".join([f"{self.game.items.get_item_name(k)}x{v}" for k, v in loc.resources.items()])
                ttk.Label(self.surroundings_frame, text=f"资源: {res_text}", style="Status.TLabel").pack(anchor="w")
        npcs = self.game.npcs.get_npcs_at_location(self.game.player.location)
        for npc in npcs:
            btn = ttk.Button(self.surroundings_frame, text=f"NPC: {npc['name']}",
                             command=lambda n=npc: self.select_surrounding(n))
            btn.pack(fill="x", pady=1)
        if self.game.farming.can_plant(self.game.player.location):
            ttk.Button(self.surroundings_frame, text="农田",
                       command=self.show_farming).pack(fill="x", pady=1)
        elif self.game.farming.is_farmable_location(self.game.player.location):
            ttk.Button(self.surroundings_frame, text="开垦农田",
                       command=lambda: self.game.perform_action("clear_farmland")).pack(fill="x", pady=1)
        connected = self.game.world.get_connected_locations() if loc else []
        for dest in connected:
            if dest.discovered:
                ttk.Button(self.surroundings_frame, text=f"前往: {dest.name}",
                           command=lambda lid=dest.id: self.game.perform_action("move", location_id=lid)).pack(fill="x", pady=1)
    
    def select_surrounding(self, obj):
        self.selected_surrounding = obj
        self.update_action_buttons()
    
    def create_log_frame(self, parent):
        label_frame = ttk.LabelFrame(parent, text="游戏日志", padding=5)
        label_frame.pack(fill="both", expand=True, pady=5)
        self.log_text = scrolledtext.ScrolledText(label_frame, wrap=tk.WORD, font=("Arial", 9))
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state="disabled")
    
    def create_action_buttons_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="操作", padding=5)
        frame.pack(side="right", fill="y", padx=(5,0))
        self.action_buttons_container = ttk.Frame(frame)
        self.action_buttons_container.pack(fill="both", expand=True)
        self.action_canvas = tk.Canvas(self.action_buttons_container, highlightthickness=0)
        self.action_scrollbar = ttk.Scrollbar(self.action_buttons_container, orient="vertical", command=self.action_canvas.yview)
        self.action_scrollable = ttk.Frame(self.action_canvas)
        self.action_scrollable.bind("<Configure>", lambda e: self.action_canvas.configure(scrollregion=self.action_canvas.bbox("all")))
        self.action_canvas.create_window((0,0), window=self.action_scrollable, anchor="nw")
        self.action_canvas.configure(yscrollcommand=self.action_scrollbar.set)
        self.action_canvas.pack(side="left", fill="both", expand=True)
        self.action_scrollbar.pack(side="right", fill="y")
    
    def update_action_buttons(self):
        for widget in self.action_scrollable.winfo_children():
            widget.destroy()
        # 检查是否有选中事物或物品
        if hasattr(self, 'selected_surrounding') and self.selected_surrounding:
            obj = self.selected_surrounding
            ttk.Button(self.action_scrollable, text="对话", command=lambda: self.do_surrounding_action(obj, "对话")).pack(fill="x", pady=2)
            ttk.Button(self.action_scrollable, text="取消选择", command=self.clear_surrounding_selection).pack(fill="x", pady=2)
            if 'services' in obj:
                for service in obj['services']:
                    label = self.get_service_label(service)
                    btn = ttk.Button(self.action_scrollable, text=label, command=lambda s=service: self.do_surrounding_action(obj, s))
                    btn.pack(fill="x", pady=2)
        elif hasattr(self, 'selected_item') and self.selected_item:
            item_id = self.selected_item
            item_data = self.game.items.get_item_data(item_id)
            if item_data:
                btn = ttk.Button(self.action_scrollable, text="使用", command=lambda: self.game.perform_action("use_item", item_id=item_id))
                btn.pack(fill="x", pady=2)
                if item_data.get('type') == 'weapon' or item_data.get('type') == 'armor':
                    btn = ttk.Button(self.action_scrollable, text="装备", command=lambda: self.game.player.equip_item(item_id, item_data.get('equip_slot', 'weapon')))
                    btn.pack(fill="x", pady=2)
        else:
            # 默认全局操作
            actions = [
                ("探索", lambda: self.game.perform_action("explore")),
                ("休息", lambda: self.game.perform_action("rest")),
                ("睡觉", self.show_sleep_dialog),
                ("进食", self.show_eat_dialog),
                ("喝水", self.show_drink_dialog),
                ("钓鱼", lambda: self.game.perform_action("fish")),
                ("狩猎", lambda: self.game.perform_action("hunt")),
                ("砍柴", lambda: self.game.perform_action("chop_wood")),
                ("采药", lambda: self.game.perform_action("gather_herbs")),
                ("冥想", lambda: self.game.perform_action("meditate")),
                ("背包", self.show_inventory),
                ("地图", self.show_map),
                ("任务", self.show_quests),
                ("农业", self.show_farming),
                ("交易", self.show_trade_dialog)
            ]
            for text, cmd in actions:
                btn = ttk.Button(self.action_scrollable, text=text, command=cmd, style="Action.TButton")
                btn.pack(fill="x", pady=2)
    
    def get_service_label(self, service):
        labels = {
            "quests": "任务", "trade": "交易", "healing": "治疗", "farming_tips": "农耕建议",
            "medical_supplies": "医疗物资", "security_tips": "防卫建议", "weapon_training": "武器训练",
            "crafting": "制作", "repair": "修理", "map_info": "地图情报", "location_tips": "地点提示",
            "information": "打听消息", "weapon_info": "武器情报", "research": "研究",
            "tech_items": "科技物品", "radiation_treatment": "辐射治疗", "special_quests": "特殊任务",
            "training": "训练", "survival_tips": "生存技巧", "meditation": "冥想指导"
        }
        return labels.get(service, service)

    def clear_surrounding_selection(self):
        self.selected_surrounding = None
        self.selected_item = None
        self.update_action_buttons()

    def do_surrounding_action(self, obj, service):
        npc_id = obj.get('id')
        if service in ("对话", "dialogue"):
            greeting = obj.get('dialogue', {}).get('greeting', "......")
            self.show_dialogue_window(obj, greeting)
            self.game.npcs.record_interaction(npc_id)
            self.game.quests.update_quest_progress('npc_talked', npc_id=npc_id)
            self.game.quests.update_quest_progress('npc_met', npc_id=npc_id)
        elif service in ("交易", "trade", "medical_supplies", "tech_items"):
            self.show_npc_trade(obj)
        elif service in ("任务", "quests", "special_quests"):
            self.offer_npc_quests(obj)
        elif service in ("healing", "radiation_treatment"):
            self.handle_npc_healing(obj, service)
        elif service in ("farming_tips", "security_tips", "weapon_training", "map_info",
                         "location_tips", "information", "weapon_info", "survival_tips", "training"):
            self.show_npc_tip(obj, service)
        elif service in ("crafting",):
            self.show_crafting()
        elif service in ("repair",):
            self.show_repair_dialog()
        elif service in ("research",):
            self.game.perform_action("research")
        elif service in ("meditation",):
            self.game.perform_action("meditate")
        else:
            self.game.add_game_log(f"与{obj['name']}进行{self.get_service_label(service)}...")
        self.game.npcs.record_interaction(npc_id)

    def show_npc_trade(self, npc):
        shop_id = npc.get('shop')
        if not shop_id:
            messagebox.showinfo("提示", f"{npc['name']} 没有商店")
            return
        shop = self.game.npcs.get_shop_inventory(shop_id)
        if not shop:
            messagebox.showinfo("提示", f"{npc['name']} 的商店暂时无法营业")
            return
        win = tk.Toplevel(self.root)
        win.title(f"与 {npc['name']} 交易")
        win.geometry("600x400")
        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        buy_frame = ttk.Frame(notebook)
        notebook.add(buy_frame, text="购买")
        sell_frame = ttk.Frame(notebook)
        notebook.add(sell_frame, text="出售")
        self.create_buy_tab(buy_frame, shop, shop_id)
        self.create_sell_tab(sell_frame, shop, shop_id)
        ttk.Label(win, text=f"金钱: {self.game.player.money}").pack()
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)

    def offer_npc_quests(self, npc):
        quest_ids = npc.get('quests', [])
        available = []
        for qid in quest_ids:
            quest = self.game.quests.quests.get(qid)
            if not quest:
                continue
            if qid in self.game.quests.active_quests:
                continue
            if qid in self.game.quests.completed_quests and not quest.get('repeatable'):
                continue
            available.append(quest)
        if not available:
            self.show_quests()
            return
        win = tk.Toplevel(self.root)
        win.title(f"{npc['name']} 的任务")
        win.geometry("500x360")
        for quest in available:
            frame = ttk.Frame(win, relief="solid", padding=8)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=quest['name'], style="Subtitle.TLabel").pack(anchor="w")
            ttk.Label(frame, text=quest.get('description', ''), wraplength=440).pack(anchor="w")
            ttk.Button(frame, text="接受", command=lambda qid=quest['id']: self.accept_npc_quest(qid, win)).pack(anchor="e")
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=8)

    def accept_npc_quest(self, quest_id, win):
        result = self.game.quests.start_quest(quest_id)
        messagebox.showinfo("任务", result.get('message', ''))
        win.destroy()

    def handle_npc_healing(self, npc, service):
        cost = 20 if service == "healing" else 35
        if not self.game.player.spend_money(cost):
            messagebox.showwarning("治疗", f"金钱不足，需要{cost}")
            return
        if service == "healing":
            self.game.player.modify_health(40)
            self.game.add_game_log(f"{npc['name']}为你进行了治疗，花费{cost}。")
        else:
            self.game.player.radiation = max(0, self.game.player.radiation - 25)
            self.game.radiation_level = max(0, self.game.radiation_level - 10)
            self.game.add_game_log(f"{npc['name']}帮你降低了辐射，花费{cost}。")

    def show_npc_tip(self, npc, service):
        topics = npc.get('dialogue', {}).get('topics', {})
        topic_map = {
            "farming_tips": "farming", "security_tips": "security", "weapon_training": "weapons",
            "map_info": "maps", "location_tips": "locations", "information": "rumors",
            "weapon_info": "weapons", "survival_tips": "survival", "training": "survival"
        }
        topic = topic_map.get(service)
        text = topics.get(topic) if topic else None
        if not text:
            text = topics.get(next(iter(topics), ''), npc.get('dialogue', {}).get('greeting', '......'))
        self.show_dialogue_window(npc, text)
        self.game.player.gain_skill_exp('social', 3)
    
    def create_status_summary(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(side="left", fill="both", expand=True)
        self.status_summary_label = ttk.Label(frame, text="生命: 100/100  体力: 100/100", style="Normal.TLabel")
        self.status_summary_label.pack(anchor="w")
        status_button = ttk.Button(frame, text="状态详情", command=self.show_full_status)
        status_button.pack(anchor="w", pady=2)
        # 任务信息
        self.quest_info_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=5, font=("Arial", 8))
        self.quest_info_text.pack(fill="both", expand=True)
        self.quest_info_text.config(state="disabled")
    
    def create_command_area(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(side="right", fill="both", expand=True)
        # 快捷物品栏
        item_frame = ttk.LabelFrame(frame, text="快捷物品栏", padding=5)
        item_frame.pack(fill="x", pady=5)
        self.quick_items_frame = ttk.Frame(item_frame)
        self.quick_items_frame.pack(fill="x")
        # 指令输入框
        cmd_frame = ttk.Frame(frame)
        cmd_frame.pack(fill="x", pady=5)
        ttk.Label(cmd_frame, text="指令:").pack(side="left")
        self.cmd_entry = ttk.Entry(cmd_frame)
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.cmd_entry.bind("<Return>", self.execute_command)
        # 功能按钮组
        func_frame = ttk.Frame(frame)
        func_frame.pack(fill="x", pady=5)
        for text, cmd in [("背包", self.show_inventory), ("研究", self.show_research), ("制造", self.show_crafting), ("地图", self.show_map), ("医疗", self.show_medical), ("建造", self.show_construction)]:
            btn = ttk.Button(func_frame, text=text, command=cmd)
            btn.pack(side="left", padx=2)
    
    def update_quick_items(self):
        for widget in self.quick_items_frame.winfo_children():
            widget.destroy()
        items = list(self.game.player.inventory.items())[:5]
        for item_id, qty in items:
            item_data = self.game.items.get_item_data(item_id)
            name = item_data['name'] if item_data else item_id
            btn = ttk.Button(self.quick_items_frame, text=f"{name}({qty})",
                             command=lambda iid=item_id: self.select_item(iid))
            btn.pack(side="left", padx=2)
    
    def select_item(self, item_id):
        self.selected_item = item_id
        self.update_action_buttons()
    
    def execute_command(self, event=None):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        self.cmd_entry.delete(0, tk.END)
        self.game.execute_command(cmd)
    
    def update_status_display(self):
        if not self.game.player.initialized:
            return
        p = self.game.player
        time_name = self.game.get_time_of_day_name() if hasattr(self.game, 'get_time_of_day_name') else ""
        weight = p.get_inventory_weight()
        max_weight = p.get_max_carry_weight()
        overload = " 超重" if p.is_overencumbered() else ""
        status_text = (f"{p.name} | 生命: {p.health}/{p.max_health} | 体力: {p.stamina}/{p.max_stamina} | "
                       f"精神: {p.mental}/{p.max_mental} | 疲劳: {p.fatigue}/{self.game.max_fatigue} | "
                       f"辐射: {self.game.radiation_level}% | 第{self.game.day_count}天 {self.game.format_time()} {time_name} | "
                       f"{self.game.get_weather_name()} | {self.game.get_season_name()} | 负重 {weight}/{max_weight}{overload}")
        self.status_label.config(text=status_text)
        self.status_summary_label.config(text=f"生命{p.health}/{p.max_health}  体力{p.stamina}/{p.max_stamina}  精神{p.mental}/{p.max_mental}  金钱{p.money}  负重{weight}/{max_weight}")
        self.update_quest_display()
        self.update_quick_items()
        self.update_surroundings()
    
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
        self.quest_info_text.config(state="normal")
        self.quest_info_text.delete(1.0, tk.END)
        self.quest_info_text.insert(1.0, quest_text)
        self.quest_info_text.config(state="disabled")
    
    def add_log_message(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        lines = self.log_text.get(1.0, tk.END).split('\n')
        if len(lines) > 100:
            self.log_text.delete(1.0, f"{len(lines)-100}.0")
    
    # ---------- 对话框和子窗口 ----------
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
            item_frame = ttk.Frame(scrollable_frame, relief="solid", padding=8)
            item_frame.pack(fill="x", pady=2, padx=5)
            info_text = f"{item_data['name']} x{quantity}\n{item_data['description']}"
            if item_data.get('health_restore', 0) > 0:
                info_text += f"\n恢复生命: {item_data['health_restore']}"
            if item_data.get('stamina_restore', 0) > 0:
                info_text += f" | 恢复体力: {item_data['stamina_restore']}"
            ttk.Label(item_frame, text=info_text, style="Normal.TLabel").pack(side="left", anchor="w")
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
        columns = ("名称", "数量", "重量", "类型", "描述")
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
        weight = self.game.player.get_inventory_weight()
        max_weight = self.game.player.get_max_carry_weight()
        extra = "（超重，行动更耗体力）" if self.game.player.is_overencumbered() else ""
        ttk.Label(parent, text=f"负重: {weight}/{max_weight}{extra}").pack(anchor="w", padx=8, pady=4)
        self.refresh_inventory()
    
    def refresh_inventory(self):
        if hasattr(self, 'inventory_tree'):
            for item in self.inventory_tree.get_children():
                self.inventory_tree.delete(item)
            for item_id, quantity in self.game.player.inventory.items():
                if quantity > 0:
                    item_data = self.game.items.get_item_data(item_id)
                    if item_data:
                        item_weight = float(item_data.get('weight', 0.5) or 0.5) * quantity
                        self.inventory_tree.insert("", "end", values=(
                            item_data['name'], quantity, f"{item_weight:.1f}", item_data.get('type', '未知'), item_data.get('description', '')
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
                "forest": "#2d6a4f", "plain": "#a7c5a3", "mountain": "#8d6b63", "river": "#4ea8de",
                "urban": "#4a6e8c"
            }.get(loc.terrain, "#cccccc")
            size = 12
            canvas.create_oval(loc.x-size, loc.y-size, loc.x+size, loc.y+size, fill=terrain_color, outline="white", width=1, tags=loc.id)
            label = loc.name
            if loc.id in self.game.farming.farmlands:
                label = f"{loc.name} [耕地]"
                canvas.create_rectangle(loc.x-6, loc.y+10, loc.x+6, loc.y+16, fill="#c4a35a", outline="", tags=loc.id)
            canvas.create_text(loc.x, loc.y-12, text=label, fill="white", font=("Arial", 9), tags=loc.id)
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
                self.show_craft_tier_dialog(recipe)
        ttk.Button(parent, text="制作", command=craft_selected).pack(pady=5)
    
    def show_craft_tier_dialog(self, recipe):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"制作 - {recipe['name']}")
        dialog.geometry("400x300")
        ttk.Label(dialog, text=f"选择制作挡级：", style="Subtitle.TLabel").pack(pady=10)
        tier_var = tk.IntVar(value=2)
        tiers = [
            (1, "一挡：消耗最少材料，产出低品质物品"),
            (2, "二挡：标准配方，产出标准品质"),
            (3, "三挡：消耗更多材料，产出高品质物品")
        ]
        for tier, desc in tiers:
            ttk.Radiobutton(dialog, text=desc, variable=tier_var, value=tier).pack(anchor="w", padx=20, pady=5)
        def confirm():
            self.game.perform_action("craft", recipe_id=recipe['id'], tier=tier_var.get())
            dialog.destroy()
        ttk.Button(dialog, text="制作", command=confirm).pack(pady=10)
        ttk.Button(dialog, text="取消", command=dialog.destroy).pack()
    
    def show_farming(self):
        win = tk.Toplevel(self.root)
        win.title("农业")
        win.geometry("600x500")
        current_loc = self.game.player.location
        if not self.game.farming.can_plant(current_loc):
            if self.game.farming.is_farmable_location(current_loc):
                ttk.Label(win, text="这里可以开垦农田，需要木锄或铁锄以及3个木材。").pack(pady=20)
                ttk.Button(win, text="开垦耕地", command=lambda: [self.game.perform_action("clear_farmland"), win.destroy()]).pack(pady=6)
            else:
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
        ttk.Button(parent, text="全部浇水", command=lambda: self.game.perform_action("water_crops")).pack(pady=4)
        ttk.Button(parent, text="施肥", command=lambda: self.game.perform_action("fertilize")).pack(pady=4)
        ttk.Button(parent, text="扩展农田", command=lambda: self.game.perform_action("expand_farmland")).pack(pady=4)
        for plot in status.get('plots_details', []):
            frame = ttk.Frame(parent, relief="solid", padding=6)
            frame.pack(fill="x", padx=8, pady=4)
            if plot.get('crop_type'):
                ttk.Label(frame, text=f"地块 {plot['id']}: {plot.get('crop_name', '未知')} | {plot.get('growth_description', '未知')}").pack(anchor="w")
                ttk.Label(frame, text=f"健康: {int(plot.get('health', 0))}% | 水分: {int(plot.get('water_level', 0))}% | 害虫: {int(plot.get('pest_infestation', 0))}% | 杂草: {int(plot.get('weeds', 0))}%").pack(anchor="w")
                btn_frame = ttk.Frame(frame)
                btn_frame.pack(anchor="e")
                ttk.Button(btn_frame, text="浇水", command=lambda pid=plot['id']: self.game.perform_action("water_crops", plot_id=pid)).pack(side="left", padx=2)
                ttk.Button(btn_frame, text="除草", command=lambda pid=plot['id']: self.game.perform_action("remove_weeds", plot_id=pid)).pack(side="left", padx=2)
                if plot.get('is_mature'):
                    ttk.Button(btn_frame, text="收获", command=lambda pid=plot['id']: self.game.perform_action("harvest", plot_id=pid)).pack(side="left", padx=2)
            else:
                ttk.Label(frame, text=f"地块 {plot['id']}: 空闲").pack(anchor="w")
    
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
        ttk.Label(status_frame, text=f"疲劳值: {player.fatigue}/{self.game.max_fatigue}").pack(anchor="w")
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
        win.geometry("600x420")
        location = self.game.world.get_current_location()
        built = set(getattr(location, 'structures', []) or []) if location else set()
        loc_name = location.name if location else "未知地点"
        ttk.Label(win, text=f"当前地点: {loc_name}", style="Subtitle.TLabel").pack(anchor="w", padx=10, pady=(8, 4))
        for structure in self.game.get_buildable_structures():
            frame = ttk.Frame(win, relief="solid", padding=10)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=structure["name"], style="Subtitle.TLabel").pack(anchor="w")
            ttk.Label(frame, text=structure["description"]).pack(anchor="w")
            materials_text = "需要: " + ", ".join([f"{self.game.items.get_item_name(mat)}x{amt}" for mat, amt in structure["materials"].items()])
            ttk.Label(frame, text=materials_text, style="Status.TLabel").pack(anchor="w")
            already = structure["id"] in built
            can_build = (not already) and all(self.game.player.has_item(mat, amt) for mat, amt in structure["materials"].items())
            if already:
                button_text, button_state = "已建成", "disabled"
            elif can_build:
                button_text, button_state = "建造", "normal"
            else:
                button_text, button_state = "材料不足", "disabled"
            ttk.Button(frame, text=button_text, state=button_state, command=lambda s=structure, w=win: self.build_structure(s, w)).pack(anchor="e")
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
    def build_structure(self, structure, win=None):
        result = self.game.action_build(structure["id"])
        if result.get('success'):
            messagebox.showinfo("建造完成", result['message'])
            if win:
                win.destroy()
                self.show_construction()
        else:
            messagebox.showwarning("建造失败", result.get('message', '无法建造'))
    
    def show_research(self):
        win = tk.Toplevel(self.root)
        win.title("研究")
        win.geometry("520x420")
        done = set(getattr(self.game, 'completed_research', []) or [])
        for project in self.game.get_research_projects():
            frame = ttk.Frame(win, relief="solid", padding=10)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=project["name"], style="Subtitle.TLabel").pack(anchor="w")
            ttk.Label(frame, text=project["description"]).pack(anchor="w")
            cost_text = "需要: " + ", ".join([f"{self.game.items.get_item_name(mat)}x{amt}" for mat, amt in project["cost"].items()])
            ttk.Label(frame, text=cost_text, style="Status.TLabel").pack(anchor="w")
            already = project["id"] in done
            can_research = (not already) and all(self.game.player.has_item(mat, amt) for mat, amt in project["cost"].items())
            if already:
                button_text, button_state = "已完成", "disabled"
            elif can_research:
                button_text, button_state = "研究", "normal"
            else:
                button_text, button_state = "资料不足", "disabled"
            ttk.Button(frame, text=button_text, state=button_state, command=lambda p=project, w=win: self.start_research(p, w)).pack(anchor="e")
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
    def start_research(self, project, win=None):
        result = self.game.action_research(project["id"])
        if result.get('success'):
            messagebox.showinfo("研究完成", result['message'])
            if win:
                win.destroy()
                self.show_research()
        else:
            messagebox.showwarning("研究失败", result.get('message', '无法研究'))
    
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
        merchants = [n for n in npcs if n.get('shop') or 'trade' in n.get('services', []) or 'medical_supplies' in n.get('services', [])]
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
        win = tk.Toplevel(self.root)
        win.title("修理")
        win.geometry("520x420")
        ttk.Label(win, text="可修理物品", style="Subtitle.TLabel").pack(anchor="w", padx=10, pady=(8, 4))
        candidates = []
        seen = set()
        for item_id in list(self.game.player.inventory.keys()) + list(self.game.player.equipment.values()):
            if not item_id or item_id in seen:
                continue
            seen.add(item_id)
            max_d = self.game.player.get_item_max_durability(item_id)
            if not max_d:
                continue
            current = self.game.player.get_item_durability(item_id)
            candidates.append((item_id, current, max_d))
        if not candidates:
            ttk.Label(win, text="没有可修理的装备或工具").pack(pady=20)
            ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
            return
        for item_id, current, max_d in candidates:
            frame = ttk.Frame(win, relief="solid", padding=8)
            frame.pack(fill="x", padx=10, pady=4)
            name = self.game.items.get_item_name(item_id)
            ttk.Label(frame, text=f"{name}  耐久 {current}/{max_d}").pack(anchor="w")
            cost = self.game.player.get_repair_cost(item_id)
            if current >= max_d:
                ttk.Label(frame, text="完好，无需修理", style="Status.TLabel").pack(anchor="w")
                continue
            cost_text = f"需要: 金属x{cost['metal']}、材料x{cost['materials']}"
            ttk.Label(frame, text=cost_text, style="Status.TLabel").pack(anchor="w")
            can_repair = self.game.player.has_item('metal', cost['metal']) and self.game.player.has_item('materials', cost['materials'])
            button_text = "修理" if can_repair else "材料不足"
            button_state = "normal" if can_repair else "disabled"
            ttk.Button(frame, text=button_text, state=button_state, command=lambda iid=item_id, w=win: self.do_repair(iid, w)).pack(anchor="e")
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)

    def do_repair(self, item_id, win):
        result = self.game.player.repair_item(item_id)
        if result.get('success'):
            self.game.advance_time(2)
            messagebox.showinfo("修理完成", result['message'])
            win.destroy()
            self.show_repair_dialog()
        else:
            messagebox.showwarning("修理失败", result.get('message', '无法修理'))
    
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
        speed_var = tk.DoubleVar(master=dialog,value=self.game.game_speed)
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
        self.show_info_window("游戏背景", self.game.story_reader.get_background_story() if hasattr(self.game.story_reader, 'get_background_story') else "暂无背景故事")
    
    def show_codex(self):
        self.show_info_window("图鉴", self.game.story_reader.get_codex_content() if hasattr(self.game.story_reader, 'get_codex_content') else "暂无图鉴")
    
    def show_story_book(self):
        """显示故事列表，点击标题后显示具体内容"""
        stories = self.game.story_reader.get_unlocked_stories()
        logging.info(f"故事书: 找到 {len(stories)} 个故事")
        if not stories:
        	messagebox.showinfo("提示", "暂无解锁的故事")
        	return
        
        win = tk.Toplevel(self.root)
        win.title("故事书")
        win.geometry("500x400")
        win.transient(self.root)
        win.grab_set()
        
        # 创建故事列表（可滚动）
        canvas = tk.Canvas(win, highlightthickness=0)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 每个故事一个按钮
        for story in stories:
        	title = story.get('title', '未知故事')
        	# 使用带下划线的样式模拟链接
        	btn = ttk.Button(scrollable_frame, text=title, style="Action.TButton",command=lambda s=story: self._show_story_content(s))
        	btn.pack(fill="x", padx=10, pady=2)
        	
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
    def _show_story_content(self, story):
    	"""显示单个故事内容"""
    	content_win = tk.Toplevel(self.root)
    	content_win.title(story.get('title', '故事内容'))
    	content_win.geometry("600x500")
    	content_win.transient(self.root)
    	content_win.grab_set()
    	
    	text = scrolledtext.ScrolledText(content_win, wrap=tk.WORD, font=("Arial", 10))
    	text.pack(fill="both", expand=True, padx=10, pady=10)
    	text.insert(1.0, story.get('content', '无内容'))
    	text.config(state="disabled")
    	
    	ttk.Button(content_win, text="关闭", command=content_win.destroy).pack(pady=10)


    def show_gameplay_help(self):
        help_text = """《末日生存者》游戏玩法

基本目标：
- 在这个末日世界中尽可能长时间地生存下去
- 探索世界，收集资源，制作物品
- 避免危险，保持健康和体力

游戏机制：
- 时间系统：游戏内时间会流逝，影响资源消耗和事件发生
- 生存需求：每天需要消耗食物和水，否则会损失生命值
- 体力系统：行动会消耗体力，休息可以恢复
- 战斗系统：遇到敌人时会弹出选择（战斗/逃跑）
- 精神系统：保持精神状态良好，避免精神崩溃
- 疲劳系统：长时间活动会累积疲劳，影响属性
- 天气系统：不同天气影响行动效率和资源获取

操作指南：
主界面右侧有快捷操作按钮，下方有指令输入框，可输入：
- help：显示帮助
- status：显示状态
- inventory：显示背包
- map：显示地图
- quit：退出

生存技巧：
1. 合理分配资源，确保每天有足够的食物和水
2. 探索新区域时要小心，危险程度各不相同
3. 制作物品可以提高生存效率
4. 遇到强敌时，考虑暂时逃跑
5. 保持精神状态，避免长时间不睡觉
6. 注意疲劳值，过度疲劳会影响战斗和行动
7. 关注天气变化，恶劣天气时减少外出
8. 与NPC建立良好关系，获取更多帮助

祝你好运，幸存者！
        
        """
        
        self.show_info_window("游戏玩法",help_text)
    
    def show_mod_manager(self):
        # 简单的MOD管理界面
        win = tk.Toplevel(self.root)
        win.title("模组管理")
        win.geometry("500x400")
        ttk.Label(win, text="全局模组列表", style="Subtitle.TLabel").pack(pady=10)
        mods_frame = ttk.Frame(win)
        mods_frame.pack(fill="both", expand=True, padx=10, pady=10)
        # 扫描 global mods
        import os
        mods_dir = "mods/global"
        if os.path.exists(mods_dir):
            for mod_id in os.listdir(mods_dir):
                mod_path = os.path.join(mods_dir, mod_id)
                if os.path.isdir(mod_path):
                    frame = ttk.Frame(mods_frame, relief="solid", padding=5)
                    frame.pack(fill="x", pady=2)
                    info = {}
                    info_file = os.path.join(mod_path, "mod_info.json")
                    if os.path.exists(info_file):
                        try:
                            import json
                            with open(info_file, 'r', encoding='utf-8') as f:
                                info = json.load(f)
                        except:
                            pass
                    mod_name = info.get('name', mod_id)
                    enabled = self.game.mod_manager.enabled_global_mods.get(mod_id, False)
                    var = tk.BooleanVar(value=enabled)
                    def toggle(mod_id=mod_id):
                        self.game.mod_manager.enabled_global_mods[mod_id] = var.get()
                        # 保存配置
                        with open(os.path.join(mods_dir, "enabled.json"), 'w') as f:
                            json.dump(self.game.mod_manager.enabled_global_mods, f)
                    chk = ttk.Checkbutton(frame, text=mod_name, variable=var, command=toggle)
                    chk.pack(side="left")
                    ttk.Label(frame, text=info.get('description', '')).pack(side="left", padx=10)
        ttk.Label(win, text="提示：启用/禁用模组后需要重启游戏才能生效。", style="Status.TLabel").pack(pady=10)
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)
    
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
    
    def show_full_status(self):
        win = tk.Toplevel(self.root)
        win.title("详细状态")
        win.geometry("500x600")
        p = self.game.player
        text = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Arial", 9))
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert(tk.END, f"角色: {p.name}\n")
        text.insert(tk.END, f"生命: {p.health}/{p.max_health}\n")
        text.insert(tk.END, f"体力: {p.stamina}/{p.max_stamina}\n")
        text.insert(tk.END, f"精神: {p.mental}/{p.max_mental}\n")
        text.insert(tk.END, f"疲劳: {p.fatigue}/{self.game.max_fatigue}\n")
        text.insert(tk.END, f"辐射: {self.game.radiation_level}%\n")
        text.insert(tk.END, f"力量: {p.strength}  敏捷: {p.agility}  智力: {p.intelligence}  耐力: {p.endurance}  幸运: {p.luck}\n")
        text.insert(tk.END, "\n技能:\n")
        for skill, level in p.skills.items():
            text.insert(tk.END, f"  {skill}: {level} (经验: {p.skill_exp.get(skill,0)})\n")
        text.insert(tk.END, "\n装备:\n")
        for slot, item_id in p.equipment.items():
            if item_id:
                item_data = self.game.items.get_item_data(item_id)
                text.insert(tk.END, f"  {slot}: {item_data['name'] if item_data else item_id}\n")
        text.insert(tk.END, "\n当前效果:\n")
        for buff in p.buffs:
            text.insert(tk.END, f"  + {buff['name']} (剩余{buff['duration']}小时)\n")
        for debuff in p.debuffs:
            text.insert(tk.END, f"  - {debuff['name']} (剩余{debuff['duration']}小时)\n")
        text.config(state="disabled")
        ttk.Button(win, text="关闭", command=win.destroy).pack(pady=10)