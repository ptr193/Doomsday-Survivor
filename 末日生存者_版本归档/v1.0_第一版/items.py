# -*- coding: utf-8 -*-

import random
import logging
from typing import Dict, List, Optional

class ItemSystem:
    def __init__(self, game):
        self.game = game
        self.items = {}
        self.recipes = {}
        self.initialized = False
        
    def initialize(self):
        """初始化物品系统"""
        try:
            self.create_items()
            self.create_recipes()
            self.initialized = True
            logging.info("物品系统初始化完成")
        except Exception as e:
            logging.error(f"物品系统初始化失败: {e}")
            raise
    
    def create_items(self):
        """创建所有物品"""
        # === 食物类 ===
        self.items['food'] = {
            'id': 'food',
            'name': '食物',
            'type': 'food',
            'description': '基本的食物，可以充饥',
            'health_restore': 10,
            'stamina_restore': 5,
            'weight': 0.5,
            'value': 5,
            'stackable': True,
            'max_stack': 20
        }
        
        self.items['fresh_food'] = {
            'id': 'fresh_food',
            'name': '新鲜食物',
            'type': 'food',
            'description': '新鲜的食物，营养价值更高',
            'health_restore': 20,
            'stamina_restore': 10,
            'mental_restore': 5,
            'weight': 0.5,
            'value': 10,
            'stackable': True,
            'max_stack': 10
        }
        
        self.items['canned_food'] = {
            'id': 'canned_food',
            'name': '罐头食品',
            'type': 'food',
            'description': '密封保存的罐头，保质期长',
            'health_restore': 15,
            'stamina_restore': 8,
            'weight': 1.0,
            'value': 8,
            'stackable': True,
            'max_stack': 15
        }
        
        self.items['military_ration'] = {
            'id': 'military_ration',
            'name': '军用口粮',
            'type': 'food',
            'description': '高能量的军用口粮',
            'health_restore': 25,
            'stamina_restore': 20,
            'mental_restore': 10,
            'weight': 0.8,
            'value': 15,
            'stackable': True,
            'max_stack': 10
        }
        
        self.items['energy_bar'] = {
            'id': 'energy_bar',
            'name': '能量棒',
            'type': 'food',
            'description': '快速补充能量的食品',
            'health_restore': 5,
            'stamina_restore': 30,
            'weight': 0.2,
            'value': 12,
            'stackable': True,
            'max_stack': 25
        }
        
        # === 饮品类 ===
        self.items['water'] = {
            'id': 'water',
            'name': '水',
            'type': 'drink',
            'description': '干净的水源',
            'stamina_restore': 15,
            'weight': 1.0,
            'value': 3,
            'stackable': True,
            'max_stack': 10
        }
        
        self.items['clean_water'] = {
            'id': 'clean_water',
            'name': '纯净水',
            'type': 'drink',
            'description': '经过净化的纯净水',
            'stamina_restore': 25,
            'health_restore': 5,
            'weight': 1.0,
            'value': 6,
            'stackable': True,
            'max_stack': 10
        }
        
        self.items['energy_drink'] = {
            'id': 'energy_drink',
            'name': '能量饮料',
            'type': 'drink',
            'description': '提神醒脑的功能饮料',
            'stamina_restore': 40,
            'mental_restore': 10,
            'caffeine': 1,
            'addictive': True,
            'weight': 0.5,
            'value': 15,
            'stackable': True,
            'max_stack': 8
        }
        
        self.items['herbal_tea'] = {
            'id': 'herbal_tea',
            'name': '草药茶',
            'type': 'drink',
            'description': '用草药泡制的茶，有治疗效果',
            'health_restore': 10,
            'mental_restore': 20,
            'weight': 0.3,
            'value': 8,
            'stackable': True,
            'max_stack': 12
        }
        
        self.items['coffee'] = {
            'id': 'coffee',
            'name': '咖啡',
            'type': 'drink',
            'description': '热咖啡，提神效果明显',
            'stamina_restore': 25,
            'mental_restore': 15,
            'caffeine': 2,
            'addictive': True,
            'weight': 0.3,
            'value': 10,
            'stackable': True,
            'max_stack': 10
        }
        
        # === 材料类 ===
        self.items['materials'] = {
            'id': 'materials',
            'name': '材料',
            'type': 'material',
            'description': '基础制作材料',
            'weight': 1.0,
            'value': 2,
            'stackable': True,
            'max_stack': 50
        }
        
        self.items['wood'] = {
            'id': 'wood',
            'name': '木材',
            'type': 'material',
            'description': '可用于建造和燃料',
            'weight': 2.0,
            'value': 1,
            'stackable': True,
            'max_stack': 30
        }
        
        self.items['metal'] = {
            'id': 'metal',
            'name': '金属',
            'type': 'material',
            'description': '金属材料，用于制作工具和武器',
            'weight': 3.0,
            'value': 5,
            'stackable': True,
            'max_stack': 20
        }
        
        self.items['cloth'] = {
            'id': 'cloth',
            'name': '布料',
            'type': 'material',
            'description': '纺织品，用于制作衣物',
            'weight': 0.5,
            'value': 3,
            'stackable': True,
            'max_stack': 25
        }
        
        self.items['electronic'] = {
            'id': 'electronic',
            'name': '电子元件',
            'type': 'material',
            'description': '电子设备零件',
            'weight': 0.3,
            'value': 8,
            'stackable': True,
            'max_stack': 15
        }
        
        self.items['advanced_alloy'] = {
            'id': 'advanced_alloy',
            'name': '高级合金',
            'type': 'material',
            'description': '高性能合金材料',
            'weight': 2.0,
            'value': 20,
            'stackable': True,
            'max_stack': 10
        }
        
        self.items['stone'] = {
            'id': 'stone',
            'name': '石头',
            'type': 'material',
            'description': '基础建筑材料',
            'weight': 4.0,
            'value': 1,
            'stackable': True,
            'max_stack': 25
        }
        
        self.items['plastic'] = {
            'id': 'plastic',
            'name': '塑料',
            'type': 'material',
            'description': '塑料材料，用途广泛',
            'weight': 0.5,
            'value': 2,
            'stackable': True,
            'max_stack': 30
        }
        
        # === 医疗类 ===
        self.items['medicine'] = {
            'id': 'medicine',
            'name': '药品',
            'type': 'medicine',
            'description': '基础医疗用品',
            'health_restore': 20,
            'weight': 0.3,
            'value': 10,
            'stackable': True,
            'max_stack': 15
        }
        
        self.items['bandage'] = {
            'id': 'bandage',
            'name': '绷带',
            'type': 'medicine',
            'description': '用于止血和包扎伤口',
            'health_restore': 15,
            'weight': 0.2,
            'value': 5,
            'stackable': True,
            'max_stack': 20
        }
        
        self.items['antidote'] = {
            'id': 'antidote',
            'name': '解毒剂',
            'type': 'medicine',
            'description': '解除中毒状态',
            'health_restore': 10,
            'special_effect': 'cure_poison',
            'weight': 0.3,
            'value': 15,
            'stackable': True,
            'max_stack': 10
        }
        
        self.items['antidepressant'] = {
            'id': 'antidepressant',
            'name': '抗抑郁药',
            'type': 'medicine',
            'description': '缓解精神压力',
            'mental_restore': 30,
            'addictive': True,
            'weight': 0.2,
            'value': 12,
            'stackable': True,
            'max_stack': 8
        }
        
        self.items['first_aid_kit'] = {
            'id': 'first_aid_kit',
            'name': '急救包',
            'type': 'medicine',
            'description': '完整的急救用品',
            'health_restore': 50,
            'mental_restore': 10,
            'weight': 1.0,
            'value': 25,
            'stackable': True,
            'max_stack': 5
        }
        
        self.items['radiation_pills'] = {
            'id': 'radiation_pills',
            'name': '抗辐射药',
            'type': 'medicine',
            'description': '减少辐射伤害',
            'special_effect': 'reduce_radiation',
            'addictive': True,
            'weight': 0.1,
            'value': 20,
            'stackable': True,
            'max_stack': 12
        }
        
        # === 种子类 ===
        self.items['seeds'] = {
            'id': 'seeds',
            'name': '种子',
            'type': 'seed',
            'description': '农作物种子',
            'weight': 0.1,
            'value': 2,
            'stackable': True,
            'max_stack': 50
        }
        
        self.items['vegetable_seeds'] = {
            'id': 'vegetable_seeds',
            'name': '蔬菜种子',
            'type': 'seed',
            'description': '各种蔬菜种子',
            'weight': 0.1,
            'value': 3,
            'stackable': True,
            'max_stack': 40
        }
        
        self.items['grain_seeds'] = {
            'id': 'grain_seeds',
            'name': '谷物种子',
            'type': 'seed',
            'description': '粮食作物种子',
            'weight': 0.2,
            'value': 4,
            'stackable': True,
            'max_stack': 30
        }
        
        self.items['herb_seeds'] = {
            'id': 'herb_seeds',
            'name': '草药种子',
            'type': 'seed',
            'description': '药用植物种子',
            'weight': 0.1,
            'value': 5,
            'stackable': True,
            'max_stack': 25
        }
        
        # === 武器类 ===
        self.items['knife'] = {
            'id': 'knife',
            'name': '小刀',
            'type': 'weapon',
            'equip_slot': 'weapon',
            'description': '基础近战武器',
            'damage': 8,
            'durability': 50,
            'weight': 1.0,
            'value': 15,
            'effects': [
                {'type': 'stat_bonus', 'stat': 'strength', 'value': 1}
            ]
        }
        
        self.items['baseball_bat'] = {
            'id': 'baseball_bat',
            'name': '棒球棍',
            'type': 'weapon',
            'equip_slot': 'weapon',
            'description': '钝器武器，击打效果好',
            'damage': 12,
            'durability': 40,
            'weight': 2.0,
            'value': 10,
            'effects': [
                {'type': 'stat_bonus', 'stat': 'strength', 'value': 2}
            ]
        }
        
        self.items['pistol'] = {
            'id': 'pistol',
            'name': '手枪',
            'type': 'weapon',
            'equip_slot': 'weapon',
            'description': '基础枪械武器',
            'damage': 20,
            'durability': 30,
            'weight': 1.5,
            'value': 50,
            'ammo_type': '9mm',
            'effects': [
                {'type': 'stat_bonus', 'stat': 'agility', 'value': 1}
            ]
        }
        
        self.items['shotgun'] = {
            'id': 'shotgun',
            'name': '霰弹枪',
            'type': 'weapon',
            'equip_slot': 'weapon',
            'description': '近距离高伤害武器',
            'damage': 35,
            'durability': 25,
            'weight': 3.0,
            'value': 80,
            'ammo_type': 'shells',
            'effects': [
                {'type': 'stat_bonus', 'stat': 'strength', 'value': 2}
            ]
        }
        
        self.items['assault_rifle'] = {
            'id': 'assault_rifle',
            'name': '突击步枪',
            'type': 'weapon',
            'equip_slot': 'weapon',
            'description': '全自动步枪，火力强大',
            'damage': 25,
            'durability': 40,
            'weight': 3.5,
            'value': 120,
            'ammo_type': '5.56mm',
            'effects': [
                {'type': 'stat_bonus', 'stat': 'agility', 'value': 2},
                {'type': 'stat_bonus', 'stat': 'strength', 'value': 1}
            ]
        }
        
        # === 防具类 ===
        self.items['cloth_armor'] = {
            'id': 'cloth_armor',
            'name': '布甲',
            'type': 'armor',
            'equip_slot': 'chest',
            'description': '基础防护服装',
            'defense': 5,
            'durability': 30,
            'weight': 2.0,
            'value': 20,
            'effects': [
                {'type': 'stat_bonus', 'stat': 'endurance', 'value': 1}
            ]
        }
        
        self.items['leather_armor'] = {
            'id': 'leather_armor',
            'name': '皮甲',
            'type': 'armor',
            'equip_slot': 'chest',
            'description': '皮革制成的护甲',
            'defense': 8,
            'durability': 40,
            'weight': 3.0,
            'value': 35,
            'effects': [
                {'type': 'stat_bonus', 'stat': 'endurance', 'value': 2},
                {'type': 'stat_bonus', 'stat': 'agility', 'value': 1}
            ]
        }
        
        self.items['metal_armor'] = {
            'id': 'metal_armor',
            'name': '金属护甲',
            'type': 'armor',
            'equip_slot': 'chest',
            'description': '金属板制成的重甲',
            'defense': 15,
            'durability': 50,
            'weight': 8.0,
            'value': 60,
            'effects': [
                {'type': 'stat_bonus', 'stat': 'endurance', 'value': 3},
                {'type': 'stat_bonus', 'stat': 'strength', 'value': 1}
            ]
        }
        
        self.items['tactical_vest'] = {
            'id': 'tactical_vest',
            'name': '战术背心',
            'type': 'armor',
            'equip_slot': 'chest',
            'description': '军用战术装备',
            'defense': 12,
            'durability': 45,
            'weight': 4.0,
            'value': 80,
            'effects': [
                {'type': 'stat_bonus', 'stat': 'endurance', 'value': 2},
                {'type': 'stat_bonus', 'stat': 'agility', 'value': 2}
            ]
        }
        
        # === 头盔类 ===
        self.items['cloth_helmet'] = {
            'id': 'cloth_helmet',
            'name': '布帽',
            'type': 'helmet',
            'equip_slot': 'head',
            'description': '基础头部防护',
            'defense': 3,
            'durability': 25,
            'weight': 0.5,
            'value': 10,
            'effects': [
                {'type': 'stat_bonus', 'stat': 'endurance', 'value': 1}
            ]
        }
        
        self.items['metal_helmet'] = {
            'id': 'metal_helmet',
            'name': '金属头盔',
            'type': 'helmet',
            'equip_slot': 'head',
            'description': '金属制成的头盔',
            'defense': 8,
            'durability': 35,
            'weight': 2.0,
            'value': 25,
            'effects': [
                {'type': 'stat_bonus', 'stat': 'endurance', 'value': 2}
            ]
        }
        
        # === 背包类 ===
        self.items['small_backpack'] = {
            'id': 'small_backpack',
            'name': '小背包',
            'type': 'backpack',
            'equip_slot': 'backpack',
            'description': '增加携带容量',
            'capacity_bonus': 10,
            'weight': 1.0,
            'value': 15,
            'effects': [
                {'type': 'carry_capacity', 'value': 10}
            ]
        }
        
        self.items['hiking_backpack'] = {
            'id': 'hiking_backpack',
            'name': '登山包',
            'type': 'backpack',
            'equip_slot': 'backpack',
            'description': '大容量背包',
            'capacity_bonus': 25,
            'weight': 2.0,
            'value': 40,
            'effects': [
                {'type': 'carry_capacity', 'value': 25}
            ]
        }
        
        self.items['military_backpack'] = {
            'id': 'military_backpack',
            'name': '军用背包',
            'type': 'backpack',
            'equip_slot': 'backpack',
            'description': '专业军用背包',
            'capacity_bonus': 40,
            'weight': 3.0,
            'value': 80,
            'effects': [
                {'type': 'carry_capacity', 'value': 40},
                {'type': 'stat_bonus', 'stat': 'endurance', 'value': 1}
            ]
        }
        
        # === 特殊物品 ===
        self.items['map_fragment'] = {
            'id': 'map_fragment',
            'name': '地图碎片',
            'type': 'special',
            'description': '世界地图的一部分',
            'weight': 0.1,
            'value': 5,
            'stackable': True,
            'max_stack': 10
        }
        
        self.items['research_data'] = {
            'id': 'research_data',
            'name': '研究资料',
            'type': 'special',
            'description': '科学研究的记录',
            'weight': 0.2,
            'value': 15,
            'stackable': True,
            'max_stack': 5
        }
        
        self.items['ancient_artifact'] = {
            'id': 'ancient_artifact',
            'name': '古代文物',
            'type': 'special',
            'description': '神秘的古代物品',
            'weight': 1.0,
            'value': 100,
            'stackable': False
        }
        
        self.items['rare_herbs'] = {
            'id': 'rare_herbs',
            'name': '稀有草药',
            'type': 'special',
            'description': '具有特殊药效的植物',
            'health_restore': 30,
            'mental_restore': 20,
            'weight': 0.1,
            'value': 25,
            'stackable': True,
            'max_stack': 8
        }
        
        self.items['rare_minerals'] = {
            'id': 'rare_minerals',
            'name': '稀有矿物',
            'type': 'special',
            'description': '稀有的矿物晶体',
            'weight': 0.5,
            'value': 50,
            'stackable': True,
            'max_stack': 5
        }
        
        logging.info(f"创建了{len(self.items)}种物品")
    
    def create_recipes(self):
        """创建所有制作配方"""
        # === 工具类配方 ===
        self.recipes['make_knife'] = {
            'id': 'make_knife',
            'name': '制作小刀',
            'category': 'tools',
            'difficulty': 1,
            'materials': {'metal': 2, 'wood': 1},
            'products': {'knife': 1},
            'exp': 15,
            'description': '制作一把基础小刀'
        }
        
        self.recipes['make_baseball_bat'] = {
            'id': 'make_baseball_bat',
            'name': '制作棒球棍',
            'category': 'tools',
            'difficulty': 1,
            'materials': {'wood': 3},
            'products': {'baseball_bat': 1},
            'exp': 10,
            'description': '制作一根棒球棍'
        }
        
        # === 防具类配方 ===
        self.recipes['make_cloth_armor'] = {
            'id': 'make_cloth_armor',
            'name': '制作布甲',
            'category': 'armor',
            'difficulty': 1,
            'materials': {'cloth': 5},
            'products': {'cloth_armor': 1},
            'exp': 20,
            'description': '制作基础布甲'
        }
        
        self.recipes['make_leather_armor'] = {
            'id': 'make_leather_armor',
            'name': '制作皮甲',
            'category': 'armor',
            'difficulty': 2,
            'materials': {'cloth': 3, 'leather': 4},
            'products': {'leather_armor': 1},
            'exp': 30,
            'description': '制作皮革护甲'
        }
        
        # === 医疗类配方 ===
        self.recipes['make_bandage'] = {
            'id': 'make_bandage',
            'name': '制作绷带',
            'category':'medical',
            'difficulty': 1,
            'materials': {'cloth': 2},
            'products': {'bandage': 2},
            'exp': 10,
            'description': '制作医疗绷带'
        }
        
        self.recipes['make_medicine'] = {
            'id': 'make_medicine',
            'name': '制作药品',
            'category': 'medical',
            'difficulty': 2,
            'materials': {'rare_herbs': 1, 'materials': 3},
            'products': {'medicine': 2},
            'exp': 25,
            'description': '制作基础药品'
        }
        
        # === 食物类配方 ===
        self.recipes['cook_food'] = {
            'id': 'cook_food',
            'name': '烹饪食物',
            'category': 'food',
            'difficulty': 1,
            'materials': {'food': 2},
            'products': {'fresh_food': 1},
            'exp': 8,
            'description': '烹饪新鲜食物'
        }
        
        self.recipes['purify_water'] = {
            'id': 'purify_water',
            'name': '净化水',
            'category': 'food',
            'difficulty': 1,
            'materials': {'water': 3},
            'products': {'clean_water': 2},
            'exp': 5,
            'description': '净化饮用水'
        }
        
        # === 建筑类配方 ===
        self.recipes['build_shelter'] = {
            'id': 'build_shelter',
            'name': '建造庇护所',
            'category': 'construction',
            'difficulty': 3,
            'materials': {'wood': 10, 'cloth': 5, 'materials': 8},
            'products': {'shelter': 1},
            'exp': 50,
            'description': '建造一个简易庇护所'
        }
        
        self.recipes['repair_tools'] = {
            'id': 'repair_tools',
            'name': '修理工具',
            'category': 'tools',
            'difficulty': 2,
            'materials': {'metal': 2, 'materials': 3},
            'products': {'tool_kit': 1},
            'exp': 20,
            'description': '修理和维护工具'
        }
        
        # === 高级配方 ===
        self.recipes['advanced_weapon'] = {
            'id': 'advanced_weapon',
            'name': '制作高级武器',
            'category': 'weapons',
            'difficulty': 4,
            'materials': {'advanced_alloy': 3, 'electronic': 2, 'metal': 5},
            'products': {'advanced_weapon': 1},
            'exp': 80,
            'description': '制作高性能武器'
        }
        
        self.recipes['energy_pack'] = {
            'id': 'energy_pack',
            'name': '制作能量包',
            'category': 'special',
            'difficulty': 3,
            'materials': {'electronic': 3, 'rare_minerals': 1, 'materials': 5},
            'products': {'energy_pack': 1},
            'exp': 40,
            'description': '制作高能量设备'
        }
        
        logging.info(f"创建了{len(self.recipes)}个制作配方")
    
    def load_data(self, save_data):
        """加载物品系统数据"""
        try:
            # 可以在这里加载自定义物品或配方
            self.initialized = True
            logging.info("物品系统数据加载完成")
        except Exception as e:
            logging.error(f"加载物品系统数据失败: {e}")
            raise
    
    def get_save_data(self):
        """获取保存数据"""
        return {
            'items': self.items,
            'recipes': self.recipes
        }
    
    def get_item_data(self, item_id):
        """获取物品数据"""
        return self.items.get(item_id)
    
    def get_item_name(self, item_id):
        """获取物品名称"""
        item_data = self.get_item_data(item_id)
        return item_data.get('name', '未知物品') if item_data else '未知物品'
    
    def get_recipe(self, recipe_id):
        """获取配方"""
        return self.recipes.get(recipe_id)
    
    def get_recipes_by_category(self, category):
        """按分类获取配方"""
        return [recipe for recipe in self.recipes.values() if recipe.get('category') == category]
    
    def get_available_recipes(self, player_skills):
        """获取可用的配方（基于玩家技能）"""
        available = []
        for recipe in self.recipes.values():
            difficulty = recipe.get('difficulty', 1)
            required_skill = difficulty * 10
            player_crafting_skill = player_skills.get('crafting', 1) * 10
            
            if player_crafting_skill >= required_skill:
                available.append(recipe)
        
        return available
    
    def can_craft(self, recipe_id, player_inventory):
        """检查是否可以制作"""
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return False
        
        for material, amount in recipe['materials'].items():
            if player_inventory.get(material, 0) < amount:
                return False
        
        return True
    
    def get_crafting_cost(self, recipe_id):
        """获取制作成本"""
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return {}
        
        return recipe.get('materials', {})
    
    def get_item_value(self, item_id, quantity=1):
        """获取物品价值"""
        item_data = self.get_item_data(item_id)
        if not item_data:
            return 0
        
        base_value = item_data.get('value', 0)
        return base_value * quantity
    
    def generate_loot(self, enemy_level, location_type):
        """生成战利品"""
        loot = {}
        
        # 基础战利品
        base_chance = random.randint(1, 100)
        if base_chance <= 70:  # 70%几率获得基础物品
            loot['materials'] = random.randint(1, 3)
        
        # 根据敌人等级增加战利品
        if enemy_level >= 3:
            if random.randint(1, 100) <= 40:
                loot['medicine'] = random.randint(1, 2)
        
        if enemy_level >= 5:
            if random.randint(1, 100) <= 25:
                weapon_chance = random.randint(1, 100)
                if weapon_chance <= 50:
                    loot['knife'] = 1
                elif weapon_chance <= 80:
                    loot['baseball_bat'] = 1
                else:
                    loot['pistol'] = 1
        
        # 根据地点类型增加特殊战利品
        if location_type == 'forest':
            if random.randint(1, 100) <= 30:
                loot['rare_herbs'] = random.randint(1, 2)
        elif location_type == 'mountain':
            if random.randint(1, 100) <= 25:
                loot['rare_minerals'] = random.randint(1, 2)
        elif location_type == 'urban':
            if random.randint(1, 100) <= 35:
                loot['electronic'] = random.randint(1, 3)
        
        return loot
    
    def get_item_categories(self):
        """获取物品分类"""
        categories = set()
        for item in self.items.values():
            categories.add(item.get('type', 'other'))
        return sorted(list(categories))
    
    def get_items_by_category(self, category):
        """按分类获取物品"""
        return [item for item in self.items.values() if item.get('type') == category]
    
    def validate_item_stack(self, item_id, quantity):
        """验证物品堆叠数量"""
        item_data = self.get_item_data(item_id)
        if not item_data:
            return 0
        
        max_stack = item_data.get('max_stack', 1)
        return min(quantity, max_stack)
    
    def get_item_description(self, item_id):
        """获取物品详细描述"""
        item_data = self.get_item_data(item_id)
        if not item_data:
            return "未知物品"
        
        description = item_data.get('description', '')
        additional_info = []
        
        # 添加效果信息
        if item_data.get('health_restore', 0) > 0:
            additional_info.append(f"恢复生命: {item_data['health_restore']}")
        if item_data.get('stamina_restore', 0) > 0:
            additional_info.append(f"恢复体力: {item_data['stamina_restore']}")
        if item_data.get('mental_restore', 0) > 0:
            additional_info.append(f"恢复精神: {item_data['mental_restore']}")
        if item_data.get('damage', 0) > 0:
            additional_info.append(f"伤害: {item_data['damage']}")
        if item_data.get('defense', 0) > 0:
            additional_info.append(f"防御: {item_data['defense']}")
        
        if additional_info:
            description += f"\n效果: {', '.join(additional_info)}"
        
        return description