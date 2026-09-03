# -*- coding: utf-8 -*-

import random
import logging
import json
import os

class ItemSystem:
    def __init__(self, game):
        self.game = game
        self.items = {}
        self.recipes = {}
        self.initialized = False

    def initialize(self):
        try:
            self.load_items_from_file()
            self.initialized = True
            logging.info("物品系统初始化完成")
        except Exception as e:
            logging.error(f"从文件加载物品失败: {e}，使用硬编码数据")
            self.create_items()
            self.create_recipes()
            self.initialized = True

    def load_items_from_file(self):
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        items_file = os.path.join(data_dir, 'items.json')
        if not os.path.exists(items_file):
            raise FileNotFoundError(f"物品数据文件不存在: {items_file}")
        with open(items_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.items = data.get('items', {})
        self.recipes = data.get('recipes', {})
        logging.info(f"从 {items_file} 加载了 {len(self.items)} 种物品和 {len(self.recipes)} 个配方")

    def create_items(self):
        self.items = {
            'food': {'id': 'food', 'name': '食物', 'type': 'food', 'description': '基本的食物', 'health_restore': 10, 'stamina_restore': 5, 'weight': 0.5, 'value': 5, 'stackable': True, 'max_stack': 20},
            'water': {'id': 'water', 'name': '水', 'type': 'drink', 'description': '干净的水源', 'stamina_restore': 15, 'weight': 1.0, 'value': 3, 'stackable': True, 'max_stack': 10},
            'materials': {'id': 'materials', 'name': '材料', 'type': 'material', 'description': '基础制作材料', 'weight': 1.0, 'value': 2, 'stackable': True, 'max_stack': 50},
            'wood': {'id': 'wood', 'name': '木材', 'type': 'material', 'description': '可用于建造和燃料', 'weight': 2.0, 'value': 1, 'stackable': True, 'max_stack': 30},
            'medicine': {'id': 'medicine', 'name': '药品', 'type': 'medicine', 'description': '基础医疗用品', 'health_restore': 20, 'weight': 0.3, 'value': 10, 'stackable': True, 'max_stack': 15},
        }
        logging.info(f"创建了 {len(self.items)} 种硬编码物品")

    def create_recipes(self):
        self.recipes = {
            'make_knife': {'id': 'make_knife', 'name': '制作小刀', 'category': 'tools', 'difficulty': 1, 'materials': {'metal': 2, 'wood': 1}, 'products': {'knife': 1}, 'exp': 15, 'description': '制作一把基础小刀'},
        }
        logging.info(f"创建了 {len(self.recipes)} 个硬编码配方")

    def load_data(self, save_data):
        self.initialized = True
        logging.info("物品系统数据加载完成")

    def get_save_data(self):
        return {'items': self.items, 'recipes': self.recipes}

    def get_item_data(self, item_id):
        return self.items.get(item_id)

    def get_item_name(self, item_id):
        item = self.get_item_data(item_id)
        return item.get('name', '未知物品') if item else '未知物品'

    def get_recipe(self, recipe_id):
        return self.recipes.get(recipe_id)

    def get_recipes_by_category(self, category):
        return [r for r in self.recipes.values() if r.get('category') == category]

    def get_available_recipes(self, player_skills):
        available = []
        for recipe in self.recipes.values():
            difficulty = recipe.get('difficulty', 1)
            required_skill = difficulty * 10
            player_crafting_skill = player_skills.get('crafting', 1) * 10
            if player_crafting_skill >= required_skill:
                available.append(recipe)
        return available

    def can_craft(self, recipe_id, player_inventory):
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return False
        for material, amount in recipe['materials'].items():
            if player_inventory.get(material, 0) < amount:
                return False
        return True

    def get_crafting_cost(self, recipe_id):
        recipe = self.get_recipe(recipe_id)
        return recipe.get('materials', {}) if recipe else {}

    def get_item_value(self, item_id, quantity=1):
        item = self.get_item_data(item_id)
        if not item:
            return 0
        return item.get('value', 0) * quantity

    def generate_loot(self, enemy_level, location_type):
        loot = {}
        if random.randint(1, 100) <= 70:
            loot['materials'] = random.randint(1, 3)
        if enemy_level >= 3:
            if random.randint(1, 100) <= 40:
                loot['medicine'] = random.randint(1, 2)
        if enemy_level >= 5:
            if random.randint(1, 100) <= 25:
                weapon = random.choice(['knife', 'baseball_bat', 'pistol'])
                loot[weapon] = 1
        if location_type == 'forest' and random.randint(1, 100) <= 30:
            loot['rare_herbs'] = random.randint(1, 2)
        elif location_type == 'mountain' and random.randint(1, 100) <= 25:
            loot['rare_minerals'] = random.randint(1, 2)
        elif location_type == 'urban' and random.randint(1, 100) <= 35:
            loot['electronic'] = random.randint(1, 3)
        return loot

    def get_item_categories(self):
        categories = set()
        for item in self.items.values():
            categories.add(item.get('type', 'other'))
        return sorted(list(categories))

    def get_items_by_category(self, category):
        return [item for item in self.items.values() if item.get('type') == category]

    def validate_item_stack(self, item_id, quantity):
        item = self.get_item_data(item_id)
        if not item:
            return 0
        max_stack = item.get('max_stack', 1)
        return min(quantity, max_stack)

    def get_item_description(self, item_id):
        item = self.get_item_data(item_id)
        if not item:
            return "未知物品"
        desc = item.get('description', '')
        effects = []
        if item.get('health_restore', 0) > 0:
            effects.append(f"恢复生命: {item['health_restore']}")
        if item.get('stamina_restore', 0) > 0:
            effects.append(f"恢复体力: {item['stamina_restore']}")
        if item.get('mental_restore', 0) > 0:
            effects.append(f"恢复精神: {item['mental_restore']}")
        if item.get('damage', 0) > 0:
            effects.append(f"伤害: {item['damage']}")
        if item.get('defense', 0) > 0:
            effects.append(f"防御: {item['defense']}")
        if effects:
            desc += f"\n效果: {', '.join(effects)}"
        return desc

    # 新增方法：获取带挡级的配方
    def get_recipe_with_tier(self, recipe_id, tier=2):
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return None
        base_materials = recipe['materials']
        base_products = recipe['products']
        if tier == 1:
            materials = {k: max(1, int(v * 0.5)) for k, v in base_materials.items()}
            products = {k: max(1, int(v * 0.7)) for k, v in base_products.items()}
        elif tier == 3:
            materials = {k: int(v * 1.5) for k, v in base_materials.items()}
            products = {k: int(v * 1.3) for k, v in base_products.items()}
        else:
            materials = base_materials
            products = base_products
        return {
            'materials': materials,
            'products': products,
            'exp': recipe.get('exp', 10),
            'name': recipe['name']
        }

    # 新增方法：附魔物品
    def enchant_item(self, item_id, enchantment_data):
        item = self.items.get(item_id)
        if not item:
            return None
        new_item = item.copy()
        if 'effects' not in new_item:
            new_item['effects'] = []
        new_item['effects'].append(enchantment_data)
        new_id = f"{item_id}_enchanted"
        self.items[new_id] = new_item
        return new_id