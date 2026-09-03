# -*- coding: utf-8 -*-

import random
import logging
from datetime import datetime

class Player:
    def __init__(self, game):
        self.game = game
        self.initialized = False
        
    def initialize(self, character_data):
        """初始化玩家角色"""
        try:
            self.name = character_data['name']
            self.character_class = character_data.get('class', 'survivor')
            
            # 核心属性
            self.health = character_data.get('health', 100)
            self.max_health = character_data.get('max_health', 100)
            self.stamina = character_data.get('stamina', 100)
            self.max_stamina = character_data.get('max_stamina', 100)
            self.mental = character_data.get('mental', 100)
            self.max_mental = character_data.get('max_mental', 100)
            
            # 基础能力值
            self.strength = character_data.get('strength', 5)
            self.agility = character_data.get('agility', 5)
            self.intelligence = character_data.get('intelligence', 5)
            self.endurance = character_data.get('endurance', 5)
            self.luck = character_data.get('luck', 5)
            
            # 状态效果
            self.buffs = []
            self.debuffs = []
            self.addictions = []
            
            # 疲劳系统 (v1.6.0新增)
            self.fatigue = 0
            self.max_fatigue = 100
            self.night_penalty = False
            self.stamina_modifier = 1.0
            
            # 装备系统
            self.equipment = {
                'weapon': None, 'head': None, 'chest': None, 'legs': None,
                'backpack': None, 'accessory1': None, 'accessory2': None
            }
            
            # 背包系统
            self.inventory = {
                'food': 5, 'water': 5, 'materials': 10, 'medicine': 2
            }
            
            # 技能系统
            self.skills = {
                'survival': 1, 'combat': 1, 'crafting': 1,
                'farming': 1, 'medical': 1, 'social': 1,
                'intelligence': 1, 'mental': 1
            }
            
            # 技能经验值
            self.skill_exp = {
                'survival': 0, 'combat': 0, 'crafting': 0,
                'farming': 0, 'medical': 0, 'social': 0,
                'intelligence': 0, 'mental': 0
            }
            
            # 位置信息
            self.location = "starting_area"
            self.discovered_locations = ["starting_area"]
            
            # 时间记录
            self.last_sleep_time = None
            self.continuous_awake_hours = 0
            
            # 统计数据
            self.stats = {
                'days_survived': 0, 'enemies_defeated': 0, 'locations_discovered': 1,
                'items_crafted': 0, 'crops_harvested': 0, 'distance_traveled': 0,
                'quests_completed': 0, 'npcs_met': 0
            }
            
            self.initialized = True
            logging.info(f"玩家角色初始化完成: {self.name}")
            
        except Exception as e:
            logging.error(f"玩家初始化失败: {e}")
            raise
    
    def load_data(self, save_data):
        """加载玩家数据"""
        try:
            self.name = save_data.get('name', '幸存者')
            self.character_class = save_data.get('character_class', 'survivor')
            
            # 核心属性
            self.health = save_data.get('health', 100)
            self.max_health = save_data.get('max_health', 100)
            self.stamina = save_data.get('stamina', 100)
            self.max_stamina = save_data.get('max_stamina', 100)
            self.mental = save_data.get('mental', 100)
            self.max_mental = save_data.get('max_mental', 100)
            
            # 基础能力值
            self.strength = save_data.get('strength', 5)
            self.agility = save_data.get('agility', 5)
            self.intelligence = save_data.get('intelligence', 5)
            self.endurance = save_data.get('endurance', 5)
            self.luck = save_data.get('luck', 5)
            
            # 状态效果
            self.buffs = save_data.get('buffs', [])
            self.debuffs = save_data.get('debuffs', [])
            self.addictions = save_data.get('addictions', [])
            
            # 疲劳系统
            self.fatigue = save_data.get('fatigue', 0)
            self.max_fatigue = save_data.get('max_fatigue', 100)
            self.night_penalty = save_data.get('night_penalty', False)
            self.stamina_modifier = save_data.get('stamina_modifier', 1.0)
            
            # 装备
            self.equipment = save_data.get('equipment', self.equipment)
            
            # 背包
            self.inventory = save_data.get('inventory', self.inventory)
            
            # 技能系统
            self.skills = save_data.get('skills', self.skills)
            self.skill_exp = save_data.get('skill_exp', self.skill_exp)
            
            # 位置信息
            self.location = save_data.get('location', 'starting_area')
            self.discovered_locations = save_data.get('discovered_locations', ['starting_area'])
            
            # 时间记录
            self.last_sleep_time = save_data.get('last_sleep_time')
            self.continuous_awake_hours = save_data.get('continuous_awake_hours', 0)
            
            # 统计数据
            self.stats = save_data.get('stats', self.stats)
            
            self.initialized = True
            logging.info(f"玩家数据加载完成: {self.name}")
            
        except Exception as e:
            logging.error(f"加载玩家数据失败: {e}")
            raise
    
    def get_save_data(self):
        """获取保存数据"""
        return {
            'name': self.name,
            'character_class': self.character_class,
            'health': self.health, 'max_health': self.max_health,
            'stamina': self.stamina, 'max_stamina': self.max_stamina,
            'mental': self.mental, 'max_mental': self.max_mental,
            'strength': self.strength, 'agility': self.agility,
            'intelligence': self.intelligence, 'endurance': self.endurance,
            'luck': self.luck,
            'buffs': self.buffs, 'debuffs': self.debuffs, 'addictions': self.addictions,
            'fatigue': self.fatigue, 'max_fatigue': self.max_fatigue,
            'night_penalty': self.night_penalty, 'stamina_modifier': self.stamina_modifier,
            'equipment': self.equipment,
            'inventory': self.inventory,
            'skills': self.skills,
            'skill_exp': self.skill_exp,
            'location': self.location,
            'discovered_locations': self.discovered_locations,
            'last_sleep_time': self.last_sleep_time,
            'continuous_awake_hours': self.continuous_awake_hours,
            'stats': self.stats
        }
    
    def modify_health(self, amount):
        """修改生命值"""
        old = self.health
        self.health = max(0, min(self.max_health, self.health + amount))
        if amount < 0:
            logging.info(f"玩家生命值减少: {old} -> {self.health} (-{abs(amount)})")
        elif amount > 0:
            logging.info(f"玩家生命值恢复: {old} -> {self.health} (+{amount})")
        return self.health
    
    def modify_stamina(self, amount):
        """修改体力值，考虑疲劳和天气修正"""
        # 应用天气修正（在 game.py 中已设置 stamina_modifier）
        effective_amount = amount * self.stamina_modifier
        
        # 夜间惩罚（在 game.py 中已设置 night_penalty）
        if self.night_penalty and effective_amount < 0:
            effective_amount *= 1.2  # 夜间消耗增加20%
        
        # 疲劳惩罚：疲劳越高，消耗越大，恢复越慢
        if self.fatigue > 50 and effective_amount < 0:
            effective_amount *= (1 + self.fatigue / 100)
        
        old = self.stamina
        self.stamina = max(0, min(self.max_stamina, self.stamina + effective_amount))
        
        if amount < 0:
            logging.info(f"玩家体力减少: {old} -> {self.stamina} (-{abs(effective_amount):.1f})")
        elif amount > 0:
            logging.info(f"玩家体力恢复: {old} -> {self.stamina} (+{effective_amount:.1f})")
        return self.stamina
    
    def modify_mental(self, amount):
        """修改精神值"""
        old = self.mental
        self.mental = max(0, min(self.max_mental, self.mental + amount))
        if amount < 0:
            logging.info(f"玩家精神值减少: {old} -> {self.mental} (-{abs(amount)})")
        elif amount > 0:
            logging.info(f"玩家精神值恢复: {old} -> {self.mental} (+{amount})")
        return self.mental
    
    def modify_fatigue(self, amount):
        """修改疲劳值"""
        old = self.fatigue
        self.fatigue = max(0, min(self.max_fatigue, self.fatigue + amount))
        
        if amount > 0:
            if self.fatigue >= 80 and old < 80:
                self.game.add_game_log("警告：你感到极度疲劳，行动困难！")
                # 添加负面效果
                self.add_debuff({
                    "name": "极度疲劳", "type": "fatigue", "duration": 24,
                    "attack_penalty": 0.5, "stamina_regen_penalty": 0.5
                })
            logging.info(f"玩家疲劳增加: {old} -> {self.fatigue} (+{amount})")
        elif amount < 0:
            if self.fatigue < 80 and old >= 80:
                # 移除极度疲劳负面效果
                self.debuffs = [d for d in self.debuffs if d.get('name') != '极度疲劳']
            logging.info(f"玩家疲劳减少: {old} -> {self.fatigue} ({amount})")
        
        return self.fatigue
    
    def handle_time_passage(self, hours):
        """处理时间流逝的影响"""
        # 更新清醒时间
        self.continuous_awake_hours += hours
        
        # 长时间不睡觉的精神惩罚
        if self.continuous_awake_hours > 24:
            mental_penalty = (self.continuous_awake_hours - 24) * 0.5
            self.modify_mental(-mental_penalty)
            if self.continuous_awake_hours > 48:
                self.game.add_game_log("警告：你已经很久没有睡觉了！")
        
        # 累积疲劳（醒着时累积）
        fatigue_gain = hours * 2
        self.modify_fatigue(fatigue_gain)
        
        # 处理成瘾效果
        self.handle_addictions(hours)
        
        # 处理状态效果持续时间
        self.update_status_effects(hours)
    
    def handle_addictions(self, hours):
        """处理成瘾效果"""
        for addiction in self.addictions[:]:
            addiction['withdrawal_time'] += hours
            
            # 戒断症状
            if addiction['withdrawal_time'] > 24:
                withdrawal_strength = min(5, (addiction['withdrawal_time'] - 24) // 12)
                
                if addiction['type'] == 'caffeine':
                    self.modify_mental(-withdrawal_strength)
                    self.modify_stamina(-withdrawal_strength * 2)
                elif addiction['type'] == 'nicotine':
                    self.modify_mental(-withdrawal_strength * 2)
                elif addiction['type'] == 'medicine':
                    self.modify_health(-withdrawal_strength)
                
                # 检查是否戒除
                if addiction['withdrawal_time'] > addiction.get('withdrawal_duration', 168):
                    self.addictions.remove(addiction)
                    self.game.add_game_log(f"你成功戒除了{addiction['name']}的成瘾！")
    
    def update_status_effects(self, hours):
        """更新状态效果"""
        # 更新增益效果
        for buff in self.buffs[:]:
            buff['duration'] -= hours
            if buff['duration'] <= 0:
                self.buffs.remove(buff)
                self.game.add_game_log(f"{buff['name']}效果消失了。")
        
        # 更新减益效果
        for debuff in self.debuffs[:]:
            debuff['duration'] -= hours
            if debuff['duration'] <= 0:
                self.debuffs.remove(debuff)
                self.game.add_game_log(f"{debuff['name']}效果消失了。")
    
    def daily_recovery(self):
        """每日恢复"""
        # 基础恢复
        health_recovery = min(10, self.max_health - self.health)
        mental_recovery = min(15, self.max_mental - self.mental)
        
        self.modify_health(health_recovery)
        self.modify_mental(mental_recovery)
        
        # 技能经验增长
        for skill in self.skills:
            self.gain_skill_exp(skill, 1)
    
    def daily_consumption(self):
        """每日消耗"""
        # 消耗食物和水
        if self.inventory.get('food', 0) > 0:
            self.remove_item('food', 1)
        else:
            self.modify_health(-15)
            self.game.add_game_log("警告：你没有食物了，生命值减少！")
        
        if self.inventory.get('water', 0) > 0:
            self.remove_item('water', 1)
        else:
            self.modify_health(-10)
            self.modify_stamina(-20)
            self.game.add_game_log("警告：你没有水了，生命值和体力减少！")
        
        # 更新统计数据
        self.stats['days_survived'] += 1
    
    def add_item(self, item_id, quantity=1):
        """添加物品到背包"""
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity
        logging.info(f"获得物品: {item_id} x{quantity}")
        return True
    
    def remove_item(self, item_id, quantity=1):
        """从背包移除物品"""
        if item_id not in self.inventory or self.inventory[item_id] < quantity:
            return False
        self.inventory[item_id] -= quantity
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
        logging.info(f"消耗物品: {item_id} x{quantity}")
        return True
    
    def has_item(self, item_id, quantity=1):
        """检查是否有指定物品"""
        return self.inventory.get(item_id, 0) >= quantity
    
    def get_item_quantity(self, item_id):
        """获取物品数量"""
        return self.inventory.get(item_id, 0)
    
    def craft_item(self, recipe):
        """制作物品"""
        # 检查材料是否足够
        for material, amount in recipe['materials'].items():
            if not self.has_item(material, amount):
                return {
                    'success': False,
                    'message': f"材料不足，需要{amount}个{self.game.items.get_item_name(material)}"
                }
        
        # 消耗材料
        for material, amount in recipe['materials'].items():
            self.remove_item(material, amount)
        
        # 获得成品
        for product, amount in recipe['products'].items():
            self.add_item(product, amount)
        
        # 增加制作技能经验
        self.gain_skill_exp('crafting', recipe.get('exp', 10))
        
        # 更新统计数据
        self.stats['items_crafted'] += 1
        
        return {
            'success': True,
            'message': f"成功制作了{recipe['name']}！"
        }
    
    def use_item(self, item_id):
        """使用物品"""
        item_data = self.game.items.get_item_data(item_id)
        if not item_data:
            return {'success': False, 'message': '未知物品'}
        
        # 检查物品数量
        if not self.has_item(item_id):
            return {'success': False, 'message': '物品数量不足'}
        
        # 根据物品类型处理效果
        item_type = item_data.get('type')
        message = f"使用了{item_data['name']}"
        
        if item_type == 'medicine':
            # 医疗物品效果
            health_restore = item_data.get('health_restore', 0)
            mental_restore = item_data.get('mental_restore', 0)
            
            self.modify_health(health_restore)
            self.modify_mental(mental_restore)
            
            message += f"，恢复了{health_restore}生命值和{mental_restore}精神值"
            
            # 检查成瘾性
            if item_data.get('addictive', False):
                self.add_addiction({
                    'type': 'medicine',
                    'name': item_data['name'],
                    'withdrawal_time': 0,
                    'withdrawal_duration': 168  # 7天
                })
        
        elif item_type == 'food':
            # 食物效果
            health_restore = item_data.get('health_restore', 0)
            stamina_restore = item_data.get('stamina_restore', 0)
            
            self.modify_health(health_restore)
            self.modify_stamina(stamina_restore)
            
            message += f"，恢复了{health_restore}生命值和{stamina_restore}体力"
        
        elif item_type == 'drink':
            # 饮品效果
            stamina_restore = item_data.get('stamina_restore', 0)
            mental_restore = item_data.get('mental_restore', 0)
            
            self.modify_stamina(stamina_restore)
            self.modify_mental(mental_restore)
            
            message += f"，恢复了{stamina_restore}体力和{mental_restore}精神值"
            
            # 咖啡因成瘾检查
            if item_data.get('caffeine', 0) > 0:
                self.add_addiction({
                    'type': 'caffeine',
                    'name': item_data['name'],
                    'withdrawal_time': 0,
                    'withdrawal_duration': 120  # 5天
                })
        
        # 消耗物品
        self.remove_item(item_id, 1)
        
        return {'success': True, 'message': message}
    
    def add_addiction(self, addiction_data):
        """添加成瘾"""
        # 检查是否已有同类型成瘾
        for existing in self.addictions:
            if existing['type'] == addiction_data['type']:
                existing['withdrawal_time'] = 0  # 重置戒断时间
                return
        
        self.addictions.append(addiction_data)
        self.game.add_game_log(f"警告：你对{addiction_data['name']}产生了依赖！")
    
    def add_buff(self, buff_data):
        """添加增益效果"""
        self.buffs.append(buff_data)
        self.game.add_game_log(f"获得了{buff_data['name']}效果！")
    
    def add_debuff(self, debuff_data):
        """添加减益效果"""
        self.debuffs.append(debuff_data)
        self.game.add_game_log(f"受到了{debuff_data['name']}效果！")
    
    def gain_skill_exp(self, skill, exp_amount):
        """获得技能经验"""
        if skill not in self.skill_exp:
            self.skill_exp[skill] = 0
        
        self.skill_exp[skill] += exp_amount
        
        # 检查升级
        exp_required = self.skills[skill] * 100
        if self.skill_exp[skill] >= exp_required:
            self.skills[skill] += 1
            self.skill_exp[skill] = 0
            self.game.add_game_log(f"{skill}技能提升到了{self.skills[skill]}级！")
    
    def equip_item(self, item_id, slot):
        """装备物品"""
        item_data = self.game.items.get_item_data(item_id)
        if not item_data:
            return False
        
        # 检查物品类型是否匹配装备槽
        if item_data.get('equip_slot') != slot:
            return False
        
        # 卸下当前装备
        old_item = self.equipment[slot]
        if old_item:
            self.add_item(old_item)
        
        # 装备新物品
        self.equipment[slot] = item_id
        self.remove_item(item_id, 1)
        
        self.game.add_game_log(f"装备了{item_data['name']}")
        return True
    
    def unequip_item(self, slot):
        """卸下装备"""
        item_id = self.equipment[slot]
        if not item_id:
            return False
        
        item_data = self.game.items.get_item_data(item_id)
        if item_data:
            self.add_item(item_id)
            self.equipment[slot] = None
            self.game.add_game_log(f"卸下了{item_data['name']}")
        return True
    
    def get_total_stats(self):
        """获取总属性（包括装备加成）"""
        base_stats = {
            'strength': self.strength,
            'agility': self.agility,
            'intelligence': self.intelligence,
            'endurance': self.endurance,
            'luck': self.luck
        }
        
        # 计算装备加成
        for slot, item_id in self.equipment.items():
            if item_id:
                item_data = self.game.items.get_item_data(item_id)
                if item_data and 'effects' in item_data:
                    for effect in item_data['effects']:
                        if effect['type'] == 'stat_bonus':
                            base_stats[effect['stat']] += effect['value']
        
        return base_stats
    
    def get_combat_stats(self):
        """获取战斗相关属性"""
        total_stats = self.get_total_stats()
        
        # 应用疲劳减益
        fatigue_penalty = 1.0
        if self.fatigue > 50:
            fatigue_penalty = 1.0 - (self.fatigue - 50) / 100
        
        return {
            'attack': (total_stats['strength'] * 2 + total_stats['agility']) * fatigue_penalty,
            'defense': (total_stats['endurance'] * 2 + total_stats['agility']) * fatigue_penalty,
            'accuracy': (total_stats['agility'] * 3 + total_stats['luck']) * fatigue_penalty,
            'dodge': (total_stats['agility'] * 2 + total_stats['luck']) * fatigue_penalty,
            'critical': total_stats['luck'] * 2
        }
    
    def sleep(self, hours):
        """睡觉"""
        self.last_sleep_time = self.game.game_time
        self.continuous_awake_hours = 0
        
        # 环境因素影响恢复效果
        location = self.game.world.get_current_location()
        if location.safety_level >= 8:
            multiplier = 1.5
        elif location.safety_level <= 3:
            multiplier = 0.5
        else:
            multiplier = 1.0
        
        stamina_recovery = min(50 * multiplier, self.max_stamina - self.stamina)
        health_recovery = min(25 * multiplier, self.max_health - self.health)
        mental_recovery = min(40 * multiplier, self.max_mental - self.mental)
        
        self.modify_stamina(stamina_recovery)
        self.modify_health(health_recovery)
        self.modify_mental(mental_recovery)
        self.modify_fatigue(-hours * 10)  # 睡眠减轻疲劳
        
        return {
            'stamina_recovery': stamina_recovery,
            'health_recovery': health_recovery,
            'mental_recovery': mental_recovery
        }