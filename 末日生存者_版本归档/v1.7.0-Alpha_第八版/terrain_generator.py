# -*- coding: utf-8 -*-
import random
import logging
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class TerrainConfig:
    name: str
    description: str
    resource_distribution: Dict[str, float]  # 资源类型 -> 出现概率
    enemy_pool: List[str]
    safety_base: int
    visual_color: str

class TerrainGenerator:
    def __init__(self, game):
        self.game = game
        self.terrain_types = {}  # terrain_id -> TerrainConfig
        self.loaded = False

    def load_from_mods(self):
        """从ModManager加载地形配置"""
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
        """回退：创建默认地形"""
        self.terrain_types = {
            'plain': TerrainConfig('平原', '开阔的平原', {'food':0.4,'water':0.2,'materials':0.3}, ['mutant_rat','radroach'], 6, '#a7c5a3'),
            'forest': TerrainConfig('森林', '茂密的森林', {'wood':0.5,'medicine':0.2,'rare_herbs':0.1}, ['mutant_wolf','giant_spider'], 4, '#2d6a4f'),
            'mountain': TerrainConfig('山地', '崎岖的山地', {'stone':0.6,'rare_minerals':0.2}, ['mutant_bear','radscorpion'], 5, '#8d6b63'),
            'river': TerrainConfig('河流', '清澈的河流', {'water':0.7,'food':0.3}, ['mutant_rat','zombie'], 7, '#4ea8de'),
            'urban': TerrainConfig('城市废墟', '倒塌的建筑', {'materials':0.5,'electronic':0.3,'cloth':0.2}, ['raider_elite','ghost_soldier'], 3, '#4a6e8c')
        }

    def generate_map(self, width=10, height=10, seed=None):
        """生成包含命名关键地点的可玩地图。"""
        if seed:
            random.seed(seed)
        named = {
            "starting_area": {
                "name": "起始营地", "description": "一个相对安全的废弃营地，这里有基本的生存设施。",
                "terrain": "plain", "safety": 7, "x": 400, "y": 400,
                "connected": ["north_forest", "east_river", "south_plains"],
                "discovered": True, "special_events": ["safe_rest", "basic_supplies"]
            },
            "north_forest": {
                "name": "北部森林", "description": "茂密的森林，资源丰富但隐藏着危险。",
                "terrain": "forest", "safety": 4, "x": 400, "y": 220,
                "connected": ["starting_area", "deep_forest", "mountain_foot"]
            },
            "east_river": {
                "name": "东部河流", "description": "一条清澈的河流，是重要的水源地。",
                "terrain": "river", "safety": 6, "x": 580, "y": 400,
                "connected": ["starting_area", "river_source", "fishing_spot"]
            },
            "south_plains": {
                "name": "南部平原", "description": "开阔的平原，视野良好但缺乏遮蔽。",
                "terrain": "plain", "safety": 5, "x": 400, "y": 580,
                "connected": ["starting_area", "abandoned_farm", "old_road"]
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
                "connected": ["east_river"]
            },
            "abandoned_farm": {
                "name": "废弃农场", "description": "被遗弃的农场，可能还留有一些物资。",
                "terrain": "plain", "safety": 4, "x": 250, "y": 620,
                "connected": ["south_plains", "farmhouse"]
            },
            "old_road": {
                "name": "老路", "description": "破旧的公路，连接着各个幸存者据点。",
                "terrain": "urban", "safety": 5, "x": 560, "y": 650,
                "connected": ["south_plains", "trading_post"]
            },
            "ancient_ruins": {
                "name": "古代遗迹", "description": "神秘的古代建筑遗迹，隐藏着古老的秘密。",
                "terrain": "urban", "safety": 3, "x": 150, "y": 100,
                "connected": ["deep_forest"]
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
                "connected": ["mountain_path"]
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