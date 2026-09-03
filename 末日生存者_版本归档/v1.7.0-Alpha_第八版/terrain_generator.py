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
        """动态生成地图，返回 location_id -> (terrain_id, x, y) 和邻接关系"""
        if seed:
            random.seed(seed)
        locations = {}
        # 简单生成网格地图
        for y in range(height):
            for x in range(width):
                # 随机地形
                terrain_id = random.choice(list(self.terrain_types.keys()))
                loc_id = f"loc_{x}_{y}"
                locations[loc_id] = {
                    'terrain': terrain_id,
                    'x': x * 100 + 50,  # 视觉坐标
                    'y': y * 100 + 50,
                    'connected': []
                }
        # 连接相邻格子
        for y in range(height):
            for x in range(width):
                loc_id = f"loc_{x}_{y}"
                neighbors = []
                if x > 0:
                    neighbors.append(f"loc_{x-1}_{y}")
                if x < width-1:
                    neighbors.append(f"loc_{x+1}_{y}")
                if y > 0:
                    neighbors.append(f"loc_{x}_{y-1}")
                if y < height-1:
                    neighbors.append(f"loc_{x}_{y+1}")
                locations[loc_id]['connected'] = neighbors
        # 添加起始地点（强制为平原）
        start_id = f"loc_0_0"
        locations[start_id]['terrain'] = 'plain'
        return locations