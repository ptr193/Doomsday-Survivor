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
        quests_data = self.game.mod_manager.get_data('quests', None) or {}
        if quests_data:
            self.quests = {}
            for qid, quest in quests_data.items():
                q = dict(quest)
                q['id'] = q.get('id', qid)
                q['objectives'] = [dict(obj) for obj in q.get('objectives', [])]
                for obj in q['objectives']:
                    obj['current'] = obj.get('current', 0)
                q['prerequisites'] = list(q.get('prerequisites', []))
                q['repeatable'] = bool(q.get('repeatable', False))
                self.quests[qid] = q
            logging.info(f"从JSON加载了{len(self.quests)}个任务")
            return
        self.quests['main_01'] = {'id': 'main_01', 'name': '初来乍到', 'category': 'main', 'difficulty': 1, 'description': '在这个陌生的世界中生存下来，学习基本的生存技能。', 'objectives': [{'id': 'explore_start', 'description': '探索起始区域', 'type': 'explore_location', 'target': 'starting_area', 'required': 1, 'current': 0}, {'id': 'collect', 'description': '收集5个基础物资', 'type': 'collect_items', 'target': 'materials', 'required': 5, 'current': 0}, {'id': 'craft', 'description': '制作第一个物品', 'type': 'craft_item', 'target': 'any', 'required': 1, 'current': 0}], 'prerequisites': [], 'rewards': {'exp': 100, 'items': {'food': 5, 'water': 5, 'materials': 10}, 'money': 50, 'unlocks': ['main_02']}, 'time_limit': None, 'repeatable': False, 'giver_npc': 'system', 'story_text': '在这个破碎的世界中，每一个幸存者都要从零开始。'}
        self.quests['side_01'] = {'id': 'side_01', 'name': '老农的请求', 'category': 'side', 'difficulty': 2, 'description': '帮助老农民恢复他的农田。', 'objectives': [{'id': 'clear_weeds', 'description': '清除农田里的杂草', 'type': 'farm_action', 'target': 'remove_weeds', 'required': 3, 'current': 0}, {'id': 'plant_crops', 'description': '种植2种不同的作物', 'type': 'plant_crops', 'target': 'any', 'required': 2, 'current': 0}, {'id': 'harvest_crops', 'description': '收获5个农作物', 'type': 'harvest_crops', 'target': 'any', 'required': 5, 'current': 0}], 'prerequisites': [], 'rewards': {'exp': 150, 'items': {'vegetable_seeds': 5, 'fresh_food': 3}, 'money': 80, 'reputation': {'survivors': 10}}, 'time_limit': 7, 'repeatable': False, 'giver_npc': 'old_farmer'}
        self.quests['daily_01'] = {'id': 'daily_01', 'name': '日常收集', 'category': 'daily', 'difficulty': 1, 'description': '收集一些基础生存物资。', 'objectives': [{'id': 'collect', 'description': '收集10个材料', 'type': 'collect_items', 'target': 'materials', 'required': 10, 'current': 0}], 'prerequisites': [], 'rewards': {'exp': 50, 'items': {'food': 2, 'water': 2}, 'money': 30}, 'time_limit': 1, 'repeatable': True, 'giver_npc': 'system'}
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
                    if qdata.get('start_time'):
                        self.quests[qid]['start_time'] = qdata['start_time']
            self.initialized = True
            logging.info("任务系统数据加载完成")
        except Exception as e:
            logging.error(f"加载任务系统数据失败: {e}")
            raise

    def get_save_data(self):
        progress = {}
        for qid, quest in self.quests.items():
            start_time = quest.get('start_time')
            if hasattr(start_time, 'isoformat'):
                start_time = start_time.isoformat()
            progress[qid] = {
                'objectives': [{'current': obj['current']} for obj in quest['objectives']],
                'start_time': start_time
            }
        return {'active_quests': self.active_quests, 'completed_quests': self.completed_quests, 'failed_quests': self.failed_quests, 'quests_progress': progress}

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
        quest['start_time'] = self.game.game_time.isoformat() if self.game.game_time else None
        logging.info(f"开始任务: {quest['name']}")
        self.game.add_game_log(f"新任务: {quest['name']}")
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
            loc_id = data.get('location_id')
            if loc_id is None and loc is not None:
                loc_id = loc if isinstance(loc, str) else getattr(loc, 'id', None)
            if target == 'any' or loc_id == target or loc == target or (target == 'dangerous' and loc and getattr(loc, 'safety_level', 99) <= 3):
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
        if 'reputation' in rewards:
            for faction, amount in rewards['reputation'].items():
                self.game.npcs.change_relationship(faction, amount)
        if 'money' in rewards:
            self.game.player.add_money(rewards['money'])
            self.game.add_game_log(f"获得金钱: {rewards['money']}")

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
        return {'quest': quest, 'objectives': [{'description': obj['description'], 'current': obj['current'], 'required': obj['required'], 'completed': obj['current'] >= obj['required']} for obj in quest['objectives']], 'completed': quest_id in self.completed_quests, 'failed': quest_id in self.failed_quests, 'active': quest_id in self.active_quests}

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
            if quest.get('time_limit') and quest.get('start_time'):
                start_time = quest['start_time']
                if isinstance(start_time, str):
                    try:
                        start_time = datetime.fromisoformat(start_time)
                    except ValueError:
                        continue
                time_passed = (self.game.game_time - start_time).days
                if time_passed >= quest['time_limit']:
                    self.fail_quest(qid)

    def get_quest_giver_name(self, giver_id):
        names = {'system': '系统', 'old_farmer': '老农民张大爷', 'doctor_li': '李医生', 'security_chief': '王队长', 'cartographer': '地图绘制师', 'master_crafter': '工匠大师'}
        return names.get(giver_id, giver_id)