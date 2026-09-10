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
    structures: List[str] = None

    def __post_init__(self):
        if self.structures is None:
            self.structures = []

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
                discovered=bool(loc_info.get('discovered', loc_id == "starting_area")),
                structures=list(loc_info.get('structures', []))
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
            connected_locations=["north_forest", "east_river", "south_plains", "west_swamp"],
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
            connected_locations=["starting_area", "river_source", "fishing_spot", "west_swamp"],
            special_events=["fishing", "water_source", "river_treasure"],
            x=600, y=400
        )
        self.locations["south_plains"] = Location(
            id="south_plains", name="南部平原",
            description="开阔的平原，视野良好但缺乏遮蔽。",
            terrain="plain", safety_level=5, resources={"food": 4, "water": 3, "materials": 4},
            connected_locations=["starting_area", "abandoned_farm", "old_road", "ash_wasteland"],
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
            connected_locations=["south_plains", "trading_post", "ash_wasteland"],
            special_events=["traveler_encounter", "roadside_find", "car_wreck"],
            x=550, y=650
        )
        self.locations["ancient_ruins"] = Location(
            id="ancient_ruins", name="古代遗迹",
            description="神秘的古代建筑遗迹，隐藏着古老的秘密。",
            terrain="urban", safety_level=3, resources={"ancient_artifacts": 5, "stone": 4},
            connected_locations=["deep_forest", "research_lab"],
            special_events=["artifact_discovery", "ancient_trap", "historical_insight"],
            x=150, y=100
        )
        self.locations["research_lab"] = Location(
            id="research_lab", name="研究实验室",
            description="半倒塌的地下实验室，残留着未完成的实验。",
            terrain="urban", safety_level=3, resources={"research_data": 4, "electronic": 3, "materials": 2},
            connected_locations=["ancient_ruins"],
            special_events=["lab_records", "unstable_experiment", "radiation_leak"],
            x=80, y=180
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
        self.locations["west_swamp"] = Location(
            id="west_swamp", name="西部沼泽",
            description="泥炭与浊水交织的低地，滤芯在这里比食物更珍贵。",
            terrain="swamp", safety_level=3, resources={"water": 5, "rare_herbs": 2, "peat_brick": 3},
            connected_locations=["starting_area", "east_river"],
            special_events=["bog_mist", "peat_harvest"],
            x=220, y=480
        )
        self.locations["ash_wasteland"] = Location(
            id="ash_wasteland", name="灰烬荒原",
            description="辐射尘覆盖的干燥荒原，盐晶在风里发亮。",
            terrain="wasteland", safety_level=3, resources={"rare_minerals": 4, "stone": 3, "materials": 2},
            connected_locations=["south_plains", "old_road"],
            special_events=["dust_storm", "salt_cache"],
            x=500, y=520
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
                        explored=loc_data.get('explored', False),
                        structures=list(loc_data.get('structures', []))
                    )
            else:
                if not self.locations:
                    self.create_locations()
                for loc_id, loc_data in locations_data.items():
                    if loc_id in self.locations:
                        self.locations[loc_id].discovered = loc_data.get('discovered', False)
                        self.locations[loc_id].explored = loc_data.get('explored', False)
                        self.locations[loc_id].structures = list(loc_data.get('structures', getattr(self.locations[loc_id], 'structures', []) or []))
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
                'explored': location.explored,
                'structures': list(getattr(location, 'structures', []) or [])
            }
        return {
            'current_location_id': self.current_location_id,
            'locations': locations_data
        }

    def get_terrain_color(self, terrain_id):
        terrain_gen = getattr(self.game, 'terrain_gen', None)
        cfg = getattr(terrain_gen, 'terrain_types', {}).get(terrain_id) if terrain_gen else None
        if cfg and getattr(cfg, 'visual_color', None):
            return cfg.visual_color
        defaults = {
            'plain': '#a7c5a3', 'forest': '#2d6a4f', 'mountain': '#8d6b63',
            'river': '#4ea8de', 'urban': '#4a6e8c',
            'swamp': '#3d5c4a', 'wasteland': '#c4a35a'
        }
        return defaults.get(terrain_id, '#cccccc')

    def get_safety_color(self, safety_level):
        level = int(safety_level or 0)
        if level >= 8:
            return '#4caf50'
        if level >= 5:
            return '#ffcc66'
        return '#e57373'

    def get_map_style(self):
        night = False
        if hasattr(self.game, 'is_night'):
            try:
                night = bool(self.game.is_night())
            except Exception:
                night = False
        return {
            'night_dim': 0.55 if night else 1.0,
            'grid': True,
            'grid_color': '#2a2a2a',
            'fog_color': '#1c1c1c',
            'current_outline': '#ffcc66',
            'npc_marker': '#f4d35e',
            'background': '#121212' if night else '#1a1a1a',
        }

    def get_map_snapshot(self):
        nodes = []
        seen_edges = set()
        edges = []
        legend = {}
        terrain_gen = getattr(self.game, 'terrain_gen', None)
        terrain_types = getattr(terrain_gen, 'terrain_types', {}) if terrain_gen else {}
        for tid, cfg in terrain_types.items():
            legend[tid] = {
                'name': getattr(cfg, 'name', tid),
                'color': getattr(cfg, 'visual_color', self.get_terrain_color(tid)),
            }
        if not legend:
            legend = {
                'plain': {'name': '平原', 'color': '#a7c5a3'},
                'forest': {'name': '森林', 'color': '#2d6a4f'},
                'mountain': {'name': '山地', 'color': '#8d6b63'},
                'river': {'name': '河流', 'color': '#4ea8de'},
                'urban': {'name': '城市废墟', 'color': '#4a6e8c'},
                'swamp': {'name': '沼泽', 'color': '#3d5c4a'},
                'wasteland': {'name': '灰烬荒原', 'color': '#c4a35a'},
            }
        npc_by_loc = {}
        npcs = getattr(getattr(self.game, 'npcs', None), 'npcs', {}) or {}
        for npc in npcs.values():
            loc_id = npc.get('location')
            if not loc_id:
                continue
            npc_by_loc.setdefault(loc_id, []).append(npc.get('id'))
        for loc in self.locations.values():
            discovered = bool(loc.discovered)
            nodes.append({
                'id': loc.id,
                'name': loc.name,
                'x': loc.x,
                'y': loc.y,
                'terrain': loc.terrain,
                'terrain_color': self.get_terrain_color(loc.terrain),
                'safety_color': self.get_safety_color(loc.safety_level),
                'current': loc.id == self.current_location_id,
                'discovered': discovered,
                'fog': not discovered,
                'safety_level': loc.safety_level,
                'explored': loc.explored,
                'npc_ids': list(npc_by_loc.get(loc.id, [])),
            })
            for conn_id in loc.connected_locations:
                if conn_id not in self.locations:
                    continue
                key = tuple(sorted((loc.id, conn_id)))
                if key in seen_edges:
                    continue
                seen_edges.add(key)
                edges.append({'from': key[0], 'to': key[1]})
        return {
            'current': self.current_location_id,
            'nodes': nodes,
            'edges': edges,
            'legend': legend,
            'style': self.get_map_style(),
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
        night = self.game.is_night() if hasattr(self.game, 'is_night') else False
        enemy_weight = max(5, int(25 - safety * 2 * weather_mod))
        if night:
            enemy_weight = int(enemy_weight * 1.8)
        event_weights = {
            'resource': max(10, int(40 - safety * 3 * weather_mod)),
            'enemy': enemy_weight,
            'discovery': 10 if night else 15,
            'npc': 6 if night else 10,
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
            'urban': ['materials', 'electronic', 'cloth'],
            'swamp': ['water', 'rare_herbs', 'peat_brick'],
            'wasteland': ['rare_minerals', 'stone', 'materials']
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
        enemies = self.game.mod_manager.get_data('enemies') or {}
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
            {'id': 'old_hermit', 'name': '老隐士', 'type': 'hermit', 'dialogue': '年轻人...', 'services': ['information', 'training']},
            {'id': 'scout_lin', 'name': '侦察员小林', 'type': 'scout', 'dialogue': '前方的路我走过。', 'services': ['information', 'map_info']}
        ])
        return {'type': 'npc', 'npc_data': npc_data, 'message': f"在{location.name}遇到了{npc_data['name']}"}

    def get_wildlife_pool(self, location):
        wildlife = (self.game.mod_manager.get_data('wildlife') or {}) if hasattr(self.game, 'mod_manager') else {}
        if wildlife:
            terrain = location.terrain if location else 'plain'
            candidates = [w for w in wildlife.values() if terrain in w.get('habitats', ['plain', 'forest'])]
            return candidates or list(wildlife.values())
        return [
            {'id': 'wild_rabbit', 'name': '野兔', 'loot': {'food': [1, 2], 'animal_hide': [0, 1]}},
            {'id': 'mutant_crow', 'name': '变异鸦', 'loot': {'food': [1, 1], 'toxin_gland': [0, 1]}}
        ]

    def _special_event(self, location):
        events = [
            {'type': 'special', 'message': f"在{location.name}发现了一个隐藏的补给箱！", 'reward': {'materials': 5, 'food': 3, 'water': 3}},
            {'type': 'special', 'message': f"在{location.name}找到了一本生存指南，学到了新知识！", 'reward': {'research_data': 1}},
            {'type': 'special', 'message': f"在{location.name}的废墟中发现了前辈留下的物资！", 'reward': {'medicine': 2, 'materials': 4}},
            {'type': 'special', 'message': f"在{location.name}发现了一棵古老的灵药草！", 'reward': {'rare_herbs': 2, 'medicine': 1}}
        ]
        return random.choice(events)

    def get_hop_distance(self, from_id, to_id):
        if from_id == to_id:
            return 0
        if from_id not in self.locations or to_id not in self.locations:
            return None
        visited = {from_id}
        queue = [(from_id, 0)]
        while queue:
            current_id, dist = queue.pop(0)
            current = self.locations.get(current_id)
            if not current:
                continue
            for nxt in current.connected_locations:
                if nxt in visited:
                    continue
                if nxt == to_id:
                    return dist + 1
                visited.add(nxt)
                queue.append((nxt, dist + 1))
        return None

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
            'urban': '倒塌的建筑，可能隐藏着危险',
            'swamp': '泥泞腥臭，滤水困难，潜伏着沼蛭',
            'wasteland': '辐射尘覆盖的干燥荒原，盐晶与灰烬并存',
            'coast': '盐风拍打的破碎海岸，海藻与残骸堆积',
            'tundra': '永冻的北地，风雪掩盖着兽径'
        }
        return desc.get(terrain, '未知地形')

    def update_location_resources(self, location_id, resource_changes):
        if location_id in self.locations:
            loc = self.locations[location_id]
            explore = bool(getattr(self.game, 'is_explore_mode', lambda: False)())
            for r, change in resource_changes.items():
                if r in loc.resources:
                    if explore and change < 0:
                        continue
                    loc.resources[r] = max(0, loc.resources[r] + change)


