# -*- coding: utf-8 -*-
import os
import logging

class StoryReader:
    def __init__(self, game):
        self.game = game
        self.stories = {}  # story_id -> {'title':..., 'content':...}
        self.unlocked_stories = set()
        self.initialized = False

    def initialize(self):
        """从MOD管理器加载故事"""
        self.reload_stories()
        default_stories = ["core_whisper", "river_pulse", "word_gatherer", "core_echo"]
        for story_id in default_stories:
            if story_id in self.stories:
               self.unlocked_stories.add(story_id)
               logging.info(f"默认解锁故事: {story_id}")
        
        self.initialized = True
        logging.info(f"故事阅读器初始化完成，已解锁 {len(self.unlocked_stories)} 个故事")

    def load_data(self, save_data):
        self.reload_stories()
        saved = save_data.get('unlocked_stories', []) if save_data else []
        self.unlocked_stories = set(saved) if saved else set(self.unlocked_stories)
        self.initialized = True

    def get_save_data(self):
        return {'unlocked_stories': list(self.unlocked_stories)}

    def reload_stories(self):
        """从 ModManager 重新加载故事数据"""
        self.stories = self.game.mod_manager.get_data('stories', None) or {}

    def unlock_story(self, story_id):
        if story_id in self.stories and story_id not in self.unlocked_stories:
            self.unlocked_stories.add(story_id)
            return True
        return False

    def get_unlock_rules(self):
        return {
            'guide_01': {'farmlands_min': 1},
            'location_01': {'locations': ['old_road', 'trading_post', 'survivor_camp']},
            'location_02': {'locations': ['ancient_ruins']},
            'location_03': {'locations': ['abandoned_farm', 'farmhouse', 'south_plains']},
            'character_01': {'locations': ['survivor_camp']},
            'character_02': {'locations': ['research_lab']},
            'origin_01': {'locations': ['research_lab']},
            'origin_02': {'locations': ['trading_post', 'old_road']},
            'origin_03': {'day_count_min': 5},
            'mystery_01': {'locations': ['deep_forest', 'north_forest']},
            'red_dawn_01': {'quests_completed': ['epic_01']},
            'epic_whisper': {'quests_completed': ['epic_01'], 'day_count_min': 8},
        }

    def check_unlock_conditions(self, context):
        newly = []
        discovered = set(context.get('discovered_locations') or [])
        farmlands = context.get('farmlands') or []
        day_count = context.get('day_count', 1)
        current = context.get('location')
        quests_completed = set(context.get('quests_completed') or [])
        for story_id, rule in self.get_unlock_rules().items():
            if story_id not in self.stories or story_id in self.unlocked_stories:
                continue
            ok = True
            if 'locations' in rule:
                locs = set(rule['locations'])
                ok = current in locs or bool(locs & discovered)
            if ok and 'farmlands_min' in rule:
                ok = len(farmlands) >= rule['farmlands_min']
            if ok and 'day_count_min' in rule:
                ok = day_count >= rule['day_count_min']
            if ok and 'quests_completed' in rule:
                needed = set(rule['quests_completed'])
                ok = needed.issubset(quests_completed)
            if ok and self.unlock_story(story_id):
                story = self.stories.get(story_id) or {}
                newly.append(story.get('title', story_id))
        return newly

    def get_story(self, story_id):
        return self.stories.get(story_id)

    def get_unlocked_stories(self):
        self.reload_stories()
        return [self.stories[sid] for sid in self.unlocked_stories if sid in self.stories]

    def get_all_stories(self):
        return list(self.stories.values())
    
    def get_background_story(self):
        """返回游戏背景故事"""
        return """
《末日生存者》游戏背景

2035年3月，政府启动了代号「红色黎明」的地心能量开采计划，试图用地壳深处的脉动解决全球能源危机。项目首席科学家张明博士多次警告能量读数已越过安全阈值，上级仍下令继续。3月21日，反应堆紧急制动全部失效。天空变成血色，城市在扭曲中崩塌，辐射与变异席卷大地。

灾难后第十三年，幸存者们在废墟中结成松散营地。幸存者联盟试图重建秩序，掠夺者部落以暴力换取物资，科技教会仍在追寻地核的「语言」，商人联盟则在废路上维持最后的贸易。农田、电台、渔港和研究所成为稀缺的据点。

你是新上岸的幸存者。你需要寻找食物、水和材料，建造庇护所，制作工具，并与变异生物、掠夺者以及更古老的东西作斗争。主线将带你从求生走向揭开红色黎明的真相；史诗任务则会把你推向传说级的战场。

每一天都是新的挑战。记下你的昵称，让废土记住你走过的路。
"""

    def get_codex_content(self):
    	"""返回图鉴内容"""
    	return """
【物品图鉴】

食物类：
- 食物：基本的食物，可以充饥
- 新鲜食物：新鲜的食物，营养价值更高
- 罐头食品：密封保存的罐头，保质期长
- 军用口粮：高能量的军用口粮
- 能量棒：快速补充能量的食品
- 苹果：新鲜水果，补充维生素
- 面包：主食，提供能量
- 肉干：高蛋白食物，耐储存
- 蘑菇汤：热汤，温暖身心

饮品类：
- 水：干净的水源
- 纯净水：经过净化的纯净水
- 能量饮料：提神醒脑的功能饮料
- 草药茶：用草药泡制的茶，有治疗效果
- 咖啡：热咖啡，提神效果明显
- 浆果汁：酸甜解渴

材料类：
- 材料：基础制作材料
- 木材：可用于建造和燃料
- 金属：金属材料，用于制作工具和武器
- 布料：纺织品，用于制作衣物
- 电子元件：电子设备零件
- 高级合金：高性能合金材料
- 石头：基础建筑材料
- 塑料：塑料材料，用途广泛
- 皮革：动物皮毛加工而成
- 木炭：燃料和过滤材料
- 玻璃碎片：锋利的玻璃碎片
- 橡胶：弹性材料
- 绳索：实用工具

医疗类：
- 药品：基础医疗用品
- 绷带：用于止血和包扎伤口
- 解毒剂：解除中毒状态
- 抗抑郁药：缓解精神压力
- 急救包：完整的急救用品
- 抗辐射药：减少辐射伤害
- 草药补剂：增强体质
- 消毒剂：消毒伤口
- 止痛药：缓解疼痛
- 抗生素：治疗感染

武器类：
- 小刀：基础近战武器
- 棒球棍：钝器武器，击打效果好
- 手枪：基础枪械武器
- 霰弹枪：近距离高伤害武器
- 突击步枪：全自动步枪，火力强大
- 弓：远程武器
- 猎刀：锋利的猎刀，适合剥皮和战斗

防具类：
- 布甲：基础防护服装
- 皮甲：皮革制成的护甲
- 金属护甲：金属板制成的重甲
- 战术背心：军用战术装备
- 布帽：基础头部防护
- 金属头盔：金属制成的头盔
- 皮背心：轻便防护

背包类：
- 小背包：增加携带容量
- 登山包：大容量背包
- 军用背包：专业军用背包

工具类：
- 鱼竿：用于钓鱼
- 净水器：净化脏水
- 雨水收集器：收集雨水
- 渔网：捕鱼工具
- 捕兽夹：捕获小动物
- 木锄：基础农具
- 铁锄：铁制农具
- 浇水壶：浇水工具

特殊物品：
- 地图碎片：世界地图的一部分
- 研究资料：科学研究的记录
- 古代文物：神秘的古代物品
- 稀有草药：具有特殊药效的植物
- 稀有矿物：稀有的矿物晶体
- 电池：存储电能
- 太阳能板：发电设备
"""