# -*- coding: utf-8 -*-

import random
import logging
import tkinter as tk
from tkinter import ttk, messagebox

class CombatSystem:
    def __init__(self, game):
        self.game = game
        self.enemy_types = {}
        self.combat_log = []
        self.initialized = False

    def initialize(self):
        try:
            self.create_enemy_types()
            self.initialized = True
            logging.info("战斗系统初始化完成")
        except Exception as e:
            logging.error(f"战斗系统初始化失败: {e}")
            raise

    def create_enemy_types(self):
        # 从MOD管理器加载，如果没有则使用硬编码
        enemies_data = self.game.mod_manager.get_data('enemies', None)
        if enemies_data:
            self.enemy_types = enemies_data
            logging.info(f"从MOD加载了 {len(self.enemy_types)} 种敌人")
        else:
            self.enemy_types = {
                'mutant_rat': {'id': 'mutant_rat', 'name': '变异鼠', 'level': 1, 'health': 20, 'max_health': 20, 'attack': 5, 'defense': 2, 'speed': 8, 'exp_reward': 10, 'loot_chance': 70, 'loot_table': {'food': (1, 1, 50), 'materials': (1, 2, 30)}, 'abilities': ['quick_bite'], 'description': '受到辐射变异的老鼠，攻击性很强'},
                'radroach': {'id': 'radroach', 'name': '辐射蟑螂', 'level': 1, 'health': 15, 'max_health': 15, 'attack': 4, 'defense': 3, 'speed': 6, 'exp_reward': 8, 'loot_chance': 60, 'loot_table': {'materials': (1, 3, 40), 'medicine': (1, 1, 20)}, 'abilities': ['dodge'], 'description': '巨大的变异蟑螂，外壳坚硬'},
                'mutant_wolf': {'id': 'mutant_wolf', 'name': '变异狼', 'level': 2, 'health': 30, 'max_health': 30, 'attack': 8, 'defense': 3, 'speed': 7, 'exp_reward': 20, 'loot_chance': 75, 'loot_table': {'food': (1, 2, 60), 'materials': (1, 2, 40), 'cloth': (1, 1, 25)}, 'abilities': ['pounce', 'howl'], 'description': '凶猛的变异狼，擅长群体作战'},
                'zombie': {'id': 'zombie', 'name': '僵尸', 'level': 2, 'health': 40, 'max_health': 40, 'attack': 6, 'defense': 5, 'speed': 3, 'exp_reward': 18, 'loot_chance': 65, 'loot_table': {'cloth': (1, 3, 45), 'materials': (1, 2, 35), 'medicine': (1, 1, 15)}, 'abilities': ['grapple', 'infectious_bite'], 'description': '行动缓慢但生命力顽强的僵尸'},
                'giant_spider': {'id': 'giant_spider', 'name': '巨型蜘蛛', 'level': 3, 'health': 35, 'max_health': 35, 'attack': 12, 'defense': 2, 'speed': 9, 'exp_reward': 25, 'loot_chance': 70, 'loot_table': {'medicine': (1, 2, 50), 'rare_herbs': (1, 1, 30), 'materials': (1, 3, 40)}, 'abilities': ['web_shot', 'poison_bite'], 'description': '毒性强烈的巨型蜘蛛，行动敏捷'},
                'mutant_bear': {'id': 'mutant_bear', 'name': '变异熊', 'level': 4, 'health': 60, 'max_health': 60, 'attack': 15, 'defense': 8, 'speed': 5, 'exp_reward': 40, 'loot_chance': 85, 'loot_table': {'food': (2, 3, 70), 'materials': (2, 4, 60), 'rare_herbs': (1, 2, 35)}, 'abilities': ['ferocious_charge', 'roar'], 'description': '巨大的变异熊，力量惊人'},
                'raider_elite': {'id': 'raider_elite', 'name': '掠夺者精英', 'level': 4, 'health': 50, 'max_health': 50, 'attack': 12, 'defense': 6, 'speed': 6, 'exp_reward': 35, 'loot_chance': 80, 'loot_table': {'electronic': (1, 2, 45), 'materials': (2, 5, 65), 'medicine': (1, 2, 40), 'pistol': (1, 1, 15)}, 'abilities': ['tactical_strike', 'grenade_throw'], 'description': '经验丰富的掠夺者战士，装备精良'},
                'radscorpion': {'id': 'radscorpion', 'name': '辐射蝎子', 'level': 5, 'health': 55, 'max_health': 55, 'attack': 18, 'defense': 7, 'speed': 4, 'exp_reward': 45, 'loot_chance': 80, 'loot_table': {'rare_minerals': (1, 2, 40), 'antidote': (1, 2, 50), 'materials': (3, 5, 70)}, 'abilities': ['tail_sting', 'burrow'], 'description': '致命的辐射蝎子，尾刺含有剧毒'},
                'mutant_behemoth': {'id': 'mutant_behemoth', 'name': '变异巨兽', 'level': 8, 'health': 150, 'max_health': 150, 'attack': 25, 'defense': 15, 'speed': 3, 'exp_reward': 100, 'loot_chance': 95, 'loot_table': {'advanced_alloy': (2, 3, 80), 'rare_minerals': (3, 5, 75), 'ancient_artifact': (1, 1, 50), 'military_ration': (3, 5, 90)}, 'abilities': ['earth_shatter', 'furious_swipe', 'regenerate'], 'description': '传说中的变异巨兽，拥有毁灭性的力量'},
                'raider_commander': {'id': 'raider_commander', 'name': '掠夺者指挥官', 'level': 7, 'health': 120, 'max_health': 120, 'attack': 20, 'defense': 12, 'speed': 6, 'exp_reward': 80, 'loot_chance': 90, 'loot_table': {'assault_rifle': (1, 1, 60), 'tactical_vest': (1, 1, 70), 'advanced_alloy': (1, 2, 65), 'electronic': (3, 5, 85)}, 'abilities': ['command_aura', 'precision_shot', 'tactical_retreat'], 'description': '掠夺者组织的首领，战术大师'},
                'ghost_soldier': {'id': 'ghost_soldier', 'name': '幽灵士兵', 'level': 6, 'health': 80, 'max_health': 80, 'attack': 16, 'defense': 10, 'speed': 7, 'exp_reward': 60, 'loot_chance': 70, 'loot_table': {'research_data': (1, 2, 55), 'map_fragment': (1, 3, 65), 'advanced_alloy': (1, 1, 40)}, 'abilities': ['phase_shift', 'energy_blast', 'teleport'], 'description': '神秘的幽灵般存在，似乎来自另一个维度'}
            }
            logging.info(f"创建了 {len(self.enemy_types)} 种硬编码敌人")

    def load_data(self, save_data):
        self.initialized = True
        logging.info("战斗系统数据加载完成")

    def get_save_data(self):
        return {}

    def start_combat(self, player, enemy_data):
        """开始战斗，增加逃跑选择"""
        self.combat_log.clear()
        # 判断是否为特殊BOSS
        is_special_boss = enemy_data.get('id') in ['mutant_behemoth', 'raider_commander']
        if is_special_boss:
            return self.start_card_battle(player, enemy_data)

        enemy = self.create_enemy(enemy_data)
        enemy_name = enemy['name']
        # 弹出选择窗口（使用tkinter对话框，带倒计时）
        import tkinter as tk
        from tkinter import simpledialog
        choice = messagebox.askquestion("战斗", f"遭遇{enemy_name}！\n\n选择：\n是 - 战斗\n否 - 逃跑")
        if choice == 'no':
            if self.attempt_escape(player, enemy):
                self.add_combat_log("成功逃脱！")
                return {'success': True, 'escaped': True, 'combat_log': self.combat_log.copy()}
            else:
                self.add_combat_log("逃跑失败！敌人先手攻击！")
                # 敌人先攻击一次
                self.enemy_turn(player, enemy)
        # 正常战斗
        rounds = 0
        while player.health > 0 and enemy['health'] > 0 and rounds < 20:
            rounds += 1
            self.add_combat_log(f"--- 第{rounds}回合 ---")
            self.player_turn(player, enemy)
            if enemy['health'] <= 0:
                break
            self.enemy_turn(player, enemy)
        return self.resolve_combat(player, enemy, rounds)

    def start_card_battle(self, player, enemy_data):
        """卡牌战斗模式（BOSS专用）"""
        from tkinter import Toplevel, Button, Label, Frame
        win = Toplevel(self.game.root)
        win.title(f"卡牌战斗 - 对战 {enemy_data.get('name')}")
        win.geometry("600x400")
        win.transient(self.game.root)
        win.grab_set()
        # 敌人实例
        enemy = self.create_enemy(enemy_data)
        # 卡牌选项（可从MOD加载）
        card_options = [
            {"name": "重击", "effect": "damage", "value": 15},
            {"name": "防御", "effect": "defend", "value": 10},
            {"name": "治疗", "effect": "heal", "value": 10},
            {"name": "闪避", "effect": "dodge", "value": 1}
        ]
        current_cards = random.sample(card_options, 4)
        # 显示区域
        info_frame = Frame(win)
        info_frame.pack(pady=10)
        enemy_label = Label(info_frame, text=f"敌人: {enemy['name']} 生命: {enemy['health']}/{enemy['max_health']}")
        enemy_label.pack()
        player_label = Label(info_frame, text=f"玩家: {player.health}/{player.max_health}")
        player_label.pack()
        card_frame = Frame(win)
        card_frame.pack(pady=10)

        def update_display():
            enemy_label.config(text=f"敌人: {enemy['name']} 生命: {enemy['health']}/{enemy['max_health']}")
            player_label.config(text=f"玩家: {player.health}/{player.max_health}")
            if enemy['health'] <= 0:
                win.destroy()
                exp = enemy.get('exp_reward', 0)
                self.reward_player(player, enemy, exp, {})
                self.game.add_game_log(f"卡牌战斗胜利！击败了{enemy['name']}")
            elif player.health <= 0:
                win.destroy()
                self.game.add_game_log(f"卡牌战斗失败！被{enemy['name']}击败")

        def choose_card(card):
            # 玩家行动
            if card['effect'] == 'damage':
                damage = card['value']
                enemy['health'] -= damage
                self.add_combat_log(f"你使用了{card['name']}，造成{damage}点伤害！")
            elif card['effect'] == 'heal':
                heal = card['value']
                player.modify_health(heal)
                self.add_combat_log(f"你使用了{card['name']}，恢复了{heal}点生命！")
            elif card['effect'] == 'defend':
                # 防御效果，下一回合敌人伤害减半（简化）
                self.add_combat_log(f"你使用了{card['name']}，防御提升！")
                # 简单实现：增加一个临时buff
                player.add_buff({"name": "防御", "type": "defense", "value": 0.5, "duration": 1})
            elif card['effect'] == 'dodge':
                # 闪避效果，敌人本回合攻击miss
                self.add_combat_log(f"你使用了{card['name']}，闪避提升！")
                player.add_buff({"name": "闪避", "type": "dodge", "value": 100, "duration": 1})
            update_display()
            if enemy['health'] <= 0:
                return
            # 敌人回合
            self.enemy_turn(player, enemy)
            update_display()
            if player.health <= 0:
                return
            # 刷新卡牌
            nonlocal current_cards
            current_cards = random.sample(card_options, 4)
            for widget in card_frame.winfo_children():
                widget.destroy()
            for card in current_cards:
                btn = Button(card_frame, text=f"{card['name']} - {card['effect']}", command=lambda c=card: choose_card(c))
                btn.pack(side="left", padx=5)

        # 初始按钮
        for card in current_cards:
            btn = Button(card_frame, text=f"{card['name']} - {card['effect']}", command=lambda c=card: choose_card(c))
            btn.pack(side="left", padx=5)

        win.wait_window()
        loot = {}
        if player.health > 0 and enemy['health'] <= 0:
            loot = self.generate_loot(enemy)
        return {
            'player_won': player.health > 0 and enemy['health'] <= 0,
            'enemy_name': enemy['name'],
            'loot': loot,
            'rounds': 0,
            'combat_log': self.combat_log.copy()
        }

    def create_enemy(self, enemy_data):
        base = self.enemy_types.get(enemy_data.get('id'))
        if not base:
            base = self.enemy_types['mutant_rat'].copy()
            base['name'] = enemy_data.get('name', base['name'])
            base['health'] = enemy_data.get('health', base['health'])
            base['max_health'] = enemy_data.get('max_health', base['max_health'])
            base['attack'] = enemy_data.get('attack', base['attack'])
            base['defense'] = enemy_data.get('defense', base['defense'])
        enemy = base.copy()
        enemy['health'] = enemy['max_health']
        enemy['status_effects'] = []
        enemy['cooldowns'] = {}
        return enemy

    def player_turn(self, player, enemy):
        attack = self.calculate_player_attack(player, enemy)
        damage = self.apply_damage(enemy, attack['damage'], attack['is_critical'])
        if attack['is_critical']:
            self.add_combat_log(f"💥 暴击！你对{enemy['name']}造成了{damage}点伤害！")
        else:
            self.add_combat_log(f"⚔️ 你对{enemy['name']}造成了{damage}点伤害！")
        weapon = player.equipment.get('weapon')
        if weapon and attack.get('is_hit', True):
            player.degrade_item(weapon, 1)
        self.check_enemy_ability_use(enemy, player, 'defensive')

    def enemy_turn(self, player, enemy):
        ability = self.check_enemy_ability_use(enemy, player, 'offensive')
        if not ability:
            attack = self.calculate_enemy_attack(enemy, player)
            damage = self.apply_damage(player, attack['damage'], attack['is_critical'])
            if attack['is_critical']:
                self.add_combat_log(f"💥 {enemy['name']}的暴击对你造成了{damage}点伤害！")
            else:
                self.add_combat_log(f"⚔️ {enemy['name']}对你造成了{damage}点伤害！")

    def calculate_player_attack(self, player, enemy):
        stats = player.get_combat_stats()
        base = stats['attack']
        weapon = player.equipment.get('weapon')
        if weapon:
            wdata = self.game.items.get_item_data(weapon)
            if wdata:
                base += wdata.get('damage', 0)
        if 'weapon_upgrade' in getattr(self.game, 'completed_research', []):
            base += 2
        damage = max(1, base + random.randint(-2, 2))
        crit = random.random() < (stats['critical'] / 100.0)
        if crit:
            damage = int(damage * 1.5)
        hit = random.random() < (0.8 + (stats['accuracy'] / 500.0))
        if not hit:
            damage = 0
            self.add_combat_log(f"❌ 你的攻击被{enemy['name']}躲开了！")
        return {'damage': damage, 'is_critical': crit, 'is_hit': hit}

    def calculate_enemy_attack(self, enemy, player):
        base = enemy['attack']
        # 应用敌人自身的buff/debuff
        for effect in enemy.get('status_effects', []):
            if effect.get('type') == 'damage_buff':
                base *= (1 + effect['value'])
        damage = max(1, base + random.randint(-1, 2))
        crit = random.random() < 0.05
        if crit:
            damage = int(damage * 1.5)
        dodge = player.get_combat_stats()['dodge'] / 200.0
        # 检查玩家闪避buff
        for buff in player.buffs:
            if buff.get('type') == 'dodge':
                dodge += buff['value'] / 100.0
        if random.random() < dodge:
            damage = 0
            self.add_combat_log(f"🛡️ 你闪避了{enemy['name']}的攻击！")
        return {'damage': damage, 'is_critical': crit, 'is_dodged': damage == 0}

    def apply_damage(self, target, damage, is_critical=False):
        if damage <= 0:
            return 0
        if isinstance(target, dict):
            actual = max(1, damage - target['defense'])
            target['health'] -= actual
            return actual
        else:
            defense = target.get_combat_stats()['defense']
            # 检查玩家防御buff
            for buff in target.buffs:
                if buff.get('type') == 'defense':
                    defense = int(defense * (1 - buff['value']))
            actual = max(1, damage - defense // 2)
            target.modify_health(-actual)
            for slot in ('chest', 'head', 'legs'):
                armor = target.equipment.get(slot)
                if armor:
                    target.degrade_item(armor, 1)
                    break
            return actual

    def get_ability_data(self, ability_id):
        abilities = {
            'quick_bite': {'id': 'quick_bite', 'name': '快速撕咬', 'type': 'offensive', 'damage_multiplier': 0.6, 'attack_count': 2, 'cooldown': 2, 'priority': 2},
            'pounce': {'id': 'pounce', 'name': '猛扑', 'type': 'offensive', 'damage_multiplier': 1.5, 'cooldown': 3, 'priority': 3},
            'poison_bite': {'id': 'poison_bite', 'name': '毒液撕咬', 'type': 'offensive', 'damage_multiplier': 1.0, 'special_effect': 'poison', 'cooldown': 4, 'priority': 4},
            'tail_sting': {'id': 'tail_sting', 'name': '尾刺攻击', 'type': 'offensive', 'damage_multiplier': 2.0, 'cooldown': 5, 'priority': 5},
            'dodge': {'id': 'dodge', 'name': '闪避', 'type': 'defensive', 'dodge_bonus': 0.5, 'duration': 1, 'cooldown': 3, 'priority': 1},
            'howl': {'id': 'howl', 'name': '嚎叫', 'type': 'defensive', 'attack_debuff': 0.3, 'duration': 2, 'cooldown': 4, 'priority': 2},
            'roar': {'id': 'roar', 'name': '怒吼', 'type': 'defensive', 'stun_duration': 1, 'cooldown': 6, 'priority': 5},
            'regenerate': {'id': 'regenerate', 'name': '再生', 'type': 'defensive', 'heal_amount': 20, 'cooldown': 8, 'priority': 4},
            'web_shot': {'id': 'web_shot', 'name': '蛛网射击', 'type': 'defensive', 'slow': 0.5, 'duration': 2, 'cooldown': 4, 'priority': 3},
            'infectious_bite': {'id': 'infectious_bite', 'name': '感染撕咬', 'type': 'offensive', 'damage_multiplier': 1.2, 'special_effect': 'infection', 'cooldown': 5, 'priority': 4},
            'ferocious_charge': {'id': 'ferocious_charge', 'name': '凶猛冲撞', 'type': 'offensive', 'damage_multiplier': 1.8, 'cooldown': 4, 'priority': 5},
            'tactical_strike': {'id': 'tactical_strike', 'name': '战术打击', 'type': 'offensive', 'damage_multiplier': 1.3, 'cooldown': 2, 'priority': 3},
            'command_aura': {'id': 'command_aura', 'name': '指挥光环', 'type': 'defensive', 'buff': 'damage', 'value': 0.2, 'duration': 3, 'cooldown': 6, 'priority': 4},
            'phase_shift': {'id': 'phase_shift', 'name': '相位转移', 'type': 'defensive', 'invincible': True, 'duration': 1, 'cooldown': 5, 'priority': 5}
        }
        return abilities.get(ability_id)

    def check_enemy_ability_use(self, enemy, player, ability_type):
        abilities = enemy.get('abilities', [])
        if not abilities:
            return None
        available = []
        for aid in abilities:
            ability = self.get_ability_data(aid)
            if ability and ability.get('type') == ability_type:
                cd = enemy['cooldowns'].get(aid, 0)
                if cd <= 0:
                    available.append(ability)
        if not available:
            return None
        available.sort(key=lambda x: x.get('priority', 0), reverse=True)
        chosen = available[0]
        enemy['cooldowns'][chosen['id']] = chosen.get('cooldown', 1)
        return self.use_ability(enemy, player, chosen)

    def use_ability(self, enemy, player, ability):
        self.add_combat_log(f"🌟 {enemy['name']}使用了{ability['name']}！")
        aid = ability['id']
        if aid == 'quick_bite':
            total = 0
            for _ in range(ability['attack_count']):
                atk = self.calculate_enemy_attack(enemy, player)
                if not atk['is_dodged']:
                    dmg = self.apply_damage(player, int(atk['damage'] * ability['damage_multiplier']))
                    total += dmg
            self.add_combat_log(f"造成了{total}点伤害！")
            return {'type': 'attack', 'damage': total}
        elif aid == 'pounce':
            atk = self.calculate_enemy_attack(enemy, player)
            if atk['is_dodged']:
                self.add_combat_log("但被你闪避了！")
                return {'type': 'attack', 'damage': 0}
            dmg = self.apply_damage(player, int(atk['damage'] * ability['damage_multiplier']))
            self.add_combat_log(f"造成了{dmg}点伤害！")
            return {'type': 'attack', 'damage': dmg}
        elif aid == 'poison_bite':
            atk = self.calculate_enemy_attack(enemy, player)
            if atk['is_dodged']:
                self.add_combat_log("但被你闪避了！")
                return {'type': 'attack', 'damage': 0}
            dmg = self.apply_damage(player, int(atk['damage'] * ability['damage_multiplier']))
            player.add_debuff({'name': '中毒', 'type': 'poison', 'damage': 3, 'duration': 3})
            self.add_combat_log(f"造成了{dmg}点伤害，并附加中毒效果！")
            return {'type': 'attack', 'damage': dmg}
        elif aid == 'tail_sting':
            atk = self.calculate_enemy_attack(enemy, player)
            if atk['is_dodged']:
                self.add_combat_log("但被你闪避了！")
                return {'type': 'attack', 'damage': 0}
            dmg = self.apply_damage(player, int(atk['damage'] * ability['damage_multiplier']))
            player.add_debuff({'name': '麻痹', 'type': 'paralyze', 'speed_penalty': 0.5, 'duration': 2})
            self.add_combat_log(f"造成了{dmg}点伤害，并附加麻痹效果！")
            return {'type': 'attack', 'damage': dmg}
        elif aid == 'dodge':
            enemy['status_effects'].append({'type': 'dodge_bonus', 'value': ability['dodge_bonus'], 'duration': ability['duration']})
            self.add_combat_log(f"{enemy['name']}的闪避率提升了！")
            return {'type': 'buff'}
        elif aid == 'howl':
            player.add_debuff({'name': '威慑', 'type': 'attack_debuff', 'value': ability['attack_debuff'], 'duration': ability['duration']})
            self.add_combat_log("你的攻击力降低了！")
            return {'type': 'debuff'}
        elif aid == 'roar':
            player.add_debuff({'name': '眩晕', 'type': 'stun', 'duration': ability['stun_duration']})
            self.add_combat_log("你被震慑，无法行动一回合！")
            return {'type': 'stun'}
        elif aid == 'regenerate':
            heal = ability['heal_amount']
            enemy['health'] = min(enemy['max_health'], enemy['health'] + heal)
            self.add_combat_log(f"{enemy['name']}恢复了{heal}点生命值！")
            return {'type': 'heal', 'amount': heal}
        elif aid == 'web_shot':
            player.add_debuff({'name': '减速', 'type': 'slow', 'speed_penalty': ability['slow'], 'duration': ability['duration']})
            self.add_combat_log("你被蛛网缠住，速度降低了！")
            return {'type': 'debuff'}
        elif aid == 'ferocious_charge':
            atk = self.calculate_enemy_attack(enemy, player)
            if atk['is_dodged']:
                self.add_combat_log("但被你闪避了！")
                return {'type': 'attack', 'damage': 0}
            dmg = self.apply_damage(player, int(atk['damage'] * ability['damage_multiplier']))
            self.add_combat_log(f"造成了{dmg}点伤害！")
            return {'type': 'attack', 'damage': dmg}
        elif aid == 'command_aura':
            enemy['status_effects'].append({'type': 'damage_buff', 'value': ability['value'], 'duration': ability['duration']})
            self.add_combat_log(f"{enemy['name']}的攻击力提升了！")
            return {'type': 'buff'}
        elif aid == 'phase_shift':
            enemy['status_effects'].append({'type': 'invincible', 'duration': ability['duration']})
            self.add_combat_log(f"{enemy['name']}进入了相位转移状态，暂时无敌！")
            return {'type': 'buff'}
        return None

    def resolve_combat(self, player, enemy, rounds):
        if enemy['health'] <= 0:
            exp = enemy['exp_reward']
            loot = self.generate_loot(enemy)
            self.reward_player(player, enemy, exp, loot)
            self.add_combat_log(f"🎉 胜利！获得了{exp}经验值")
            return {
                'player_won': True, 'enemy_name': enemy['name'], 'exp_reward': exp,
                'loot': loot, 'rounds': rounds, 'combat_log': self.combat_log.copy()
            }
        else:
            self.add_combat_log("💀 战斗失败！")
            return {
                'player_won': False, 'enemy_name': enemy['name'], 'rounds': rounds,
                'combat_log': self.combat_log.copy()
            }

    def generate_loot(self, enemy):
        loot = {}
        if random.randint(1, 100) <= enemy.get('loot_chance', 0):
            for item_id, entry in enemy.get('loot_table', {}).items():
                if isinstance(entry, dict):
                    min_q = int(entry.get('min', 1))
                    max_q = int(entry.get('max', min_q))
                    chance = int(entry.get('chance', 100))
                else:
                    min_q, max_q, chance = entry
                    min_q, max_q, chance = int(min_q), int(max_q), int(chance)
                if random.randint(1, 100) <= chance:
                    qty = random.randint(min_q, max(min_q, max_q))
                    loot[item_id] = loot.get(item_id, 0) + qty
        return loot

    def reward_player(self, player, enemy, exp, loot):
        player.gain_skill_exp('combat', exp)
        player.stats['enemies_defeated'] = player.stats.get('enemies_defeated', 0) + 1
        if hasattr(self.game, 'quests') and self.game.quests:
            self.game.quests.update_quest_progress('enemy_defeated', enemy_type=enemy.get('id'))
        if loot:
            loot_text = ', '.join([f'{self.game.items.get_item_name(i)} x{q}' for i, q in loot.items()])
            self.add_combat_log(f"获得战利品: {loot_text}")

    def add_combat_log(self, msg):
        self.combat_log.append(msg)
        logging.info(f"战斗日志: {msg}")

    def get_combat_log(self):
        return self.combat_log.copy()

    def get_enemy_by_id(self, enemy_id):
        return self.enemy_types.get(enemy_id)

    def get_enemies_by_level(self, min_level, max_level):
        return [enemy for enemy in self.enemy_types.values() if min_level <= enemy['level'] <= max_level]

    def calculate_difficulty_rating(self, player_level, enemy_level):
        diff = enemy_level - player_level
        if diff <= -3: return "非常简单"
        if diff <= -1: return "简单"
        if diff == 0: return "中等"
        if diff <= 2: return "困难"
        if diff <= 4: return "非常困难"
        return "极度危险"

    def can_escape(self, player, enemy):
        player_speed = player.get_combat_stats()['dodge']
        enemy_speed = enemy['speed']
        escape_chance = 0.3 + (player_speed - enemy_speed) * 0.05
        escape_chance = max(0.1, min(0.9, escape_chance))
        return random.random() < escape_chance

    def attempt_escape(self, player, enemy):
        if self.can_escape(player, enemy):
            self.add_combat_log("✅ 成功逃脱！")
            return True
        else:
            self.add_combat_log("❌ 逃脱失败！")
            return False