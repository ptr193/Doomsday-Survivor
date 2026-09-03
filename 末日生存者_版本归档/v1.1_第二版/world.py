# -*- coding: utf-8 -*-

import random
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Location:
    """地点数据类"""
    id: str
    name: str
    description: str
    terrain: str
    safety_level: int  # 1-10, 1最危险，10最安全
    resources: Dict[str, int]
    connected_locations: List[str]
    special_events: List[str]
    discovered: bool = False
    explored: bool = False

class GameWorld:
    def __init__(self, game):
        self.game = game
        self.locations = {}
        self.current_location_id = "starting_area"
        self.initialized = False
        
    def initialize(self):
        """初始化游戏世界"""
        try:
            self.create_locations()
            self.current_location_id = "starting_area"
            self.initialized = True
            logging.info("游戏世界初始化完成")
        except Exception as e:
            logging.error(f"世界初始化失败: {e}")
            raise
    
    def create_locations(self):
        """创建所有地点"""
        # 起始区域
        self.locations["starting_area"] = Location(
            id="starting_area",
            name="起始营地",
            description="一个相对安全的废弃营地，这里有基本的生存设施。",
            terrain="平原",
            safety_level=7,
            resources={"food": 3, "water": 3, "materials": 5},
            connected_locations=["north_forest", "east_river", "south_plains"],
            special_events=["safe_rest", "basic_supplies"],
            discovered=True,
            explored=True
        )
        
        # 北部森林
        self.locations["north_forest"] = Location(
            id="north_forest",
            name="北部森林",
            description="茂密的森林，资源丰富但隐藏着危险。",
            terrain="森林",
            safety_level=4,
            resources={"food": 5, "water": 2, "wood": 8, "medicine": 2},
            connected_locations=["starting_area", "deep_forest", "mountain_foot"],
            special_events=["animal_encounter", "herb_discovery", "hidden_cache"]
        )
        
        # 东部河流
        self.locations["east_river"] = Location(
            id="east_river",
            name="东部河流",
            description="一条清澈的河流，是重要的水源地。",
            terrain="河流",
            safety_level=6,
            resources={"water": 8, "food": 2, "materials": 3},
            connected_locations=["starting_area", "river_source", "fishing_spot"],
            special_events=["fishing", "water_source", "river_treasure"]
        )
        
        # 南部平原
        self.locations["south_plains"] = Location(
            id="south_plains",
            name="南部平原",
            description="开阔的平原，视野良好但缺乏遮蔽。",
            terrain="平原",
            safety_level=5,
            resources={"food": 4, "water": 3, "materials": 4},
            connected_locations=["starting_area", "abandoned_farm", "old_road"],
            special_events=["weather_exposure", "plains_hunting", "traveler_meet"]
        )
        
        # 深林区
        self.locations["deep_forest"] = Location(
            id="deep_forest",
            name="深林区",
            description="森林深处，光线昏暗，充满未知危险。",
            terrain="森林",
            safety_level=2,
            resources={"wood": 10, "medicine": 4, "rare_herbs": 2},
            connected_locations=["north_forest", "ancient_ruins"],
            special_events=["predator_attack", "ancient_discovery", "mysterious_sounds"]
        )
        
        # 山脚
        self.locations["mountain_foot"] = Location(
            id="mountain_foot",
            name="山脚",
            description="雄伟山脉的起点，地势开始升高。",
            terrain="山地",
            safety_level=5,
            resources={"stone": 6, "materials": 4, "water": 2},
            connected_locations=["north_forest", "mountain_path"],
            special_events=["rockfall", "mineral_find", "mountain_view"]
        )
        
        # 河流源头
        self.locations["river_source"] = Location(
            id="river_source",
            name="河流源头",
            description="河流的发源地，水质纯净。",
            terrain="山地",
            safety_level=7,
            resources={"water": 10, "rare_minerals": 3},
            connected_locations=["east_river", "mountain_path"],
            special_events=["pure_water", "source_discovery", "mysterious_cave"]
        )
        
        # 钓鱼点
        self.locations["fishing_spot"] = Location(
            id="fishing_spot",
            name="钓鱼点",
            description="理想的钓鱼位置，水流平缓。",
            terrain="河流",
            safety_level=6,
            resources={"food": 6, "water": 5},
            connected_locations=["east_river"],
            special_events=["big_catch", "fisherman_ghost", "underwater_treasure"]
        )
        
        # 废弃农场
        self.locations["abandoned_farm"] = Location(
            id="abandoned_farm",
            name="废弃农场",
            description="被遗弃的农场，可能还留有一些物资。",
            terrain="农田",
            safety_level=4,
            resources={"food": 8, "materials": 6, "seeds": 4},
            connected_locations=["south_plains", "farmhouse"],
            special_events=["farm_tools", "hidden_cellar", "scarecrow_secret"]
        )
        
        # 老路
        self.locations["old_road"] = Location(
            id="old_road",
            name="老路",
            description="破旧的公路，连接着各个幸存者据点。",
            terrain="道路",
            safety_level=5,
            resources={"materials": 3, "electronic": 2},
            connected_locations=["south_plains", "trading_post"],
            special_events=["traveler_encounter", "roadside_find", "car_wreck"]
        )
        
        # 古代遗迹
        self.locations["ancient_ruins"] = Location(
            id="ancient_ruins",
            name="古代遗迹",
            description="神秘的古代建筑遗迹，隐藏着古老的秘密。",
            terrain="遗迹",
            safety_level=3,
            resources={"ancient_artifacts": 5, "stone": 4},
            connected_locations=["deep_forest"],
            special_events=["artifact_discovery", "ancient_trap", "historical_insight"]
        )
        
        # 山路
        self.locations["mountain_path"] = Location(
            id="mountain_path",
            name="山路",
            description="陡峭的山路，通向更高的地方。",
            terrain="山地",
            safety_level=4,
            resources={"stone": 5, "rare_herbs": 3},
            connected_locations=["mountain_foot", "river_source", "mountain_peak"],
            special_events=["climbing_challenge", "avalanche_risk", "mountain_goat"]
        )
        
        # 农舍
        self.locations["farmhouse"] = Location(
            id="farmhouse",
            name="农舍",
            description="破旧的农舍，可能还保留着一些生活用品。",
            terrain="建筑",
            safety_level=6,
            resources={"food": 4, "materials": 8, "cloth": 5},
            connected_locations=["abandoned_farm"],
            special_events=["shelter_find", "old_diary", "hidden_stash"]
        )
        
        # 贸易站
        self.locations["trading_post"] = Location(
            id="trading_post",
            name="贸易站",
            description="幸存者建立的交易场所，可以交换物资。",
            terrain="建筑",
            safety_level=8,
            resources={"various": 10},  # 特殊资源，表示可以交易
            connected_locations=["old_road", "survivor_camp"],
            special_events=["trade_opportunity", "information_exchange", "quest_offer"]
        )
        
        # 幸存者营地
        self.locations["survivor_camp"] = Location(
            id="survivor_camp",
            name="幸存者营地",
            description="其他幸存者建立的营地，相对安全。",
            terrain="营地",
            safety_level=9,
            resources={"food": 3, "water": 4, "medicine": 3},
            connected_locations=["trading_post"],
            special_events=["ally_meeting", "camp_services", "group_quest"]
        )
        
        # 山顶
        self.locations["mountain_peak"] = Location(
            id="mountain_peak",
            name="山顶",
            description="山脉的最高点，可以俯瞰整个区域。",
            terrain="山地",
            safety_level=6,
            resources={"rare_minerals": 5, "strategic_view": 1},
            connected_locations=["mountain_path"],
            special_events=["view_discovery", "weather_observation", "signal_boost"]
        )
        
        logging.info(f"创建了{len(self.locations)}个地点")
    
    def load_data(self, save_data):
        """加载世界数据"""
        try:
            self.current_location_id = save_data.get('current_location_id', 'starting_area')
            
            # 重建地点数据
            locations_data = save_data.get('locations', {})
            for loc_id, loc_data in locations_data.items():
                if loc_id in self.locations:
                    self.locations[loc_id].discovered = loc_data.get('discovered', False)
                    self.locations[loc_id].explored = loc_data.get('explored', False)
            
            self.initialized = True
            logging.info("世界数据加载完成")
            
        except Exception as e:
            logging.error(f"加载世界数据失败: {e}")
            raise
    
    def get_save_data(self):
        """获取保存数据"""
        locations_data = {}
        for loc_id, location in self.locations.items():
            locations_data[loc_id] = {
                'discovered': location.discovered,
                'explored': location.explored
            }
        
        return {
            'current_location_id': self.current_location_id,
            'locations': locations_data
        }
    
    def get_current_location(self):
        """获取当前位置"""
        return self.locations.get(self.current_location_id)
    
    def get_connected_locations(self):
        """获取相连地点"""
        current_loc = self.get_current_location()
        if not current_loc:
            return []
        
        connected = []
        for loc_id in current_loc.connected_locations:
            if loc_id in self.locations:
                connected.append(self.locations[loc_id])
        
        return connected
    
    def move_to_location(self, location_id):
        """移动到指定地点"""
        if location_id not in self.locations:
            return {'success': False, 'message': '未知地点'}
        
        current_loc = self.get_current_location()
        if location_id not in current_loc.connected_locations:
            return {'success': False, 'message': '无法到达该地点'}
        
        # 检查地点是否已发现
        target_loc = self.locations[location_id]
        if not target_loc.discovered:
            target_loc.discovered = True
            self.game.player.stats['locations_discovered'] += 1
            self.game.achievements.check_exploration_achievements()
        
        # 更新当前位置
        old_location = self.current_location_id
        self.current_location_id = location_id
        
        # 更新玩家位置
        self.game.player.location = location_id
        
        # 记录移动
        logging.info(f"玩家从 {old_location} 移动到 {location_id}")
        
        return {
            'success': True,
            'message': f"你移动到了{target_loc.name}。",
            'new_location': target_loc
        }
    
    def discover_location(self, location):
        """发现新地点"""
        if location.id in self.locations:
            self.locations[location.id].discovered = True
            self.game.player.discovered_locations.append(location.id)
            self.game.player.stats['locations_discovered'] += 1
    
    def generate_exploration_event(self):
        """生成探索事件"""
        current_loc = self.get_current_location()
        if not current_loc:
            return {'type': 'nothing', 'message': '未知地点'}
        
        # 标记为已探索
        current_loc.explored = True
        
        # 根据安全等级决定事件类型概率
        safety = current_loc.safety_level
        event_weights = {
            'resource': max(10, 40 - safety * 3),  # 安全的地方资源更多
            'enemy': max(5, 25 - safety * 2),      # 危险的地方敌人更多
            'discovery': 15,
            'npc': 10,
            'special': 5,
            'nothing': max(5, safety * 2)
        }
        
        event_types = list(event_weights.keys())
        weights = list(event_weights.values())
        event_type = random.choices(event_types, weights=weights)[0]
        
        if event_type == 'resource':
            return self.generate_resource_event(current_loc)
        elif event_type == 'enemy':
            return self.generate_enemy_event(current_loc)
        elif event_type == 'discovery':
            return self.generate_discovery_event(current_loc)
        elif event_type == 'npc':
            return self.generate_npc_event(current_loc)
        elif event_type == 'special':
            return self.generate_special_event(current_loc)
        else:
            return {'type': 'nothing', 'message': '没有发现特别的东西'}
    
    def generate_resource_event(self, location):
        """生成资源事件"""
        # 根据地形决定资源类型
        terrain_resources = {
            '森林': ['wood', 'medicine', 'food', 'rare_herbs'],
            '平原': ['food', 'materials', 'cloth'],
            '山地': ['stone', 'rare_minerals', 'water'],
            '河流': ['water', 'food', 'materials'],
            '农田': ['food', 'seeds', 'materials'],
            '道路': ['materials', 'electronic', 'cloth'],
            '遗迹': ['ancient_artifacts', 'stone', 'research_data'],
            '建筑': ['materials', 'cloth', 'electronic', 'food'],
            '营地': ['food', 'water', 'medicine', 'materials']
        }
        
        available_resources = terrain_resources.get(location.terrain, ['materials'])
        resource_type = random.choice(available_resources)
        
        # 数量基于安全等级和运气
        base_amount = random.randint(1, 3)
        luck_bonus = self.game.player.luck // 3
        amount = max(1, base_amount + luck_bonus)
        
        return {
            'type': 'resource',
            'resource_type': resource_type,
            'amount': amount,
            'message': f"在{location.name}找到了{amount}个{self.game.items.get_item_name(resource_type)}"
        }
    
    def generate_enemy_event(self, location):
        """生成敌人事件"""
        # 根据安全等级决定敌人强度
        safety = location.safety_level
        enemy_pool = []
        
        if safety >= 7:
            enemy_pool = [
                {'name': '变异鼠', 'health': 20, 'attack': 5, 'defense': 2, 'loot': {'food': 1}},
                {'name': '辐射蟑螂', 'health': 15, 'attack': 4, 'defense': 3, 'loot': {'materials': 2}}
            ]
        elif safety >= 5:
            enemy_pool = [
                {'name': '变异狼', 'health': 30, 'attack': 8, 'defense': 3, 'loot': {'food': 2, 'materials': 1}},
                {'name': '掠夺者新手', 'health': 25, 'attack': 7, 'defense': 4, 'loot': {'materials': 3}}
            ]
        elif safety >= 3:
            enemy_pool = [
                {'name': '巨型蜘蛛', 'health': 35, 'attack': 12, 'defense': 2, 'loot': {'medicine': 2, 'materials': 2}},
                {'name': '僵尸', 'health': 40, 'attack': 6, 'defense': 5, 'loot': {'cloth': 3}}
            ]
        else:
            enemy_pool = [
                {'name': '变异熊', 'health': 60, 'attack': 15, 'defense': 8, 'loot': {'food': 3, 'materials': 4}},
                {'name': '掠夺者精英', 'health': 50, 'attack': 12, 'defense': 6, 'loot': {'electronic': 2, 'materials': 5}}
            ]
        
        enemy_data = random.choice(enemy_pool)
        
        return {
            'type': 'enemy',
            'enemy_data': enemy_data,
            'message': f"在{location.name}遭遇了{enemy_data['name']}！"
        }
    
    def generate_discovery_event(self, location):
        """生成发现事件"""
        # 寻找未发现的地点
        undiscovered_locations = []
        for loc_id in location.connected_locations:
            if loc_id in self.locations and not self.locations[loc_id].discovered:
                undiscovered_locations.append(self.locations[loc_id])
        
        if undiscovered_locations:
            new_location = random.choice(undiscovered_locations)
            return {
                'type': 'discovery',
                'location': new_location,
                'message': f"发现了一个新的地点：{new_location.name}"
            }
        else:
            # 没有新地点时，给予额外资源
            return self.generate_resource_event(location)
    
    def generate_npc_event(self, location):
        """生成NPC事件"""
        npc_types = [
            {
                'id': 'wandering_merchant',
                'name': '流浪商人',
                'type': 'merchant',
                'dialogue': '需要交易吗？我有各种好东西。',
                'services': ['trade']
            },
            {
                'id': 'injured_survivor',
                'name': '受伤的幸存者',
                'type': 'survivor',
                'dialogue': '帮帮我...我被袭击了...',
                'services': ['quest', 'information']
            },
            {
                'id': 'old_hermit',
                'name': '老隐士',
                'type': 'hermit',
                'dialogue': '年轻人，这个世界比你想的要复杂...',
                'services': ['information', 'training']
            }
        ]
        
        npc_data = random.choice(npc_types)
        
        return {
            'type': 'npc',
            'npc_data': npc_data,
            'message': f"在{location.name}遇到了{npc_data['name']}"
        }
    
    def generate_special_event(self, location):
        """生成特殊事件"""
        special_events = [
            {
                'type': 'special',
                'message': f"在{location.name}发现了一个隐藏的补给箱！",
                'reward': {'materials': 5, 'food': 3, 'water': 3}
            },
            {
                'type': 'special',
                'message': f"在{location.name}找到了一本生存指南，学到了新知识！",
                'reward': {'research_data': 1}
            },
            {
                'type': 'special',
                'message': f"在{location.name}的废墟中发现了前辈留下的物资！",
                'reward': {'medicine': 2, 'materials': 4}
            }
        ]
        
        return random.choice(special_events)
    
    def get_location_by_id(self, location_id):
        """根据ID获取地点"""
        return self.locations.get(location_id)
    
    def get_all_discovered_locations(self):
        """获取所有已发现的地点"""
        return [loc for loc in self.locations.values() if loc.discovered]
    
    def get_location_danger_description(self, safety_level):
        """获取危险程度描述"""
        if safety_level >= 9:
            return "非常安全"
        elif safety_level >= 7:
            return "安全"
        elif safety_level >= 5:
            return "一般"
        elif safety_level >= 3:
            return "危险"
        else:
            return "极度危险"
    
    def get_terrain_description(self, terrain):
        """获取地形描述"""
        descriptions = {
            '森林': '茂密的树木提供了掩护，但也隐藏着危险',
            '平原': '开阔的视野便于观察，但缺乏遮蔽物',
            '山地': '崎岖的地形难以通行，但可能有稀有资源',
            '河流': '重要的水源，但要注意水流和生物',
            '农田': '可能找到食物种子，但土壤可能被污染',
            '道路': '便于移动，但可能遇到其他旅行者',
            '遗迹': '隐藏着古老秘密，但可能有陷阱',
            '建筑': '提供遮蔽，但可能有不速之客',
            '营地': '相对安全，可能有其他幸存者'
        }
        return descriptions.get(terrain, '未知地形')
    
    def update_location_resources(self, location_id, resource_changes):
        """更新地点资源"""
        if location_id in self.locations:
            location = self.locations[location_id]
            for resource, change in resource_changes.items():
                if resource in location.resources:
                    location.resources[resource] += change
                    location.resources[resource] = max(0, location.resources[resource])
    
    def can_travel_to(self, location_id):
        """检查是否可以旅行到指定地点"""
        if location_id not in self.locations:
            return False
        
        current_loc = self.get_current_location()
        if not current_loc:
            return False
        
        return location_id in current_loc.connected_locations
    
    def get_travel_cost(self, location_id):
        """获取旅行消耗"""
        current_terrain = self.get_current_location().terrain
        target_terrain = self.locations[location_id].terrain
        
        # 不同地形间的旅行消耗
        terrain_costs = {
            '平原': 1,
            '道路': 1,
            '农田': 2,
            '森林': 3,
            '河流': 2,
            '山地': 4,
            '遗迹': 3,
            '建筑': 1,
            '营地': 1
        }
        
        cost = terrain_costs.get(current_terrain, 2) + terrain_costs.get(target_terrain, 2)
        return cost

#版权归 乐观的兔子/研究员要加钱 所有