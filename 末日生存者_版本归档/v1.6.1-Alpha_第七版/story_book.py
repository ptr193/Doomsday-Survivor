# -*- coding: utf-8 -*-

import logging

class StoryBook:
    def __init__(self, game):
        self.game = game
        self.stories = {}
        self.unlocked_stories = set()
        self.initialized = False

    def initialize(self):
        try:
            self.create_stories()
            self.unlock_initial_stories()
            self.initialized = True
            logging.info("故事书系统初始化完成")
        except Exception as e:
            logging.error(f"故事书系统初始化失败: {e}")
            raise

    def create_stories(self):
        """创建所有故事内容"""
        # === 灾难起源篇 ===
        self.stories['origin_01'] = {
            'id': 'origin_01', 'title': '红色黎明计划', 'author': '张明博士 - 项目首席科学家',
            'category': 'origin', 'unlock_condition': 'start_game',
            'content': """
当政府找到我时，他们说这是为了应对全球能源危机。"红色黎明"——一个利用地心能量的宏伟计划。

我警告过他们，地球的脉动不是人类能够驾驭的。地核能量就像一头沉睡的巨兽，我们却在试图唤醒它。

但没人听一个科学家的"迷信"。他们说这是人类的未来，是科技进步的必然。

在实验室的最后一夜，我看着那些闪烁的仪器，心中充满不安。能量读数已经超出了安全阈值，但上级的命令是继续。

我记得最后看到的是监控屏幕上的一片血红，然后是永无止境的警报声...

如果当时有人听劝，也许这一切都不会发生。
"""
        }
        self.stories['origin_02'] = {
            'id': 'origin_02', 'title': '最后的广播', 'author': '李静 - 央视新闻主播',
            'category': 'origin', 'unlock_condition': 'survive_3_days',
            'content': """
...这里是中央电视台紧急广播。请所有市民立即前往指定避难所...

重复，这不是演习。地壳活动异常...天空为什么是红色的？

等等，那是什么...（剧烈的震动声）

（背景传来尖叫声和玻璃破碎声）

我...我看到窗外...建筑物在...在融化？不，是在扭曲...

（巨大的爆炸声）

天啊...（哭泣声）这个世界...完了...

（信号中断）
"""
        }
        self.stories['origin_03'] = {
            'id': 'origin_03', 'title': '逃亡日记 - 第一页', 'author': '王小明 - 小学生',
            'category': 'origin', 'unlock_condition': 'find_diary',
            'content': """
2025年3月15日

今天爸爸妈妈没叫我起床，外面一直在打雷。窗户变成了红色，李老师说过红色是警告色。

我饿了，冰箱里的布丁还在。电视没有信号，手机也是。

听到外面有奇怪的声音，像很多人在哭。我不敢出去。

妈妈说过，遇到危险要躲起来。我躲在床底下，这里很安全。

希望爸爸妈妈快点回来。我想他们了。
"""
        }

        # === 时间线故事 ===
        self.stories['timeline_01'] = {
            'id': 'timeline_01', 'title': '混乱七日', 'author': '匿名幸存者',
            'category': 'timeline', 'unlock_condition': 'survive_7_days',
            'content': """
灾难后第一周：

城市在哭泣。高速公路变成了停车场，永远塞满了想要逃离的车辆。

超市被洗劫一空，人们在为最后一瓶水争斗。法律和秩序成了奢侈品。

我躲在图书馆里，书页的香味让我想起文明的味道。但外面的枪声提醒我，那个世界已经结束了。

第三天，我看到了第一个变异生物——一只比狗还大的老鼠。它用血红的眼睛盯着我，然后消失在废墟中。

第七天，我遇到了其他幸存者。我们相视无言，彼此眼中只有恐惧和警惕。

这就是新世界的开始。
"""
        }
        self.stories['timeline_02'] = {
            'id': 'timeline_02', 'title': '新秩序', 'author': '前消防员 - 老张',
            'category': 'timeline', 'unlock_condition': 'survive_30_days',
            'content': """
灾难后第一个月：

掠夺者开始组织起来，他们自称"血牙帮"。幸存者在老消防站建立了第一个避难所。

张医生用图书馆的医学书建起了诊所。我们开始学习新的规则：信任需要证明，善良需要代价。

食物配给制开始了。每个人都要工作，没有人可以坐享其成。

孩子们在废墟中学习识字，课本是幸存的书籍。我们必须把文明的火种传下去。

夜晚的守夜成了最重要的任务。变异生物的嚎叫声越来越近...

但我们还活着，这就是希望。
"""
        }
        self.stories['timeline_03'] = {
            'id': 'timeline_03', 'title': '希望之种', 'author': '农夫 - 李大爷',
            'category': 'timeline', 'unlock_condition': 'harvest_first_crop',
            'content': """
灾难后第一年：

在废墟中，我们发现了第一株绿芽。老农民李大爷说这是上天的启示。

我们开始清理学校的操场，用找到的种子尝试种植。土壤被辐射污染了，但有些植物顽强地活了下来。

第一次收获很少，只有几颗土豆和萝卜。但那晚，我们举行了灾难后的第一次庆祝。

孩子们第一次尝到了新鲜蔬菜的味道，他们的笑容让我想起了从前。

农业小组成立了，我们收集所有能找到的种子。图书馆的农业书籍成了宝典。

虽然收成很少，但这是希望的味道。土地没有放弃我们，我们也不能放弃土地。
"""
        }
        self.stories['timeline_04'] = {
            'id': 'timeline_04', 'title': '传承之火', 'author': '教师 - 王老师',
            'category': 'timeline', 'unlock_condition': 'survive_1_year',
            'content': """
灾难后第五年：

孩子们在废墟中长大，他们不知道手机是什么，但知道如何辨别可食用的蘑菇。

我们在旧课本上教他们识字，在断壁残垣间讲述过去的世界。文明的火种必须传承下去。

老人们在夜晚围着篝火，讲述灾难前的故事。年轻人则规划着如何重建。

我们建立了简易的学校，用木炭当粉笔，石板当练习本。知识成了最珍贵的遗产。

有些孩子展现了特殊的天赋——对机械的理解、对植物的敏感、甚至是对危险的直觉。

他们是新世界的希望，是文明复兴的种子。
"""
        }

        # === 地点故事 ===
        self.stories['location_01'] = {
            'id': 'location_01', 'title': '北京地铁迷城', 'author': '地铁幸存者团体',
            'category': 'location', 'unlock_condition': 'explore_subway',
            'content': """
地铁变成了地下城市。1号线是主要居住区，2号线是交易市场，10号线...最好不要去。

我们在隧道里建立了社区，用废弃的车厢当房屋。虽然黑暗，但相对安全。

发电机是从站台拆下来的，用电很节约。水源来自深层地下水，需要严格净化。

有人说在隧道深处看到了发光的眼睛，也有人说找到了通往旧政府避难所的密道。

夜晚能听到奇怪的敲击声，像是某种密码。我们不敢深究。

这里是我们躲避地上危险的家园，也是充满未知的迷宫。
"""
        }
        self.stories['location_02'] = {
            'id': 'location_02', 'title': '上海金融中心废墟', 'author': '高空观察者',
            'category': 'location', 'unlock_condition': 'explore_city_center',
            'content': """
陆家嘴的高楼大多已经倒塌，但金茂大厦奇迹般屹立着。

顶层的观景台现在是瞭望哨，我们能看到黄浦江的水变成了诡异的绿色。

东方明珠塔倾斜了，像在向逝去的时代鞠躬。

金融中心的金库被洗劫一空，但有些办公室还保留着灾难当天的样子——咖啡杯、打开的电脑、散落的文件。

夜晚，废墟中会亮起奇怪的灯光，不是电力，而是某种生物发光。

偶尔，江面会泛起不自然的波纹，好像有什么巨大的东西在水下游弋...
"""
        }
        self.stories['location_03'] = {
            'id': 'location_03', 'title': '成都平原的绿洲', 'author': '农业社区记录',
            'category': 'location', 'unlock_condition': 'discover_farmland',
            'content': """
都江堰依然在发挥作用，李冰父子的智慧超越了时间。

我们在这里重建了农业社区，用找到的种子恢复耕种。土壤的辐射水平较低，作物生长良好。

古老的灌溉系统需要维护，但我们有水利工程师的后代。

平原相对安全，变异生物较少。但我们仍然需要警惕掠夺者的袭击。

夜晚的平原并不安全，有什么东西在稻田里游荡——不是动物，也不是人类。

老人们说，这是土地的记忆在徘徊，是古老灵魂的守护。
"""
        }
        self.stories['location_04'] = {
            'id': 'location_04', 'title': '青藏高原哨站', 'author': '高原守望者',
            'category': 'location', 'unlock_condition': 'reach_high_altitude',
            'content': """
海拔保护了我们，辐射云层在脚下翻涌。

这里是最后的净土，但也最接近星空。夜晚的星星异常明亮，有时太过明亮了...

我们在古老的寺庙里建立了基地，僧侣的智慧帮助我们适应高原生活。

空气稀薄，但纯净。水源来自冰川，需要小心融化。

守望者们记录着天空的变化——星座在移动，月亮出现了新的纹理。

有人说在雪山上看到了发光的门户，有人说听到了来自星星的低语。

我们既是幸存者，也是观察者，记录着这个变化中的世界。
"""
        }

        # === 人物故事 ===
        self.stories['character_01'] = {
            'id': 'character_01', 'title': '老兵的独白', 'author': '王队长',
            'category': 'character', 'unlock_condition': 'meet_security_chief',
            'content': """
我参加过三次维和行动，见过战争的各种面孔。但这次不同，敌人看不见摸不着。

大地本身在反抗我们。红色黎明...多么讽刺的名字，那确实是我们的最后一个黎明。

现在，我保护着这个小小的避难所，这是我最后的阵地。

孩子们在废墟中玩耍，他们不知道什么是和平年代。我的职责是让他们活下去，直到...直到什么？

也许直到人类学会谦卑，学会与自然和谐相处。

每晚巡逻时，我都会想起那些牺牲的战友。现在我们每个人都在前线，没有后方。
"""
        }
        self.stories['character_02'] = {
            'id': 'character_02', 'title': '科学家的忏悔', 'author': '张明博士',
            'category': 'character', 'unlock_condition': 'find_research_data',
            'content': """
我们以为自己能驾驭自然，像驯服野马一样控制地球的能量。

现在我明白了，我们只是孩子，在玩着不该碰的玩具。

实验室的最后时刻永远烙印在我的记忆中——仪器过载的尖啸、同事的惨叫、还有那片吞噬一切的红光。

我活下来了，但这是诅咒而不是祝福。每一天，我都在为我的傲慢付出代价。

如果当时我能更坚决地反对，如果我能说服他们...

但现在说这些都没用了。我只能用余生来弥补，帮助幸存者理解这个新世界。

科学应该是服务生命，而不是毁灭它。
"""
        }
        self.stories['character_03'] = {
            'id': 'character_03', 'title': '教师的最后一课', 'author': '王老师',
            'category': 'character', 'unlock_condition': 'teach_skill',
            'content': """
孩子们，拿出你们的石板。今天我们要讲的是"希望"。

在这个破碎的世界里，希望不是等待救援，而是明天太阳会照常升起，种子会发芽，人类会继续前行。

记住灾难前的世界，但不要沉溺于过去。我们要建设新的未来。

知识是我们最强大的武器。数学能计算配给，物理能建造庇护所，生物能辨别食物。

但最重要的是品德——互助、勇敢、诚实。这些品质比任何技术都珍贵。

我的最后一课是：永远不要放弃学习，永远不要停止希望。
"""
        }

        # === 神秘事件 ===
        self.stories['mystery_01'] = {
            'id': 'mystery_01', 'title': '夜光森林的歌声', 'author': '探险队报告',
            'category': 'mystery', 'unlock_condition': 'explore_forest_at_night',
            'content': """
在郊外的辐射区内，树木发出了诡异的绿光。

夜晚，那里会传来歌声，既不是人类也不是已知动物发出的。旋律古老而悲伤，像是某种失传的语言。

去过的人都说感到平静，但回来后头发开始脱落，皮肤出现荧光斑点。

有些人声称在光芒中看到了逝去的亲人，有人说听到了地球的心跳。

科学小组无法解释这种现象。辐射读数正常，但生物检测显示异常能量波动。

森林在变化，在生长，在用我们无法理解的方式沟通。

这是诅咒，还是祝福？也许两者都是。
"""
        }
        self.stories['mystery_02'] = {
            'id': 'mystery_02', 'title': '时间错位区', 'author': '物理学家笔记',
            'category': 'mystery', 'unlock_condition': 'discover_anomaly',
            'content': """
城市中心的广场，有时会出现过去的影像：孩子们在玩耍，情侣在散步，小贩在叫卖。

这些幻影如此真实，你能听到他们的笑声，闻到食物的香味。

但触摸这些幻影会感到刺骨的寒冷。试图互动只会让影像消散。

物理学家认为这是时空裂缝，是灾难造成的创伤在重播过去的记忆。

有些人沉迷于这些幻影，整天守在广场，希望能看到逝去的亲人。

但幻影也在变化——最近开始出现我们没经历过的场景，像是来自未来...

时间本身似乎在这个区域变得不稳定。
"""
        }
        self.stories['mystery_03'] = {
            'id': 'mystery_03', 'title': '地下深处的鼓声', 'author': '隧道勘探记录',
            'category': 'mystery', 'unlock_condition': 'explore_deep_tunnel',
            'content': """
在地铁最深的隧道里，能听到有节奏的震动，像巨大的心跳。

工程师说这是地壳运动，但为什么每次鼓声后，辐射值都会异常波动？

勘探队带着防护装备深入，但没有人回来。只传回断断续续的无线电信息：

"...不是机械...是活着的...地球在呼吸..."

后来，隧道被封锁了。但鼓声越来越响，越来越近。

有些夜晚，整个地铁站都能感觉到震动，像是有什么巨大的东西在下面移动。

我们在监视，在记录，在祈祷。希望那只是地质活动，而不是...别的什么。
"""
        }

        # === 生存指南 ===
        self.stories['guide_01'] = {
            'id': 'guide_01', 'title': '李大爷的种地心得', 'author': '老农民李大爷',
            'category': 'guide', 'unlock_condition': 'learn_farming',
            'content': """
末世种地三要素：好土、好种、好心态。

辐射土要先用艾草熏，种子要选饱满的，人要有耐心。

记住，地不会骗人，你付出多少，它就还你多少。

春季种土豆萝卜，夏季种玉米瓜果，秋季收成储备，冬季休养生息。

雨水要收集，肥料要自制。动物粪便和植物残渣都是宝。

害虫用手捉，杂草及时除。化学农药不能用，会污染土壤。

最重要的是观察——看云识天气，看叶知健康，看地懂肥瘦。

土地是我们的母亲，要用心对待。
"""
        }
        self.stories['guide_02'] = {
            'id': 'guide_02', 'title': '张医生的末世医疗笔记', 'author': '张医生',
            'category': 'guide', 'unlock_condition': 'learn_healing',
            'content': """
没有抗生素？试试大蒜汁。骨折了？旧杂志和胶带能做夹板。

清洁比消毒更重要。沸水是最好的杀菌剂。

辐射病要早发现早治疗。恶心、脱发、疲劳都是警告信号。

药用植物要认识——金银花消炎，艾草驱虫，车前草止血。

心理卫生同样重要。谈话、音乐、写作都能缓解压力。

记住，心死了，药石无医。保持希望是最好的良药。

建立医疗档案，记录每个人的健康状况。预防胜于治疗。

在这个世界，医生不仅是治疗者，更是希望的守护者。
"""
        }
        self.stories['guide_03'] = {
            'id': 'guide_03', 'title': '王师傅的修理哲学', 'author': '工匠王师傅',
            'category': 'guide', 'unlock_condition': 'learn_crafting',
            'content': """
东西坏了不要扔，修修补补又三年。

收音机能改造成辐射探测器，自行车能发电，塑料瓶能做成过滤器。

在这个世界，创造力比黄金珍贵。

了解材料特性——金属导电，塑料绝缘，木材保温。

工具要保养，上油防锈，磨刀不误砍柴工。

安全第一。用电要小心，高空作业要系绳，化学物品要标识。

最重要的是耐心。急不得，慌不得，一步步来。

每个修复的物品都是对旧世界的纪念，对新世界的贡献。
"""
        }

        # === 游戏资料 ===
        self.stories['codex_background'] = {
            'id': 'codex_background', 'title': '背景故事', 'author': '游戏制作组',
            'category': 'codex', 'unlock_condition': 'start_game',
            'content': self.get_background_story()
        }
        self.stories['codex_items'] = {
            'id': 'codex_items', 'title': '物品图鉴', 'author': '游戏制作组',
            'category': 'codex', 'unlock_condition': 'start_game',
            'content': self.get_codex_content()
        }
        self.stories['codex_creatures'] = {
            'id': 'codex_creatures', 'title': '生物图鉴', 'author': '游戏制作组',
            'category': 'codex', 'unlock_condition': 'start_game',
            'content': """
生物图鉴：

普通敌人：
- 变异鼠：受到辐射变异的老鼠，攻击性很强
- 辐射蟑螂：巨大的变异蟑螂，外壳坚硬
- 变异狼：凶猛的变异狼，擅长群体作战
- 僵尸：行动缓慢但生命力顽强的僵尸
- 巨型蜘蛛：毒性强烈的巨型蜘蛛，行动敏捷

精英敌人：
- 变异熊：巨大的变异熊，力量惊人
- 掠夺者精英：经验丰富的掠夺者战士，装备精良
- 辐射蝎子：致命的辐射蝎子，尾刺含有剧毒

BOSS敌人：
- 变异巨兽：传说中的变异巨兽，拥有毁灭性的力量
- 掠夺者指挥官：掠夺者组织的首领，战术大师

特殊敌人：
- 幽灵士兵：神秘的幽灵般存在，似乎来自另一个维度
"""
        }

        logging.info(f"创建了{len(self.stories)}个故事")

    def unlock_initial_stories(self):
        """解锁初始故事"""
        self.unlocked_stories.add('origin_01')
        self.unlocked_stories.add('guide_01')
        self.unlocked_stories.add('guide_02')
        self.unlocked_stories.add('guide_03')
        self.unlocked_stories.add('codex_background')
        self.unlocked_stories.add('codex_items')
        self.unlocked_stories.add('codex_creatures')

    def load_data(self, save_data):
        """加载故事书数据"""
        try:
            self.unlocked_stories = set(save_data.get('unlocked_stories', []))
            self.initialized = True
            logging.info("故事书数据加载完成")
        except Exception as e:
            logging.error(f"加载故事书数据失败: {e}")
            raise

    def get_save_data(self):
        """获取保存数据"""
        return {'unlocked_stories': list(self.unlocked_stories)}

    def unlock_story(self, story_id):
        """解锁故事"""
        if story_id in self.stories and story_id not in self.unlocked_stories:
            self.unlocked_stories.add(story_id)
            logging.info(f"解锁故事: {self.stories[story_id]['title']}")
            return True
        return False

    def check_unlock_conditions(self, condition):
        """检查解锁条件（供外部调用）"""
        unlocked = []
        for sid, story in self.stories.items():
            if sid not in self.unlocked_stories and story['unlock_condition'] == condition:
                if self.unlock_story(sid):
                    unlocked.append(story)
        return unlocked

    def get_story(self, story_id):
        """获取故事内容"""
        return self.stories.get(story_id)

    def get_unlocked_stories(self):
        """获取已解锁的故事"""
        return [self.stories[sid] for sid in self.unlocked_stories if sid in self.stories]

    def get_stories_by_category(self, category):
        """按分类获取故事"""
        return [s for s in self.get_unlocked_stories() if s['category'] == category]

    def get_all_categories(self):
        """获取所有分类"""
        return sorted(set(s['category'] for s in self.stories.values()))

    def get_background_story(self):
        """获取游戏背景故事"""
        return """
《末日生存者》游戏背景

在不久的将来，一场未知的灾难席卷了全球，人类社会几乎崩溃。
大多数人口消失，城市变成了废墟，自然环境发生了剧变。

你是一名幸存者，必须在这个危险的世界中努力生存。
你需要寻找食物、水和其他资源，建造庇护所，制作工具，并与各种威胁作斗争。

在这个世界里，你会遇到：
- 变异的生物和危险的敌人
- 其他幸存者，可能是朋友也可能是敌人
- 各种资源点和隐藏的秘密

你的目标是尽可能长时间地生存下去，同时探索这个世界的真相。
每一天都是新的挑战，每一个决定都可能影响你的生存机会。

祝你好运，幸存者！
"""

    def get_codex_content(self):
        """获取图鉴内容"""
        return """
物品图鉴：

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

    def get_gameplay_help(self):
        """获取游戏玩法帮助"""
        return """
