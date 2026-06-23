# -*- coding: utf-8 -*-
"""
PlantVillage 数据集 38 类病害详细信息
包含：中文名称、植物种类、病害描述、症状、防治方案、危害等级
"""

# 38 个类别的中英文对照及详细信息
DISEASE_INFO = {
    "Apple___Apple_scab": {
        "zh_name": "苹果黑星病",
        "plant": "苹果",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "苹果黑星菌 (Venturia inaequalis)",
        "description": "苹果黑星病是由苹果黑星菌引起的真菌性病害，是世界苹果产区最重要的病害之一，可造成严重的产量和品质损失。",
        "symptoms": "叶片正面出现橄榄绿至黑褐色放射状病斑，背面出现暗绿色绒状斑点；果实表面出现黑色硬化斑点，影响商品价值。",
        "treatment": "1. 发病初期喷施甲基硫菌灵或多菌灵可湿性粉剂；2. 使用苯醚甲环唑或腈菌唑等甾醇抑制剂；3. 合理使用波尔多液保护性喷药。",
        "prevention": "1. 清除落叶减少初侵染源；2. 选种抗病品种；3. 果园合理密植保持通风；4. 花前花后各喷一次保护性杀菌剂。",
        "color": "#FF6B35"
    },
    "Apple___Black_rot": {
        "zh_name": "苹果黑腐病",
        "plant": "苹果",
        "is_healthy": False,
        "severity": "重度",
        "pathogen": "仁果壳囊孢菌 (Botryosphaeria obtusa)",
        "description": "苹果黑腐病可侵害果实、叶片和枝干，导致果实腐烂，严重时造成大量落果，危害极大。",
        "symptoms": "果实出现褐色至黑色腐烂斑，表面有同心环状斑纹，呈蛙眼状；叶片出现圆形紫色至褐色斑点。",
        "treatment": "1. 彻底清除园内病果、病叶和枯死枝；2. 喷施代森锰锌、苯醚甲环唑等杀菌剂；3. 枝干病部刮除后涂石硫合剂消毒。",
        "prevention": "1. 及时修剪枯枝病枝，伤口及时保护；2. 保持园内清洁卫生；3. 避免机械损伤造成伤口感染。",
        "color": "#8B0000"
    },
    "Apple___Cedar_apple_rust": {
        "zh_name": "苹果锈病",
        "plant": "苹果",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "山田胶锈菌 (Gymnosporangium yamadae)",
        "description": "苹果锈病需要柏科植物作为转主寄主，在苹果产区附近种植柏类植物时容易大面积发生。",
        "symptoms": "叶片正面出现橙黄色有光泽病斑，斑上生有性孢子器；背面出现黄色毛刺状锈子器突起，孢子橙黄色。",
        "treatment": "1. 发芽前后各喷一次石硫合剂；2. 花后10天喷施三唑类杀菌剂（腈菌唑、丙环唑）；3. 病害严重时每隔10-15天重复喷药。",
        "prevention": "1. 苹果园5千米内避免种植柏类植物；2. 已有柏类植物在秋末冬初喷石硫合剂铲除病原；3. 选用抗病苹果品种。",
        "color": "#FFA500"
    },
    "Apple___healthy": {
        "zh_name": "苹果（健康）",
        "plant": "苹果",
        "is_healthy": True,
        "severity": "无",
        "description": "叶片生长健壮，颜色鲜绿，无病斑或异常现象，表明植株处于健康状态。",
        "symptoms": "无明显病害症状，叶面光滑有光泽。",
        "treatment": "保持日常管理，无需额外处理。",
        "prevention": "定期检查，保持合理施肥与灌溉。",
        "color": "#28A745"
    },
    "Blueberry___healthy": {
        "zh_name": "蓝莓（健康）",
        "plant": "蓝莓",
        "is_healthy": True,
        "severity": "无",
        "description": "蓝莓叶片健康，无明显病害，植株生长旺盛。",
        "symptoms": "无",
        "treatment": "保持日常管理。",
        "prevention": "定期检查病虫害。",
        "color": "#28A745"
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "zh_name": "樱桃白粉病",
        "plant": "樱桃",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "嗜果白粉菌 (Podosphaera clandestina)",
        "description": "樱桃白粉病广泛分布于各樱桃产区，影响叶片和嫩枝，严重时导致叶片扭曲脱落。",
        "symptoms": "叶片正面出现白色粉状霉层，严重时覆盖整个叶面；嫩枝和幼果亦可感染，导致畸形。",
        "treatment": "1. 喷施三唑酮（粉锈宁）、腈菌唑等三唑类杀菌剂；2. 使用硫磺悬浮剂；3. 发病严重时每隔7天连续防治2-3次。",
        "prevention": "1. 选育抗病品种；2. 控制氮肥用量防止枝叶徒长；3. 增施磷钾肥增强抗病能力；4. 适当修剪改善通风透光。",
        "color": "#F0E68C"
    },
    "Cherry_(including_sour)___healthy": {
        "zh_name": "樱桃（健康）",
        "plant": "樱桃",
        "is_healthy": True,
        "severity": "无",
        "description": "樱桃叶片健康，生长正常。",
        "symptoms": "无",
        "treatment": "保持日常管理。",
        "prevention": "定期检查。",
        "color": "#28A745"
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "zh_name": "玉米灰斑病",
        "plant": "玉米",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "玉米尾孢菌 (Cercospora zeae-maydis)",
        "description": "玉米灰斑病是近年来危害日益严重的叶部真菌病害，在高温高湿地区发病重。",
        "symptoms": "叶片出现长方形灰白色至灰褐色病斑，边缘平直，受叶脉限制，严重时整叶枯死。",
        "treatment": "1. 喷施苯醚甲环唑、丙环唑或嘧菌酯；2. 大喇叭口期至抽雄期为防治关键期；3. 发病初期及时施药。",
        "prevention": "1. 选用抗病品种；2. 轮作倒茬；3. 清除田间病残体；4. 合理密植，避免田间郁闭。",
        "color": "#808080"
    },
    "Corn_(maize)___Common_rust_": {
        "zh_name": "玉米普通锈病",
        "plant": "玉米",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "玉米柄锈菌 (Puccinia sorghi)",
        "description": "玉米普通锈病在冷凉多雨地区危害严重，高感品种可导致严重减产。",
        "symptoms": "叶片两面散生或密生砖红色至褐色夏孢子堆，后期变为黑色冬孢子堆，叶片变黄干枯。",
        "treatment": "1. 发病初期喷施三唑酮、烯唑醇或丙环唑；2. 每隔7-10天喷一次，连喷2-3次；3. 严重时使用复配杀菌剂。",
        "prevention": "1. 种植抗病品种是最经济有效的方法；2. 适时晚播错开发病高峰；3. 科学施肥提高植株抗性。",
        "color": "#B8860B"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "zh_name": "玉米大斑病",
        "plant": "玉米",
        "is_healthy": False,
        "severity": "重度",
        "pathogen": "大斑凸脐蠕孢菌 (Setosphaeria turcica)",
        "description": "玉米大斑病是玉米叶部最重要的病害之一，在凉爽潮湿气候条件下危害尤为严重，可造成严重减产。",
        "symptoms": "叶片出现长梭形、灰绿色至褐色大型病斑，长5-20cm，潮湿时病斑上产生灰黑色霉层。",
        "treatment": "1. 发病初期喷施苯醚甲环唑·丙环唑复配剂；2. 嘧菌酯、吡唑醚菌酯等有较好防效；3. 抽雄前后为防治关键期。",
        "prevention": "1. 推广种植抗病、耐病品种；2. 及时清除病残体；3. 合理密植和施肥；4. 轮作减少初侵染源。",
        "color": "#8B4513"
    },
    "Corn_(maize)___healthy": {
        "zh_name": "玉米（健康）",
        "plant": "玉米",
        "is_healthy": True,
        "severity": "无",
        "description": "玉米叶片深绿健壮，生长旺盛，无病害。",
        "symptoms": "无",
        "treatment": "保持日常管理。",
        "prevention": "定期检查。",
        "color": "#28A745"
    },
    "Grape___Black_rot": {
        "zh_name": "葡萄黑腐病",
        "plant": "葡萄",
        "is_healthy": False,
        "severity": "重度",
        "pathogen": "葡萄鬼伞 (Guignardia bidwellii)",
        "description": "葡萄黑腐病可造成叶片、果实大量腐烂，是葡萄种植中损失最大的病害之一。",
        "symptoms": "叶片出现红褐色圆形病斑，边缘有深色线纹，果实感染后初期红褐色后变为黑色干瘪僵果。",
        "treatment": "1. 嫩梢期至果实着色前多次喷施甲基硫菌灵或苯醚甲环唑；2. 剪除病果、病叶集中销毁；3. 雨后及时补喷。",
        "prevention": "1. 彻底清除园内越冬病残体；2. 合理整枝保持通风透光；3. 避免果园积水；4. 雨季前提前预防。",
        "color": "#4B0082"
    },
    "Grape___Esca_(Black_Measles)": {
        "zh_name": "葡萄埃斯卡病（黑麻疹病）",
        "plant": "葡萄",
        "is_healthy": False,
        "severity": "重度",
        "pathogen": "多种真菌复合侵染 (Phaeomoniella chlamydospora 等)",
        "description": "葡萄埃斯卡病是一种木质部复合病害，由多种真菌共同作用，可导致葡萄逐渐衰退死亡。",
        "symptoms": "叶片出现黄白色或棕褐色虎纹状斑纹，果实出现紫黑色斑点，木质部变色坏死。",
        "treatment": "1. 目前无有效化学防治方法；2. 及时切除发病枝条并涂抹伤口保护剂；3. 严重植株需整株拔除销毁。",
        "prevention": "1. 使用无病苗木；2. 避免大伤口，修剪后涂抹保护剂；3. 加强园地排水，减少积水。",
        "color": "#800080"
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "zh_name": "葡萄叶斑病",
        "plant": "葡萄",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "葡萄葛氏菌 (Pseudocercospora vitis)",
        "description": "葡萄叶斑病主要危害叶片，造成早期落叶，影响果实品质和来年产量。",
        "symptoms": "叶片出现不规则深褐色病斑，病斑周围有黄色晕圈，背面可见灰黑色霉层。",
        "treatment": "1. 喷施代森锰锌、苯醚甲环唑等杀菌剂；2. 发病初期连续防治3次；3. 雨季加强防治频次。",
        "prevention": "1. 清除园内落叶；2. 合理夏季修剪改善通风；3. 避免园地过度郁闭。",
        "color": "#A0522D"
    },
    "Grape___healthy": {
        "zh_name": "葡萄（健康）",
        "plant": "葡萄",
        "is_healthy": True,
        "severity": "无",
        "description": "葡萄叶片健康，色泽鲜绿，无病害症状。",
        "symptoms": "无",
        "treatment": "保持日常管理。",
        "prevention": "定期检查。",
        "color": "#28A745"
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "zh_name": "柑橘黄龙病（绿化病）",
        "plant": "柑橘/橙",
        "is_healthy": False,
        "severity": "毁灭性",
        "pathogen": "亚洲柑橘黄龙病菌 (Candidatus Liberibacter asiaticus)",
        "description": "柑橘黄龙病是由韧皮部细菌引起的检疫性病害，被列为柑橘种植业最具毁灭性的病害，目前无有效治疗方法。",
        "symptoms": "叶片出现黄绿色不对称斑驳（俗称黄化叶），果实发育不良，呈歪斜畸形，着色异常呈红鼻果。",
        "treatment": "1. 目前无有效化学治疗方法；2. 发现病树必须立即整株连根挖除销毁；3. 彻底消灭传播媒介木虱。",
        "prevention": "1. 使用无病苗木建园；2. 防治柑橘木虱切断传播途径；3. 建立严格的检疫制度；4. 加强监测早发现早处理。",
        "color": "#FFD700"
    },
    "Peach___Bacterial_spot": {
        "zh_name": "桃细菌性穿孔病",
        "plant": "桃",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "黄单胞菌桃李致病变种 (Xanthomonas arboricola pv. pruni)",
        "description": "桃细菌性穿孔病在潮湿多雨地区普遍发生，可造成叶片穿孔脱落和果实品质下降。",
        "symptoms": "叶片出现水渍状小斑点，扩大后变为褐色，最终脱落形成穿孔；果实出现暗紫色斑点，严重时龟裂。",
        "treatment": "1. 发芽前喷施石硫合剂或硫酸铜石灰液；2. 展叶后喷施农用链霉素、中生菌素；3. 雨前雨后及时防治。",
        "prevention": "1. 合理修剪保持通风；2. 避免在低洼潮湿地建园；3. 选抗病品种；4. 冬季清园减少越冬菌源。",
        "color": "#CD853F"
    },
    "Peach___healthy": {
        "zh_name": "桃（健康）",
        "plant": "桃",
        "is_healthy": True,
        "severity": "无",
        "description": "桃树叶片健康，生长旺盛。",
        "symptoms": "无",
        "treatment": "保持日常管理。",
        "prevention": "定期检查。",
        "color": "#28A745"
    },
    "Pepper,_bell___Bacterial_spot": {
        "zh_name": "甜椒细菌性斑点病",
        "plant": "甜椒",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "番茄黄单胞菌辣椒叶斑病致病变种 (Xanthomonas euvesicatoria)",
        "description": "甜椒细菌性斑点病在温暖多雨季节流行，严重时导致大量落叶和果实商品性下降。",
        "symptoms": "叶片出现水渍状小斑，扩展为褐色病斑，有黄色晕圈；果实出现深褐色疮痂状病斑，影响外观。",
        "treatment": "1. 发病初期喷施铜制剂（氢氧化铜、波尔多液）；2. 与农用链霉素交替使用；3. 发病期每5-7天喷一次。",
        "prevention": "1. 种子消毒（55℃热水浸种30分钟）；2. 与非茄科作物轮作2-3年；3. 控制浇水量减少叶面积水。",
        "color": "#FF4500"
    },
    "Pepper,_bell___healthy": {
        "zh_name": "甜椒（健康）",
        "plant": "甜椒",
        "is_healthy": True,
        "severity": "无",
        "description": "甜椒植株健康，叶片深绿有光泽。",
        "symptoms": "无",
        "treatment": "保持日常管理。",
        "prevention": "定期检查。",
        "color": "#28A745"
    },
    "Potato___Early_blight": {
        "zh_name": "马铃薯早疫病",
        "plant": "马铃薯",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "茄链格孢 (Alternaria solani)",
        "description": "马铃薯早疫病是常见的叶部病害，多从下部老叶开始发病，逐渐向上蔓延，影响光合作用和产量。",
        "symptoms": "叶片出现深褐色圆形至近圆形病斑，具有明显的同心轮纹，外有黄色晕圈，潮湿时病斑上有黑色霉层。",
        "treatment": "1. 喷施代森锰锌、百菌清或异菌脲；2. 发病初期每7-10天喷一次，连喷3-4次；3. 与苯醚甲环唑等内吸剂交替使用。",
        "prevention": "1. 选用耐病品种；2. 增施磷钾肥增强抗性；3. 适时早种避开高温多湿季节；4. 合理密植保持通风。",
        "color": "#8B4513"
    },
    "Potato___Late_blight": {
        "zh_name": "马铃薯晚疫病",
        "plant": "马铃薯",
        "is_healthy": False,
        "severity": "毁灭性",
        "pathogen": "致病疫霉 (Phytophthora infestans)",
        "description": "马铃薯晚疫病是历史上最具破坏性的植物病害之一（19世纪爱尔兰大饥荒的原因），至今仍是全球马铃薯生产的最大威胁。",
        "symptoms": "叶片出现水渍状不规则暗绿色斑，后变褐色腐败；潮湿时叶背面有白色霜霉状孢囊；块茎内部腐烂变褐。",
        "treatment": "1. 喷施烯酰吗啉、氟菌·霜霉威、代森锰锌等；2. 发病初期立即施药，每5-7天一次；3. 不同作用机制药剂交替使用。",
        "prevention": "1. 种植抗病品种；2. 使用脱毒种薯；3. 根据天气预报提前预防；4. 发现中心病株立即拔除销毁。",
        "color": "#2F4F4F"
    },
    "Potato___healthy": {
        "zh_name": "马铃薯（健康）",
        "plant": "马铃薯",
        "is_healthy": True,
        "severity": "无",
        "description": "马铃薯植株健康，叶片绿色光亮。",
        "symptoms": "无",
        "treatment": "保持日常管理。",
        "prevention": "定期检查。",
        "color": "#28A745"
    },
    "Raspberry___healthy": {
        "zh_name": "覆盆子（健康）",
        "plant": "覆盆子",
        "is_healthy": True,
        "severity": "无",
        "description": "覆盆子植株健康，正常生长。",
        "symptoms": "无",
        "treatment": "保持日常管理。",
        "prevention": "定期检查。",
        "color": "#28A745"
    },
    "Soybean___healthy": {
        "zh_name": "大豆（健康）",
        "plant": "大豆",
        "is_healthy": True,
        "severity": "无",
        "description": "大豆植株健康，叶片浓绿，生长良好。",
        "symptoms": "无",
        "treatment": "保持日常管理。",
        "prevention": "定期检查。",
        "color": "#28A745"
    },
    "Squash___Powdery_mildew": {
        "zh_name": "南瓜白粉病",
        "plant": "南瓜",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "葫芦科白粉菌 (Podosphaera xanthii)",
        "description": "南瓜白粉病是葫芦科作物最常见的病害，高温干燥条件下发病迅速，严重影响植株生长。",
        "symptoms": "叶片正面出现白色圆形粉状霉斑，逐渐扩大连成片，后期叶片变黄干枯；茎蔓也可感染。",
        "treatment": "1. 喷施硫磺悬浮剂、三唑酮或苯醚甲环唑；2. 发病初期每7天防治一次；3. 注意药剂轮换使用。",
        "prevention": "1. 选用抗白粉病品种；2. 合理密植，加强通风；3. 控制氮肥，增施磷钾肥；4. 及时摘除发病严重叶片。",
        "color": "#F5F5DC"
    },
    "Strawberry___Leaf_scorch": {
        "zh_name": "草莓叶焦病",
        "plant": "草莓",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "草莓拟茎点霉 (Diplocarpon earlianum)",
        "description": "草莓叶焦病在温暖潮湿条件下流行，影响植株光合效能，严重时导致植株衰弱，产量下降。",
        "symptoms": "叶片出现不规则深褐色至紫色病斑，中心灰白色，严重时叶缘和叶尖呈焦枯状；叶柄和果梗也可受侵害。",
        "treatment": "1. 喷施甲基硫菌灵、多菌灵或苯醚甲环唑；2. 发病初期每7-10天防治一次；3. 摘除严重病叶集中销毁。",
        "prevention": "1. 选用抗病品种；2. 合理密植，保持良好通风；3. 避免大水漫灌，推广滴灌技术；4. 适时清除病残叶。",
        "color": "#DC143C"
    },
    "Strawberry___healthy": {
        "zh_name": "草莓（健康）",
        "plant": "草莓",
        "is_healthy": True,
        "severity": "无",
        "description": "草莓植株健康，叶片浓绿光亮，生长旺盛。",
        "symptoms": "无",
        "treatment": "保持日常管理。",
        "prevention": "定期检查。",
        "color": "#28A745"
    },
    "Tomato___Bacterial_spot": {
        "zh_name": "番茄细菌性斑点病",
        "plant": "番茄",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "番茄黄单胞菌 (Xanthomonas vesicatoria)",
        "description": "番茄细菌性斑点病在温暖多雨、多露季节发病严重，严重影响叶片功能和果实商品性。",
        "symptoms": "叶片出现小而圆的水渍状褪绿斑，后变为褐色，有黄色晕圈；果实出现褐色疮痂，表面粗糙。",
        "treatment": "1. 铜制剂（氢氧化铜）与农用链霉素交替喷施；2. 发病期每5-7天防治一次；3. 雨后及时补喷。",
        "prevention": "1. 使用无病种子，播前种子消毒；2. 避免连作，与非茄科轮作；3. 采用膜下滴灌减少叶面积水。",
        "color": "#FF6347"
    },
    "Tomato___Early_blight": {
        "zh_name": "番茄早疫病",
        "plant": "番茄",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "茄链格孢 (Alternaria solani)",
        "description": "番茄早疫病是番茄生产中最常见的叶部病害，从结果期开始发生，影响果实产量和品质。",
        "symptoms": "叶片出现深褐色同心轮纹病斑（靶斑状），有黄色晕圈；茎部病斑椭圆形，有时导致茎干折断。",
        "treatment": "1. 喷施代森锰锌、百菌清、嘧菌酯等；2. 发病初期7天一次，连喷4次；3. 注意药剂轮换。",
        "prevention": "1. 合理密植，改善通风透光；2. 增施有机肥，增强植株抗性；3. 及时摘除下部老叶和病叶；4. 轮作减少菌源。",
        "color": "#D2691E"
    },
    "Tomato___Late_blight": {
        "zh_name": "番茄晚疫病",
        "plant": "番茄",
        "is_healthy": False,
        "severity": "重度",
        "pathogen": "致病疫霉 (Phytophthora infestans)",
        "description": "番茄晚疫病与马铃薯晚疫病由同一病原菌引起，阴雨低温条件下可在2-3天内毁灭成片番茄田。",
        "symptoms": "叶片出现深绿色水渍状不规则大型病斑，迅速扩展变褐腐烂；潮湿时叶背有白色霉层；果实腐烂成暗褐色硬块。",
        "treatment": "1. 喷施烯酰吗啉、嘧菌酯、霜脲·锰锌；2. 发病初期每5天喷一次；3. 不同作用机制药剂交替使用。",
        "prevention": "1. 种植抗病品种；2. 控制保护地内湿度；3. 避免大水漫灌；4. 发现中心病株立即拔除并施药。",
        "color": "#006400"
    },
    "Tomato___Leaf_Mold": {
        "zh_name": "番茄叶霉病",
        "plant": "番茄",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "黄枝孢菌 (Passalora fulva)",
        "description": "番茄叶霉病是保护地番茄生产中的重要病害，高温高湿条件下发展极快，严重时导致叶片枯死。",
        "symptoms": "叶片正面出现不规则黄绿色至黄色病斑，对应背面出现灰白色至紫灰色绒状霉层，后期叶片干枯卷曲。",
        "treatment": "1. 喷施腈菌唑、氟硅唑或苯醚甲环唑；2. 发病初期每7天防治一次；3. 保护地注意通风降湿。",
        "prevention": "1. 选用高抗叶霉病品种；2. 保持保护地通风，控制湿度低于90%；3. 避免过密种植。",
        "color": "#808000"
    },
    "Tomato___Septoria_leaf_spot": {
        "zh_name": "番茄匍柄霉叶斑病（七星病）",
        "plant": "番茄",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "番茄壳针孢 (Septoria lycopersici)",
        "description": "番茄七星病是番茄常见叶部病害，多从植株中下部叶片开始发病，造成下部叶片大量枯死脱落。",
        "symptoms": "叶片出现圆形小病斑，中心灰白色，边缘深褐色，中心有黑色小点（分生孢子器），形似靶心。",
        "treatment": "1. 喷施代森锰锌、苯醚甲环唑或嘧菌酯；2. 发病初期连续防治3-4次；3. 与百菌清等交替使用。",
        "prevention": "1. 及时打掉病叶，减少再侵染；2. 合理密植；3. 采用膜下滴灌；4. 与非茄科蔬菜轮作。",
        "color": "#708090"
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "zh_name": "番茄二斑叶螨（红蜘蛛）",
        "plant": "番茄",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "二斑叶螨 (Tetranychus urticae) — 害虫，非真菌",
        "description": "二斑叶螨是番茄生产中最重要的螨类害虫，高温干燥条件下繁殖极快，爆发时可造成严重减产。",
        "symptoms": "叶片正面出现灰白色细小斑点（刺吸痕），叶背可见细白网丝和橙黄色小螨虫，严重时叶片变黄焦枯。",
        "treatment": "1. 使用阿维菌素、哒螨灵或螺螨酯喷施叶背；2. 注意药剂轮换，避免产生抗药性；3. 保护天敌（植绥螨）进行生物防治。",
        "prevention": "1. 保持适当田间湿度；2. 清除田间杂草减少虫源；3. 利用黄板粘虫监测；4. 收获后及时清园。",
        "color": "#FF0000"
    },
    "Tomato___Target_Spot": {
        "zh_name": "番茄靶斑病",
        "plant": "番茄",
        "is_healthy": False,
        "severity": "中度",
        "pathogen": "多主棒孢菌 (Corynespora cassiicola)",
        "description": "番茄靶斑病是一种新兴病害，近年来在保护地番茄中发病面积不断扩大，危害程度逐渐加重。",
        "symptoms": "叶片出现近圆形至不规则深褐色病斑，具有明显靶心状轮纹，潮湿时病斑扩展迅速，呈水渍状。",
        "treatment": "1. 喷施苯醚甲环唑·丙环唑复配剂或嘧菌酯；2. 发病初期每7天防治一次；3. 与百菌清交替使用。",
        "prevention": "1. 采用通风降湿措施；2. 及时摘除病叶；3. 避免大水漫灌；4. 收获后彻底清园。",
        "color": "#A52A2A"
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "zh_name": "番茄黄化曲叶病毒病",
        "plant": "番茄",
        "is_healthy": False,
        "severity": "毁灭性",
        "pathogen": "番茄黄化曲叶病毒 (TYLCV) — 由烟粉虱传播",
        "description": "番茄黄化曲叶病毒病由烟粉虱(Bemisia tabaci)传播，一旦感染无法治愈，是番茄生产中最具毁灭性的病毒病。",
        "symptoms": "植株矮化，叶片黄化卷曲皱缩，叶缘向上反卷呈杯状，心叶小而黄化，果实少且发育不良。",
        "treatment": "1. 感染后无有效治疗方法；2. 彻底防治传播媒介烟粉虱；3. 发病严重植株及时拔除并销毁；4. 喷施吡虫啉等防虱。",
        "prevention": "1. 种植高抗TY品种是最有效的方法；2. 覆盖防虫网隔离烟粉虱；3. 育苗期严格防虫；4. 及时清除园地杂草。",
        "color": "#FFD700"
    },
    "Tomato___Tomato_mosaic_virus": {
        "zh_name": "番茄花叶病毒病",
        "plant": "番茄",
        "is_healthy": False,
        "severity": "重度",
        "pathogen": "番茄花叶病毒 (ToMV) / 烟草花叶病毒 (TMV)",
        "description": "番茄花叶病毒病可通过汁液接触、嫁接、昆虫等多种途径传播，一旦感染难以防治，常与其他病毒复合侵染。",
        "symptoms": "叶片出现黄绿相间的花叶状斑驳，严重时叶片皱缩、蕨叶状畸形；植株矮化，果实产生坏死斑点。",
        "treatment": "1. 感染后无有效化学治疗方法；2. 喷施病毒唑（宁南霉素）有一定抑制效果；3. 增施磷钾肥提高植株抗性。",
        "prevention": "1. 种子消毒（10%磷酸三钠浸种15分钟）；2. 田间操作前洗手，工具消毒；3. 防治蚜虫切断传播途径；4. 拔除并销毁病株。",
        "color": "#9ACD32"
    },
    "Tomato___healthy": {
        "zh_name": "番茄（健康）",
        "plant": "番茄",
        "is_healthy": True,
        "severity": "无",
        "description": "番茄植株健康，叶片深绿有光泽，无任何病毒、真菌或细菌感染迹象。",
        "symptoms": "无",
        "treatment": "保持日常管理，合理水肥。",
        "prevention": "定期监测病虫害，保持园地清洁。",
        "color": "#28A745"
    }
}

# 类别索引列表（与模型输出顺序对应）
CLASS_NAMES = sorted(list(DISEASE_INFO.keys()))

# 植物种类列表（用于筛选过滤）
PLANT_TYPES = sorted(list(set(v["plant"] for v in DISEASE_INFO.values())))

def get_disease_info(class_name: str) -> dict:
    """根据英文类名获取病害详细信息"""
    return DISEASE_INFO.get(class_name, {
        "zh_name": class_name,
        "plant": "未知",
        "is_healthy": False,
        "severity": "未知",
        "description": "暂无详细信息",
        "symptoms": "暂无症状描述",
        "treatment": "请咨询专业农业技术人员",
        "prevention": "加强日常监测",
        "color": "#6C757D"
    })

def get_severity_color(severity: str) -> str:
    """获取危害等级对应的颜色"""
    colors = {
        "无": "#28A745",
        "中度": "#FFC107",
        "重度": "#FF5722",
        "毁灭性": "#DC3545"
    }
    return colors.get(severity, "#6C757D")
