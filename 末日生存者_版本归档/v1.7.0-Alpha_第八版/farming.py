# -*- coding: utf-8 -*-

import random
import logging
import json
import os
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
            self.load_crops_from_file()
            self.create_farming_tools()
            self.initialize_farmlands()
            self.initialized = True
            logging.info("农业系统初始化完成")
        except Exception as e:
            logging.error(f"从文件加载农作物失败: {e}，使用硬编码")
            self.create_crops()
            self.create_farming_tools()
            self.initialize_farmlands()
            self.initialized = True

    def load_crops_from_file(self):
        """从 ModManager 或 JSON 文件加载农作物数据"""
        mod_crops = self.game.mod_manager.get_data('crops', None) or {}
        if mod_crops:
            self.crops = dict(mod_crops)
            logging.info(f"从MOD管理器加载了 {len(self.crops)} 种农作物")
            return
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        crops_file = os.path.join(data_dir, 'crops.json')
        if not os.path.exists(crops_file):
            raise FileNotFoundError(f"农作物数据文件不存在: {crops_file}")
        with open(crops_file, 'r', encoding='utf-8') as f:
            self.crops = json.load(f)
        logging.info(f"从 {crops_file} 加载了 {len(self.crops)} 种农作物")

    def create_crops(self):
        """硬编码创建农作物（回退）"""
        self.crops = {
            'rice': {
                'id': 'rice', 'name': '水稻', 'type': 'grain', 'growth_stages': 5,
                'growth_days_per_stage': 18, 'yield_amount': [3, 5], 'seed_cost': 2,
                'water_requirement': 3, 'fertility_requirement': 2,
                'season_preference': ['spring', 'summer'], 'description': '主要粮食作物',
                'harvest_product': 'food', 'special_products': {'straw': [1, 2]}, 'exp_reward': 25
            },
            'wheat': {
                'id': 'wheat', 'name': '小麦', 'type': 'grain', 'growth_stages': 4,
                'growth_days_per_stage': 30, 'yield_amount': [2, 4], 'seed_cost': 2,
                'water_requirement': 2, 'fertility_requirement': 3,
                'season_preference': ['autumn', 'winter'], 'description': '耐寒作物',
                'harvest_product': 'grain_seeds', 'special_products': {'flour': [1, 2]}, 'exp_reward': 30
            }
        }
        logging.info(f"创建了 {len(self.crops)} 种硬编码农作物")

    def create_farming_tools(self):
        """创建农具"""
        self.farming_tools = {
            'wooden_hoe': {'id': 'wooden_hoe', 'name': '木锄', 'type': 'tool', 'efficiency': 1.0, 'durability': 20, 'description': '基础农具'},
            'iron_hoe': {'id': 'iron_hoe', 'name': '铁锄', 'type': 'tool', 'efficiency': 1.5, 'durability': 40, 'description': '铁制农具'},
            'watering_can': {'id': 'watering_can', 'name': '浇水壶', 'type': 'tool', 'efficiency': 1.0, 'durability': 30, 'description': '浇水工具'}
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
                'upgrades': {'irrigation': False, 'fence': False, 'greenhouse': False}
            }
            for i in range(3):
                self.farmlands[location_id]['plots'].append({
                    'id': i, 'crop_type': None, 'planting_date': None, 'growth_stage': 0,
                    'health': 100, 'water_level': 50, 'pest_infestation': 0, 'weeds': 0
                })

    def load_data(self, save_data):
        """加载农业系统数据"""
        try:
            if not self.farmlands:
                self.initialize_farmlands()
            farmlands_data = save_data.get('farmlands', {})
            for loc_id, farmland_data in farmlands_data.items():
                plots = []
                for plot in farmland_data.get('plots', []):
                    plot = dict(plot)
                    planting_date = plot.get('planting_date')
                    if isinstance(planting_date, str):
                        try:
                            plot['planting_date'] = datetime.fromisoformat(planting_date)
                        except ValueError:
                            plot['planting_date'] = None
                    plots.append(plot)
                farmland_data = dict(farmland_data)
                farmland_data['plots'] = plots
                if loc_id in self.farmlands:
                    self.farmlands[loc_id].update(farmland_data)
                else:
                    self.farmlands[loc_id] = farmland_data
            self.initialized = True
            logging.info("农业系统数据加载完成")
        except Exception as e:
            logging.error(f"加载农业系统数据失败: {e}")
            raise

    def get_save_data(self):
        """获取保存数据"""
        farmlands = {}
        for loc_id, farmland in self.farmlands.items():
            plots = []
            for plot in farmland.get('plots', []):
                plot_data = dict(plot)
                planting_date = plot_data.get('planting_date')
                if isinstance(planting_date, datetime):
                    plot_data['planting_date'] = planting_date.isoformat()
                plots.append(plot_data)
            farmlands[loc_id] = dict(farmland)
            farmlands[loc_id]['plots'] = plots
        return {'farmlands': farmlands}

    def can_plant(self, location_id):
        """检查是否可以种植"""
        return location_id in self.farmlands

    def get_available_plots(self, location_id):
        """获取可用的地块"""
        if location_id not in self.farmlands:
            return []
        farmland = self.farmlands[location_id]
        return [p for p in farmland['plots'] if p['crop_type'] is None]

    def plant_crop(self, crop_type, location_id, plot_id=None):
        """种植作物"""
        if location_id not in self.farmlands:
            return {'success': False, 'message': '这里不能种植'}
        crop_data = self.crops.get(crop_type)
        if not crop_data:
            return {'success': False, 'message': '未知的作物类型'}
        if not self.game.player.has_item('seeds', crop_data['seed_cost']):
            return {'success': False, 'message': f"需要{crop_data['seed_cost']}个种子"}

        farmland = self.farmlands[location_id]
        if plot_id is None:
            available = self.get_available_plots(location_id)
            if not available:
                return {'success': False, 'message': '没有可用的地块'}
            plot = available[0]
        else:
            plot = self.get_plot(location_id, plot_id)
            if not plot or plot['crop_type'] is not None:
                return {'success': False, 'message': '无效的地块'}

        # 季节检查
        current_season = self.game.season
        if crop_data['season_preference'] != ['all'] and current_season not in crop_data['season_preference']:
            season_names = {'spring': '春季', 'summer': '夏季', 'autumn': '秋季', 'winter': '冬季'}
            return {'success': False, 'message': f"{crop_data['name']}不适合在当前季节种植"}

        self.game.player.remove_item('seeds', crop_data['seed_cost'])
        hoe = 'iron_hoe' if self.game.player.has_item('iron_hoe') else 'wooden_hoe' if self.game.player.has_item('wooden_hoe') else None
        if hoe:
            self.game.player.degrade_item(hoe, 1)
        plot['crop_type'] = crop_type
        plot['planting_date'] = self.game.game_time
        plot['growth_stage'] = 0
        plot['growth_progress'] = 0
        plot['health'] = 100
        plot['water_level'] = 50
        plot['pest_infestation'] = 0
        plot['weeds'] = 0

        self.game.player.gain_skill_exp('farming', 5)
        if hasattr(self.game, 'quests') and self.game.quests:
            self.game.quests.update_quest_progress('crop_planted', crop_type=crop_type)
        logging.info(f"在{location_id}种植了{crop_data['name']}")
        return {'success': True, 'message': f"成功种植了{crop_data['name']}！", 'plot_id': plot['id']}

    def get_plot(self, location_id, plot_id):
        """获取指定地块"""
        if location_id not in self.farmlands:
            return None
        for plot in self.farmlands[location_id]['plots']:
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
        # 土壤肥力
        fertility = farmland['fertility']
        fertility_factor = min(1.5, fertility / crop_data['fertility_requirement'])
        base_rate *= fertility_factor
        # 水分
        water_need = crop_data['water_requirement'] * 10
        if plot['water_level'] < water_need:
            water_factor = max(0.1, plot['water_level'] / water_need)
            base_rate *= water_factor
        # 季节
        if self.game.season in crop_data['season_preference']:
            base_rate *= 1.2
        elif crop_data['season_preference'] != ['all']:
            base_rate *= 0.5
        # 天气
        weather = self.game.weather
        if weather == 'rainy':
            base_rate *= 1.1
        elif weather == 'stormy':
            base_rate *= 0.8
        # 害虫杂草
        if plot['pest_infestation'] > 50:
            base_rate *= 0.7
        if plot['weeds'] > 50:
            base_rate *= 0.8
        return base_rate

    def update_crop_health(self, plot, crop_data, farmland, hours_passed):
        """更新作物健康度"""
        # 水分消耗
        water_consumption = crop_data['water_requirement'] * hours_passed / 24
        plot['water_level'] = max(0, plot['water_level'] - water_consumption)
        if plot['water_level'] < 20:
            health_loss = (20 - plot['water_level']) * 0.1
            plot['health'] = max(0, plot['health'] - health_loss)

        pest_chance = 0.01
        weed_chance = 0.02
        if farmland.get('upgrades', {}).get('fence'):
            pest_chance *= 0.35
            weed_chance *= 0.6
        if random.random() < pest_chance:
            plot['pest_infestation'] = min(100, plot['pest_infestation'] + 10)
        if random.random() < weed_chance:
            plot['weeds'] = min(100, plot['weeds'] + 5)

        # 害虫杂草损害
        if plot['pest_infestation'] > 0:
            plot['health'] = max(0, plot['health'] - plot['pest_infestation'] * 0.05)
        if plot['weeds'] > 0:
            plot['health'] = max(0, plot['health'] - plot['weeds'] * 0.03)

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
            if plot and plot['crop_type'] is not None and plot['water_level'] < 80:
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
        if self.game.player.has_item('watering_can'):
            self.game.player.degrade_item('watering_can', 1)

        return {'success': True, 'message': f'成功为{len(plots_to_water)}块地浇水'}

    def harvest_crop(self, location_id, plot_id):
        """收获作物"""
        plot = self.get_plot(location_id, plot_id)
        if not plot or plot['crop_type'] is None:
            return {'success': False, 'message': '没有作物可收获'}
        crop_data = self.crops.get(plot['crop_type'])
        if not crop_data:
            return {'success': False, 'message': '作物数据错误'}
        if plot['growth_stage'] < crop_data['growth_stages']:
            return {'success': False, 'message': '作物还未成熟'}
        if plot['health'] < 30:
            return {'success': False, 'message': '作物健康状况太差，无法收获'}

        min_yield, max_yield = crop_data['yield_amount']
        base_yield = random.randint(min_yield, max_yield)
        if 'basic_farming' in getattr(self.game, 'completed_research', []):
            base_yield = int(base_yield * 1.25)
        final_yield = int(base_yield * (plot['health'] / 100))
        if final_yield <= 0:
            return {'success': False, 'message': '作物已经完全枯萎'}

        harvest_product = crop_data['harvest_product']
        self.game.player.add_item(harvest_product, final_yield)

        special_products = crop_data.get('special_products', {})
        for product, amount in special_products.items():
            if isinstance(amount, dict):
                min_q = int(amount.get('min', 1))
                max_q = int(amount.get('max', min_q))
            else:
                min_q, max_q = amount
                min_q, max_q = int(min_q), int(max_q)
            if random.random() < 0.7:
                qty = random.randint(min_q, max(min_q, max_q))
                self.game.player.add_item(product, qty)

        self.game.player.gain_skill_exp('farming', crop_data['exp_reward'])
        self.game.player.stats['crops_harvested'] += 1
        if hasattr(self.game, 'quests') and self.game.quests:
            self.game.quests.update_quest_progress('crop_harvested', quantity=final_yield)

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

        return {'success': True, 'message': f"收获了{final_yield}个{crop_data['name']}！", 'yield_amount': final_yield}

    def remove_weeds(self, location_id, plot_id):
        """除草"""
        plot = self.get_plot(location_id, plot_id)
        if not plot or plot['weeds'] == 0:
            return {'success': False, 'message': '没有杂草需要清除'}
        if self.game.player.stamina < 5:
            return {'success': False, 'message': '体力不足'}
        self.game.player.modify_stamina(-5)
        removed = min(plot['weeds'], 50)
        plot['weeds'] = max(0, plot['weeds'] - removed)
        self.game.player.gain_skill_exp('farming', 3)
        if hasattr(self.game, 'quests') and self.game.quests:
            self.game.quests.update_quest_progress('farm_action_completed', action='remove_weeds')
        return {'success': True, 'message': f'清除了{removed}%的杂草'}

    def remove_pests(self, location_id, plot_id):
        """除虫"""
        plot = self.get_plot(location_id, plot_id)
        if not plot or plot['pest_infestation'] == 0:
            return {'success': False, 'message': '没有害虫需要清除'}
        if not self.game.player.has_item('medicine'):
            return {'success': False, 'message': '需要药品来制作杀虫剂'}
        self.game.player.remove_item('medicine', 1)
        removed = min(plot['pest_infestation'], 70)
        plot['pest_infestation'] = max(0, plot['pest_infestation'] - removed)
        self.game.player.gain_skill_exp('farming', 5)
        return {'success': True, 'message': f'清除了{removed}%的害虫'}

    def fertilize_soil(self, location_id):
        """施肥"""
        if location_id not in self.farmlands:
            return {'success': False, 'message': '这里没有农田'}
        if not self.game.player.has_item('materials', 3):
            return {'success': False, 'message': '需要3个材料来制作肥料'}
        self.game.player.remove_item('materials', 3)
        increase = random.randint(1, 3)
        self.farmlands[location_id]['fertility'] = min(10, self.farmlands[location_id]['fertility'] + increase)
        self.game.player.gain_skill_exp('farming', 8)
        return {'success': True, 'message': f'施肥成功，土壤肥力提升了{increase}点'}

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
        new_id = len(farmland['plots'])
        farmland['plots'].append({
            'id': new_id, 'crop_type': None, 'planting_date': None, 'growth_stage': 0,
            'health': 100, 'water_level': 50, 'pest_infestation': 0, 'weeds': 0
        })
        self.game.player.gain_skill_exp('farming', 15)
        return {'success': True, 'message': '成功扩展了农田！', 'new_plot_id': new_id}

    def upgrade_farmland(self, location_id, upgrade_type):
        """升级农田设施"""
        if location_id not in self.farmlands:
            return {'success': False, 'message': '这里没有农田'}
        upgrades = {
            'irrigation': {'name': '灌溉系统', 'cost': {'electronic': 2, 'materials': 5}, 'description': '自动浇水'},
            'fence': {'name': '围栏', 'cost': {'wood': 10, 'materials': 3}, 'description': '防止野生动物'},
            'greenhouse': {'name': '温室', 'cost': {'electronic': 5, 'materials': 10, 'cloth': 8}, 'description': '控制环境'}
        }
        up = upgrades.get(upgrade_type)
        if not up:
            return {'success': False, 'message': '无效的升级类型'}
        if self.farmlands[location_id]['upgrades'][upgrade_type]:
            return {'success': False, 'message': f'{up["name"]}已经建造完成'}
        for item, amount in up['cost'].items():
            if not self.game.player.has_item(item, amount):
                return {'success': False, 'message': f'材料不足，需要{amount}个{self.game.items.get_item_name(item)}'}
        for item, amount in up['cost'].items():
            self.game.player.remove_item(item, amount)
        self.farmlands[location_id]['upgrades'][upgrade_type] = True
        self.game.player.gain_skill_exp('farming', 25)
        return {'success': True, 'message': f'成功建造了{up["name"]}！'}

    def get_crop_growth_description(self, growth_stage, total_stages):
        """获取作物生长阶段描述"""
        if growth_stage == 0:
            return "刚播种"
        if growth_stage < total_stages:
            progress = (growth_stage / total_stages) * 100
            if progress < 25: return "幼苗期"
            if progress < 50: return "生长期"
            if progress < 75: return "开花期"
            return "结果期"
        return "已成熟"

    def get_farmland_status(self, location_id):
        """获取农田状态"""
        if location_id not in self.farmlands:
            return None
        farmland = self.farmlands[location_id]
        status = {
            'location_id': location_id, 'fertility': farmland['fertility'],
            'water_source': farmland['water_source'], 'total_plots': len(farmland['plots']),
            'max_plots': farmland['max_plots'], 'empty_plots': len(self.get_available_plots(location_id)),
            'growing_crops': 0, 'mature_crops': 0, 'upgrades': farmland['upgrades'].copy(),
            'plots_details': []
        }
        for plot in farmland['plots']:
            plot_info = {
                'id': plot['id'], 'crop_type': plot['crop_type'], 'growth_stage': plot['growth_stage'],
                'health': plot['health'], 'water_level': plot['water_level'],
                'pest_infestation': plot['pest_infestation'], 'weeds': plot['weeds']
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
        current = self.game.season
        return [c for c in self.crops.values() if c['season_preference'] == ['all'] or current in c['season_preference']]

    def get_crop_info(self, crop_type):
        """获取作物详细信息"""
        return self.crops.get(crop_type)

    def get_all_crops(self):
        """获取所有作物"""
        return list(self.crops.values())