# -*- coding: utf-8 -*-

import random
import logging
from typing import Dict, List, Optional

class CombatSystem:
    def __init__(self, game):
        self.game = game
        self.enemy_types = {}
        self.combat_log = []
        self.initialized = False
        
    def initialize(self):
        """初始化战斗系统"""
        try:
            self.create_enemy_types()
            self.initialized = True
            logging.info("战斗系统初始化完成")
        except Exception as e:
            logging.error(f"战斗系统初始化失败: {e}")
            raise
    
    def create_enemy_types(self):
        """创建敌人类型"""
        # === 普通敌人 ===
        self.enemy_types['mutant_rat'] = {
            'id': 'mutant_rat',
            'name': '变异鼠',
            'level': 1,
            'health': 20,
            'max_health': 20,
            'attack': 5,
            'defense': 2,
            'speed': 8,
            'exp_reward': 10,
            'loot_chance': 70,
            'loot_table': {
                'food': (1, 1, 50),
                'materials': (1, 2, 30)
            },
            'abilities': ['quick_bite'],
            'description': '受到辐射变异的老鼠，攻击性很强'
        }
        
        self.enemy_types['radroach'] = {
            'id': 'radroach',
            'name': '辐射蟑螂',
            'level': 1,
            'health': 15,
            'max_health': 15,
            'attack': 4,
            'defense': 3,
            'speed': 6,
            'exp_reward': 8,
            'loot_chance': 60,
            'loot_table': {
                'materials': (1, 3, 40),
                'medicine': (1, 1, 20)
            },
            'abilities': ['dodge'],
            'description': '巨大的变异蟑螂，外壳坚硬'
        }
        
        self.enemy_types['mutant_wolf'] = {
            'id': 'mutant_wolf',
            'name': '变异狼',
            'level': 2,
            'health': 30,
            'max_health': 30,
            'attack': 8,
            'defense': 3,
            'speed': 7,
            'exp_reward': 20,
            'loot_chance': 75,
            'loot_table': {
                'food': (1, 2, 60),
                'materials': (1, 2, 40),
                'cloth': (1, 1, 25)
            },
            'abilities': ['pounce', 'howl'],
            'description': '凶猛的变异狼，擅长群体作战'
        }
        
        self.enemy_types['zombie'] = {
            'id': 'zombie',
            'name': '僵尸',
            'level': 2,
            'health': 40,
            'max_health': 40,
            'attack': 6,
            'defense': 5,
            'speed': 3,
            'exp_reward': 18,
            'loot_chance': 65,
            'loot_table': {
                'cloth': (1, 3, 45),
                'materials': (1, 2, 35),
                'medicine': (1, 1, 15)
            },
            'abilities': ['grapple', 'infectious_bite'],
            'description': '行动缓慢但生命力顽强的僵尸'
        }
        
        self.enemy_types['giant_spider'] = {
            'id': 'giant_spider',
            'name': '巨型蜘蛛',
            'level': 3,
            'health': 35,
            'max_health': 35,
            'attack': 12,
            'defense': 2,
            'speed': 9,
            'exp_reward': 25,
            'loot_chance': 70,
            'loot_table': {
                'medicine': (1, 2, 50),
                'rare_herbs': (1, 1, 30),
                'materials': (1, 3, 40)
            },
            'abilities': ['web_shot', 'poison_bite'],
            'description': '毒性强烈的巨型蜘蛛，行动敏捷'
        }
        
        # === 精英敌人 ===
        self.enemy_types['mutant_bear'] = {
            'id': 'mutant_bear',
            'name': '变异熊',
            'level': 4,
            'health': 60,
            'max_health': 60,
            'attack': 15,
            'defense': 8,
            'speed': 5,
            'exp_reward': 40,
            'loot_chance': 85,
            'loot_table': {
                'food': (2, 3, 70),
                'materials': (2, 4, 60),
                'rare_herbs': (1, 2, 35)
            },
            'abilities': ['ferocious_charge', 'roar'],
            'description': '巨大的变异熊，力量惊人'
        }
        
        self.enemy_types['raider_elite'] = {
            'id': 'raider_elite',
            'name': '掠夺者精英',
            'level': 4,
            'health': 50,
            'max_health': 50,
            'attack': 12,
            'defense': 6,
            'speed': 6,
            'exp_reward': 35,
            'loot_chance': 80,
            'loot_table': {
                'electronic': (1, 2, 45),
                'materials': (2, 5, 65),
                'medicine': (1, 2, 40),
                'pistol': (1, 1, 15)
            },
            'abilities': ['tactical_strike', 'grenade_throw'],
            'description': '经验丰富的掠夺者战士，装备精良'
        }
        
        self.enemy_types['radscorpion'] = {
            'id': 'radscorpion',
            'name': '辐射蝎子',
            'level': 5,
            'health': 55,
            'max_health': 55,
            'attack': 18,
            'defense': 7,
            'speed': 4,
            'exp_reward': 45,
            'loot_chance': 80,
            'loot_table': {
                'rare_minerals': (1, 2, 40),
                'antidote': (1, 2, 50),
                'materials': (3, 5, 70)
            },
            'abilities': ['tail_sting', 'burrow'],
            'description': '致命的辐射蝎子，尾刺含有剧毒'
        }
        
        # === BOSS敌人 ===
        self.enemy_types['mutant_behemoth'] = {
            'id': 'mutant_behemoth',
            'name': '变异巨兽',
            'level': 8,
            'health': 150,
            'max_health': 150,
            'attack': 25,
            'defense': 15,
            'speed': 3,
            'exp_reward': 100,
            'loot_chance': 95,
            'loot_table': {
                'advanced_alloy': (2, 3, 80),
                'rare_minerals': (3, 5, 75),
                'ancient_artifact': (1, 1, 50),
                'military_ration': (3, 5, 90)
            },
            'abilities': ['earth_shatter', 'furious_swipe', 'regenerate'],
            'description': '传说中的变异巨兽，拥有毁灭性的力量'
        }
        
        self.enemy_types['raider_commander'] = {
            'id': 'raider_commander',
            'name': '掠夺者指挥官',
            'level': 7,
            'health': 120,
            'max_health': 120,
            'attack': 20,
            'defense': 12,
            'speed': 6,
            'exp_reward': 80,
            'loot_chance': 90,
            'loot_table': {
                'assault_rifle': (1, 1, 60),
                'tactical_vest': (1, 1, 70),
                'advanced_alloy': (1, 2, 65),
                'electronic': (3, 5, 85)
            },
            'abilities': ['command_aura', 'precision_shot', 'tactical_retreat'],
            'description': '掠夺者组织的首领，战术大师'
        }
        
        # === 特殊敌人 ===
        self.enemy_types['ghost_soldier'] = {
            'id': 'ghost_soldier',
            'name': '幽灵士兵',
            'level': 6,
            'health': 80,
            'max_health': 80,
            'attack': 16,
            'defense': 10,
            'speed': 7,
            'exp_reward': 60,
            'loot_chance': 70,
            'loot_table': {
                'research_data': (1, 2, 55),
                'map_fragment': (1, 3, 65),
                'advanced_alloy': (1, 1, 40)
            },
            'abilities': ['phase_shift', 'energy_blast', 'teleport'],
            'description': '神秘的幽灵般存在，似乎来自另一个维度'
        }
        
        logging.info(f"创建了{len(self.enemy_types)}种敌人类型")
    
    def load_data(self, save_data):
        """加载战斗系统数据"""
        try:
            self.initialized = True
            logging.info("战斗系统数据加载完成")
        except Exception as e:
            logging.error(f"加载战斗系统数据失败: {e}")
            raise
    
    def get_save_data(self):
        """获取保存数据"""
        return {
            'enemy_types': self.enemy_types
        }
    
    def start_combat(self, player, enemy_data):
        """开始战斗"""
        try:
            self.combat_log.clear()
            
            # 创建敌人实例
            enemy = self.create_enemy(enemy_data)
            if not enemy:
                return {'success': False, 'message': '无效的敌人数据'}
            
            self.add_combat_log(f"遭遇了{enemy['name']}！")
            
            # 战斗循环
            round_count = 0
            max_rounds = 20  # 防止无限战斗
            
            while (player.health > 0 and enemy['health'] > 0 and 
                   round_count < max_rounds):
                
                round_count += 1
                self.add_combat_log(f"--- 第{round_count}回合 ---")
                
                # 玩家回合
                player_turn_result = self.player_turn(player, enemy)
                if enemy['health'] <= 0:
                    break
                
                # 敌人回合
                enemy_turn_result = self.enemy_turn(player, enemy)
                if player.health <= 0:
                    break
            
            # 战斗结果
            combat_result = self.resolve_combat(player, enemy, round_count)
            return combat_result
            
        except Exception as e:
            logging.error(f"战斗过程中出错: {e}")
            return {'success': False, 'message': '战斗过程出现错误'}
    
    def create_enemy(self, enemy_data):
        """创建敌人实例"""
        enemy_type = self.enemy_types.get(enemy_data.get('id'))
        if not enemy_type:
            return None
        
        # 创建敌人副本
        enemy = enemy_type.copy()
        enemy['health'] = enemy['max_health']
        enemy['status_effects'] = []
        enemy['cooldowns'] = {}
        
        return enemy
    
    def player_turn(self, player, enemy):
        """玩家回合"""
        # 计算玩家攻击
        player_attack = self.calculate_player_attack(player, enemy)
        
        # 应用攻击
        damage_dealt = self.apply_damage(enemy, player_attack['damage'], player_attack['is_critical'])
        
        # 记录战斗日志
        if player_attack['is_critical']:
            self.add_combat_log(f"💥 暴击！你对{enemy['name']}造成了{damage_dealt}点伤害！")
        else:
            self.add_combat_log(f"⚔️ 你对{enemy['name']}造成了{damage_dealt}点伤害！")
        
        # 检查敌人是否使用能力
        self.check_enemy_ability_use(enemy, player, 'defensive')
        
        return {
            'damage_dealt': damage_dealt,
            'was_critical': player_attack['is_critical'],
            'ability_used': player_attack.get('ability_used')
        }
    
    def enemy_turn(self, player, enemy):
        """敌人回合"""
        # 检查敌人能力使用
        ability_used = self.check_enemy_ability_use(enemy, player, 'offensive')
        
        if not ability_used:
            # 普通攻击
            enemy_attack = self.calculate_enemy_attack(enemy, player)
            damage_dealt = self.apply_damage(player, enemy_attack['damage'], enemy_attack['is_critical'])
            
            if enemy_attack['is_critical']:
                self.add_combat_log(f"💥 {enemy['name']}的暴击对你造成了{damage_dealt}点伤害！")
            else:
                self.add_combat_log(f"⚔️ {enemy['name']}对你造成了{damage_dealt}点伤害！")
        else:
            damage_dealt = 0
        
        return {
            'damage_dealt': damage_dealt,
            'ability_used': ability_used
        }
    
    def calculate_player_attack(self, player, enemy):
        """计算玩家攻击"""
        # 获取玩家战斗属性
        combat_stats = player.get_combat_stats()
        
        # 基础伤害计算
        base_damage = combat_stats['attack']
        
        # 武器加成
        weapon = player.equipment.get('weapon')
        if weapon:
            weapon_data = self.game.items.get_item_data(weapon)
            if weapon_data:
                base_damage += weapon_data.get('damage', 0)
        
        # 随机波动
        damage_variation = random.randint(-2, 2)
        final_damage = max(1, base_damage + damage_variation)
        
        # 暴击计算
        critical_chance = combat_stats['critical'] / 100.0
        is_critical = random.random() < critical_chance
        if is_critical:
            final_damage = int(final_damage * 1.5)
        
        # 命中计算
        accuracy = combat_stats['accuracy'] / 100.0
        hit_chance = 0.8 + (accuracy * 0.2)  # 基础80%命中率，最高100%
        is_hit = random.random() < hit_chance
        
        if not is_hit:
            final_damage = 0
            self.add_combat_log(f"❌ 你的攻击被{enemy['name']}躲开了！")
        
        return {
            'damage': final_damage if is_hit else 0,
            'is_critical': is_critical and is_hit,
            'is_hit': is_hit
        }
    
    def calculate_enemy_attack(self, enemy, player):
        """计算敌人攻击"""
        # 基础伤害
        base_damage = enemy['attack']
        
        # 随机波动
        damage_variation = random.randint(-1, 2)
        final_damage = max(1, base_damage + damage_variation)
        
        # 暴击计算
        critical_chance = 0.05  # 敌人基础暴击率5%
        is_critical = random.random() < critical_chance
        if is_critical:
            final_damage = int(final_damage * 1.5)
        
        # 玩家闪避计算
        dodge_chance = player.get_combat_stats()['dodge'] / 200.0  # 降低闪避效果
        is_dodged = random.random() < dodge_chance
        
        if is_dodged:
            final_damage = 0
            self.add_combat_log(f"🛡️ 你闪避了{enemy['name']}的攻击！")
        
        return {
            'damage': final_damage if not is_dodged else 0,
            'is_critical': is_critical and not is_dodged,
            'is_dodged': is_dodged
        }
    
    def apply_damage(self, target, damage, is_critical=False):
        """应用伤害"""
        if damage <= 0:
            return 0
        
        # 防御减免
        if isinstance(target, dict):  # 敌人
            defense = target['defense']
            actual_damage = max(1, damage - defense)
            target['health'] -= actual_damage
        else:  # 玩家
            defense = target.get_combat_stats()['defense']
            actual_damage = max(1, damage - (defense // 2))  # 玩家防御效果减半
            target.modify_health(-actual_damage)
        
        return actual_damage
    
    def check_enemy_ability_use(self, enemy, player, ability_type):
        """检查敌人是否使用能力"""
        abilities = enemy.get('abilities', [])
        if not abilities:
            return None
        
        # 过滤符合类型的能力
        available_abilities = []
        for ability_id in abilities:
            ability = self.get_ability_data(ability_id)
            if ability and ability.get('type') == ability_type:
                # 检查冷却
                cooldown = enemy['cooldowns'].get(ability_id, 0)
                if cooldown <= 0:
                    available_abilities.append(ability)
        
        if not available_abilities:
            return None
        
        # 根据优先级选择能力
        available_abilities.sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        # 设置冷却时间
        enemy['cooldowns'][chosen_ability['id']] = chosen_ability.get('cooldown', 1)
        
        return ability_result
    
    def get_ability_data(self, ability_id):
        """获取能力数据"""
        abilities = {
            # 攻击型能力
            'quick_bite': {
                'id': 'quick_bite',
                'name': '快速撕咬',
                'type': 'offensive',
                'description': '快速发动两次攻击',
                'damage_multiplier': 0.6,
                'attack_count': 2,
                'cooldown': 2,
                'priority': 2
            },
            'pounce': {
                'id': 'pounce',
                'name': '猛扑',
                'type': 'offensive',
                'description': '强力跳跃攻击，造成额外伤害',
                'damage_multiplier': 1.5,
                'cooldown': 3,
                'priority': 3
            },
            'poison_bite': {
                'id': 'poison_bite',
                'name': '毒液撕咬',
                'type': 'offensive',
                'description': '攻击附带中毒效果',
                'damage_multiplier': 1.0,
                'special_effect': 'poison',
                'cooldown': 4,
                'priority': 4
            },
            'tail_sting': {
                'id': 'tail_sting',
                'name': '尾刺攻击',
                'type': 'offensive',
                'description': '致命的尾刺攻击，高伤害',
                'damage_multiplier': 2.0,
                'cooldown': 5,
                'priority': 5
            },
            
            # 防御型能力
            'dodge': {
                'id': 'dodge',
                'name': '闪避',
                'type': 'defensive',
                'description': '大幅提升闪避率',
                'dodge_bonus': 0.5,
                'duration': 1,
                'cooldown': 3,
                'priority': 1
            },
            'howl': {
                'id': 'howl',
                'name': '嚎叫',
                'type': 'defensive',
                'description': '发出威慑性的嚎叫，降低玩家攻击力',
                'attack_debuff': 0.3,
                'duration': 2,
                'cooldown': 4,
                'priority': 2
            },
            'roar': {
                'id': 'roar',
                'name': '怒吼',
                'type': 'defensive',
                'description': '震慑性的怒吼，使玩家失去一回合',
                'stun_duration': 1,
                'cooldown': 6,
                'priority': 5
            },
            'regenerate': {
                'id': 'regenerate',
                'name': '再生',
                'type': 'defensive',
                'description': '快速恢复生命值',
                'heal_amount': 20,
                'cooldown': 8,
                'priority': 4
            }
        }
        
        return abilities.get(ability_id)
    
    def use_ability(self, enemy, player, ability):
        """使用能力"""
        ability_id = ability['id']
        self.add_combat_log(f"🌟 {enemy['name']}使用了{ability['name']}！")
        
        if ability_id == 'quick_bite':
            # 快速两次攻击
            total_damage = 0
            for i in range(ability['attack_count']):
                attack = self.calculate_enemy_attack(enemy, player)
                damage = self.apply_damage(player, int(attack['damage'] * ability['damage_multiplier']))
                total_damage += damage
                if i == 0:  # 只记录第一次攻击的命中情况
                    if attack['is_dodged']:
                        self.add_combat_log("但被你闪避了！")
                        return {'type': 'attack', 'damage': 0}
            
            self.add_combat_log(f"造成了{total_damage}点伤害！")
            return {'type': 'attack', 'damage': total_damage}
        
        elif ability_id == 'pounce':
            # 猛扑攻击
            attack = self.calculate_enemy_attack(enemy, player)
            if attack['is_dodged']:
                self.add_combat_log("但被你闪避了！")
                return {'type': 'attack', 'damage': 0}
            
            damage = self.apply_damage(player, int(attack['damage'] * ability['damage_multiplier']))
            self.add_combat_log(f"造成了{damage}点伤害！")
            return {'type': 'attack', 'damage': damage}
        
        elif ability_id == 'dodge':
            # 闪避提升
            enemy['status_effects'].append({
                'type': 'dodge_bonus',
                'value': ability['dodge_bonus'],
                'duration': ability['duration']
            })
            self.add_combat_log(f"{enemy['name']}的闪避率提升了！")
            return {'type': 'buff', 'effect': 'dodge_bonus'}
        
        elif ability_id == 'howl':
            # 攻击力降低
            player.add_debuff({
                'name': '威慑',
                'type': 'attack_debuff',
                'value': ability['attack_debuff'],
                'duration': ability['duration']
            })
            self.add_combat_log("你的攻击力降低了！")
            return {'type': 'debuff', 'effect': 'attack_debuff'}
        
        elif ability_id == 'regenerate':
            # 生命恢复
            heal_amount = ability['heal_amount']
            enemy['health'] = min(enemy['max_health'], enemy['health'] + heal_amount)
            self.add_combat_log(f"{enemy['name']}恢复了{heal_amount}点生命值！")
            return {'type': 'heal', 'amount': heal_amount}
        
        return None
    
    def resolve_combat(self, player, enemy, round_count):
        """结算战斗"""
        player_won = enemy['health'] <= 0
        
        if player_won:
            # 玩家胜利
            exp_reward = enemy['exp_reward']
            loot = self.generate_enemy_loot(enemy)
            
            # 奖励玩家
            self.reward_player(player, enemy, exp_reward, loot)
            
            self.add_combat_log(f"🎉 胜利！获得了{exp_reward}经验值")
            
            return {
                'player_won': True,
                'enemy_name': enemy['name'],
                'exp_reward': exp_reward,
                'loot': loot,
                'rounds': round_count,
                'combat_log': self.combat_log.copy()
            }
        else:
            # 玩家失败
            self.add_combat_log("💀 战斗失败！")
            
            return {
                'player_won': False,
                'enemy_name': enemy['name'],
                'rounds': round_count,
                'combat_log': self.combat_log.copy()
            }
    
    def generate_enemy_loot(self, enemy):
        """生成敌人战利品"""
        loot = {}
        
        # 检查是否掉落物品
        if random.randint(1, 100) <= enemy['loot_chance']:
            loot_table = enemy.get('loot_table', {})
            
            for item_id, loot_data in loot_table.items():
                min_qty, max_qty, chance = loot_data
                if random.randint(1, 100) <= chance:
                    quantity = random.randint(min_qty, max_qty)
                    loot[item_id] = loot.get(item_id, 0) + quantity
        
        return loot
    
    def reward_player(self, player, enemy, exp_reward, loot):
        """奖励玩家"""
        # 经验值奖励
        player.gain_skill_exp('combat', exp_reward)
        
        # 物品奖励
        for item_id, quantity in loot.items():
            player.add_item(item_id, quantity)
        
        # 更新统计数据
        player.stats['enemies_defeated'] += 1
        
        # 记录战利品
        if loot:
            loot_text = ', '.join([f"{self.game.items.get_item_name(item)} x{qty}" for item, qty in loot.items()])
            self.add_combat_log(f"获得战利品: {loot_text}")
    
    def add_combat_log(self, message):
        """添加战斗日志"""
        self.combat_log.append(message)
        logging.info(f"战斗日志: {message}")
    
    def get_combat_log(self):
        """获取战斗日志"""
        return self.combat_log.copy()
    
    def get_enemy_by_id(self, enemy_id):
        """根据ID获取敌人数据"""
        return self.enemy_types.get(enemy_id)
    
    def get_enemies_by_level(self, min_level, max_level):
        """根据等级获取敌人"""
        return [enemy for enemy in self.enemy_types.values() 
                if min_level <= enemy['level'] <= max_level]
    
    def calculate_difficulty_rating(self, player_level, enemy_level):
        """计算难度评级"""
        level_diff = enemy_level - player_level
        
        if level_diff <= -3:
            return "非常简单"
        elif level_diff <= -1:
            return "简单"
        elif level_diff == 0:
            return "中等"
        elif level_diff <= 2:
            return "困难"
        elif level_diff <= 4:
            return "非常困难"
        else:
            return "极度危险"
    
    def can_escape(self, player, enemy):
        """判断是否可以逃跑"""
        player_speed = player.get_combat_stats()['dodge']
        enemy_speed = enemy['speed']
        
        escape_chance = 0.3 + (player_speed - enemy_speed) * 0.05
        escape_chance = max(0.1, min(0.9, escape_chance))
        
        return random.random() < escape_chance
    
    def attempt_escape(self, player, enemy):
        """尝试逃跑"""
        if self.can_escape(player, enemy):
            self.add_combat_log("✅ 成功逃脱！")
            return True
        else:
            self.add_combat_log("❌ 逃脱失败！")
            return False
