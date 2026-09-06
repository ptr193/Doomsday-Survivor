# -*- coding: utf-8 -*-

import random
import logging

class NPCSystem:
    def __init__(self, game):
        self.game = game
        self.npcs = {}
        self.factions = {}
        self.relationships = {}
        self.shop_inventories = {}
        self.initialized = False

    def initialize(self):
        try:
            self.create_factions()
            self.create_npcs()
            self.create_shop_inventories()
            self.initialize_relationships()
            self.initialized = True
            logging.info("NPC系统初始化完成")
        except Exception as e:
            logging.error(f"NPC系统初始化失败: {e}")
            raise

    def create_factions(self):
        self.factions = {
            'survivors': {'id': 'survivors', 'name': '幸存者联盟', 'description': '致力于重建文明的幸存者组织', 'alignment': 'good', 'base_reputation': 50, 'relationships': {'raiders': -100, 'tech_cult': 0, 'traders': 75}},
            'raiders': {'id': 'raiders', 'name': '掠夺者部落', 'description': '以掠夺和暴力为生的危险组织', 'alignment': 'evil', 'base_reputation': -50, 'relationships': {'survivors': -100, 'tech_cult': -50, 'traders': -75}},
            'tech_cult': {'id': 'tech_cult', 'name': '科技教会', 'description': '崇拜科技的神秘组织', 'alignment': 'neutral', 'base_reputation': 0, 'relationships': {'survivors': 0, 'raiders': -50, 'traders': 25}},
            'traders': {'id': 'traders', 'name': '商人行会', 'description': '专注于贸易的商业组织', 'alignment': 'neutral', 'base_reputation': 25, 'relationships': {'survivors': 75, 'raiders': -75, 'tech_cult': 25}}
        }

    def create_npcs(self):
        npcs_data = self.game.mod_manager.get_data('npcs', None) or {}
        if npcs_data:
            self.npcs = {}
            for nid, npc in npcs_data.items():
                data = dict(npc)
                data['id'] = data.get('id', nid)
                self.npcs[nid] = data
            logging.info(f"从JSON加载了{len(self.npcs)}个NPC")
            return
        self.npcs = {
            'old_farmer': {'id': 'old_farmer', 'name': '老农民张大爷', 'faction': 'survivors', 'location': 'abandoned_farm', 'type': 'quest_giver', 'description': '经验丰富的老农民，一直在努力恢复农业生产', 'dialogue': {'greeting': '年轻人，看来你也是个懂得土地价值的人。', 'farewell': '小心那些变异生物，它们最近很活跃。', 'topics': {'farming': '土地是我们的根本，没有粮食什么都谈不上。', 'survival': '我经历过最艰难的日子，但只要不放弃，总有希望。', 'threats': '晚上最好不要出门，有些东西在黑暗中游荡...'}}, 'services': ['quests', 'farming_tips'], 'quests': ['side_01'], 'shop': None, 'reputation_required': 0},
            'doctor_li': {'id': 'doctor_li', 'name': '李医生', 'faction': 'survivors', 'location': 'starting_area', 'type': 'healer', 'description': '前医院医生，现在为幸存者提供医疗服务', 'dialogue': {'greeting': '你好，需要医疗帮助吗？', 'farewell': '保持健康，这个世界需要每一个幸存者。', 'topics': {'medicine': '药品很稀缺，我们必须谨慎使用。', 'injuries': '我见过太多因为小伤口感染而失去的生命。', 'radiation': '辐射病的症状很隐蔽，要定期检查。'}}, 'services': ['healing', 'quests', 'medical_supplies'], 'quests': ['side_02'], 'shop': 'medical_shop', 'reputation_required': 10},
            'security_chief': {'id': 'security_chief', 'name': '王队长', 'faction': 'survivors', 'location': 'survivor_camp', 'type': 'guard', 'description': '前警察，负责营地的安全工作', 'dialogue': {'greeting': '保持警惕，这里并不安全。', 'farewell': '如果你看到任何异常，立即报告。', 'topics': {'security': '我们人手不足，每个人都必须参与防卫。', 'raiders': '那些掠夺者越来越猖狂了。', 'weapons': '好的武器能让你活得更久。'}}, 'services': ['quests', 'security_tips', 'weapon_training'], 'quests': ['side_03'], 'shop': None, 'reputation_required': 20},
            'master_crafter': {'id': 'master_crafter', 'name': '工匠大师', 'faction': 'survivors', 'location': 'trading_post', 'type': 'crafter', 'description': '技艺精湛的工匠，能制作各种物品', 'dialogue': {'greeting': '需要制作什么吗？我的手艺可是一流的。', 'farewell': '材料要好好保管，都是宝贵的资源。', 'topics': {'crafting': '好的工具能让工作事半功倍。', 'materials': '我认识每一种材料的特性。', 'repair': '修复比制作更需要技巧。'}}, 'services': ['crafting', 'quests', 'repair'], 'quests': ['craft_01'], 'shop': 'crafting_shop', 'reputation_required': 15},
            'cartographer': {'id': 'cartographer', 'name': '地图绘制师', 'faction': 'survivors', 'location': 'survivor_camp', 'type': 'explorer', 'description': '专注于绘制世界地图的探险家', 'dialogue': {'greeting': '你对这个世界了解多少？', 'farewell': '小心探索，安全第一。', 'topics': {'exploration': '每个角落都可能隐藏着秘密。', 'maps': '一张好地图能救你的命。', 'locations': '我记录了上百个重要地点。'}}, 'services': ['quests', 'map_info', 'location_tips'], 'quests': ['explore_01'], 'shop': None, 'reputation_required': 5},
            'wandering_merchant': {'id': 'wandering_merchant', 'name': '流浪商人卡尔', 'faction': 'traders', 'location': 'starting_area', 'wandering': True, 'type': 'merchant', 'description': '四处旅行的商人，商品种类丰富', 'dialogue': {'greeting': '来看看我的货物吧，都是好东西！', 'farewell': '下次见，希望你还活着。', 'topics': {'trade': '公平交易，童叟无欺。', 'prices': '价格随供求变化，你懂的。', 'rumors': '我听到一些有趣的消息...'}}, 'services': ['trade', 'information'], 'quests': [], 'shop': 'general_shop', 'reputation_required': 0},
            'weapon_dealer': {'id': 'weapon_dealer', 'name': '军火商文森特', 'faction': 'traders', 'location': 'trading_post', 'type': 'merchant', 'description': '专营武器和装备的商人', 'dialogue': {'greeting': '需要保护自己吗？我这里有好东西。', 'farewell': '记住，武器只是工具，人才是关键。', 'topics': {'weapons': '我这里的武器都是精品。', 'defense': '好的防具比武器更重要。', 'ammo': '没有弹药的枪还不如一根棍子。'}}, 'services': ['trade', 'weapon_info'], 'quests': [], 'shop': 'weapon_shop', 'reputation_required': 25},
            'mad_scientist': {'id': 'mad_scientist', 'name': '疯狂科学家', 'faction': 'tech_cult', 'location': 'research_lab', 'type': 'researcher', 'description': '行为古怪但知识渊博的科学家', 'dialogue': {'greeting': '啊！一个新的测试对象...我是说，访客！', 'farewell': '科学万岁！', 'topics': {'technology': '科技能解决所有问题，包括这个末日。', 'research': '我的研究即将突破！', 'radiation': '辐射不是诅咒，而是机遇！'}}, 'services': ['research', 'tech_items', 'radiation_treatment'], 'quests': [], 'shop': 'tech_shop', 'reputation_required': 30},
            'mysterious_stranger': {'id': 'mysterious_stranger', 'name': '神秘陌生人', 'faction': 'neutral', 'location': 'deep_forest', 'wandering': True, 'type': 'special', 'description': '身份不明的旅行者，似乎知道很多秘密', 'dialogue': {'greeting': '你不该来这里...但既然来了，也许能帮上忙。', 'farewell': '小心你信任的人，这个世界已经变了。', 'topics': {'secrets': '有些真相还是不知道为好。', 'prophecy': '星星在移动，平衡正在改变...', 'warning': '不要相信你看到的一切。'}}, 'services': ['information', 'special_quests'], 'quests': [], 'shop': None, 'reputation_required': 50},
            'hermit': {'id': 'hermit', 'name': '山中隐士', 'faction': 'neutral', 'location': 'mountain_path', 'type': 'teacher', 'description': '独自生活在山中的智者', 'dialogue': {'greeting': '很少有人能找到这里。', 'farewell': '愿自然之力保护你。', 'topics': {'nature': '大自然在自我修复，人类只是过客。', 'survival': '真正的生存技巧来自对自然的理解。', 'meditation': '内心的平静比任何武器都强大。'}}, 'services': ['training', 'survival_tips', 'meditation'], 'quests': [], 'shop': None, 'reputation_required': 40}
        }
        logging.info(f"创建了{len(self.npcs)}个NPC")

    def create_shop_inventories(self):
        self.shop_inventories = {
            'medical_shop': {'items': {'medicine': {'price': 15, 'stock': 10}, 'bandage': {'price': 8, 'stock': 20}, 'antidote': {'price': 25, 'stock': 5}, 'first_aid_kit': {'price': 50, 'stock': 3}, 'radiation_pills': {'price': 30, 'stock': 8}}, 'buys': ['rare_herbs', 'medicine', 'antidote'], 'price_modifier': 1.0},
            'general_shop': {'items': {'food': {'price': 5, 'stock': 20}, 'water': {'price': 3, 'stock': 25}, 'materials': {'price': 2, 'stock': 50}, 'cloth': {'price': 4, 'stock': 15}, 'wood': {'price': 3, 'stock': 30}, 'seeds': {'price': 2, 'stock': 40}}, 'buys': ['food', 'water', 'materials', 'cloth', 'wood'], 'price_modifier': 1.2},
            'weapon_shop': {'items': {'knife': {'price': 20, 'stock': 5}, 'baseball_bat': {'price': 15, 'stock': 8}, 'pistol': {'price': 80, 'stock': 3}, 'shotgun': {'price': 120, 'stock': 2}, 'bow': {'price': 35, 'stock': 4}, 'arrow': {'price': 2, 'stock': 50}, 'cloth_armor': {'price': 25, 'stock': 6}, 'leather_armor': {'price': 45, 'stock': 4}}, 'buys': ['knife', 'baseball_bat', 'pistol', 'cloth_armor', 'arrow'], 'price_modifier': 1.5},
            'crafting_shop': {'items': {'metal': {'price': 6, 'stock': 20}, 'electronic': {'price': 12, 'stock': 10}, 'advanced_alloy': {'price': 25, 'stock': 5}, 'wooden_hoe': {'price': 15, 'stock': 8}, 'iron_hoe': {'price': 30, 'stock': 5}, 'fishing_rod': {'price': 20, 'stock': 6}, 'trap': {'price': 25, 'stock': 4}}, 'buys': ['metal', 'electronic', 'advanced_alloy', 'rare_minerals'], 'price_modifier': 1.3},
            'tech_shop': {'items': {'electronic': {'price': 15, 'stock': 15}, 'advanced_alloy': {'price': 35, 'stock': 8}, 'research_data': {'price': 20, 'stock': 12}, 'energy_drink': {'price': 18, 'stock': 10}, 'radiation_pills': {'price': 25, 'stock': 10}, 'battery': {'price': 10, 'stock': 20}, 'solar_panel': {'price': 100, 'stock': 2}}, 'buys': ['electronic', 'advanced_alloy', 'research_data', 'ancient_artifact'], 'price_modifier': 2.0}
        }

    def initialize_relationships(self):
        self.relationships = {'survivors': 50, 'raiders': -50, 'tech_cult': 0, 'traders': 25}

    def load_data(self, save_data):
        try:
            self.relationships = save_data.get('relationships', self.relationships)
            npcs_data = save_data.get('npcs', {})
            for npc_id, npc_data in npcs_data.items():
                if npc_id in self.npcs:
                    self.npcs[npc_id]['location'] = npc_data.get('location', self.npcs[npc_id]['location'])
                    self.npcs[npc_id]['last_interaction'] = npc_data.get('last_interaction')
            shops_data = save_data.get('shops', {})
            for shop_id, shop_data in shops_data.items():
                if shop_id in self.shop_inventories:
                    for item_id, item_info in shop_data.get('items', {}).items():
                        if item_id in self.shop_inventories[shop_id]['items']:
                            self.shop_inventories[shop_id]['items'][item_id]['stock'] = item_info.get('stock')
            self.initialized = True
            logging.info("NPC系统数据加载完成")
        except Exception as e:
            logging.error(f"加载NPC系统数据失败: {e}")
            raise

    def get_save_data(self):
        npcs_data = {}
        for npc_id, npc in self.npcs.items():
            npcs_data[npc_id] = {'location': npc['location'], 'last_interaction': npc.get('last_interaction')}
        shops_data = {}
        for shop_id, shop in self.shop_inventories.items():
            shops_data[shop_id] = {'items': {iid: {'stock': info['stock']} for iid, info in shop['items'].items()}}
        return {'relationships': self.relationships, 'npcs': npcs_data, 'shops': shops_data}

    def get_npc(self, npc_id):
        return self.npcs.get(npc_id)

    def get_npcs_at_location(self, location_id):
        result = []
        for npc_id, npc in self.npcs.items():
            if npc.get('location') == location_id:
                result.append(npc)
        return result

    def get_dialogue(self, npc_id, topic='greeting'):
        npc = self.get_npc(npc_id)
        if not npc:
            return "......"
        if topic in npc['dialogue']:
            return npc['dialogue'][topic]
        elif topic in npc['dialogue'].get('topics', {}):
            return npc['dialogue']['topics'][topic]
        return "我现在没什么可说的。"

    def get_services(self, npc_id):
        npc = self.get_npc(npc_id)
        return npc.get('services', []) if npc else []

    def can_access_service(self, npc_id, service):
        npc = self.get_npc(npc_id)
        if not npc:
            return False
        rep_needed = npc.get('reputation_required', 0)
        faction = npc.get('faction')
        if faction and self.relationships.get(faction, 0) < rep_needed:
            return False
        return service in npc.get('services', [])

    def get_shop_inventory(self, shop_id):
        return self.shop_inventories.get(shop_id)

    def buy_item(self, shop_id, item_id, quantity=1):
        shop = self.get_shop_inventory(shop_id)
        if not shop:
            return {'success': False, 'message': '商店不存在'}
        if item_id not in shop['items']:
            return {'success': False, 'message': '商品不存在'}
        item_info = shop['items'][item_id]
        if item_info['stock'] < quantity:
            return {'success': False, 'message': '库存不足'}
        total_price = item_info['price'] * quantity
        if not self.game.player.can_carry(item_id, quantity):
            return {'success': False, 'message': '负重已满，无法购买'}
        if not self.game.player.spend_money(total_price):
            return {'success': False, 'message': f'金钱不足，需要{total_price}'}
        item_info['stock'] -= quantity
        self.game.player.add_item(item_id, quantity, force=True)
        self.game.quests.update_quest_progress('trade_completed', shop_id=shop_id)
        logging.info(f"购买物品: {item_id} x{quantity}, 价格: {total_price}")
        return {'success': True, 'message': f"成功购买{quantity}个{self.game.items.get_item_name(item_id)}，花费{total_price}", 'item_id': item_id, 'quantity': quantity, 'total_price': total_price}

    def sell_item(self, shop_id, item_id, quantity=1):
        shop = self.get_shop_inventory(shop_id)
        if not shop:
            return {'success': False, 'message': '商店不存在'}
        if item_id not in shop.get('buys', []):
            return {'success': False, 'message': '商店不收这种物品'}
        if not self.game.player.has_item(item_id, quantity):
            return {'success': False, 'message': '物品数量不足'}
        base_price = 0
        for shop_item_id, shop_item in shop['items'].items():
            if shop_item_id == item_id:
                base_price = shop_item['price']
                break
        if base_price == 0:
            item_data = self.game.items.get_item_data(item_id)
            base_price = item_data.get('value', 1) if item_data else 1
        sell_price = int(base_price * 0.6 * quantity)
        self.game.player.remove_item(item_id, quantity)
        self.game.player.add_money(sell_price)
        logging.info(f"出售物品: {item_id} x{quantity}, 价格: {sell_price}")
        return {'success': True, 'message': f"成功出售{quantity}个{self.game.items.get_item_name(item_id)}，获得{sell_price}", 'item_id': item_id, 'quantity': quantity, 'total_price': sell_price}

    def change_relationship(self, faction, amount):
        if faction not in self.relationships:
            self.relationships[faction] = 0
        old = self.relationships[faction]
        new = max(-100, min(100, old + amount))
        self.relationships[faction] = new
        faction_name = self.factions.get(faction, {}).get('name', faction)
        self.game.add_game_log(f"与{faction_name}的关系{'增加' if amount>0 else '减少'}了{abs(amount)}点")
        self.game.quests.update_quest_progress('reputation_changed', faction=faction, new_reputation=new)
        return new

    def get_relationship_level(self, faction):
        rep = self.relationships.get(faction, 0)
        if rep >= 80: return "崇敬"
        if rep >= 60: return "尊敬"
        if rep >= 40: return "友好"
        if rep >= 20: return "中立"
        if rep >= 0: return "冷淡"
        if rep >= -20: return "敌对"
        if rep >= -40: return "仇恨"
        return "死敌"

    def get_player_relationships(self):
        res = {}
        for fid, faction in self.factions.items():
            res[fid] = {'faction': faction, 'reputation': self.relationships.get(fid, faction['base_reputation']), 'level': self.get_relationship_level(fid)}
        return res

    def get_faction_info(self, faction_id):
        return self.factions.get(faction_id)

    def get_all_factions(self):
        return list(self.factions.values())

    def add_encountered_npc(self, npc_data):
        npc_id = npc_data['id']
        if npc_id not in self.npcs:
            self.npcs[npc_id] = npc_data
            self.game.player.stats['npcs_met'] += 1
            logging.info(f"添加新NPC: {npc_data['name']}")

    def record_interaction(self, npc_id):
        if npc_id in self.npcs:
            self.npcs[npc_id]['last_interaction'] = self.game.game_time.isoformat()

    def restock_shops(self):
        for shop_id, shop in self.shop_inventories.items():
            for item_id, item_info in shop['items'].items():
                max_stock = item_info.get('max_stock', item_info['stock'] * 2)
                restock_amount = random.randint(max_stock // 2, max_stock)
                item_info['stock'] = min(item_info['stock'] + restock_amount, max_stock)
            shop['last_restock'] = self.game.game_time.isoformat()
        logging.info("商店库存已补充")

    def move_wandering_npcs(self):
        for npc_id, npc in self.npcs.items():
            if npc.get('location') == 'random' or npc.get('wandering'):
                npc['wandering'] = True
                locations = list(self.game.world.locations.keys())
                if not locations:
                    continue
                new_location = random.choice(locations)
                npc['location'] = new_location
                logging.info(f"NPC {npc['name']} 移动到了 {new_location}")