《末日生存者》游戏玩法

基本目标：
- 在这个末日世界中尽可能长时间地生存下去
- 探索世界，收集资源，制作物品
- 避免危险，保持健康和体力

游戏机制：
- 时间系统：游戏内时间会流逝，影响资源消耗和事件发生
- 生存需求：每天需要消耗食物和水，否则会损失生命值
- 体力系统：行动会消耗体力，休息可以恢复
- 战斗系统：遇到敌人时会自动进行战斗
- 精神系统：保持精神状态良好，避免精神崩溃
- 疲劳系统：长时间活动会累积疲劳，影响属性
- 天气系统：不同天气影响行动效率和资源获取

操作指南：

主界面操作：
- 探索：搜索当前位置的资源，可能发现物品或遇到敌人
- 休息：恢复体力和少量生命值
- 睡觉：长时间休息，大幅恢复各项状态
- 进食/喝水：消耗食物和水恢复生命值/体力
- 钓鱼：在水边钓鱼获取食物
- 狩猎：在森林或平原狩猎动物
- 砍柴：收集木材
- 采药：采集草药
- 交易：与NPC交易物品
- 修理：修理损坏的装备
- 研究：消耗研究资料解锁新知识
- 冥想：恢复精神值
- 查看背包：查看拥有的物品和装备
- 查看地图：查看已探索的区域和当前位置
- 制作：使用材料制作有用的物品
- 农业：种植和收获农作物

生存技巧：
1. 合理分配资源，确保每天有足够的食物和水
2. 探索新区域时要小心，危险程度各不相同
3. 制作物品可以提高生存效率
4. 遇到强敌时，考虑暂时撤退
5. 保持精神状态，避免长时间不睡觉
6. 注意疲劳值，过度疲劳会影响战斗和行动
7. 关注天气变化，恶劣天气时减少外出
8. 与NPC建立良好关系，获取更多帮助

提示：
- 注意季节变化，不同季节适合种植不同的作物
- 建立多个庇护所，分散风险
- 与其他幸存者建立良好关系
- 定期检查装备耐久度
- 记录重要地点的位置

祝你好运，幸存者！
"""

    def get_all_stories(self):
        """获取所有已解锁的故事内容"""
        content = "《末日生存者》故事书\n\n"
        content += "=" * 50 + "\n\n"

        categories = self.get_all_categories()
        for category in categories:
            content += f"【{category.upper()}】\n\n"
            stories = self.get_stories_by_category(category)
            for story in stories:
                content += f"《{story['title']}》 - {story['author']}\n"
                content += story['content'] + "\n"
                content += "-" * 30 + "\n\n"

        return content