# -*- coding: utf-8 -*-

import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class QuestSystem:
    def __init__(self, game):
        self.game = game
        self.quests = {}
        self.active_quests = []
        self.completed_quests = []
        self.failed_quests = []
        self.quest_categories = {}
        self.initialized = False
        
    def initialize(self):
        """初始化任务系统"""
        try:
            self.create_quest_categories()
            self.create_quests()
            self.initialized = True
            logging.info("任务系统初始化完成")
        except Exception as e:
            logging.error(f"任务系统初始化失败: {e}")
            raise
    
    def create_quest_categories(self):
        """创建任务分类"""
        self.quest_categories = {
            'main': {
                'name': '主线任务',
                'color': '#FF6B35',
                'description': '推动故事发展的主要任务'
            },
            'side': {
                'name': '支线任务',
                'color': '#4ECDC4',
                'description': '可选的额外任务，提供奖励'
            },
            'daily': {
                'name': '日常任务',
                'color': '#45B7D1',
                'description': '每日刷新的小型任务'
            },
            'faction': {
                'name': '阵营任务',
                'color': '#96CEB4',
                'description': '与特定阵营相关的任务'
            },
            'exploration': {
                'name': '探索任务',
                'color': '#FFEAA7',
                'description': '探索世界和发现秘密'
            },
            'crafting': {
                'name': '制作任务',
                'color': '#DDA0DD',
                'description': '制作和收集相关任务'
            },
            'combat': {
                'name': '战斗任务',
                'color': '#F8B195',
                'description': '战斗和生存相关任务'
            }
        }
    
    def create_quests(self):
        """创建所有任务"""
        # === 主线任务 ===
        self.quests['main_01'] = {
            'id': 'main_01',
            'name': '初来乍到',
            'category': 'main',
            'difficulty': 1,
            'description': '在这个陌生的世界中生存下来，学习基本的生存技能。',
            'objectives': [
                {
                    'id': 'explore_starting_area',
                    'description': '探索起始区域',
                    'type': 'explore_location',
                    'target': 'starting_area',
                    'required_count': 1,
                    'current_count': 0
                },
                {
                    'id': 'collect_basic_supplies',
                    'description': '收集5个基础物资',
                    'type': 'collect_items',
                    'target': 'materials',
                    'required_count': 5,
                    'current_count': 0
                },
                {
                    'id': 'craft_first_item',
                    'description': '制作第一个物品',
                    'type': 'craft_item',
                    'target': 'any',
                    'required_count': 1,
                    'current_count': 0
                }
            ],
            'prerequisites': [],
            'rewards': {
                'exp': 100,
                'items': {'food': 5, 'water': 5, 'materials': 10},
                'money': 50,
                'unlocks': ['main_02']
            },
            'time_limit': None,
            'repeatable': False,
            'giver_npc': 'system',
            'story_text': '在这个破碎的世界中，每一个幸存者都要从零开始。学习生存的基本法则是你当前最重要的任务。'
        }
        
        self.quests['main_02'] = {
            'id': 'main_02',
            'name': '建立据点',
            'category': 'main',
            'difficulty': 2,
            'description': '找到一个安全的场所建立你的第一个庇护所。',
            'objectives': [
                {
                    'id': 'discover_safe_location',
                    'description': '发现3个安全地点（安全等级≥7）',
                    'type': 'discover_locations',
                    'target': 'safe',
                    'required_count': 3,
                    'current_count': 0
                },
                {
                    'id': 'build_shelter',
                    'description': '建造一个简易庇护所',
                    'type': 'craft_item',
                    'target': 'shelter',
                    'required_count': 1,
                    'current_count': 0
                },
                {
                    'id': 'store_supplies',
                    'description': '储备10个食物和10个水',
                    'type': 'collect_items',
                    'target': 'food_water',
                    'required_count': 20,
                    'current_count': 0
                }
            ],
            'prerequisites': ['main_01'],
            'rewards': {
                'exp': 200,
                'items': {'cloth_armor': 1, 'knife': 1},
                'money': 100,
                'unlocks': ['main_03']
            },
            'time_limit': None,
            'repeatable': False,
            'giver_npc': 'system',
            'story_text': '一个稳定的据点是长期生存的关键。找到合适的地点，建立你的家园。'
        }
        
        self.quests['main_03'] = {
            'id': 'main_03',
            'name': '寻找其他幸存者',
            'category': 'main',
            'difficulty': 3,
            'description': '在这个孤独的世界中，找到其他幸存者建立联系。',
            'objectives': [
                {
                    'id': 'meet_survivors',
                    'description': '遇到3个不同的NPC',
                    'type': 'meet_npcs',
                    'target': 'any',
                    'required_count': 3,
                    'current_count': 0
                },
                {
                    'id': 'complete_survivor_quest',
                    'description': '完成一个幸存者给予的任务',
                    'type': 'complete_quests',
                    'target': 'side',
                    'required_count': 1,
                    'current_count': 0
                },
                {
                    'id': 'establish_trade',
                    'description': '与商人进行交易',
                    'type': 'trade',
                    'target': 'any',
                    'required_count': 1,
                    'current_count': 0
                }
            ],
            'prerequisites': ['main_02'],
            'rewards': {
                'exp': 300,
                'items': {'map_fragment': 2, 'medicine': 3},
                'money': 150,
                'unlocks': ['main_04']
            },
            'time_limit': None,
            'repeatable': False,
            'giver_npc': 'system',
            'story_text': '人类是群居动物，即使在末日中也是如此。找到其他幸存者，建立新的社区。'
        }
        
        # === 支线任务 ===
        self.quests['side_01'] = {
            'id': 'side_01',
            'name': '老农的请求',
            'category': 'side',
            'difficulty': 2,
            'description': '帮助老农民恢复他的农田。',
            'objectives': [
                {
                    'id': 'clear_weeds',
                    'description': '清除农田里的杂草',
                    'type': 'farm_action',
                    'target': 'remove_weeds',
                    'required_count': 3,
                    'current_count': 0
                },
                {
                    'id': 'plant_crops',
                    'description': '种植2种不同的作物',
                    'type': 'plant_crops',
                    'target': 'any',
                    'required_count': 2,
                    'current_count': 0
                },
                {
                    'id': 'harvest_crops',
                    'description': '收获5个农作物',
                    'type': 'harvest_crops',
                    'target': 'any',
                    'required_count': 5,
                    'current_count': 0
                }
            ],
            'prerequisites': [],
            'rewards': {
                'exp': 150,
                'items': {'vegetable_seeds': 5, 'fresh_food': 3},
                'money': 80,
                'reputation': {'survivors': 10}
            },
            'time_limit': 7,  # 7天时间限制
            'repeatable': False,
            'giver_npc': 'old_farmer',
            'story_text': '这片土地曾经很肥沃，但现在...也许你能帮我让它重新焕发生机。'
        }
        
        self.quests['side_02'] = {
            'id': 'side_02',
            'name': '医生的困境',
            'category': 'side',
            'difficulty': 3,
            'description': '为诊所收集急需的医疗物资。',
            'objectives': [
                {
                    'id': 'collect_medicine',
                    'description': '收集5个药品',
                    'type': 'collect_items',
                    'target': 'medicine',
                    'required_count': 5,
                    'current_count': 0
                },
                {
                    'id': 'find_rare_herbs',
                    'description': '找到3个稀有草药',
                    'type': 'collect_items',
                    'target': 'rare_herbs',
                    'required_count': 3,
                    'current_count': 0
                },
                {
                    'id': 'deliver_supplies',
                    'description': '将物资送到诊所',
                    'type': 'deliver_items',
                    'target': 'medical_supplies',
                    'required_count': 1,
                    'current_count': 0
                }
            ],
            'prerequisites': ['main_03'],
            'rewards': {
                'exp': 200,
                'items': {'first_aid_kit': 1, 'antidote': 2},
                'money': 120,
                'reputation': {'survivors': 15},
                'unlocks': ['side_03']
            },
            'time_limit': 5,
            'repeatable': False,
            'giver_npc': 'doctor_li',
            'story_text': '伤员越来越多，但我们的医疗物资严重不足。你能帮我们找到一些吗？'
        }
        
        self.quests['side_03'] = {
            'id': 'side_03',
            'name': '清除威胁',
            'category': 'side',
            'difficulty': 4,
            'description':'清理区域内的危险生物，保护幸存者安全。',
            'objectives': [
                {
                    'id': 'defeat_mutants',
                    'description': '击败10个变异生物',
                    'type': 'defeat_enemies',
                    'target': 'mutant',
                    'required_count': 10,
                    'current_count': 0
                },
                {
                    'id': 'defeat_raiders',
                    'description': '击败5个掠夺者',
                    'type': 'defeat_enemies',
                    'target': 'raider',
                    'required_count': 5,
                    'current_count': 0
                },
                {
                    'id': 'clear_danger_zone',
                    'description': '清理一个危险区域（安全等级≤3）',
                    'type': 'explore_location',
                    'target': 'dangerous',
                    'required_count': 1,
                    'current_count': 0
                }
            ],
            'prerequisites': ['side_02'],
            'rewards': {
                'exp': 350,
                'items': {'assault_rifle': 1, 'tactical_vest': 1},
                'money': 200,
                'reputation': {'survivors': 25}
            },
            'time_limit': None,
            'repeatable': True,
            'giver_npc': 'security_chief',
            'story_text': '这些怪物和掠夺者威胁着我们的安全。我们需要有人来清理它们。'
        }
        
        # === 日常任务 ===
        self.quests['daily_01'] = {
            'id': 'daily_01',
            'name': '日常收集',
            'category': 'daily',
            'difficulty': 1,
            'description': '收集一些基础生存物资。',
            'objectives': [
                {
                    'id': 'collect_daily_materials',
                    'description': '收集10个材料',
                    'type': 'collect_items',
                    'target': 'materials',
                    'required_count': 10,
                    'current_count': 0
                }
            ],
            'prerequisites': [],
            'rewards': {
                'exp': 50,
                'items': {'food': 2, 'water': 2},
                'money': 30
            },
            'time_limit': 1,
            'repeatable': True,
            'giver_npc': 'system',
            'story_text': '每天的物资收集是生存的基础。'
        }
        
        self.quests['daily_02'] = {
            'id': 'daily_02',
            'name': '巡逻任务',
            'category': 'daily',
            'difficulty': 2,
            'description': '巡逻周边区域，确保安全。',
            'objectives': [
                {
                    'id': 'explore_daily',
                    'description': '探索3个不同的地点',
                    'type': 'explore_locations',
                    'target': 'any',
                    'required_count': 3,
                    'current_count': 0
                },
                {
                    'id': 'defeat_daily_enemies',
                    'description': '击败3个敌人',
                    'type': 'defeat_enemies',
                    'target': 'any',
                    'required_count': 3,
                    'current_count': 0
                }
            ],
            'prerequisites': [],
            'rewards': {
                'exp': 80,
                'items': {'medicine': 1, 'materials': 5},
                'money': 50
            },
            'time_limit': 1,
            'repeatable': True,
            'giver_npc': 'system',
            'story_text': '保持警惕，及时发现潜在威胁。'
        }
        
        # === 探索任务 ===
        self.quests['explore_01'] = {
            'id': 'explore_01',
            'name': '地图绘制者',
            'category': 'exploration',
            'difficulty': 2,
            'description': '探索未知区域，完善世界地图。',
            'objectives': [
                {
                    'id': 'discover_new_locations',
                    'description': '发现5个新地点',
                    'type': 'discover_locations',
                    'target': 'any',
                    'required_count': 5,
                    'current_count': 0
                },
                {
                    'id': 'collect_map_fragments',
                    'description': '收集3个地图碎片',
                    'type': 'collect_items',
                    'target': 'map_fragment',
                    'required_count': 3,
                    'current_count': 0
                }
            ],
            'prerequisites': ['main_01'],
            'rewards': {
                'exp': 180,
                'items': {'advanced_map': 1},
                'money': 100,
                'unlocks': ['explore_02']
            },
            'time_limit': None,
            'repeatable': False,
            'giver_npc': 'cartographer',
            'story_text': '这个世界还有很多未知等待发现。每一片地图碎片都可能指引我们找到重要的资源。'
        }
        
        # === 制作任务 ===
        self.quests['craft_01'] = {
            'id': 'craft_01',
            'name': '工匠的试炼',
            'category': 'crafting',
            'difficulty': 3,
            'description': '证明你的制作技能，制作一些高级物品。',
            'objectives': [
                {
                    'id': 'craft_weapon',
                    'description': '制作一把武器',
                    'type': 'craft_item',
                    'target': 'weapon',
                    'required_count': 1,
                    'current_count': 0
                },
                {
                    'id': 'craft_armor',
                    'description': '制作一件防具',
                    'type': 'craft_item',
                    'target': 'armor',
                    'required_count': 1,
                    'current_count': 0
                },
                {
                    'id': 'craft_tool',
                    'description': '制作一个工具',
                    'type': 'craft_item',
                    'target': 'tool',
                    'required_count': 1,
                    'current_count': 0
                }
            ],
            'prerequisites': ['main_02'],
            'rewards': {
                'exp': 220,
                'items': {'advanced_tools': 1},
                'money': 150,
                'reputation': {'craftsmen': 20}
            },
            'time_limit': None,
            'repeatable': False,
            'giver_npc': 'master_crafter',
            'story_text': '在这个世界里，一个好的工匠比十个战士更有价值。让我看看你的手艺。'
        }
        
        logging.info(f"创建了{len(self.quests)}个任务")
    
    def load_data(self, save_data):
        """加载任务系统数据"""
        try:
            self.active_quests = save_data.get('active_quests', [])
            self.completed_quests = save_data.get('completed_quests', [])
            self.failed_quests = save_data.get('failed_quests', [])
            
            # 更新任务进度
            quests_data = save_data.get('quests_progress', {})
            for quest_id, quest_data in quests_data.items():
                if quest_id in self.quests:
                    for i, objective in enumerate(quest_data.get('objectives', [])):
                        if i < len(self.quests[quest_id]['objectives']):
                            self.quests[quest_id]['objectives'][i]['current_count'] = objective.get('current_count', 0)
            
            self.initialized = True
            logging.info("任务系统数据加载完成")
        except Exception as e:
            logging.error(f"加载任务系统数据失败: {e}")
            raise
    
    def get_save_data(self):
        """获取保存数据"""
        quests_progress = {}
        for quest_id in self.quests:
            quests_progress[quest_id] = {
                'objectives': [obj.copy() for obj in self.quests[quest_id]['objectives']]
            }
        
        return {
            'active_quests': self.active_quests,
            'completed_quests': self.completed_quests,
            'failed_quests': self.failed_quests,
            'quests_progress': quests_progress
        }
    
    def start_quest(self, quest_id):
        """开始任务"""
        if quest_id not in self.quests:
            return {'success': False, 'message': '未知的任务'}
        
        quest = self.quests[quest_id]
        
        # 检查前置任务
        for prereq in quest['prerequisites']:
            if prereq not in self.completed_quests:
                return {'success': False, 'message': '前置任务未完成'}
        
        # 检查是否已经接受或完成
        if quest_id in self.active_quests:
            return {'success': False, 'message': '任务已在进行中'}
        
        if quest_id in self.completed_quests and not quest['repeatable']:
            return {'success': False, 'message': '任务已完成且不可重复'}
        
        # 添加到活跃任务
        self.active_quests.append(quest_id)
        
        # 记录任务开始时间（用于限时任务）
        if 'start_time' not in quest:
            quest['start_time'] = self.game.game_time
        
        logging.info(f"开始任务: {quest['name']}")
        
        self.game.add_game_log(f"新任务: {quest['name']}")
        self.game.add_game_log(quest['description'])
        
        return {'success': True, 'message': f"开始任务: {quest['name']}"}
    
    def update_quest_progress(self, event_type, **kwargs):
        """更新任务进度"""
        updated_quests = []
        
        for quest_id in self.active_quests[:]:
            quest = self.quests.get(quest_id)
            if not quest:
                continue
            
            updated = False
            all_completed = True
            
            for objective in quest['objectives']:
                if self.check_objective_completion(objective, event_type, kwargs):
                    updated = True
                
                if objective['current_count'] < objective['required_count']:
                    all_completed = False
            
            if updated:
                updated_quests.append(quest_id)
            
            # 检查任务完成
            if all_completed:
                self.complete_quest(quest_id)
            # 检查任务失败（限时任务）
            elif quest['time_limit'] and self.is_quest_expired(quest):
                self.fail_quest(quest_id)
        
        return updated_quests
    
    def check_objective_completion(self, objective, event_type, event_data):
        """检查目标完成情况"""
        obj_type = objective['type']
        updated = False
        
        if obj_type == 'explore_location' and event_type == 'location_discovered':
            location = event_data.get('location')
            if location and self.matches_target(objective, location):
                objective['current_count'] += 1
                updated = True
        
        elif obj_type == 'collect_items' and event_type == 'item_collected':
            item_id = event_data.get('item_id')
            quantity = event_data.get('quantity', 1)
            if item_id and self.matches_target(objective, item_id):
                objective['current_count'] += quantity
                updated = True
        
        elif obj_type == 'craft_item' and event_type == 'item_crafted':
            item_id = event_data.get('item_id')
            if item_id and self.matches_target(objective, item_id):
                objective['current_count'] += 1
                updated = True
        
        elif obj_type == 'defeat_enemies' and event_type == 'enemy_defeated':
            enemy_type = event_data.get('enemy_type')
            if enemy_type and self.matches_target(objective, enemy_type):
                objective['current_count'] += 1
                updated = True
        
        elif obj_type == 'meet_npcs' and event_type == 'npc_met':
            npc_type = event_data.get('npc_type')
            if npc_type and self.matches_target(objective, npc_type):
                objective['current_count'] += 1
                updated = True
        
        elif obj_type == 'farm_action' and event_type == 'farm_action_completed':
            action_type = event_data.get('action_type')
            if action_type and self.matches_target(objective, action_type):
                objective['current_count'] += 1
                updated = True
        
        # 确保不超过要求数量
        if objective['current_count'] > objective['required_count']:
            objective['current_count'] = objective['required_count']
        
        return updated
    
    def matches_target(self, objective, value):
        """检查值是否匹配目标"""
        target = objective['target']
        
        if target == 'any':
            return True
        elif target == 'safe':
            # 安全地点检查
            if hasattr(value, 'safety_level'):
                return value.safety_level >= 7
            return False
        elif target == 'dangerous':
            # 危险地点检查
            if hasattr(value, 'safety_level'):
                return value.safety_level <= 3
            return False
        elif target == 'mutant':
            return 'mutant' in value.lower()
        elif target == 'raider':
            return 'raider' in value.lower()
        elif target == 'food_water':
            return value in ['food', 'water']
        else:
            return target == value
    
    def is_quest_expired(self, quest):
        """检查任务是否过期"""
        if not quest['time_limit'] or 'start_time' not in quest:
            return False
        
        time_passed = self.game.game_time - quest['start_time']
        return time_passed.days >= quest['time_limit']
    
    def complete_quest(self, quest_id):
        """完成任务"""
        if quest_id not in self.active_quests:
            return
        
        quest = self.quests[quest_id]
        
        # 从活跃任务移除
        self.active_quests.remove(quest_id)
        
        # 添加到完成列表
        if quest_id not in self.completed_quests or quest['repeatable']:
            if quest_id not in self.completed_quests:
                self.completed_quests.append(quest_id)
            
            # 发放奖励
            self.give_quest_rewards(quest)
            
            # 解锁新任务
            self.unlock_new_quests(quest)
            
            logging.info(f"完成任务: {quest['name']}")
            self.game.add_game_log(f"🎉 完成任务: {quest['name']}！")
        
        # 更新统计数据
        self.game.player.stats['quests_completed'] += 1
    
    def fail_quest(self, quest_id):
        """任务失败"""
        if quest_id not in self.active_quests:
            return
        
        quest = self.quests[quest_id]
        
        # 从活跃任务移除
        self.active_quests.remove(quest_id)
        
        # 添加到失败列表
        self.failed_quests.append(quest_id)
        
        logging.info(f"任务失败: {quest['name']}")
        self.game.add_game_log(f"❌ 任务失败: {quest['name']}")
    
    def give_quest_rewards(self, quest):
        """发放任务奖励"""
        rewards = quest['rewards']
        
        # 经验奖励
        if 'exp' in rewards:
            # 平均分配到各个技能
            exp_per_skill = rewards['exp'] // 3
            self.game.player.gain_skill_exp('survival', exp_per_skill)
            self.game.player.gain_skill_exp('combat', exp_per_skill)
            self.game.player.gain_skill_exp('crafting', exp_per_skill)
        
        # 物品奖励
        if 'items' in rewards:
            for item_id, quantity in rewards['items'].items():
                self.game.player.add_item(item_id, quantity)
                self.game.add_game_log(f"获得: {self.game.items.get_item_name(item_id)} x{quantity}")
        
        # 金钱奖励
        if 'money' in rewards:
            # 这里可以添加金钱系统
            pass
        
        # 声望奖励
        if 'reputation' in rewards:
            # 这里可以添加声望系统
            pass
    
    def unlock_new_quests(self, quest):
        """解锁新任务"""
        rewards = quest['rewards']
        
        if 'unlocks' in rewards:
            for new_quest_id in rewards['unlocks']:
                if new_quest_id in self.quests:
                    self.game.add_game_log(f"新任务已解锁: {self.quests[new_quest_id]['name']}")
    
    def get_available_quests(self):
        """获取可接受的任务"""
        available = []
        
        for quest_id, quest in self.quests.items():
            # 检查是否已经完成（非重复任务）
            if quest_id in self.completed_quests and not quest['repeatable']:
                continue
            
            # 检查是否正在进行
            if quest_id in self.active_quests:
                continue
            
            # 检查是否失败
            if quest_id in self.failed_quests and not quest['repeatable']:
                continue
            
            # 检查前置任务
            prerequisites_met = True
            for prereq in quest['prerequisites']:
                if prereq not in self.completed_quests:
                    prerequisites_met = False
                    break
            
            if prerequisites_met:
                available.append(quest)
        
        return available
    
    def get_quest_progress(self, quest_id):
        """获取任务进度"""
        if quest_id not in self.quests:
            return None
        
        quest = self.quests[quest_id]
        progress = {
            'quest': quest,
            'objectives': [],
            'completed': quest_id in self.completed_quests,
            'failed': quest_id in self.failed_quests,
            'active': quest_id in self.active_quests
        }
        
        for objective in quest['objectives']:
            progress['objectives'].append({
                'description': objective['description'],
                'current': objective['current_count'],
                'required': objective['required_count'],
                'completed': objective['current_count'] >= objective['required_count']
            })
        
        return progress
    
    def get_all_quests_by_category(self, category):
        """按分类获取所有任务"""
        return [quest for quest in self.quests.values() if quest['category'] == category]
    
    def check_daily_quests(self):
        """检查日常任务"""
        # 重置日常任务
        daily_quests = self.get_all_quests_by_category('daily')
        for quest in daily_quests:
            if quest['id'] in self.active_quests:
                self.fail_quest(quest['id'])
            elif quest['id'] in self.completed_quests:
                self.completed_quests.remove(quest['id'])
            
            # 重置任务进度
            for objective in quest['objectives']:
                objective['current_count'] = 0
            
            # 自动开始日常任务
            self.start_quest(quest['id'])
    
    def check_timed_quests(self):
        """检查限时任务"""
        for quest_id in self.active_quests[:]:
            quest = self.quests[quest_id]
            if quest['time_limit'] and self.is_quest_expired(quest):
                self.fail_quest(quest_id)
    
    def abandon_quest(self, quest_id):
        """放弃任务"""
        if quest_id not in self.active_quests:
            return {'success': False, 'message': '任务未在进行中'}
        
        self.active_quests.remove(quest_id)
        
        # 重置任务进度
        quest = self.quests[quest_id]
        for objective in quest['objectives']:
            objective['current_count'] = 0
        
        if 'start_time' in quest:
            del quest['start_time']
        
        logging.info(f"放弃任务: {quest['name']}")
        return {'success': True, 'message': f"已放弃任务: {quest['name']}"}
    
    def get_quest_giver_name(self, giver_id):
        """获取任务给予者名称"""
        giver_names = {
            'system': '系统',
            'old_farmer': '老农民',
            'doctor_li': '李医生',
            'security_chief': '安保队长',
            'cartographer': '地图绘制师',
            'master_crafter': '工匠大师'
        }
        return giver_names.get(giver_id, giver_id)
