# -*- coding: utf-8 -*-

import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class FarmingSystem:
    def __init__(self, game):
        self.game = game
        self.crops = {}
        self.farmlands = {}
        self.farming_tools = {}
        self.initialized = False
        
    def initialize(self):
        """初始化农业系统"""
        try:
            self.create_crops()
            self.create_farming_tools()
            self.initialize_farmlands()
            self.initialized = True
            logging.info("农业系统初始化完成")
        except Exception as e:
            logging.error(f"农业系统初始化失败: {e}")
            raise
    
    def create_crops(self):
        """创建农作物类型"""
        # === 粮食作物 ===
        self.crops['rice'] = {
            'id': 'rice',
            'name': '水稻',
            'type': 'grain',
            'growth_stages': 5,
            'growth_days_per_stage': 18,
            'yield_amount': (3, 5),
            'seed_cost': 2,
            'water_requirement': 3,
            'fertility_requirement': 2,
            'season_preference': ['spring', 'summer'],
            'description': '主要粮食作物，需要充足的水源',
            'harvest_product': 'food',
            'special_products': {'straw': (1, 2)},
            'exp_reward': 25
        }
        
        self.crops['wheat'] = {
            'id': 'wheat',
            'name': '小麦',
            'type': 'grain',
            'growth_stages': 4,
            'growth_days_per_stage': 30,
            'yield_amount': (2, 4),
            'seed_cost': 2,
            'water_requirement': 2,
            'fertility_requirement': 3,
            'season_preference': ['autumn', 'winter'],
            'description': '耐寒作物，适合秋冬种植',
            'harvest_product': 'grain_seeds',
            'special_products': {'flour': (1, 2)},
            'exp_reward': 30
        }
        
        self.crops['corn'] = {
            'id': 'corn',
            'name': '玉米',
            'type': 'grain',
            'growth_stages': 4,
            'growth_days_per_stage': 20,
            'yield_amount': (4, 6),
            'seed_cost': 3,
            'water_requirement': 2,
            'fertility_requirement': 2,
            'season_preference': ['spring', 'summer'],
            'description': '高产作物，生长快速',
            'harvest_product': 'food',
            'special_products': {'corn_seeds': (2, 3)},
            'exp_reward': 20
        }
        
        # === 蔬菜作物 ===
        self.crops['cabbage'] = {
            'id': 'cabbage',
            'name': '大白菜',
            'type': 'vegetable',
            'growth_stages': 3,
            'growth_days_per_stage': 20,
            'yield_amount': (2, 4),
            'seed_cost': 1,
            'water_requirement': 2,
            'fertility_requirement': 2,
            'season_preference': ['spring', 'autumn'],
            'description': '耐储存的蔬菜，适合初学者',
            'harvest_product': 'fresh_food',
            'special_products': {'vegetable_seeds': (1, 2)},
            'exp_reward': 15
        }
        
        self.crops['carrot'] = {
            'id': 'carrot',
            'name': '胡萝卜',
            'type': 'vegetable',
            'growth_stages': 3,
            'growth_days_per_stage': 15,
            'yield_amount': (3, 5),
            'seed_cost': 1,
            'water_requirement': 2,
            'fertility_requirement': 1,
            'season_preference': ['spring', 'summer'],
            'description': '生长快速的根茎类蔬菜',
            'harvest_product': 'fresh_food',
            'special_products': {'carrot_seeds': (2, 3)},
            'exp_reward': 12
        }
        
        self.crops['potato'] = {
            'id': 'potato',
            'name': '土豆',
            'type': 'vegetable',
            'growth_stages': 4,
            'growth_days_per_stage': 25,
            'yield_amount': (5, 8),
            'seed_cost': 2,
            'water_requirement': 1,
            'fertility_requirement': 2,
            'season_preference': ['spring'],
            'description': '高产作物，提供大量食物',
            'harvest_product': 'food',
            'special_products': {'potato_seeds': (3, 5)},
            'exp_reward': 35
        }
        
        # === 经济作物 ===
        self.crops['cotton'] = {
            'id': 'cotton',
            'name': '棉花',
            'type': 'cash_crop',
            'growth_stages': 5,
            'growth_days_per_stage': 30,
            'yield_amount': (1, 2),
            'seed_cost': 3,
            'water_requirement': 2,
            'fertility_requirement': 3,
            'season_preference': ['spring', 'summer'],
            'description': '纺织原料，生长期长但价值高',
            'harvest_product': 'cloth',
            'special_products': {'cotton_seeds': (1, 2)},
            'exp_reward': 40
        }
        
        self.crops['tea'] = {
            'id': 'tea',
            'name': '茶叶',
            'type': 'cash_crop',
            'growth_stages': 6,
            'growth_days_per_stage': 60,
            'yield_amount': (1, 2),
            'seed_cost': 5,
            'water_requirement': 3,
            'fertility_requirement': 4,
            'season_preference': ['spring', 'autumn'],
            'description': '多年生植物，可多次收获',
            'harvest_product': 'herbal_tea',
            'special_products': {'tea_seeds': (1, 1)},
            'exp_reward': 50,
            'perennial': True
        }
        
        # === 药用植物 ===
        self.crops['ginseng'] = {
            'id': 'ginseng',
            'name': '人参',
            'type': 'medicinal',
            'growth_stages': 7,
            'growth_days_per_stage': 90,
            'yield_amount': (1, 1),
            'seed_cost': 10,
            'water_requirement': 2,
            'fertility_requirement': 4,
            'season_preference': ['spring', 'autumn'],
            'description': '珍稀药材，生长极其缓慢',
            'harvest_product': 'rare_herbs',
            'special_products': {'ginseng_root': (1, 1)},
            'exp_reward': 100
        }
        
        self.crops['medicinal_herbs'] = {
            'id': 'medicinal_herbs',
            'name': '药用草药',
            'type': 'medicinal',
            'growth_stages': 3,
            'growth_days_per_stage': 25,
            'yield_amount': (2, 4),
            'seed_cost': 2,
            'water_requirement': 2,
            'fertility_requirement': 2,
            'season_preference': ['spring', 'summer'],
            'description': '基础药用植物',
            'harvest_product': 'medicine',
            'special_products': {'herb_seeds': (1, 3)},
            'exp_reward': 20
        }
        
        # === 特殊作物 ===
        self.crops['glowing_mushroom'] = {
            'id': 'glowing_mushroom',
            'name': '发光蘑菇',
            'type': 'special',
            'growth_stages': 2,
            'growth_days_per_stage': 10,
            'yield_amount': (1, 3),
            'seed_cost': 1,
            'water_requirement': 4,
            'fertility_requirement': 1,
            'season_preference': ['all'],
            'description': '在辐射区发现的奇异蘑菇',
            'harvest_product': 'rare_herbs',
            'special_products': {'glowing_spores': (1, 2)},
            'exp_reward': 30,
            'radiation_tolerant': True
        }
        
        logging.info(f"创建了{len(self.crops)}种农作物")
    
    def create_farming_tools(self):
        """创建农具"""
        self.farming_tools = {
            'wooden_hoe': {
                'id': 'wooden_hoe',
                'name': '木锄',
                'type': 'tool',
                'efficiency': 1.0,
                'durability': 20,
                'description': '基础农具，开垦效率一般'
            },
            'iron_hoe': {
                'id': 'iron_hoe',
                'name': '铁锄',
                'type': 'tool',
                'efficiency': 1.5,
                'durability': 40,
                'description': '铁制农具，开垦效率更高'
            },
            'watering_can': {
                'id': 'watering_can',
                'name': '浇水壶',
                'type': 'tool',
                'efficiency': 1.0,
                'durability': 30,
                'description': '用于浇水的工具'
            }
        }
    
    def initialize_farmlands(self):
        """初始化农田"""
        farmable_locations = ['starting_area', 'abandoned_farm', 'south_plains']
        
        for location_id in farmable_locations:
            self.farmlands[location_id] = {
                'plots': [],
                'fertility': random.randint(3, 7),
                'water_source': random.choice([True, False]),
                'max_plots': 5,
                'upgrades': {
                    'irrigation': False,
                    'fence': False,
                    'greenhouse': False
                }
            }
            
            for i in range(3):
                self.farmlands[location_id]['plots'].append({
                    'id': i,
                    'crop_type': None,
                    'planting_date': None,
                    'growth_stage': 0,
                    'health': 100,
                    'water_level': 50,
                    'pest_infestation': 0,
                    'weeds': 0
                })
    
    def load_data(self, save_data):
        """加载农业系统数据"""
        try:
            farmlands_data = save_data.get('farmlands', {})
            for location_id, farmland_data in farmlands_data.items():
                if location_id in self.farmlands:
                    self.farmlands[location_id].update(farmland_data)
            
            self.initialized = True
            logging.info("农业系统数据加载完成")
        except Exception as e:
            logging.error(f"加载农业系统数据失败: {e}")
            raise
    
    def get_save_data(self):
        """获取保存数据"""
        return {
            'farmlands': self.farmlands
        }
    
    def can_plant(self, location_id):
        """检查是否可以种植"""
        return location_id in self.farmlands
    
    def get_available_plots(self, location_id):
        """获取可用的地块"""
        if location_id not in self.farmlands:
            return []
        
        farmland = self.farmlands[location_id]
        available_plots = []
        
        for plot in farmland['plots']:
            if plot['crop_type'] is None:
                available_plots.append(plot)
        
        return available_plots
    
    def plant_crop(self, crop_type, location_id, plot_id=None):
        """种植作物"""
        try:
            if location_id not in self.farmlands:
                return {'success': False, 'message': '这里不能种植'}
            
            crop_data = self.crops.get(crop_type)
            if not crop_data:
                return {'success': False, 'message': '未知的作物类型'}
            
            if not self.game.player.has_item('seeds', crop_data['seed_cost']):
                return {'success': False, 'message': f"需要{crop_data['seed_cost']}个种子"}
            
            farmland = self.farmlands[location_id]
            
            if plot_id is None:
                available_plots = self.get_available_plots(location_id)
                if not available_plots:
                    return {'success': False, 'message': '没有可用的地块'}
                plot = available_plots[0]
            else:
                plot = self.get_plot(location_id, plot_id)
                if not plot or plot['crop_type'] is not None:
                    return {'success': False, 'message': '无效的地块'}
            
            current_season = self.game.season
            if (crop_data['season_preference'] != ['all'] and 
                current_season not in crop_data['season_preference']):
                season_names = {'spring': '春季', 'summer': '夏季', 'autumn': '秋季', 'winter': '冬季'}
                preferred_seasons = [season_names[s] for s in crop_data['season_preference']]
                return {
                    'success': False, 
                    'message': f"{crop_data['name']}不适合在{season_names[current_season]}种植，适宜季节：{', '.join(preferred_seasons)}"
                }
            
            self.game.player.remove_item('seeds', crop_data['seed_cost'])
            
            plot['crop_type'] = crop_type
            plot['planting_date'] = self.game.game_time
            plot['growth_stage'] = 0
            plot['health'] = 100
            plot['water_level'] = 50
            plot['pest_infestation'] = 0
            plot['weeds'] = 0
            
            self.game.player.gain_skill_exp('farming', 5)
            
            logging.info(f"在{location_id}种植了{crop_data['name']}")
            
            return {
                'success': True,
                'message': f"成功种植了{crop_data['name']}！",
                'plot_id': plot['id'],
                'crop_type': crop_type
            }
            
        except Exception as e:
            logging.error(f"种植作物时出错: {e}")
            return {'success': False, 'message': '种植过程中出现错误'}
    
    def get_plot(self, location_id, plot_id):
        """获取指定地块"""
        if location_id not in self.farmlands:
            return None
        
        farmland = self.farmlands[location_id]
        for plot in farmland['plots']:
            if plot['id'] == plot_id:
                return plot
        
        return None
    
    def update_crops_growth(self, hours_passed):
        """更新作物生长"""
        for location_id, farmland in self.farmlands.items():
            for plot in farmland['plots']:
                if plot['crop_type'] is not None:
                    self.update_single_crop(plot, hours_passed, farmland)
    
    def update_single_crop(self, plot, hours_passed, farmland):
        """更新单个作物"""
        crop_type = plot['crop_type']
        crop_data = self.crops.get(crop_type)
        if not crop_data:
            return
        
        days_passed = hours_passed / 24
        growth_rate = self.calculate_growth_rate(plot, crop_data, farmland)
        
        required_days = crop_data['growth_days_per_stage']
        growth_progress = plot.get('growth_progress', 0) + (days_passed * growth_rate)
        
        if growth_progress >= required_days:
            plot['growth_stage'] += 1
            plot['growth_progress'] = growth_progress - required_days
            
            if plot['growth_stage'] >= crop_data['growth_stages']:
                plot['growth_stage'] = crop_data['growth_stages']
        else:
            plot['growth_progress'] = growth_progress
        
        self.update_crop_health(plot, crop_data, farmland, hours_passed)
    
    def calculate_growth_rate(self, plot, crop_data, farmland):
        """计算生长速率"""
        base_rate = 1.0
        
        # 土壤肥力影响
        fertility = farmland['fertility']
        fertility_requirement = crop_data['fertility_requirement']
        fertility_factor = min(1.5, fertility / fertility_requirement)
        base_rate *= fertility_factor
    
        # 水分影响
        water_level = plot['water_level']
        water_requirement = crop_data['water_requirement']
        if water_level < water_requirement * 10:
          water_factor = max(0.1, water_level / (water_requirement * 10))
          base_rate *= water_factor
    
        # 季节影响
        current_season = self.game.season
        if current_season in crop_data['season_preference']:
          base_rate *= 1.2  # 适宜季节生长更快
        elif crop_data['season_preference'] != ['all']:
          base_rate *= 0.5  # 不适宜季节生长缓慢
    
        # 天气影响
        weather = self.game.weather
        if weather == 'rainy':
          base_rate *= 1.1  # 雨天促进生长
        elif weather == 'stormy':
          base_rate *= 0.8  # 暴风雨影响生长
    
        # 害虫和杂草影响
        if plot['pest_infestation'] > 50:
          base_rate *= 0.7
        if plot['weeds'] > 50:
          base_rate *= 0.8
    
        return base_rate
    
    def update_crop_health(self, plot, crop_data, farmland, hours_passed):
        """更新作物健康度"""
        water_consumption = crop_data['water_requirement'] * hours_passed / 24
        plot['water_level'] = max(0, plot['water_level'] - water_consumption)
        
        if plot['water_level'] < 20:
            health_loss = (20 - plot['water_level']) * 0.1
            plot['health'] = max(0, plot['health'] - health_loss)
        
        if random.random() < 0.01:
            plot['pest_infestation'] = min(100, plot['pest_infestation'] + 10)
        
        if random.random() < 0.02:
            plot['weeds'] = min(100, plot['weeds'] + 5)
        
        if plot['pest_infestation'] > 0:
            health_loss = plot['pest_infestation'] * 0.05
            plot['health'] = max(0, plot['health'] - health_loss)
        
        if plot['weeds'] > 0:
            health_loss = plot['weeds'] * 0.03
            plot['health'] = max(0, plot['health'] - health_loss)
    
    def water_crops(self, location_id, plot_id=None):
        """浇水"""
        if location_id not in self.farmlands:
            return {'success': False, 'message': '这里没有农田'}
        
        farmland = self.farmlands[location_id]
        
        if not farmland['water_source'] and not farmland['upgrades']['irrigation']:
            return {'success': False, 'message': '这里没有水源'}
        
        if self.game.player.stamina < 10:
            return {'success': False, 'message': '体力不足'}
        
        plots_to_water = []
        if plot_id is not None:
            plot = self.get_plot(location_id, plot_id)
            if plot and plot['crop_type'] is not None:
                plots_to_water.append(plot)
        else:
            for plot in farmland['plots']:
                if plot['crop_type'] is not None and plot['water_level'] < 80:
                    plots_to_water.append(plot)
        
        if not plots_to_water:
            return {'success': False, 'message': '没有需要浇水的作物'}
        
        self.game.player.modify_stamina(-10)
        
        for plot in plots_to_water:
            plot['water_level'] = min(100, plot['water_level'] + 40)
        
        watered_count = len(plots_to_water)
        return {
            'success': True,
            'message': f'成功为{watered_count}块地浇水',
            'plots_watered': watered_count
        }
    
    def harvest_crop(self, location_id, plot_id):
        """收获作物"""
        plot = self.get_plot(location_id, plot_id)
        if not plot or plot['crop_type'] is None:
            return {'success': False, 'message': '没有作物可收获'}
        
        crop_type = plot['crop_type']
        crop_data = self.crops.get(crop_type)
        if not crop_data:
            return {'success': False, 'message': '作物数据错误'}
        
        if plot['growth_stage'] < crop_data['growth_stages']:
            return {'success': False, 'message': '作物还未成熟'}
        
        if plot['health'] < 30:
            return {'success': False, 'message': '作物健康状况太差，无法收获'}
        
        min_yield, max_yield = crop_data['yield_amount']
        base_yield = random.randint(min_yield, max_yield)
        
        health_factor = plot['health'] / 100
        final_yield = int(base_yield * health_factor)
        
        if final_yield <= 0:
            return {'success': False, 'message': '作物已经完全枯萎'}
        
        harvest_product = crop_data['harvest_product']
        self.game.player.add_item(harvest_product, final_yield)
        
        special_products = crop_data.get('special_products', {})
        for product, (min_qty, max_qty) in special_products.items():
            if random.random() < 0.7:
                qty = random.randint(min_qty, max_qty)
                self.game.player.add_item(product, qty)
        
        self.game.player.gain_skill_exp('farming', crop_data['exp_reward'])
        self.game.player.stats['crops_harvested'] += 1
        
        if crop_data.get('perennial', False):
            plot['growth_stage'] = 0
            plot['growth_progress'] = 0
            plot['health'] = 100
            plot['water_level'] = 50
        else:
            plot['crop_type'] = None
            plot['planting_date'] = None
            plot['growth_stage'] = 0
            plot['growth_progress'] = 0
            plot['health'] = 100
            plot['water_level'] = 50
            plot['pest_infestation'] = 0
            plot['weeds'] = 0
        
        logging.info(f"收获作物: {crop_data['name']}, 产量: {final_yield}")
        
        return {
            'success': True,
            'message': f"收获了{final_yield}个{crop_data['name']}！",
            'yield_amount': final_yield,
            'crop_name': crop_data['name']
        }
    
    def remove_weeds(self, location_id, plot_id):
        """除草"""
        plot = self.get_plot(location_id, plot_id)
        if not plot:
            return {'success': False, 'message': '无效的地块'}
        
        if plot['weeds'] == 0:
            return {'success': False, 'message': '没有杂草需要清除'}
        
        if self.game.player.stamina < 5:
            return {'success': False, 'message': '体力不足'}
        
        self.game.player.modify_stamina(-5)
        
        weed_removed = min(plot['weeds'], 50)
        plot['weeds'] = max(0, plot['weeds'] - weed_removed)
        
        self.game.player.gain_skill_exp('farming', 3)
        
        return {
            'success': True,
            'message': f'清除了{weed_removed}%的杂草',
            'weeds_removed': weed_removed
        }
    
    def remove_pests(self, location_id, plot_id):
        """除虫"""
        plot = self.get_plot(location_id, plot_id)
        if not plot:
            return {'success': False, 'message': '无效的地块'}
        
        if plot['pest_infestation'] == 0:
            return {'success': False, 'message': '没有害虫需要清除'}
        
        if not self.game.player.has_item('medicine'):
            return {'success': False, 'message': '需要药品来制作杀虫剂'}
        
        self.game.player.remove_item('medicine', 1)
        
        pest_removed = min(plot['pest_infestation'], 70)
        plot['pest_infestation'] = max(0, plot['pest_infestation'] - pest_removed)
        
        self.game.player.gain_skill_exp('farming', 5)
        
        return {
            'success': True,
            'message': f'清除了{pest_removed}%的害虫',
            'pests_removed': pest_removed
        }
    
    def fertilize_soil(self, location_id):
        """施肥"""
        if location_id not in self.farmlands:
            return {'success': False, 'message': '这里没有农田'}
        
        farmland = self.farmlands[location_id]
        
        if not self.game.player.has_item('materials', 3):
            return {'success': False, 'message': '需要3个材料来制作肥料'}
        
        self.game.player.remove_item('materials', 3)
        
        fertility_increase = random.randint(1, 3)
        farmland['fertility'] = min(10, farmland['fertility'] + fertility_increase)
        
        self.game.player.gain_skill_exp('farming', 8)
        
        return {
            'success': True,
            'message': f'施肥成功，土壤肥力提升了{fertility_increase}点',
            'fertility_increase': fertility_increase
        }
    
    def expand_farmland(self, location_id):
        """扩展农田"""
        if location_id not in self.farmlands:
            return {'success': False, 'message': '这里不能扩展农田'}
        
        farmland = self.farmlands[location_id]
        
        if len(farmland['plots']) >= farmland['max_plots']:
            return {'success': False, 'message': '已达到最大地块数量'}
        
        if not self.game.player.has_item('wood', 5) or not self.game.player.has_item('materials', 3):
            return {'success': False, 'message': '需要5个木材和3个材料来扩展农田'}
        
        self.game.player.remove_item('wood', 5)
        self.game.player.remove_item('materials', 3)
        
        new_plot_id = len(farmland['plots'])
        farmland['plots'].append({
            'id': new_plot_id,
            'crop_type': None,
            'planting_date': None,
            'growth_stage': 0,
            'health': 100,
            'water_level': 50,
            'pest_infestation': 0,
            'weeds': 0
        })
        
        self.game.player.gain_skill_exp('farming', 15)
        
        return {
            'success': True,
            'message': '成功扩展了农田！',
            'new_plot_id': new_plot_id
        }
    
    def upgrade_farmland(self, location_id, upgrade_type):
        """升级农田设施"""
        if location_id not in self.farmlands:
            return {'success': False, 'message': '这里没有农田'}
        
        farmland = self.farmlands[location_id]
        
        upgrades_data = {
            'irrigation': {
                'name': '灌溉系统',
                'cost': {'electronic': 2, 'materials': 5},
                'description': '自动浇水系统'
            },
            'fence': {
                'name': '围栏',
                'cost': {'wood': 10, 'materials': 3},
                'description': '防止野生动物破坏'
            },
            'greenhouse': {
                'name': '温室',
                'cost': {'electronic': 5, 'materials': 10, 'cloth': 8},
                'description': '控制生长环境'
            }
        }
        
        upgrade_info = upgrades_data.get(upgrade_type)
        if not upgrade_info:
            return {'success': False, 'message': '无效的升级类型'}
        
        if farmland['upgrades'][upgrade_type]:
            return {'success': False, 'message': f'{upgrade_info["name"]}已经建造完成'}
        
        for item, amount in upgrade_info['cost'].items():
            if not self.game.player.has_item(item, amount):
                return {'success': False, 'message': f'材料不足，需要{amount}个{self.game.items.get_item_name(item)}'}
        
        for item, amount in upgrade_info['cost'].items():
            self.game.player.remove_item(item, amount)
        
        farmland['upgrades'][upgrade_type] = True
        
        self.game.player.gain_skill_exp('farming', 25)
        
        return {
            'success': True,
            'message': f'成功建造了{upgrade_info["name"]}！',
            'upgrade_type': upgrade_type
        }
    
    def get_crop_growth_description(self, growth_stage, total_stages):
        """获取作物生长阶段描述"""
        if growth_stage == 0:
            return "刚播种"
        elif growth_stage < total_stages:
            progress = (growth_stage / total_stages) * 100
            if progress < 25:
                return "幼苗期"
            elif progress < 50:
                return "生长期"
            elif progress < 75:
                return "开花期"
            else:
                return "结果期"
        else:
            return "已成熟"
    
    def get_farmland_status(self, location_id):
        """获取农田状态"""
        if location_id not in self.farmlands:
            return None
        
        farmland = self.farmlands[location_id]
        status = {
            'location_id': location_id,
            'fertility': farmland['fertility'],
            'water_source': farmland['water_source'],
            'total_plots': len(farmland['plots']),
            'max_plots': farmland['max_plots'],
            'empty_plots': len(self.get_available_plots(location_id)),
            'growing_crops': 0,
            'mature_crops': 0,
            'upgrades': farmland['upgrades'].copy(),
            'plots_details': []
        }
        
        for plot in farmland['plots']:
            plot_info = {
                'id': plot['id'],
                'crop_type': plot['crop_type'],
                'growth_stage': plot.get('growth_stage', 0),
                'health': plot.get('health', 100),
                'water_level': plot.get('water_level', 50),
                'pest_infestation': plot.get('pest_infestation', 0),
                'weeds': plot.get('weeds', 0)
            }
            
            if plot['crop_type']:
                crop_data = self.crops.get(plot['crop_type'])
                if crop_data:
                    plot_info['crop_name'] = crop_data['name']
                    plot_info['growth_description'] = self.get_crop_growth_description(
                        plot['growth_stage'], crop_data['growth_stages']
                    )
                    plot_info['is_mature'] = plot['growth_stage'] >= crop_data['growth_stages']
                    
                    if plot_info['is_mature']:
                        status['mature_crops'] += 1
                    else:
                        status['growing_crops'] += 1
            
            status['plots_details'].append(plot_info)
        
        return status
    
    def get_seasonal_crops(self):
        """获取当前季节适宜的作物"""
        current_season = self.game.season
        seasonal_crops = []
        
        for crop_id, crop_data in self.crops.items():
            if (crop_data['season_preference'] == ['all'] or 
                current_season in crop_data['season_preference']):
                seasonal_crops.append(crop_data)
        
        return seasonal_crops
    
    def get_crop_info(self, crop_type):
        """获取作物详细信息"""
        return self.crops.get(crop_type)
    
    def get_all_crops(self):
        """获取所有作物"""
        return list(self.crops.values())
