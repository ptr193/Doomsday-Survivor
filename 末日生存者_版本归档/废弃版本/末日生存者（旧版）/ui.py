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
        messagebox.showinfo("功能开发中", "进食功能开发中")
    
    def show_drink_dialog(self):
        """显示喝水对话框"""
        # 实现饮水选择逻辑
        messagebox.showinfo("功能开发中", "喝水功能开发中")
    
    def show_inventory(self):
        """显示背包"""
        messagebox.showinfo("功能开发中", "背包功能开发中")
    
    def show_map(self):
        """显示地图"""
        messagebox.showinfo("功能开发中", "地图功能开发中")
    
    def show_crafting(self):
        """显示制作界面"""
        messagebox.showinfo("功能开发中", "制作功能开发中")
    
    def show_farming(self):
        """显示农业界面"""
        messagebox.showinfo("功能开发中", "农业功能开发中")
    
    def show_quests(self):
        """显示任务界面"""
        messagebox.showinfo("功能开发中", "任务功能开发中")
    
    def show_medical(self):
        """显示医疗界面"""
        messagebox.showinfo("功能开发中", "医疗功能开发中")
    
    def show_construction(self):
        """显示建造界面"""
        messagebox.showinfo("功能开发中", "建造功能开发中")
    
    def show_research(self):
        """显示研究界面"""
        messagebox.showinfo("功能开发中", "研究功能开发中")
    
    def show_social(self):
        """显示社交界面"""
        messagebox.showinfo("功能开发中", "社交功能开发中")
    
    def show_pause_menu(self):
        """显示暂停菜单"""
        # 实现暂停菜单逻辑
        pass
    
    def hide_pause_menu(self):
        """隐藏暂停菜单"""
        # 实现隐藏暂停菜单逻辑
        pass
    
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