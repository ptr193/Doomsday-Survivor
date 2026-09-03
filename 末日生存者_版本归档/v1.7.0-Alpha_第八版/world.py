# -*- coding: utf-8 -*-

import random
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Location:
    id: str
    name: str
    description: str
    terrain: str
    safety_level: int
    resources: Dict[str, int]
    connected_locations: List[str]
    special_events: List[str]
    x: float = 0
    y: float = 0
    discovered: bool = False
    explored: bool = False

class GameWorld:
    def __init__(self, game):
        self.game = game
        self.locations = {}
        self.current_location_id = "loc_0_0"
        self.initialized = False

    def generate_world(self, locations_data):
        """使用地形生成器生成世界"""
        self.locations.clear()
        for loc_id, loc_info in locations_data.items():
            terrain_id = loc_info['terrain']
            terrain_cfg = self.game.terrain_gen.terrain_types.get(terrain_id)
            display_name = loc_info.get('name')
            if terrain_cfg:
                name = display_name or f"{terrain_cfg.name}区域_{loc_id.split('_')[-2]}_{loc_id.split('_')[-1]}"
                description = loc_info.get('description') or terrain_cfg.description
                safety = loc_info.get('safety', terrain_cfg.safety_base)
                resources = {}
                for res_type, prob in terrain_cfg.resource_distribution.items():
                    if random.random() < prob:
                        resources[res_type] = random.randint(1, 3)
                weather_mod = self.game.weather_effects.get("resource_mod", 1.0)
                for res in resources:
                    resources[res] = max(1, int(resources[res] * weather_mod))
            else:
                name = display_name or loc_id
                description = loc_info.get('description', "")
                safety = loc_info.get('safety', 5)
                resources = {}
            self.locations[loc_id] = Location(
                id=loc_id,
                name=name,
                description=description,
                terrain=terrain_id,
                safety_level=safety,
                resources=resources,
                connected_locations=loc_info.get('connected', []),
                special_events=loc_info.get('special_events', []),
                x=loc_info.get('x', 0),
                y=loc_info.get('y', 0),
                discovered=bool(loc_info.get('discovered', loc_id == "starting_area"))
            )
        start_id = "starting_area" if "starting_area" in self.locations else next(iter(self.locations), None)
        self.current_location_id = start_id
        if start_id:
            self.locations[start_id].discovered = True
            self.locations[start_id].explored = True
        self.initialized = True
        logging.info(f"生成世界地图，共{len(self.locations)}个地点")

    def initialize(self):
        """保持向后兼容的初始化（旧版不使用地形生成）"""
        try:
            self.create_locations()
            self.current_location_id = "starting_area"
            self.initialized = True
            logging.info("游戏世界初始化完成")
        except Exception as e:
            logging.error(f"世界初始化失败: {e}")
            raise

    def create_locations(self):
        """旧版硬编码地图，保留以防地形生成失败"""
        self.locations["starting_area"] = Location(
            id="starting_area", name="起始营地",
            description="一个相对安全的废弃营地，这里有基本的生存设施。",
            terrain="plain", safety_level=7, resources={"food": 3, "water": 3, "materials": 5},
            connected_locations=["north_forest", "east_river", "south_plains"],
            special_events=["safe_rest", "basic_supplies"],
            x=400, y=400, discovered=True, explored=True
        )
        self.locations["north_forest"] = Location(
            id="north_forest", name="北部森林",
            description="茂密的森林，资源丰富但隐藏着危险。",
            terrain="forest", safety_level=4, resources={"food": 5, "water": 2, "wood": 8, "medicine": 2},
            connected_locations=["starting_area", "deep_forest", "mountain_foot"],
            special_events=["animal_encounter", "herb_discovery", "hidden_cache"],
            x=400, y=200
        )
        self.locations["east_river"] = Location(
            id="east_river", name="东部河流",
            description="一条清澈的河流，是重要的水源地。",
            terrain="river", safety_level=6, resources={"water": 8, "food": 2, "materials": 3},
            connected_locations=["starting_area", "river_source", "fishing_spot"],
            special_events=["fishing", "water_source", "river_treasure"],
            x=600, y=400
        )
        self.locations["south_plains"] = Location(
            id="south_plains", name="南部平原",
            description="开阔的平原，视野良好但缺乏遮蔽。",
            terrain="plain", safety_level=5, resources={"food": 4, "water": 3, "materials": 4},
            connected_locations=["starting_area", "abandoned_farm", "old_road"],
            special_events=["weather_exposure", "plains_hunting", "traveler_meet"],
            x=400, y=600
        )
        self.locations["deep_forest"] = Location(
            id="deep_forest", name="深林区",
            description="森林深处，光线昏暗，充满未知危险。",
            terrain="forest", safety_level=2, resources={"wood": 10, "medicine": 4, "rare_herbs": 2},
            connected_locations=["north_forest", "ancient_ruins"],
            special_events=["predator_attack", "ancient_discovery", "mysterious_sounds"],
            x=250, y=150
        )
        self.locations["mountain_foot"] = Location(
            id="mountain_foot", name="山脚",
            description="雄伟山脉的起点，地势开始升高。",
            terrain="mountain", safety_level=5, resources={"stone": 6, "materials": 4, "water": 2},
            connected_locations=["north_forest", "mountain_path"],
            special_events=["rockfall", "mineral_find", "mountain_view"],
            x=550, y=150
        )
        self.locations["river_source"] = Location(
            id="river_source", name="河流源头",
            description="河流的发源地，水质纯净。",
            terrain="mountain", safety_level=7, resources={"water": 10, "rare_minerals": 3},
            connected_locations=["east_river", "mountain_path"],
            special_events=["pure_water", "source_discovery", "mysterious_cave"],
            x=700, y=300
        )
        self.locations["fishing_spot"] = Location(
            id="fishing_spot", name="钓鱼点",
            description="理想的钓鱼位置，水流平缓。",
            terrain="river", safety_level=6, resources={"food": 6, "water": 5},
            connected_locations=["east_river"],
            special_events=["big_catch", "fisherman_ghost", "underwater_treasure"],
            x=700, y=500
        )
        self.locations["abandoned_farm"] = Location(
            id="abandoned_farm", name="废弃农场",
            description="被遗弃的农场，可能还留有一些物资。",
            terrain="plain", safety_level=4, resources={"food": 8, "materials": 6, "seeds": 4},
            connected_locations=["south_plains", "farmhouse"],
            special_events=["farm_tools", "hidden_cellar", "scarecrow_secret"],
            x=250, y=600
        )
        self.locations["old_road"] = Location(
            id="old_road", name="老路",
            description="破旧的公路，连接着各个幸存者据点。",
            terrain="urban", safety_level=5, resources={"materials": 3, "electronic": 2},
            connected_locations=["south_plains", "trading_post"],
            special_events=["traveler_encounter", "roadside_find", "car_wreck"],
            x=550, y=650
        )
        self.locations["ancient_ruins"] = Location(
            id="ancient_ruins", name="古代遗迹",
            description="神秘的古代建筑遗迹，隐藏着古老的秘密。",
            terrain="urban", safety_level=3, resources={"ancient_artifacts": 5, "stone": 4},
            connected_locations=["deep_forest"],
            special_events=["artifact_discovery", "ancient_trap", "historical_insight"],
            x=150, y=100
        )
        self.locations["mountain_path"] = Location(
            id="mountain_path", name="山路",
            description="陡峭的山路，通向更高的地方。",
            terrain="mountain", safety_level=4, resources={"stone": 5, "rare_herbs": 3},
            connected_locations=["mountain_foot", "river_source", "mountain_peak"],
            special_events=["climbing_challenge", "avalanche_risk", "mountain_goat"],
            x=650, y=200
        )
        self.locations["farmhouse"] = Location(
            id="farmhouse", name="农舍",
            description="破旧的农舍，可能还保留着一些生活用品。",
            terrain="urban", safety_level=6, resources={"food": 4, "materials": 8, "cloth": 5},
            connected_locations=["abandoned_farm"],
            special_events=["shelter_find", "old_diary", "hidden_stash"],
            x=150, y=650
        )
        self.locations["trading_post"] = Location(
            id="trading_post", name="贸易站",
            description="幸存者建立的交易场所，可以交换物资。",
            terrain="urban", safety_level=8, resources={"various": 10},
            connected_locations=["old_road", "survivor_camp"],
            special_events=["trade_opportunity", "information_exchange", "quest_offer"],
            x=550, y=750
        )
        self.locations["survivor_camp"] = Location(
            id="survivor_camp", name="幸存者营地",
            description="其他幸存者建立的营地，相对安全。",
            terrain="plain", safety_level=9, resources={"food": 3, "water": 4, "medicine": 3},
            connected_locations=["trading_post"],
            special_events=["ally_meeting", "camp_services", "group_quest"],
            x=450, y=750
        )
        self.locations["mountain_peak"] = Location(
            id="mountain_peak", name="山顶",
            description="山脉的最高点，可以俯瞰整个区域。",
            terrain="mountain", safety_level=6, resources={"rare_minerals": 5, "strategic_view": 1},
            connected_locations=["mountain_path"],
            special_events=["view_discovery", "weather_observation", "signal_boost"],
            x=700, y=100
        )
        logging.info(f"创建了{len(self.locations)}个地点（硬编码）")

    def load_data(self, save_data):
        try:
            locations_data = save_data.get('locations', {})
            if locations_data and any('terrain' in loc or 'name' in loc for loc in locations_data.values()):
                self.locations.clear()
                for loc_id, loc_data in locations_data.items():
                    self.locations[loc_id] = Location(
                        id=loc_id,
                        name=loc_data.get('name', loc_id),
                        description=loc_data.get('description', ''),
                        terrain=loc_data.get('terrain', 'plain'),
                        safety_level=loc_data.get('safety_level', 5),
                        resources=loc_data.get('resources', {}),
                        connected_locations=loc_data.get('connected_locations', []),
                        special_events=loc_data.get('special_events', []),
                        x=loc_data.get('x', 0),
                        y=loc_data.get('y', 0),
                        discovered=loc_data.get('discovered', False),
                        explored=loc_data.get('explored', False)
                    )
            else:
                if not self.locations:
                    self.create_locations()
                for loc_id, loc_data in locations_data.items():
                    if loc_id in self.locations:
                        self.locations[loc_id].discovered = loc_data.get('discovered', False)
                        self.locations[loc_id].explored = loc_data.get('explored', False)
            self.current_location_id = save_data.get('current_location_id', 'starting_area')
            if self.current_location_id not in self.locations and self.locations:
                self.current_location_id = next(iter(self.locations))
            self.initialized = True
            logging.info("世界数据加载完成")
        except Exception as e:
            logging.error(f"加载世界数据失败: {e}")
            raise

    def get_save_data(self):
        locations_data = {}
        for loc_id, location in self.locations.items():
            locations_data[loc_id] = {
                'name': location.name,
                'description': location.description,
                'terrain': location.terrain,
                'safety_level': location.safety_level,
                'resources': location.resources,
                'connected_locations': location.connected_locations,
                'special_events': location.special_events,
                'x': location.x,
                'y': location.y,
                'discovered': location.discovered,
                'explored': location.explored
            }
        return {
            'current_location_id': self.current_location_id,
            'locations': locations_data
        }

    def get_current_location(self):
        return self.locations.get(self.current_location_id)

    def get_connected_locations(self):
        current = self.get_current_location()
        if not current:
            return []
        connected = []
        for loc_id in current.connected_locations:
            if loc_id in self.locations:
                connected.append(self.locations[loc_id])
        return connected

    def move_to_location(self, location_id):
        if location_id not in self.locations:
            return {'success': False, 'message': '未知地点'}
        current = self.get_current_location()
        if location_id not in current.connected_locations:
            return {'success': False, 'message': '无法到达该地点'}
        target = self.locations[location_id]
        if not target.discovered:
            target.discovered = True
            self.game.player.stats['locations_discovered'] += 1
            self.game.achievements.check_exploration_achievements()
        self.current_location_id = location_id
        self.game.player.location = location_id
        if location_id not in self.game.player.discovered_locations:
            self.game.player.discovered_locations.append(location_id)
        if hasattr(self.game, 'quests') and self.game.quests:
            self.game.quests.update_quest_progress('location_discovered', location=target, location_id=target.id)
        logging.info(f"玩家从 {current.id} 移动到 {location_id}")
        return {'success': True, 'message': f"你移动到了{target.name}。", 'new_location': target}

    def discover_location(self, location):
        if location.id in self.locations:
            self.locations[location.id].discovered = True
            if location.id not in self.game.player.discovered_locations:
                self.game.player.discovered_locations.append(location.id)
            self.game.player.stats['locations_discovered'] += 1
            if hasattr(self.game, 'quests') and self.game.quests:
                self.game.quests.update_quest_progress('location_discovered', location=self.locations[location.id])

    def generate_exploration_event(self):
        current = self.get_current_location()
        if not current:
            return {'type': 'nothing', 'message': '未知地点'}
        current.explored = True

        safety = current.safety_level
        weather_mod = self.game.weather_effects.get("resource_mod", 1.0)
        event_weights = {
            'resource': max(10, int(40 - safety * 3 * weather_mod)),
            'enemy': max(5, int(25 - safety * 2 * weather_mod)),
            'discovery': 15,
            'npc': 10,
            'special': 5,
            'nothing': max(5, int(safety * 2 / weather_mod))
        }
        event_type = random.choices(list(event_weights.keys()), weights=list(event_weights.values()))[0]

        if event_type == 'resource':
            return self._resource_event(current)
        elif event_type == 'enemy':
            return self._enemy_event(current)
        elif event_type == 'discovery':
            return self._discovery_event(current)
        elif event_type == 'npc':
            return self._npc_event(current)
        elif event_type == 'special':
            return self._special_event(current)
        else:
            return {'type': 'nothing', 'message': '没有发现特别的东西'}

    def _resource_event(self, location):
        terrain_resources = {
            'forest': ['wood', 'medicine', 'food', 'rare_herbs'],
            'plain': ['food', 'materials', 'cloth'],
            'mountain': ['stone', 'rare_minerals', 'water'],
            'river': ['water', 'food', 'materials'],
            'urban': ['materials', 'electronic', 'cloth']
        }
        pool = terrain_resources.get(location.terrain, ['materials'])
        rtype = random.choice(pool)
        season_mod = {"spring": 1.2, "summer": 1.0, "autumn": 1.1, "winter": 0.7}.get(self.game.season, 1.0)
        weather_mod = self.game.weather_effects.get("resource_mod", 1.0)
        base_amount = random.randint(1, 3) + self.game.player.luck // 3
        amount = int(base_amount * season_mod * weather_mod)
        amount = max(1, amount)
        return {
            'type': 'resource',
            'resource_type': rtype,
            'amount': amount,
            'message': f"在{location.name}找到了{amount}个{self.game.items.get_item_name(rtype)}"
        }

    def _enemy_event(self, location):
        safety = location.safety_level
        # 从MOD管理器获取敌人列表
        enemies = self.game.mod_manager.get_data('enemies', {})
        if not enemies:
            # 回退
            if safety >= 7:
                pool = [{'id': 'mutant_rat', 'name': '变异鼠', 'health': 20, 'attack': 5, 'defense': 2, 'loot': {'food': 1}}]
            elif safety >= 5:
                pool = [{'id': 'mutant_wolf', 'name': '变异狼', 'health': 30, 'attack': 8, 'defense': 3, 'loot': {'food': 2}}]
            elif safety >= 3:
                pool = [{'id': 'giant_spider', 'name': '巨型蜘蛛', 'health': 35, 'attack': 12, 'defense': 2, 'loot': {'medicine': 2}}]
            else:
                pool = [{'id': 'mutant_bear', 'name': '变异熊', 'health': 60, 'attack': 15, 'defense': 8, 'loot': {'food': 3}}]
        else:
            # 根据安全等级筛选敌人
            candidates = [e for e in enemies.values() if e.get('level', 1) <= safety + 2]
            if not candidates:
                candidates = list(enemies.values())
            pool = candidates
        enemy = random.choice(pool)
        return {'type': 'enemy', 'enemy_data': enemy, 'message': f"在{location.name}遭遇了{enemy['name']}！"}

    def _discovery_event(self, location):
        undiscovered = [loc_id for loc_id in location.connected_locations
                        if loc_id in self.locations and not self.locations[loc_id].discovered]
        if undiscovered:
            new_loc = random.choice(undiscovered)
            return {'type': 'discovery', 'location': self.locations[new_loc], 'message': f"发现了一个新的地点：{self.locations[new_loc].name}"}
        else:
            return self._resource_event(location)

    def _npc_event(self, location):
        npc_data = random.choice([
            {'id': 'wandering_merchant', 'name': '流浪商人', 'type': 'merchant', 'dialogue': '需要交易吗？', 'services': ['trade']},
            {'id': 'injured_survivor', 'name': '受伤的幸存者', 'type': 'survivor', 'dialogue': '帮帮我...', 'services': ['quest', 'information']},
            {'id': 'old_hermit', 'name': '老隐士', 'type': 'hermit', 'dialogue': '年轻人...', 'services': ['information', 'training']}
        ])
        return {'type': 'npc', 'npc_data': npc_data, 'message': f"在{location.name}遇到了{npc_data['name']}"}

    def _special_event(self, location):
        events = [
            {'type': 'special', 'message': f"在{location.name}发现了一个隐藏的补给箱！", 'reward': {'materials': 5, 'food': 3, 'water': 3}},
            {'type': 'special', 'message': f"在{location.name}找到了一本生存指南，学到了新知识！", 'reward': {'research_data': 1}},
            {'type': 'special', 'message': f"在{location.name}的废墟中发现了前辈留下的物资！", 'reward': {'medicine': 2, 'materials': 4}},
            {'type': 'special', 'message': f"在{location.name}发现了一棵古老的灵药草！", 'reward': {'rare_herbs': 2, 'medicine': 1}}
        ]
        return random.choice(events)

    def get_location_by_id(self, location_id):
        return self.locations.get(location_id)

    def get_all_discovered_locations(self):
        return [loc for loc in self.locations.values() if loc.discovered]

    def get_location_danger_description(self, safety):
        if safety >= 9: return "非常安全"
        elif safety >= 7: return "安全"
        elif safety >= 5: return "一般"
        elif safety >= 3: return "危险"
        else: return "极度危险"

    def get_terrain_description(self, terrain):
        desc = {
            'forest': '茂密的树木提供了掩护，但也隐藏着危险',
            'plain': '开阔的视野便于观察，但缺乏遮蔽物',
            'mountain': '崎岖的地形难以通行，但可能有稀有资源',
            'river': '重要的水源，但要注意水流和生物',
            'urban': '倒塌的建筑，可能隐藏着危险'
        }
        return desc.get(terrain, '未知地形')

    def update_location_resources(self, location_id, resource_changes):
        if location_id in self.locations:
            loc = self.locations[location_id]
            for r, change in resource_changes.items():
                if r in loc.resources:
                    loc.resources[r] = max(0, loc.resources[r] + change)