@dataclass
class TerrainConfig:
    name: str
    description: str
    resource_distribution: Dict[str, float]
    enemy_pool: List[str]
    safety_base: int
    visual_color: str


class TerrainGenerator:
    def __init__(self, game):
        self.game = game
        self.terrain_types = {}
        self.loaded = False

    def load_from_mods(self):
        terrains_data = self.game.mod_manager.get_data('terrains', None)
        if not terrains_data:
            logging.warning("未找到地形配置，使用默认地形")
            self._create_default_terrains()
        else:
            for tid, data in terrains_data.items():
                self.terrain_types[tid] = TerrainConfig(
                    name=data.get('name', tid),
                    description=data.get('description', ''),
                    resource_distribution=data.get('resources', {}),
                    enemy_pool=data.get('enemies', []),
                    safety_base=data.get('safety', 5),
                    visual_color=data.get('color', '#cccccc')
                )
        self.loaded = True
        logging.info(f"加载了 {len(self.terrain_types)} 种地形")

    def _create_default_terrains(self):
        self.terrain_types = {
            'plain': TerrainConfig('平原', '开阔的平原', {'food': 0.4, 'water': 0.2, 'materials': 0.3}, ['mutant_rat', 'radroach'], 6, '#a7c5a3'),
            'forest': TerrainConfig('森林', '茂密的森林', {'wood': 0.5, 'medicine': 0.2, 'rare_herbs': 0.1}, ['mutant_wolf', 'giant_spider'], 4, '#2d6a4f'),
            'mountain': TerrainConfig('山地', '崎岖的山地', {'stone': 0.6, 'rare_minerals': 0.2}, ['mutant_bear', 'radscorpion'], 5, '#8d6b63'),
            'river': TerrainConfig('河流', '清澈的河流', {'water': 0.7, 'food': 0.3}, ['mutant_rat', 'zombie'], 7, '#4ea8de'),
            'urban': TerrainConfig('城市废墟', '倒塌的建筑', {'materials': 0.5, 'electronic': 0.3, 'cloth': 0.2}, ['raider_elite', 'ghost_soldier'], 3, '#4a6e8c'),
            'swamp': TerrainConfig('沼泽', '泥泞腥臭的沼泽，滤水困难', {'water': 0.5, 'rare_herbs': 0.25, 'peat_brick': 0.35}, ['bog_leech', 'swamp_lurker', 'acid_beetle'], 3, '#3d5c4a'),
            'wasteland': TerrainConfig('灰烬荒原', '辐射尘覆盖的干燥荒原', {'rare_minerals': 0.35, 'stone': 0.3, 'materials': 0.25}, ['dune_stalker', 'ash_wraith', 'radscorpion'], 3, '#c4a35a'),
            'coast': TerrainConfig('海岸', '盐风拍打的破碎海岸，海藻与残骸堆积', {'water': 0.4, 'food': 0.45, 'kelp_strip': 0.4}, ['tide_reaver', 'mutant_rat'], 4, '#3d8ea8'),
            'tundra': TerrainConfig('冻原', '永冻的北地，风雪掩盖着兽径', {'food': 0.25, 'frost_pelt': 0.3, 'stone': 0.2}, ['frost_wolf', 'mutant_wolf'], 3, '#cfe8f5')
        }

    def generate_map(self, width=10, height=10, seed=None):
        if seed:
            random.seed(seed)
        named = {
            "starting_area": {
                "name": "起始营地", "description": "一个相对安全的废弃营地，这里有基本的生存设施。",
                "terrain": "plain", "safety": 7, "x": 400, "y": 400,
                "connected": ["north_forest", "east_river", "south_plains", "west_swamp"],
                "discovered": True, "special_events": ["safe_rest", "basic_supplies"]
            },
            "north_forest": {
                "name": "北部森林", "description": "茂密的森林，资源丰富但隐藏着危险。",
                "terrain": "forest", "safety": 4, "x": 400, "y": 220,
                "connected": ["starting_area", "deep_forest", "mountain_foot", "north_tundra"]
            },
            "east_river": {
                "name": "东部河流", "description": "一条清澈的河流，是重要的水源地。",
                "terrain": "river", "safety": 6, "x": 580, "y": 400,
                "connected": ["starting_area", "river_source", "fishing_spot", "west_swamp", "east_coast"]
            },
            "south_plains": {
                "name": "南部平原", "description": "开阔的平原，视野良好但缺乏遮蔽。",
                "terrain": "plain", "safety": 5, "x": 400, "y": 580,
                "connected": ["starting_area", "abandoned_farm", "old_road", "ash_wasteland"]
            },
            "deep_forest": {
                "name": "深林区", "description": "森林深处，光线昏暗，充满未知危险。",
                "terrain": "forest", "safety": 2, "x": 250, "y": 140,
                "connected": ["north_forest", "ancient_ruins"]
            },
            "mountain_foot": {
                "name": "山脚", "description": "雄伟山脉的起点，地势开始升高。",
                "terrain": "mountain", "safety": 5, "x": 560, "y": 160,
                "connected": ["north_forest", "mountain_path"]
            },
            "river_source": {
                "name": "河流源头", "description": "河流的发源地，水质纯净。",
                "terrain": "mountain", "safety": 7, "x": 720, "y": 300,
                "connected": ["east_river", "mountain_path"]
            },
            "fishing_spot": {
                "name": "钓鱼点", "description": "理想的钓鱼位置，水流平缓。",
                "terrain": "river", "safety": 6, "x": 720, "y": 500,
                "connected": ["east_river", "east_coast"]
            },
            "abandoned_farm": {
                "name": "废弃农场", "description": "被遗弃的农场，可能还留有一些物资。",
                "terrain": "plain", "safety": 4, "x": 250, "y": 620,
                "connected": ["south_plains", "farmhouse"]
            },
            "old_road": {
                "name": "老路", "description": "破旧的公路，连接着各个幸存者据点。",
                "terrain": "urban", "safety": 5, "x": 560, "y": 650,
                "connected": ["south_plains", "trading_post", "ash_wasteland"]
            },
            "ancient_ruins": {
                "name": "古代遗迹", "description": "神秘的古代建筑遗迹，隐藏着古老的秘密。",
                "terrain": "urban", "safety": 3, "x": 150, "y": 100,
                "connected": ["deep_forest", "research_lab"]
            },
            "mountain_path": {
                "name": "山路", "description": "陡峭的山路，通向更高的地方。",
                "terrain": "mountain", "safety": 4, "x": 650, "y": 200,
                "connected": ["mountain_foot", "river_source", "mountain_peak"]
            },
            "farmhouse": {
                "name": "农舍", "description": "破旧的农舍，可能还保留着一些生活用品。",
                "terrain": "urban", "safety": 6, "x": 150, "y": 650,
                "connected": ["abandoned_farm"]
            },
            "trading_post": {
                "name": "贸易站", "description": "幸存者建立的交易场所，可以交换物资。",
                "terrain": "urban", "safety": 8, "x": 560, "y": 750,
                "connected": ["old_road", "survivor_camp"]
            },
            "survivor_camp": {
                "name": "幸存者营地", "description": "其他幸存者建立的营地，相对安全。",
                "terrain": "plain", "safety": 9, "x": 450, "y": 780,
                "connected": ["trading_post"]
            },
            "mountain_peak": {
                "name": "山顶", "description": "山脉的最高点，可以俯瞰整个区域。",
                "terrain": "mountain", "safety": 6, "x": 720, "y": 90,
                "connected": ["mountain_path", "north_tundra"]
            },
            "research_lab": {
                "name": "研究实验室", "description": "半倒塌的地下实验室，残留着未完成的实验。",
                "terrain": "urban", "safety": 3, "x": 80, "y": 180,
                "connected": ["ancient_ruins"]
            },
            "west_swamp": {
                "name": "西部沼泽", "description": "泥炭与浊水交织的低地，滤芯在这里比食物更珍贵。",
                "terrain": "swamp", "safety": 3, "x": 220, "y": 480,
                "connected": ["starting_area", "east_river"]
            },
            "ash_wasteland": {
                "name": "灰烬荒原", "description": "辐射尘覆盖的干燥荒原，盐晶在风里发亮。",
                "terrain": "wasteland", "safety": 3, "x": 500, "y": 520,
                "connected": ["south_plains", "old_road"]
            },
            "east_coast": {
                "name": "东部海岸", "description": "盐风拍打的破碎海岸，海藻与残骸堆积。",
                "terrain": "coast", "safety": 4, "x": 760, "y": 430,
                "connected": ["east_river", "fishing_spot"]
            },
            "north_tundra": {
                "name": "北部冻原", "description": "永冻的北地，风雪掩盖着兽径。",
                "terrain": "tundra", "safety": 3, "x": 330, "y": 80,
                "connected": ["north_forest", "mountain_peak"]
            }
        }
        extra_terrains = list(self.terrain_types.keys()) or ["plain"]
        extra_count = max(0, min(width * height, 24) - len(named))
        extra_ids = []
        for i in range(extra_count):
            loc_id = f"wild_{i}"
            extra_ids.append(loc_id)
            named[loc_id] = {
                "name": f"未知区域 {i + 1}",
                "description": "尚未被幸存者详细记录的区域。",
                "terrain": random.choice(extra_terrains),
                "safety": random.randint(2, 7),
                "x": 80 + (i % 6) * 90,
                "y": 80 + (i // 6) * 80,
                "connected": []
            }
        if extra_ids:
            named["old_road"]["connected"].append(extra_ids[0])
            named[extra_ids[0]]["connected"].append("old_road")
            for idx in range(len(extra_ids) - 1):
                named[extra_ids[idx]]["connected"].append(extra_ids[idx + 1])
                named[extra_ids[idx + 1]]["connected"].append(extra_ids[idx])
        return named