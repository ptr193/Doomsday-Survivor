# -*- coding: utf-8 -*-

import random
import logging

class Player:
    def __init__(self, game):
        self.game = game
        self.initialized = False
        
        self.name = "未知"
        self.character_class = "survivor"
        self.health = 100
        self.max_health = 100
        self.stamina = 100
        self.max_stamina = 100
        self.mental = 100
        self.max_mental = 100
        self.strength = 5
        self.agility = 5
        self.intelligence = 5
        self.endurance = 5
        self.luck = 5
        self.buffs = []
        self.debuffs = []
        self.addictions = []
        self.fatigue = 0
        self.max_fatigue = 100
        self.night_penalty = False
        self.stamina_modifier = 1.0
        self.equipment = {'weapon': None, 'head': None, 'chest': None, 'legs': None, 'backpack': None, 'accessory1': None, 'accessory2': None}
        self.inventory = {}
        self.item_durability = {}
        self.money = 0
        self.radiation = 0
        self.max_radiation = 100
        self.skills = {}
        self.skill_exp = {}
        self.location = "starting_area"
        self.discovered_locations = []
        self.last_sleep_time = None
        self.continuous_awake_hours = 0
        self.stats = {}
        
        

    def initialize(self, character_data):
        try:
            self.name = character_data['name']
            self.character_class = character_data.get('class', 'survivor')
            self.health = character_data.get('health', 100)
            self.max_health = character_data.get('max_health', 100)
            self.stamina = character_data.get('stamina', 100)
            self.max_stamina = character_data.get('max_stamina', 100)
            self.mental = character_data.get('mental', 100)
            self.max_mental = character_data.get('max_mental', 100)
            self.strength = character_data.get('strength', 5)
            self.agility = character_data.get('agility', 5)
            self.intelligence = character_data.get('intelligence', 5)
            self.endurance = character_data.get('endurance', 5)
            self.luck = character_data.get('luck', 5)
            self.buffs = []
            self.debuffs = []
            self.addictions = []
            self.fatigue = 0
            self.max_fatigue = 100
            self.night_penalty = False
            self.stamina_modifier = 1.0
            self.equipment = {'weapon': None, 'head': None, 'chest': None, 'legs': None, 'backpack': None, 'accessory1': None, 'accessory2': None}
            self.inventory = {'food': 5, 'water': 5, 'materials': 10, 'medicine': 2, 'seeds': 6, 'wood': 4, 'wooden_hoe': 1}
            self.item_durability = {}
            self.money = character_data.get('money', 50)
            self.radiation = 0
            self.max_radiation = 100
            self.skills = {'survival': 1, 'combat': 1, 'crafting': 1, 'farming': 1, 'medical': 1, 'social': 1, 'intelligence': 1, 'mental': 1}
            self.skill_exp = {'survival': 0, 'combat': 0, 'crafting': 0, 'farming': 0, 'medical': 0, 'social': 0, 'intelligence': 0, 'mental': 0}
            self.location = "starting_area"
            self.discovered_locations = ["starting_area"]
            self.last_sleep_time = None
            self.continuous_awake_hours = 0
            self.stats = {'days_survived': 0, 'enemies_defeated': 0, 'locations_discovered': 1, 'items_crafted': 0, 'crops_harvested': 0, 'distance_traveled': 0, 'quests_completed': 0, 'npcs_met': 0}
            self.initialized = True
            logging.info(f"玩家角色初始化完成: {self.name}")
        except Exception as e:
            logging.error(f"玩家初始化失败: {e}")
            raise

    def load_data(self, save_data):
        try:
            self.name = save_data.get('name', '幸存者')
            self.character_class = save_data.get('character_class', 'survivor')
            self.health = save_data.get('health', 100)
            self.max_health = save_data.get('max_health', 100)
            self.stamina = save_data.get('stamina', 100)
            self.max_stamina = save_data.get('max_stamina', 100)
            self.mental = save_data.get('mental', 100)
            self.max_mental = save_data.get('max_mental', 100)
            self.strength = save_data.get('strength', 5)
            self.agility = save_data.get('agility', 5)
            self.intelligence = save_data.get('intelligence', 5)
            self.endurance = save_data.get('endurance', 5)
            self.luck = save_data.get('luck', 5)
            self.buffs = save_data.get('buffs', [])
            self.debuffs = save_data.get('debuffs', [])
            self.addictions = save_data.get('addictions', [])
            self.fatigue = save_data.get('fatigue', 0)
            self.max_fatigue = save_data.get('max_fatigue', 100)
            self.night_penalty = save_data.get('night_penalty', False)
            self.stamina_modifier = save_data.get('stamina_modifier', 1.0)
            self.equipment = save_data.get('equipment', {'weapon': None, 'head': None, 'chest': None, 'legs': None, 'backpack': None, 'accessory1': None, 'accessory2': None})
            self.inventory = save_data.get('inventory', {})
            self.item_durability = save_data.get('item_durability', {})
            self.money = save_data.get('money', 0)
            self.radiation = save_data.get('radiation', 0)
            self.max_radiation = save_data.get('max_radiation', 100)
            self.skills = save_data.get('skills', {})
            self.skill_exp = save_data.get('skill_exp', {})
            self.location = save_data.get('location', 'starting_area')
            self.discovered_locations = save_data.get('discovered_locations', ['starting_area'])
            self.last_sleep_time = save_data.get('last_sleep_time')
            self.continuous_awake_hours = save_data.get('continuous_awake_hours', 0)
            self.stats = save_data.get('stats', {})
            self.initialized = True
            logging.info(f"玩家数据加载完成: {self.name}")
        except Exception as e:
            logging.error(f"加载玩家数据失败: {e}")
            raise

    def get_save_data(self):
        return {
            'name': self.name, 'character_class': self.character_class,
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
            'item_durability': self.item_durability,
            'money': self.money,
            'radiation': self.radiation,
            'max_radiation': self.max_radiation,
            'skills': self.skills,
            'skill_exp': self.skill_exp,
            'location': self.location,
            'discovered_locations': self.discovered_locations,
            'last_sleep_time': self.last_sleep_time,
            'continuous_awake_hours': self.continuous_awake_hours,
            'stats': self.stats
        }

    # 修改属性方法（保持不变）
    def modify_health(self, amount):
        old = self.health
        self.health = max(0, min(self.max_health, self.health + amount))
        if amount < 0:
            logging.info(f"玩家生命值减少: {old} -> {self.health} (-{abs(amount)})")
        elif amount > 0:
            logging.info(f"玩家生命值恢复: {old} -> {self.health} (+{amount})")
        return self.health

    def modify_stamina(self, amount):
        effective_amount = amount * self.stamina_modifier
        if self.night_penalty and effective_amount < 0:
            effective_amount *= 1.2
        if effective_amount < 0:
            effective_amount *= self.get_encumbrance_stamina_multiplier()
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
        old = self.mental
        self.mental = max(0, min(self.max_mental, self.mental + amount))
        if amount < 0:
            logging.info(f"玩家精神值减少: {old} -> {self.mental} (-{abs(amount)})")
        elif amount > 0:
            logging.info(f"玩家精神值恢复: {old} -> {self.mental} (+{amount})")
        return self.mental

    def modify_fatigue(self, amount):
        old = self.fatigue
        self.fatigue = max(0, min(self.max_fatigue, self.fatigue + amount))
        if amount > 0:
            if self.fatigue >= 80 and old < 80:
                self.game.add_game_log("警告：你感到极度疲劳，行动困难！")
                self.add_debuff({"name": "极度疲劳", "type": "fatigue", "duration": 24, "attack_penalty": 0.5, "stamina_regen_penalty": 0.5})
            logging.info(f"玩家疲劳增加: {old} -> {self.fatigue} (+{amount})")
        elif amount < 0:
            if self.fatigue < 80 and old >= 80:
                self.debuffs = [d for d in self.debuffs if d.get('name') != '极度疲劳']
            logging.info(f"玩家疲劳减少: {old} -> {self.fatigue} ({amount})")
        return self.fatigue

    def handle_time_passage(self, hours):
        self.continuous_awake_hours += hours
        if self.continuous_awake_hours > 24:
            mental_penalty = (self.continuous_awake_hours - 24) * 0.5
            self.modify_mental(-mental_penalty)
            if self.continuous_awake_hours > 48:
                self.game.add_game_log("警告：你已经很久没有睡觉了！")
        fatigue_gain = hours * 2
        self.modify_fatigue(fatigue_gain)
        self.handle_addictions(hours)
        self.update_status_effects(hours)

    def handle_addictions(self, hours):
        for addiction in self.addictions[:]:
            addiction['withdrawal_time'] += hours
            if addiction['withdrawal_time'] > 24:
                withdrawal_strength = min(5, (addiction['withdrawal_time'] - 24) // 12)
                if addiction['type'] == 'caffeine':
                    self.modify_mental(-withdrawal_strength)
                    self.modify_stamina(-withdrawal_strength * 2)
                elif addiction['type'] == 'nicotine':
                    self.modify_mental(-withdrawal_strength * 2)
                elif addiction['type'] == 'medicine':
                    self.modify_health(-withdrawal_strength)
                if addiction['withdrawal_time'] > addiction.get('withdrawal_duration', 168):
                    self.addictions.remove(addiction)
                    self.game.add_game_log(f"你成功戒除了{addiction['name']}的成瘾！")

    def update_status_effects(self, hours):
        for buff in self.buffs[:]:
            buff['duration'] -= hours
            if buff['duration'] <= 0:
                self.buffs.remove(buff)
                self.game.add_game_log(f"{buff['name']}效果消失了。")
        for debuff in self.debuffs[:]:
            debuff['duration'] -= hours
            if debuff['duration'] <= 0:
                self.debuffs.remove(debuff)
                self.game.add_game_log(f"{debuff['name']}效果消失了。")

    def daily_recovery(self):
        health_recovery = min(10, self.max_health - self.health)
        mental_recovery = min(15, self.max_mental - self.mental)
        self.modify_health(health_recovery)
        self.modify_mental(mental_recovery)
        for skill in self.skills:
            self.gain_skill_exp(skill, 1)

    def daily_consumption(self):
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
        self.stats['days_survived'] += 1

    def get_item_weight(self, item_id):
        if not hasattr(self.game, 'items') or not self.game.items:
            return 0.5
        data = self.game.items.get_item_data(item_id)
        return float((data or {}).get('weight', 0.5) or 0.5)

    def get_inventory_weight(self):
        total = 0.0
        for item_id, quantity in self.inventory.items():
            total += self.get_item_weight(item_id) * max(0, quantity)
        for item_id in self.equipment.values():
            if item_id:
                total += self.get_item_weight(item_id)
        return round(total, 1)

    def get_max_carry_weight(self):
        capacity = 20 + self.strength * 4
        backpack = self.equipment.get('backpack')
        if backpack and hasattr(self.game, 'items') and self.game.items:
            data = self.game.items.get_item_data(backpack)
            for effect in (data or {}).get('effects', []):
                if effect.get('type') == 'carry_capacity':
                    capacity += int(effect.get('value', 0))
        return capacity

    def is_overencumbered(self):
        return self.get_inventory_weight() > self.get_max_carry_weight()

    def get_encumbrance_stamina_multiplier(self):
        max_w = max(1.0, float(self.get_max_carry_weight()))
        ratio = self.get_inventory_weight() / max_w
        if ratio > 1.2:
            return 2.0
        if ratio > 1.0:
            return 1.5
        return 1.0

    def can_carry(self, item_id, quantity=1):
        extra = self.get_item_weight(item_id) * max(0, quantity)
        return self.get_inventory_weight() + extra <= self.get_max_carry_weight() * 1.2

    def add_item(self, item_id, quantity=1, force=False):
        if not force and not self.can_carry(item_id, quantity):
            if hasattr(self.game, 'add_game_log'):
                self.game.add_game_log("负重已满，无法再携带更多物品。")
            return False
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity
        max_d = self.get_item_max_durability(item_id)
        if max_d and item_id not in self.item_durability:
            self.item_durability[item_id] = max_d
        logging.info(f"获得物品: {item_id} x{quantity}")
        if hasattr(self.game, 'quests') and self.game.quests:
            self.game.quests.update_quest_progress('item_collected', item_id=item_id, quantity=quantity)
        return True

    def add_money(self, amount):
        self.money = max(0, self.money + int(amount))
        return self.money

    def spend_money(self, amount):
        amount = int(amount)
        if self.money < amount:
            return False
        self.money -= amount
        return True

    def remove_item(self, item_id, quantity=1):
        if item_id not in self.inventory or self.inventory[item_id] < quantity:
            return False
        self.inventory[item_id] -= quantity
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
            if item_id not in self.equipment.values():
                self.item_durability.pop(item_id, None)
        logging.info(f"消耗物品: {item_id} x{quantity}")
        return True

    def owns_item(self, item_id):
        return self.has_item(item_id) or item_id in self.equipment.values()

    def get_item_max_durability(self, item_id):
        item_data = self.game.items.get_item_data(item_id) if hasattr(self.game, 'items') else None
        if not item_data:
            return 0
        return int(item_data.get('durability', 0) or 0)

    def get_item_durability(self, item_id):
        max_d = self.get_item_max_durability(item_id)
        if not max_d:
            return None
        return self.item_durability.get(item_id, max_d)

    def degrade_item(self, item_id, amount=1):
        max_d = self.get_item_max_durability(item_id)
        if not max_d or not item_id:
            return False
        current = self.item_durability.get(item_id, max_d) - amount
        item_name = self.game.items.get_item_name(item_id)
        if current <= 0:
            self.item_durability.pop(item_id, None)
            broken_slot = None
            for slot, equipped in self.equipment.items():
                if equipped == item_id:
                    broken_slot = slot
                    break
            if broken_slot:
                self.equipment[broken_slot] = None
            elif self.has_item(item_id):
                self.remove_item(item_id, 1)
            self.game.add_game_log(f"{item_name}损坏了！")
            return True
        self.item_durability[item_id] = current
        if current <= max(3, max_d // 10):
            self.game.add_game_log(f"{item_name}几乎损坏了（耐久{current}/{max_d}）。")
        return False

    def get_repair_cost(self, item_id):
        max_d = self.get_item_max_durability(item_id)
        current = self.get_item_durability(item_id)
        if not max_d or current is None:
            return None
        missing = max(0, max_d - current)
        if missing <= 0:
            return {'metal': 0, 'materials': 0, 'missing': 0}
        skill = self.skills.get('crafting', 1)
        metal_cost = max(1, missing // 15 - skill // 5)
        mat_cost = max(1, missing // 20 - skill // 6)
        return {'metal': metal_cost, 'materials': mat_cost, 'missing': missing}

    def repair_item(self, item_id):
        max_d = self.get_item_max_durability(item_id)
        if not max_d:
            return {'success': False, 'message': '该物品无法修理'}
        if not self.owns_item(item_id):
            return {'success': False, 'message': '你没有这件物品'}
        current = self.get_item_durability(item_id)
        if current >= max_d:
            return {'success': False, 'message': '该物品无需修理'}
        cost = self.get_repair_cost(item_id)
        if not self.has_item('metal', cost['metal']) or not self.has_item('materials', cost['materials']):
            return {'success': False, 'message': f"材料不足，需要金属x{cost['metal']}、材料x{cost['materials']}"}
        if self.stamina < 10:
            return {'success': False, 'message': '体力不足，无法修理'}
        self.remove_item('metal', cost['metal'])
        self.remove_item('materials', cost['materials'])
        self.modify_stamina(-10)
        skill = self.skills.get('crafting', 1)
        bonus = 0
        location = self.game.world.get_current_location() if hasattr(self.game, 'world') else None
        if location and 'workbench' in (getattr(location, 'structures', None) or []):
            bonus = 8
        restored = min(max_d, current + 12 + skill * 6 + bonus)
        self.item_durability[item_id] = restored
        self.gain_skill_exp('crafting', 8)
        if hasattr(self.game, 'quests') and self.game.quests:
            self.game.quests.update_quest_progress('item_repaired', item_id=item_id)
        name = self.game.items.get_item_name(item_id)
        return {'success': True, 'message': f"修理了{name}，耐久 {restored}/{max_d}"}

    def has_item(self, item_id, quantity=1):
        return self.inventory.get(item_id, 0) >= quantity

    def get_item_quantity(self, item_id):
        return self.inventory.get(item_id, 0)

    # 原 craft_item 保持不变，新增带挡级的版本
    def craft_item(self, recipe):
        for material, amount in recipe['materials'].items():
            if not self.has_item(material, amount):
                return {'success': False, 'message': f"材料不足，需要{amount}个{self.game.items.get_item_name(material)}"}
        for material, amount in recipe['materials'].items():
            self.remove_item(material, amount)
        for product, amount in recipe['products'].items():
            self.add_item(product, amount, force=True)
        self.gain_skill_exp('crafting', recipe.get('exp', 10))
        self.stats['items_crafted'] += 1
        if hasattr(self.game, 'quests') and self.game.quests:
            for product in recipe.get('products', {}):
                self.game.quests.update_quest_progress('item_crafted', item_id=product)
        if hasattr(self.game, 'achievements') and self.game.achievements:
            self.game.achievements.check_crafting_achievements()
        return {'success': True, 'message': f"成功制作了{recipe['name']}！"}

    def craft_item_with_tier(self, recipe_id, tier, recipe_data):
        materials = recipe_data['materials']
        products = recipe_data['products']
        for mat, amt in materials.items():
            if not self.has_item(mat, amt):
                return {'success': False, 'message': f"材料不足，需要{amt}个{self.game.items.get_item_name(mat)}"}
        for mat, amt in materials.items():
            self.remove_item(mat, amt)
        for prod, amt in products.items():
            self.add_item(prod, amt, force=True)
        exp = recipe_data.get('exp', 10) * (tier // 2 + 0.5)
        self.gain_skill_exp('crafting', int(exp))
        self.stats['items_crafted'] += 1
        if hasattr(self.game, 'quests') and self.game.quests:
            for product in products:
                self.game.quests.update_quest_progress('item_crafted', item_id=product)
        if hasattr(self.game, 'achievements') and self.game.achievements:
            self.game.achievements.check_crafting_achievements()
        return {'success': True, 'message': f"成功制作了{recipe_data['name']}！"}

    def enchant_item(self, item_id, enchant_data):
        if not self.has_item(item_id):
            return None
        self.remove_item(item_id, 1)
        new_id = self.game.items.enchant_item(item_id, enchant_data)
        if new_id:
            self.add_item(new_id, 1)
            self.game.add_game_log(f"成功为{self.game.items.get_item_name(item_id)}附魔！")
            return new_id
        else:
            self.add_item(item_id, 1)
            return None

    def use_item(self, item_id):
        item_data = self.game.items.get_item_data(item_id)
        if not item_data:
            return {'success': False, 'message': '未知物品'}
        if not self.has_item(item_id):
            return {'success': False, 'message': '物品数量不足'}
        item_type = item_data.get('type')
        message = f"使用了{item_data['name']}"
        if item_type == 'medicine':
            health_restore = item_data.get('health_restore', 0)
            mental_restore = item_data.get('mental_restore', 0)
            self.modify_health(health_restore)
            self.modify_mental(mental_restore)
            message += f"，恢复了{health_restore}生命值和{mental_restore}精神值"
            if item_data.get('addictive', False):
                self.add_addiction({'type': 'medicine', 'name': item_data['name'], 'withdrawal_time': 0, 'withdrawal_duration': 168})
        elif item_type == 'food':
            health_restore = item_data.get('health_restore', 0)
            stamina_restore = item_data.get('stamina_restore', 0)
            self.modify_health(health_restore)
            self.modify_stamina(stamina_restore)
            message += f"，恢复了{health_restore}生命值和{stamina_restore}体力"
        elif item_type == 'drink':
            stamina_restore = item_data.get('stamina_restore', 0)
            mental_restore = item_data.get('mental_restore', 0)
            self.modify_stamina(stamina_restore)
            self.modify_mental(mental_restore)
            message += f"，恢复了{stamina_restore}体力和{mental_restore}精神值"
            if item_data.get('caffeine', 0) > 0:
                self.add_addiction({'type': 'caffeine', 'name': item_data['name'], 'withdrawal_time': 0, 'withdrawal_duration': 120})
        self.remove_item(item_id, 1)
        return {'success': True, 'message': message}

    def add_addiction(self, addiction_data):
        for existing in self.addictions:
            if existing['type'] == addiction_data['type']:
                existing['withdrawal_time'] = 0
                return
        self.addictions.append(addiction_data)
        self.game.add_game_log(f"警告：你对{addiction_data['name']}产生了依赖！")

    def add_buff(self, buff_data):
        self.buffs.append(buff_data)
        self.game.add_game_log(f"获得了{buff_data['name']}效果！")

    def add_debuff(self, debuff_data):
        self.debuffs.append(debuff_data)
        self.game.add_game_log(f"受到了{debuff_data['name']}效果！")

    def gain_skill_exp(self, skill, exp_amount):
        if skill not in self.skill_exp:
            self.skill_exp[skill] = 0
        self.skill_exp[skill] += exp_amount
        exp_required = self.skills[skill] * 100
        if self.skill_exp[skill] >= exp_required:
            self.skills[skill] += 1
            self.skill_exp[skill] = 0
            self.game.add_game_log(f"{skill}技能提升到了{self.skills[skill]}级！")

    def equip_item(self, item_id, slot):
        item_data = self.game.items.get_item_data(item_id)
        if not item_data or item_data.get('equip_slot') != slot:
            return False
        old_item = self.equipment[slot]
        if old_item:
            self.add_item(old_item, force=True)
        self.equipment[slot] = item_id
        self.remove_item(item_id, 1)
        self.game.add_game_log(f"装备了{item_data['name']}")
        return True

    def unequip_item(self, slot):
        item_id = self.equipment[slot]
        if not item_id:
            return False
        item_data = self.game.items.get_item_data(item_id)
        if item_data:
            self.add_item(item_id, force=True)
            self.equipment[slot] = None
            self.game.add_game_log(f"卸下了{item_data['name']}")
        return True

    def get_total_stats(self):
        base_stats = {'strength': self.strength, 'agility': self.agility, 'intelligence': self.intelligence, 'endurance': self.endurance, 'luck': self.luck}
        for slot, item_id in self.equipment.items():
            if item_id:
                item_data = self.game.items.get_item_data(item_id)
                if item_data and 'effects' in item_data:
                    for effect in item_data['effects']:
                        if effect['type'] == 'stat_bonus':
                            base_stats[effect['stat']] += effect['value']
        return base_stats

    def get_combat_stats(self):
        total_stats = self.get_total_stats()
        fatigue_penalty = 1.0
        if self.fatigue > 50:
            fatigue_penalty = 1.0 - (self.fatigue - 50) / 100
        encumbrance_penalty = 0.8 if self.is_overencumbered() else 1.0
        night_penalty = 0.85 if self.night_penalty else 1.0
        return {
            'attack': (total_stats['strength'] * 2 + total_stats['agility']) * fatigue_penalty * night_penalty,
            'defense': (total_stats['endurance'] * 2 + total_stats['agility']) * fatigue_penalty,
            'accuracy': (total_stats['agility'] * 3 + total_stats['luck']) * fatigue_penalty * encumbrance_penalty * night_penalty,
            'dodge': (total_stats['agility'] * 2 + total_stats['luck']) * fatigue_penalty * encumbrance_penalty * night_penalty,
            'critical': total_stats['luck'] * 2
        }

    def sleep(self, hours):
        self.last_sleep_time = self.game.game_time.isoformat() if self.game.game_time else None
        self.continuous_awake_hours = 0
        location = self.game.world.get_current_location()
        safety = location.safety_level if location else 5
        if location and 'shelter' in (getattr(location, 'structures', None) or []):
            safety = min(10, safety + 2)
        multiplier = 1.5 if safety >= 8 else 0.5 if safety <= 3 else 1.0
        stamina_recovery = min(50 * multiplier, self.max_stamina - self.stamina)
        health_recovery = min(25 * multiplier, self.max_health - self.health)
        mental_recovery = min(40 * multiplier, self.max_mental - self.mental)
        self.modify_stamina(stamina_recovery)
        self.modify_health(health_recovery)
        self.modify_mental(mental_recovery)
        self.modify_fatigue(-hours * 10)
        return {'stamina_recovery': stamina_recovery, 'health_recovery': health_recovery, 'mental_recovery': mental_recovery}