# -*- coding: utf-8 -*-

import random
import logging
from datetime import datetime

class QuestSystem:
    def __init__(self, game):
        self.game = game
        self.quests = {}
        self.active_quests = []
        self.completed_quests = []
        self.failed_quests = []
        self.initialized = False

    def initialize(self):
        try:
            self.create_quests()
            self.initialized = True
            logging.info("任务系统初始化完成")
        except Exception as e:
            logging.error(f"任务系统初始化失败: {e}")
            raise

    def create_quests(self):
        """创建所有任务"""
        # === 主线任务 ===
        self.quests['main_01'] = {
            'id': 'main_01', 'name': '初来乍到', 'category': 'main', 'difficulty': 1,
            'description': '在这个陌生的世界中生存下来，学习基本的生存技能。',
            'objectives': [
                {'id': 'explore_start', 'description': '探索起始区域', 'type': 'explore_location', 'target': 'starting_area', 'required': 1, 'current': 0},
                {'id': 'collect', 'description': '收集5个基础物资', 'type': 'collect_items', 'target': 'materials', 'required': 5, 'current': 0},
                {'id': 'craft', 'description': '制作第一个物品', 'type': 'craft_item', 'target': 'any', 'required': 1, 'current': 0}
            ],
            'prerequisites': [],
            'rewards': {'exp': 100, 'items': {'food': 5, 'water': 5, 'materials': 10}, 'money': 50, 'unlocks': ['main_02']},
            'time_limit': None, 'repeatable': False, 'giver_npc': 'system',
            'story_text': '在这个破碎的世界中，每一个幸存者都要从零开始。学习生存的基本法则是你当前最重要的任务。'
        }
        self.quests['main_02'] = {
            'id': 'main_02', 'name': '建立据点', 'category': 'main', 'difficulty': 2,
            'description': '找到一个安全的场所建立你的第一个庇护所。',
            'objectives': [
                {'id': 'disc_safe', 'description': '发现3个安全地点（安全等级≥7）', 'type': 'discover_locations', 'target': 'safe', 'required': 3, 'current': 0},
                {'id': 'build', 'description': '建造一个简易庇护所', 'type': 'craft_item', 'target': 'shelter', 'required': 1, 'current': 0},
                {'id': 'store', 'description': '储备10个食物和10个水', 'type': 'collect_items', 'target': 'food_water', 'required': 20, 'current': 0}
            ],
            'prerequisites': ['main_01'],
            'rewards': {'exp': 200, 'items': {'cloth_armor': 1, 'knife': 1}, 'money': 100, 'unlocks': ['main_03']},
            'time_limit': None, 'repeatable': False, 'giver_npc': 'system'
        }
        self.quests['main_03'] = {
            'id': 'main_03', 'name': '寻找其他幸存者', 'category': 'main', 'difficulty': 3,
            'description': '在这个孤独的世界中，找到其他幸存者建立联系。',
            'objectives': [
                {'id': 'meet', 'description': '遇到3个不同的NPC', 'type': 'meet_npcs', 'target': 'any', 'required': 3, 'current': 0},
                {'id': 'quest', 'description': '完成一个幸存者给予的任务', 'type': 'complete_quests', 'target': 'side', 'required': 1, 'current': 0},
                {'id': 'trade', 'description': '与商人进行交易', 'type': 'trade', 'target': 'any', 'required': 1, 'current': 0}
            ],
            'prerequisites': ['main_02'],
            'rewards': {'exp': 300, 'items': {'map_fragment': 2, 'medicine': 3}, 'money': 150, 'unlocks': ['main_04']},
            'time_limit': None, 'repeatable': False, 'giver_npc': 'system'
        }
        self.quests['main_04'] = {
            'id': 'main_04', 'name': '真相的碎片', 'category': 'main', 'difficulty': 4,
            'description': '收集地图碎片，寻找灾难的真相。',
            'objectives': [
                {'id': 'collect_maps', 'description': '收集5个地图碎片', 'type': 'collect_items', 'target': 'map_fragment', 'required': 5, 'current': 0},
                {'id': 'find_journal', 'description': '找到红色黎明计划科学家的日志', 'type': 'collect_items', 'target': 'research_data', 'required': 1, 'current': 0},
                {'id': 'read_log', 'description': '解读灾难的真正原因', 'type': 'read_document', 'target': 'research_data', 'required': 1, 'current': 0}
            ],
            'prerequisites': ['main_03'],
            'rewards': {'exp': 400, 'items': {'research_data': 3, 'advanced_map': 1}, 'money': 200, 'unlocks': ['main_05']},
            'time_limit': None, 'repeatable': False, 'giver_npc': 'cartographer'
        }
        self.quests['main_05'] = {
            'id': 'main_05', 'name': '科技教会的秘密', 'category': 'main', 'difficulty': 5,
            'description': '潜入科技教会，获取能量核心数据。',
            'objectives': [
                {'id': 'infiltrate', 'description': '潜入科技教会的研究所', 'type': 'explore_location', 'target': 'research_lab', 'required': 1, 'current': 0},
                {'id': 'get_data', 'description': '获取能量核心数据', 'type': 'collect_items', 'target': 'energy_core', 'required': 1, 'current': 0},
                {'id': 'talk_scientist', 'description': '与疯狂科学家对话', 'type': 'talk_npc', 'target': 'mad_scientist', 'required': 1, 'current': 0}
            ],
            'prerequisites': ['main_04'],
            'rewards': {'exp': 500, 'items': {'energy_core': 1, 'tech_blueprint': 2}, 'money': 250, 'unlocks': ['main_06']},
            'time_limit': None, 'repeatable': False, 'giver_npc': 'system'
        }
        self.quests['main_06'] = {
            'id': 'main_06', 'name': '联合幸存者', 'category': 'main', 'difficulty': 6,
            'description': '团结所有幸存者，建立联盟。',
            'objectives': [
                {'id': 'reputation', 'description': '提高与幸存者联盟的关系至崇敬', 'type': 'reputation', 'target': 'survivors', 'required': 80, 'current': 0},
                {'id': 'help_settlements', 'description': '帮助3个幸存者据点解决危机', 'type': 'complete_quests', 'target': 'side', 'required': 3, 'current': 0},
                {'id': 'build_network', 'description': '建立幸存者通讯网络', 'type': 'craft_item', 'target': 'radio', 'required': 1, 'current': 0}
            ],
            'prerequisites': ['main_05'],
            'rewards': {'exp': 600, 'items': {'alliance_medal': 1, 'communication_device': 1}, 'money': 300, 'unlocks': ['main_07']},
            'time_limit': None, 'repeatable': False, 'giver_npc': 'security_chief'
        }
        self.quests['main_07'] = {
            'id': 'main_07', 'name': '最终对决', 'category': 'main', 'difficulty': 7,
            'description': '击败掠夺者指挥官，摧毁科技教会的危险实验。',
            'objectives': [
                {'id': 'defeat_commander', 'description': '击败掠夺者指挥官', 'type': 'defeat_enemies', 'target': 'raider_commander', 'required': 1, 'current': 0},
                {'id': 'destroy_lab', 'description': '摧毁科技教会的危险实验', 'type': 'special_action', 'target': 'research_lab', 'required': 1, 'current': 0},
                {'id': 'repair_core', 'description': '修复地核稳定装置', 'type': 'repair_item', 'target': 'core_stabilizer', 'required': 1, 'current': 0}
            ],
            'prerequisites': ['main_06'],
            'rewards': {'exp': 800, 'items': {'legendary_weapon': 1, 'power_armor': 1}, 'money': 400, 'unlocks': ['main_08']},
            'time_limit': None, 'repeatable': False, 'giver_npc': 'system'
        }
        self.quests['main_08'] = {
            'id': 'main_08', 'name': '新黎明', 'category': 'main', 'difficulty': 8,
            'description': '建立永久性幸存者城市，恢复基础教育和医疗系统。',
            'objectives': [
                {'id': 'build_city', 'description': '建立永久性幸存者城市', 'type': 'build_structure', 'target': 'city', 'required': 1, 'current': 0},
                {'id': 'restore_edu', 'description': '恢复基础教育系统', 'type': 'build_structure', 'target': 'school', 'required': 1, 'current': 0},
                {'id': 'restore_med', 'description': '恢复医疗系统', 'type': 'build_structure', 'target': 'hospital', 'required': 1, 'current': 0}
            ],
            'prerequisites': ['main_07'],
            'rewards': {'exp': 1000, 'items': {'city_founder_medal': 1, 'legacy_book': 1}, 'money': 500, 'unlocks': []},
            'time_limit': None, 'repeatable': False, 'giver_npc': 'system'
        }

        # === 支线任务 ===
        self.quests['side_01'] = {
            'id': 'side_01', 'name': '老农的请求', 'category': 'side', 'difficulty': 2,
            'description': '帮助老农民恢复他的农田。',
            'objectives': [
                {'id': 'clear_weeds', 'description': '清除农田里的杂草', 'type': 'farm_action', 'target': 'remove_weeds', 'required': 3, 'current': 0},
                {'id': 'plant_crops', 'description': '种植2种不同的作物', 'type': 'plant_crops', 'target': 'any', 'required': 2, 'current': 0},
                {'id': 'harvest_crops', 'description': '收获5个农作物', 'type': 'harvest_crops', 'target': 'any', 'required': 5, 'current': 0}
            ],
            'prerequisites': [],
            'rewards': {'exp': 150, 'items': {'vegetable_seeds': 5, 'fresh_food': 3}, 'money': 80, 'reputation': {'survivors': 10}},
            'time_limit': 7, 'repeatable': False, 'giver_npc': 'old_farmer'
        }
        self.quests['side_02'] = {
            'id': 'side_02', 'name': '医生的困境', 'category': 'side', 'difficulty': 3,
            'description': '为诊所收集急需的医疗物资。',
            'objectives': [
                {'id': 'collect_medicine', 'description': '收集5个药品', 'type': 'collect_items', 'target': 'medicine', 'required': 5, 'current': 0},
                {'id': 'find_herbs', 'description': '找到3个稀有草药', 'type': 'collect_items', 'target': 'rare_herbs', 'required': 3, 'current': 0},
                {'id': 'deliver', 'description': '将物资送到诊所', 'type': 'deliver_items', 'target': 'clinic', 'required': 1, 'current': 0}
            ],
            'prerequisites': ['main_03'],
            'rewards': {'exp': 200, 'items': {'first_aid_kit': 1, 'antidote': 2}, 'money': 120, 'reputation': {'survivors': 15}, 'unlocks': ['side_03']},
            'time_limit': 5, 'repeatable': False, 'giver_npc': 'doctor_li'
        }
        self.quests['side_03'] = {
            'id': 'side_03', 'name': '清除威胁', 'category': 'side', 'difficulty': 4,
            'description': '清理区域内的危险生物，保护幸存者安全。',
            'objectives': [
                {'id': 'defeat_mutants', 'description': '击败10个变异生物', 'type': 'defeat_enemies', 'target': 'mutant', 'required': 10, 'current': 0},
                {'id': 'defeat_raiders', 'description': '击败5个掠夺者', 'type': 'defeat_enemies', 'target': 'raider', 'required': 5, 'current': 0},
                {'id': 'clear_danger', 'description': '清理一个危险区域（安全等级≤3）', 'type': 'explore_location', 'target': 'dangerous', 'required': 1, 'current': 0}
            ],
            'prerequisites': ['side_02'],
            'rewards': {'exp': 350, 'items': {'assault_rifle': 1, 'tactical_vest': 1}, 'money': 200, 'reputation': {'survivors': 25}},
            'time_limit': None, 'repeatable': True, 'giver_npc': 'security_chief'
        }

        # === 日常任务 ===
        self.quests['daily_01'] = {
            'id': 'daily_01', 'name': '日常收集', 'category': 'daily', 'difficulty': 1,
            'description': '收集一些基础生存物资。',
            'objectives': [{'id': 'collect', 'description': '收集10个材料', 'type': 'collect_items', 'target': 'materials', 'required': 10, 'current': 0}],
            'prerequisites': [], 'rewards': {'exp': 50, 'items': {'food': 2, 'water': 2}, 'money': 30},
            'time_limit': 1, 'repeatable': True, 'giver_npc': 'system'
        }
        self.quests['daily_02'] = {
            'id': 'daily_02', 'name': '巡逻任务', 'category': 'daily', 'difficulty': 2,
            'description': '巡逻周边区域，确保安全。',
            'objectives': [
                {'id': 'explore', 'description': '探索3个不同的地点', 'type': 'explore_locations', 'target': 'any', 'required': 3, 'current': 0},
                {'id': 'defeat', 'description': '击败3个敌人', 'type': 'defeat_enemies', 'target': 'any', 'required': 3, 'current': 0}
            ],
            'prerequisites': [], 'rewards': {'exp': 80, 'items': {'medicine': 1, 'materials': 5}, 'money': 50},
            'time_limit': 1, 'repeatable': True, 'giver_npc': 'system'
        }

        # === 探索任务 ===
        self.quests['explore_01'] = {
            'id': 'explore_01', 'name': '地图绘制者', 'category': 'exploration', 'difficulty': 2,
            'description': '探索未知区域，完善世界地图。',
            'objectives': [
                {'id': 'discover', 'description': '发现5个新地点', 'type': 'discover_locations', 'target': 'any', 'required': 5, 'current': 0},
                {'id': 'collect_maps', 'description': '收集3个地图碎片', 'type': 'collect_items', 'target': 'map_fragment', 'required': 3, 'current': 0}
            ],
            'prerequisites': ['main_01'],
            'rewards': {'exp': 180, 'items': {'advanced_map': 1}, 'money': 100, 'unlocks': ['explore_02']},
            'time_limit': None, 'repeatable': False, 'giver_npc': 'cartographer'
        }

        # === 制作任务 ===
        self.quests['craft_01'] = {
            'id': 'craft_01', 'name': '工匠的试炼', 'category': 'crafting', 'difficulty': 3,
            'description': '证明你的制作技能，制作一些高级物品。',
            'objectives': [
                {'id': 'craft_weapon', 'description': '制作一把武器', 'type': 'craft_item', 'target': 'weapon', 'required': 1, 'current': 0},
                {'id': 'craft_armor', 'description': '制作一件防具', 'type': 'craft_item', 'target': 'armor', 'required': 1, 'current': 0},
                {'id': 'craft_tool', 'description': '制作一个工具', 'type': 'craft_item', 'target': 'tool', 'required': 1, 'current': 0}
            ],
            'prerequisites': ['main_02'],
            'rewards': {'exp': 220, 'items': {'advanced_tools': 1}, 'money': 150, 'reputation': {'craftsmen': 20}},
            'time_limit': None, 'repeatable': False, 'giver_npc': 'master_crafter'
        }

        # === 战斗任务 ===
        self.quests['combat_01'] = {
            'id': 'combat_01', 'name': '猎杀变异兽', 'category': 'combat', 'difficulty': 3,
            'description': '消灭威胁营地的变异生物。',
            'objectives': [
                {'id': 'hunt', 'description': '击败5只变异狼', 'type': 'defeat_enemies', 'target': 'mutant_wolf', 'required': 5, 'current': 0},
                {'id': 'collect', 'description': '收集3张狼皮', 'type': 'collect_items', 'target': 'leather', 'required': 3, 'current': 0}
            ],
            'prerequisites': [],
            'rewards': {'exp': 250, 'items': {'hunting_knife': 1}, 'money': 120, 'reputation': {'survivors': 15}},
            'time_limit': None, 'repeatable': True, 'giver_npc': 'security_chief'
        }

        logging.info(f"创建了{len(self.quests)}个任务")

    def load_data(self, save_data):
        try:
            self.active_quests = save_data.get('active_quests', [])
            self.completed_quests = save_data.get('completed_quests', [])
            self.failed_quests = save_data.get('failed_quests', [])
            quests_progress = save_data.get('quests_progress', {})
            for qid, qdata in quests_progress.items():
                if qid in self.quests:
                    for i, obj in enumerate(qdata.get('objectives', [])):
                        if i < len(self.quests[qid]['objectives']):
                            self.quests[qid]['objectives'][i]['current'] = obj.get('current', 0)
            self.initialized = True
            logging.info("任务系统数据加载完成")
        except Exception as e:
            logging.error(f"加载任务系统数据失败: {e}")
            raise

    def get_save_data(self):
        progress = {}
        for qid, quest in self.quests.items():
            progress[qid] = {
                'objectives': [{'current': obj['current']} for obj in quest['objectives']]
            }
        return {
            'active_quests': self.active_quests,
            'completed_quests': self.completed_quests,
            'failed_quests': self.failed_quests,
            'quests_progress': progress
        }

    def start_quest(self, quest_id):
        if quest_id not in self.quests:
            return {'success': False, 'message': '未知的任务'}
        quest = self.quests[quest_id]

        for prereq in quest['prerequisites']:
            if prereq not in self.completed_quests:
                return {'success': False, 'message': '前置任务未完成'}

        if quest_id in self.active_quests:
            return {'success': False, 'message': '任务已在进行中'}
        if quest_id in self.completed_quests and not quest['repeatable']:
            return {'success': False, 'message': '任务已完成且不可重复'}

        self.active_quests.append(quest_id)
        quest['start_time'] = self.game.game_time

        logging.info(f"开始任务: {quest['name']}")
        self.game.add_game_log(f"新任务: {quest['name']}")
        self.game.add_game_log(quest['description'])

        return {'success': True, 'message': f"开始任务: {quest['name']}"}

    def update_quest_progress(self, event_type, **kwargs):
        updated = []
        for qid in list(self.active_quests):
            quest = self.quests.get(qid)
            if not quest:
                continue

            any_update = False
            all_completed = True

            for obj in quest['objectives']:
                if obj['current'] < obj['required']:
                    if self._check_objective(obj, event_type, kwargs):
                        any_update = True
                if obj['current'] < obj['required']:
                    all_completed = False

            if any_update:
                updated.append(qid)

            if all_completed:
                self.complete_quest(qid)

        return updated

    def _check_objective(self, objective, event_type, data):
        t = objective['type']
        updated = False

        if t == 'explore_location' and event_type == 'location_discovered':
            target = objective['target']
            loc = data.get('location')
            if target == 'any' or loc == target or (target == 'dangerous' and loc and loc.safety_level <= 3):
                objective['current'] += 1
                updated = True

        elif t == 'collect_items' and event_type == 'item_collected':
            target = objective['target']
            item_id = data.get('item_id')
            qty = data.get('quantity', 1)
            if target == 'any' or target == item_id or (target == 'food_water' and item_id in ['food', 'water']):
                objective['current'] += qty
                updated = True

        elif t == 'craft_item' and event_type == 'item_crafted':
            target = objective['target']
            item_id = data.get('item_id')
            if target == 'any' or target == item_id:
                objective['current'] += 1
                updated = True

        elif t == 'defeat_enemies' and event_type == 'enemy_defeated':
            target = objective['target']
            enemy_type = data.get('enemy_type')
            if target == 'any' or target == enemy_type or (target == 'mutant' and 'mutant' in enemy_type) or (target == 'raider' and 'raider' in enemy_type):
                objective['current'] += 1
                updated = True

        elif t == 'meet_npcs' and event_type == 'npc_met':
            objective['current'] += 1
            updated = True

        elif t == 'discover_locations' and event_type == 'location_discovered':
            if objective['target'] == 'any' or (objective['target'] == 'safe' and data.get('location') and data['location'].safety_level >= 7):
                objective['current'] += 1
                updated = True

        elif t == 'farm_action' and event_type == 'farm_action_completed':
            action = data.get('action')
            if objective['target'] == 'any' or action == objective['target']:
                objective['current'] += 1
                updated = True

        elif t == 'plant_crops' and event_type == 'crop_planted':
            objective['current'] += 1
            updated = True

        elif t == 'harvest_crops' and event_type == 'crop_harvested':
            qty = data.get('quantity', 1)
            objective['current'] += qty
            updated = True

        elif t == 'trade' and event_type == 'trade_completed':
            objective['current'] += 1
            updated = True

        elif t == 'complete_quests' and event_type == 'quest_completed':
            if objective['target'] == 'any' or data.get('quest_category') == objective['target']:
                objective['current'] += 1
                updated = True

        elif t == 'reputation' and event_type == 'reputation_changed':
            if data.get('faction') == objective['target']:
                objective['current'] = data.get('new_reputation', 0)
                updated = True

        elif t == 'explore_locations' and event_type == 'location_discovered':
            objective['current'] += 1
            updated = True

        elif t == 'read_document' and event_type == 'document_read':
            if data.get('item_id') == objective['target']:
                objective['current'] += 1
                updated = True

        elif t == 'talk_npc' and event_type == 'npc_talked':
            if data.get('npc_id') == objective['target']:
                objective['current'] += 1
                updated = True

        elif t == 'special_action' and event_type == 'special_action_done':
            if data.get('action') == objective['target']:
                objective['current'] += 1
                updated = True

        elif t == 'repair_item' and event_type == 'item_repaired':
            if data.get('item_id') == objective['target']:
                objective['current'] += 1
                updated = True

        elif t == 'build_structure' and event_type == 'structure_built':
            if data.get('structure') == objective['target']:
                objective['current'] += 1
                updated = True

        if objective['current'] > objective['required']:
            objective['current'] = objective['required']

        return updated

    def complete_quest(self, quest_id):
        if quest_id not in self.active_quests:
            return
        quest = self.quests[quest_id]
        self.active_quests.remove(quest_id)

        if quest_id not in self.completed_quests or quest['repeatable']:
            if quest_id not in self.completed_quests:
                self.completed_quests.append(quest_id)

            self._give_rewards(quest)
            self._unlock_new_quests(quest)

            self.game.player.stats['quests_completed'] += 1
            self.game.add_game_log(f"🎉 完成任务: {quest['name']}！")
            self.game.quests.update_quest_progress('quest_completed', quest_category=quest['category'])

    def _give_rewards(self, quest):
        rewards = quest['rewards']
        if 'exp' in rewards:
            exp = rewards['exp']
            self.game.player.gain_skill_exp('survival', exp // 3)
            self.game.player.gain_skill_exp('combat', exp // 3)
            self.game.player.gain_skill_exp('crafting', exp // 3)
        if 'items' in rewards:
            for item_id, quantity in rewards['items'].items():
                self.game.player.add_item(item_id, quantity)
                self.game.add_game_log(f"获得: {self.game.items.get_item_name(item_id)} x{quantity}")
        if 'money' in rewards:
            pass  # 金钱系统预留
        if 'reputation' in rewards:
            for faction, amount in rewards['reputation'].items():
                self.game.npcs.change_relationship(faction, amount)

    def _unlock_new_quests(self, quest):
        unlocks = quest['rewards'].get('unlocks', [])
        for new_qid in unlocks:
            if new_qid in self.quests:
                self.game.add_game_log(f"新任务已解锁: {self.quests[new_qid]['name']}")

    def fail_quest(self, quest_id):
        if quest_id not in self.active_quests:
            return
        quest = self.quests[quest_id]
        self.active_quests.remove(quest_id)
        self.failed_quests.append(quest_id)
        self.game.add_game_log(f"❌ 任务失败: {quest['name']}")

    def abandon_quest(self, quest_id):
        if quest_id not in self.active_quests:
            return {'success': False, 'message': '任务未在进行中'}
        quest = self.quests[quest_id]
        self.active_quests.remove(quest_id)
        for obj in quest['objectives']:
            obj['current'] = 0
        if 'start_time' in quest:
            del quest['start_time']
        self.game.add_game_log(f"你放弃了任务: {quest['name']}")
        return {'success': True, 'message': f"已放弃任务: {quest['name']}"}

    def get_available_quests(self):
        available = []
        for qid, quest in self.quests.items():
            if qid in self.completed_quests and not quest['repeatable']:
                continue
            if qid in self.active_quests or qid in self.failed_quests:
                continue
            prereq_ok = all(p in self.completed_quests for p in quest['prerequisites'])
            if prereq_ok:
                available.append(quest)
        return available

    def get_quest_progress(self, quest_id):
        if quest_id not in self.quests:
            return None
        quest = self.quests[quest_id]
        return {
            'quest': quest,
            'objectives': [
                {
                    'description': obj['description'],
                    'current': obj['current'],
                    'required': obj['required'],
                    'completed': obj['current'] >= obj['required']
                } for obj in quest['objectives']
            ],
            'completed': quest_id in self.completed_quests,
            'failed': quest_id in self.failed_quests,
            'active': quest_id in self.active_quests
        }

    def check_daily_quests(self):
        for qid, quest in list(self.quests.items()):
            if quest['category'] == 'daily':
                if qid in self.active_quests:
                    self.fail_quest(qid)
                elif qid in self.completed_quests:
                    self.completed_quests.remove(qid)
                for obj in quest['objectives']:
                    obj['current'] = 0
                self.start_quest(qid)

    def check_timed_quests(self):
        for qid in list(self.active_quests):
            quest = self.quests[qid]
            if quest.get('time_limit') and 'start_time' in quest:
                time_passed = (self.game.game_time - quest['start_time']).days
                if time_passed >= quest['time_limit']:
                    self.fail_quest(qid)

    def get_quest_giver_name(self, giver_id):
        names = {
            'system': '系统',
            'old_farmer': '老农民张大爷',
            'doctor_li': '李医生',
            'security_chief': '王队长',
            'cartographer': '地图绘制师',
            'master_crafter': '工匠大师'
        }
        return names.get(giver_id, giver_id)