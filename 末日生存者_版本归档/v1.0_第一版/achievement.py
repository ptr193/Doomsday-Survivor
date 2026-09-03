# -*- coding: utf-8 -*-

import logging
from typing import Dict, List, Optional

class AchievementSystem:
    def __init__(self, game):
        self.game = game
        self.achievements = {}
        self.unlocked_achievements = set()
        self.achievement_points = 0
        self.initialized = False
        
    def initialize(self):
        """初始化成就系统"""
        try:
            self.create_achievements()
            self.initialized = True
            logging.info("成就系统初始化完成")
        except Exception as e:
            logging.error(f"成就系统初始化失败: {e}")
            raise
    
    def create_achievements(self):
        """创建所有成就"""
        # === 生存大师成就 ===
        self.achievements['first_step'] = {
            'id': 'first_step',
            'name': '初来乍到',
            'category': 'survival',
            'description': '开始你的生存之旅',
            'points': 10,
            'hidden': False,
            'condition': {'type': 'start_game'},
            'icon': '🎯'
        }
        
        self.achievements['survival_week'] = {
            'id': 'survival_week',
            'name': '生存专家',
            'category': 'survival',
            'description': '生存超过7天',
            'points': 25,
            'hidden': False,
            'condition': {'type': 'survive_days', 'days': 7},
            'icon': '🏆'
        }
        
        self.achievements['survival_month'] = {
            'id': 'survival_month',
            'name': '月度幸存者',
            'category': 'survival',
            'description': '生存30天',
            'points': 50,
            'hidden': False,
            'condition': {'type': 'survive_days', 'days': 30},
            'icon': '⭐'
        }
        
        self.achievements['survival_year'] = {
            'id': 'survival_year',
            'name': '年度英雄',
            'category': 'survival',
            'description': '生存365天',
            'points': 100,
            'hidden': False,
            'condition': {'type': 'survive_days', 'days': 365},
            'icon': '👑'
        }
        
        self.achievements['never_give_up'] = {
            'id': 'never_give_up',
            'name': '永不言弃',
            'category': 'survival',
            'description': '从濒死状态恢复10次',
            'points': 30,
            'hidden': False,
            'condition': {'type': 'recover_from_near_death', 'count': 10},
            'icon': '💪'
        }
        
        self.achievements['resource_tycoon'] = {
            'id': 'resource_tycoon',
            'name': '资源大亨',
            'category': 'survival',
            'description': '同时拥有1000个各类资源',
            'points': 40,
            'hidden': False,
            'condition': {'type': 'total_resources', 'amount': 1000},
            'icon': '💰'
        }
        
        self.achievements['master_builder'] = {
            'id': 'master_builder',
            'name': '建筑大师',
            'category': 'survival',
            'description': '将基地升级到最高级',
            'points': 35,
            'hidden': False,
            'condition': {'type': 'max_base_level'},
            'icon': '🏠'
        }
        
        self.achievements['weather_master'] = {
            'id': 'weather_master',
            'name': '天气适应者',
            'category': 'survival',
            'description': '在所有天气类型中生存过',
            'points': 20,
            'hidden': False,
            'condition': {'type': 'experience_all_weather'},
            'icon': '🌤️'
        }
        
        self.achievements['season_traveler'] = {
            'id': 'season_traveler',
            'name': '季节轮回',
            'category': 'survival',
            'description': '经历完整的四季变化',
            'points': 25,
            'hidden': False,
            'condition': {'type': 'experience_all_seasons'},
            'icon': '🍂'
        }
        
        self.achievements['mental_giant'] = {
            'id': 'mental_giant',
            'name': '精神支柱',
            'category': 'survival',
            'description': '保持精神饱满状态连续10天',
            'points': 30,
            'hidden': False,
            'condition': {'type': 'maintain_high_mental', 'days': 10},
            'icon': '🧠'
        }
        
        # === 战斗专家成就 ===
        self.achievements['first_blood'] = {
            'id': 'first_blood',
            'name': '第一滴血',
            'category': 'combat',
            'description': '击败第一个敌人',
            'points': 15,
            'hidden': False,
            'condition': {'type': 'defeat_enemies', 'count': 1},
            'icon': '⚔️'
        }
        
        self.achievements['monster_hunter'] = {
            'id': 'monster_hunter',
            'name': '怪物猎人',
            'category': 'combat',
            'description': '击败100个敌人',
            'points': 35,
            'hidden': False,
            'condition': {'type': 'defeat_enemies', 'count': 100},
            'icon': '🎯'
        }
        
        self.achievements['elite_slayer'] = {
            'id': 'elite_slayer',
            'name': '精英杀手',
            'category': 'combat',
            'description': '击败所有精英怪物',
            'points': 50,
            'hidden': False,
            'condition': {'type': 'defeat_all_elites'},
            'icon': '💀'
        }
        
        self.achievements['boss_conqueror'] = {
            'id': 'boss_conqueror',
            'name': 'BOSS征服者',
            'category': 'combat',
            'description': '击败所有BOSS',
            'points': 75,
            'hidden': False,
            'condition': {'type': 'defeat_all_bosses'},
            'icon': '👹'
        }
        
        self.achievements['flawless_victory'] = {
            'id': 'flawless_victory',
            'name': '无伤大师',
            'category': 'combat',
            'description': '无伤击败一个BOSS',
            'points': 60,
            'hidden': False,
            'condition': {'type': 'defeat_boss_no_damage'},
            'icon': '🛡️'
        }
        
        self.achievements['weapon_master'] = {
            'id': 'weapon_master',
            'name': '武器专家',
            'category': 'combat',
            'description': '使用所有类型的武器击败敌人',
            'points': 40,
            'hidden': False,
            'condition': {'type': 'use_all_weapon_types'},
            'icon': '🔫'
        }
        
        self.achievements['armor_collector'] = {
            'id': 'armor_collector',
            'name': '防具收藏家',
            'category': 'combat',
            'description': '收集全套传奇防具',
            'points': 55,
            'hidden': False,
            'condition': {'type': 'collect_legendary_armor'},
            'icon': '🛡️'
        }
        
        self.achievements['combo_master'] = {
            'id': 'combo_master',
            'name': '连击高手',
            'category': 'combat',
            'description': '连续战斗获胜10次',
            'points': 30,
            'hidden': False,
            'condition': {'type': 'win_streak', 'count': 10},
            'icon': '🔥'
        }
        
        self.achievements['stealth_master'] = {
            'id': 'stealth_master',
            'name': '潜行大师',
            'category': 'combat',
            'description': '不触发战斗通过危险区域',
            'points': 35,
            'hidden': False,
            'condition': {'type': 'stealth_through_danger_zone'},
            'icon': '👻'
        }
        
        # === 探索发现成就 ===
        self.achievements['adventure_beginner'] = {
            'id': 'adventure_beginner',
            'name': '冒险启程',
            'category': 'exploration',
            'description': '发现第一个隐藏地点',
            'points': 15,
            'hidden': False,
            'condition': {'type': 'discover_location'},
            'icon': '🗺️'
        }
        
        self.achievements['map_pioneer'] = {
            'id': 'map_pioneer',
            'name': '地图开拓者',
            'category': 'exploration',
            'description': '探索所有区域',
            'points': 45,
            'hidden': False,
            'condition': {'type': 'discover_all_locations'},
            'icon': '🌍'
        }
        
        self.achievements['archaeologist'] = {
            'id': 'archaeologist',
            'name': '考古学家',
            'category': 'exploration',
            'description': '收集所有历史文档',
            'points': 40,
            'hidden': False,
            'condition': {'type': 'collect_all_documents'},
            'icon': '📜'
        }
        
        self.achievements['secret_revealer'] = {
            'id': 'secret_revealer',
            'name': '秘密揭露者',
            'category': 'exploration',
            'description': '完成所有隐藏任务',
            'points': 50,
            'hidden': False,
            'condition': {'type': 'complete_all_secret_quests'},
            'icon': '🔍'
        }
        
        self.achievements['dungeon_conqueror'] = {
            'id': 'dungeon_conqueror',
            'name': '地牢征服者',
            'category': 'exploration',
            'description': '清理所有废弃设施',
            'points': 35,
            'hidden': False,
            'condition': {'type': 'clear_all_dungeons'},
            'icon': '🏰'
        }
        
        self.achievements['sky_watcher'] = {
            'id': 'sky_watcher',
            'name': '高空观察者',
            'category': 'exploration',
            'description': '登上所有观察塔',
            'points': 25,
            'hidden': False,
            'condition': {'type': 'climb_all_towers'},
            'icon': '🗼'
        }
        
        self.achievements['deep_diver'] = {
            'id': 'deep_diver',
            'name': '水下探险',
            'category': 'exploration',
            'description': '探索辐射湖底',
            'points': 30,
            'hidden': False,
            'condition': {'type': 'explore_lake_bottom'},
            'icon': '🌊'
        }
        
        self.achievements['cave_expert'] = {
            'id': 'cave_expert',
            'name': '洞穴专家',
            'category': 'exploration',
            'description': '探索所有洞穴系统',
            'points': 35,
            'hidden': False,
            'condition': {'type': 'explore_all_caves'},
            'icon': '🕳️'
        }
        
        self.achievements['urban_cleaner'] = {
            'id': 'urban_cleaner',
            'name': '城市清理者',
            'category': 'exploration',
            'description': '清理所有城市区域',
            'points': 40,
            'hidden': False,
            'condition': {'type': 'clear_all_urban_areas'},
            'icon': '🏙️'
        }
        
        # === 制作创造成就 ===
        self.achievements['handyman'] = {
            'id': 'handyman',
            'name': '手工达人',
            'category': 'crafting',
            'description': '制作第一个物品',
            'points': 15,
            'hidden': False,
            'condition': {'type': 'craft_item'},
            'icon': '🔨'
        }
        
        self.achievements['master_crafter'] = {
            'id': 'master_crafter',
            'name': '工匠大师',
            'category': 'crafting',
            'description': '制作100个物品',
            'points': 35,
            'hidden': False,
            'condition': {'type': 'craft_items', 'count': 100},
            'icon': '⚒️'
        }
        
        self.achievements['tech_pioneer'] = {
            'id': 'tech_pioneer',
            'name': '科技先驱',
            'category': 'crafting',
            'description': '研发所有科技',
            'points': 50,
            'hidden': False,
            'condition': {'type': 'research_all_tech'},
            'icon': '🔬'
        }
        
        self.achievements['modification_expert'] = {
            'id': 'modification_expert',
            'name': '改装专家',
            'category': 'crafting',
            'description': '为武器添加所有配件',
            'points': 40,
            'hidden': False,
            'condition': {'type': 'modify_all_weapons'},
            'icon': '🔧'
        }
        
        self.achievements['enchantment_master'] = {
            'id': 'enchantment_master',
            'name': '附魔大师',
            'category': 'crafting',
            'description': '为装备添加特殊效果',
            'points': 45,
            'hidden': False,
            'condition': {'type': 'enchant_equipment'},
            'icon': '✨'
        }
        
        self.achievements['synthesis_genius'] = {
            'id': 'synthesis_genius',
            'name': '合成天才',
            'category': 'crafting',
            'description': '发现所有合成配方',
            'points': 55,
            'hidden': False,
            'condition': {'type': 'discover_all_recipes'},
            'icon': '🧪'
        }
        
        self.achievements['legendary_artisan'] = {
            'id': 'legendary_artisan',
            'name': '传奇工匠',
            'category': 'crafting',
            'description': '制作全套传奇装备',
            'points': 60,
            'hidden': False,
            'condition': {'type': 'craft_legendary_set'},
            'icon': '👑'
        }
        
        # === 社交关系成就 ===
        self.achievements['first_meeting'] = {
            'id': 'first_meeting',
            'name': '初次见面',
            'category': 'social',
            'description': '遇到第一个NPC',
            'points': 10,
            'hidden': False,
            'condition': {'type': 'meet_npc'},
            'icon': '👋'
        }
        
        self.achievements['friendship_forever'] = {
            'id': 'friendship_forever',
            'name': '友谊万岁',
            'category': 'social',
            'description': '与一个阵营达到最高声望',
            'points': 35,
            'hidden': False,
            'condition': {'type': 'max_faction_reputation'},
            'icon': '🤝'
        }
        
        self.achievements['merchant_partner'] = {
            'id': 'merchant_partner',
            'name': '商人伙伴',
            'category': 'social',
            'description': '完成所有商人任务',
            'points': 30,
            'hidden': False,
            'condition': {'type': 'complete_merchant_quests'},
            'icon': '💼'
        }
        
        self.achievements['medical_savior'] = {
            'id': 'medical_savior',
            'name': '医疗援助',
            'category': 'social',
            'description': '治愈10个受伤的NPC',
            'points': 25,
            'hidden': False,
            'condition': {'type': 'heal_npcs', 'count': 10},
            'icon': '🏥'
        }
        
        self.achievements['team_leader'] = {
            'id': 'team_leader',
            'name': '团队领袖',
            'category': 'social',
            'description': '招募10个居民到基地',
            'points': 40,
            'hidden': False,
            'condition': {'type': 'recruit_residents', 'count': 10},
            'icon': '👥'
        }
        
        self.achievements['peace_maker'] = {
            'id': 'peace_maker',
            'name': '和平使者',
            'category': 'social',
            'description': '调解两个阵营的冲突',
            'points': 45,
            'hidden': False,
            'condition': {'type': 'mediate_conflict'},
            'icon': '🕊️'
        }
        
        # === 特殊挑战成就 ===
        self.achievements['speed_survivor'] = {
            'id': 'speed_survivor',
            'name': '速度生存',
            'category': 'challenge',
            'description': '在50天内完成主线',
            'points': 65,
            'hidden': True,
            'condition': {'type': 'complete_main_quest_quick', 'days': 50},
            'icon': '⚡'
        }
        
        self.achievements['minimalist'] = {
            'id': 'minimalist',
            'name': '极简主义',
            'category': 'challenge',
            'description': '只用基础装备生存30天',
            'points': 55,
            'hidden': True,
            'condition': {'type': 'survive_with_basic_gear', 'days': 30},
            'icon': '🎒'
        }
        
        self.achievements['vegetarian'] = {
            'id': 'vegetarian',
            'name': '素食者',
            'category': 'challenge',
            'description': '只吃植物类食物生存20天',
            'points': 40,
            'hidden': True,
            'condition': {'type': 'vegetarian_survival', 'days': 20},
            'icon': '🥦'
        }
        
        self.achievements['night_walker'] = {
            'id': 'night_walker',
            'name': '夜行者',
            'category': 'challenge',
            'description': '只在夜晚活动生存15天',
            'points': 50,
            'hidden': True,
            'condition': {'type': 'nocturnal_survival', 'days': 15},
            'icon': '🌙'
        }
        
        self.achievements['perfectionist'] = {
            'id': 'perfectionist',
            'name': '完美主义者',
            'category': 'challenge',
            'description': '达成所有成就',
            'points': 100,
            'hidden': True,
            'condition': {'type': 'complete_all_achievements'},
            'icon': '🏅'
        }
        
        logging.info(f"创建了{len(self.achievements)}个成就")
    
    def unlock(self, achievement_id, progress_data=None):
        """解锁成就"""
        if achievement_id not in self.achievements:
            logging.error(f"未知成就: {achievement_id}")
            return False
        
        if achievement_id in self.unlocked_achievements:
            return False  # 已经解锁
        
        achievement = self.achievements[achievement_id]
        
        # 检查成就条件
        if not self.check_condition(achievement['condition'], progress_data):
            return False
        
        # 解锁成就
        self.unlocked_achievements.add(achievement_id)
        self.achievement_points += achievement['points']
        
        # 通知玩家
        self.game.add_game_log(f"🎉 成就解锁: {achievement['icon']} {achievement['name']} - {achievement['description']} (+{achievement['points']}点)")
        
        logging.info(f"成就解锁: {achievement['name']}")
        return True
    
    def check_condition(self, condition, progress_data):
        """检查成就条件"""
        condition_type = condition['type']
        
        if condition_type == 'start_game':
            return True
            
        elif condition_type == 'survive_days':
            required_days = condition['days']
            return self.game.day_count >= required_days
            
        elif condition_type == 'defeat_enemies':
            required_count = condition['count']
            return self.game.player.stats.get('enemies_defeated', 0) >= required_count
            
        elif condition_type == 'discover_location':
            return self.game.player.stats.get('locations_discovered', 0) >= 1
            
        elif condition_type == 'craft_item':
            return self.game.player.stats.get('items_crafted', 0) >= 1
            
        elif condition_type == 'meet_npc':
            return self.game.player.stats.get('npcs_met', 0) >= 1
            
        elif condition_type == 'harvest_crop':
            return self.game.player.stats.get('crops_harvested', 0) >= 1
            
        elif condition_type == 'complete_quest':
            return self.game.player.stats.get('quests_completed', 0) >= 1
            
        # 这里可以添加更多条件检查...
        
        return False
    
    def check_daily_achievements(self):
        """检查每日成就"""
        # 生存天数相关成就
        self.unlock('survival_week')
        self.unlock('survival_month')
        self.unlock('survival_year')
        
        # 精神状态成就
        if self.game.player.mental >= 80:
            # 这里需要跟踪连续天数
            pass
    
    def check_exploration_achievements(self):
        """检查探索成就"""
        locations_discovered = self.game.player.stats.get('locations_discovered', 0)
        
        if locations_discovered >= 1:
            self.unlock('adventure_beginner')
        
        # 更多探索成就检查...
    
    def check_combat_achievements(self, enemy_name):
        """检查战斗成就"""
        enemies_defeated = self.game.player.stats.get('enemies_defeated', 0)
        
        if enemies_defeated >= 1:
            self.unlock('first_blood')
        
        if enemies_defeated >= 100:
            self.unlock('monster_hunter')
        
        # 检查精英和BOSS击败
        if '精英' in enemy_name or 'BOSS' in enemy_name:
            # 这里需要跟踪具体击败的敌人类型
            pass
    
    def check_crafting_achievements(self):
        """检查制作成就"""
        items_crafted = self.game.player.stats.get('items_crafted', 0)
        
        if items_crafted >= 1:
            self.unlock('handyman')
        
        if items_crafted >= 100:
            self.unlock('master_crafter')
    
    def check_farming_achievements(self):
        """检查农业成就"""
        crops_harvested = self.game.player.stats.get('crops_harvested', 0)
        
        if crops_harvested >= 1:
            self.unlock('harvest_first_crop')
    
    def check_npc_achievements(self):
        """检查NPC相关成就"""
        npcs_met = self.game.player.stats.get('npcs_met', 0)
        
        if npcs_met >= 1:
            self.unlock('first_meeting')
    
    def get_achievement(self, achievement_id):
        """获取成就信息"""
        return self.achievements.get(achievement_id)
    
    def get_unlocked_achievements(self):
        """获取已解锁的成就"""
        unlocked = []
        for achievement_id in self.unlocked_achievements:
            if achievement_id in self.achievements:
                unlocked.append(self.achievements[achievement_id])
        return unlocked
    
    def get_locked_achievements(self):
        """获取未解锁的成就"""
        locked = []
        for achievement_id, achievement in self.achievements.items():
            if achievement_id not in self.unlocked_achievements and not achievement['hidden']:
                locked.append(achievement)
        return locked
    
    def get_achievements_by_category(self, category):
        """按分类获取成就"""
        achievements = []
        for achievement in self.achievements.values():
            if achievement['category'] == category:
                achievements.append(achievement)
        return achievements
    
    def get_all_categories(self):
        """获取所有分类"""
        categories = set()
        for achievement in self.achievements.values():
            categories.add(achievement['category'])
        return sorted(list(categories))
    
    def get_total_points(self):
        """获取总成就点数"""
        return self.achievement_points
    
    def get_completion_percentage(self):
        """获取完成百分比"""
        total = len(self.achievements)
        unlocked = len(self.unlocked_achievements)
        return (unlocked / total) * 100 if total > 0 else 0
    
    def load_data(self, save_data):
        """加载成就系统数据"""
        try:
            self.unlocked_achievements = set(save_data.get('unlocked_achievements', []))
            self.achievement_points = save_data.get('achievement_points', 0)
            self.initialized = True
            logging.info("成就系统数据加载完成")
        except Exception as e:
            logging.error(f"加载成就系统数据失败: {e}")
            raise
    
    def get_save_data(self):
        """获取保存数据"""
        return {
            'unlocked_achievements': list(self.unlocked_achievements),
            'achievement_points': self.achievement_points
        }
