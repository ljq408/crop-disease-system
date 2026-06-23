# -*- coding: utf-8 -*-
"""
数据预处理脚本
PlantVillage 数据集下载指引、目录检查、数据统计分析
"""

import os
import sys
import json
import shutil
import argparse
import random
from pathlib import Path
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from utils.class_info import CLASS_NAMES, get_disease_info


# ============ 数据集下载说明 ============
DOWNLOAD_GUIDE = """
====================================================================
📥 PlantVillage 数据集下载说明
====================================================================

PlantVillage 是公开可用的农作物病害图像数据集，包含38类约87,000张图片。

【方法一：Kaggle 下载（推荐）】
1. 注册/登录 Kaggle: https://www.kaggle.com
2. 搜索 "PlantVillage Dataset"
3. 下载地址: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
4. 解压后将 plantvillage dataset/segmented/ 文件夹复制到:
   {data_dir}/

【方法二：GitHub 下载】
git clone https://github.com/spMohanty/PlantVillage-Dataset.git
(注意: GitHub版本为原始图片，需自行整理目录结构)

【预期目录结构】
data/PlantVillage/
├── Apple___Apple_scab/        (约630张)
├── Apple___Black_rot/         (约621张)  
├── Apple___Cedar_apple_rust/  (约275张)
├── Apple___healthy/           (约1645张)
... (共38个子目录)

【快速验证】
运行本脚本检查数据集状态：
  py data/preprocess.py --check

====================================================================
""".format(data_dir=Config.DATA_DIR)


def check_dataset():
    """检查数据集是否存在且完整"""
    print("🔍 检查数据集状态...")
    
    if not os.path.exists(Config.DATA_DIR):
        print(f"❌ 数据集目录不存在: {Config.DATA_DIR}")
        print(DOWNLOAD_GUIDE)
        return False

    found_classes = []
    class_counts = {}
    
    for item in os.listdir(Config.DATA_DIR):
        item_path = os.path.join(Config.DATA_DIR, item)
        if os.path.isdir(item_path):
            count = len([f for f in os.listdir(item_path) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            found_classes.append(item)
            class_counts[item] = count

    if len(found_classes) == 0:
        print("❌ 数据集目录为空！")
        print(DOWNLOAD_GUIDE)
        return False

    total_images = sum(class_counts.values())
    print(f"✅ 数据集检查完成:")
    print(f"   发现类别数: {len(found_classes)}")
    print(f"   总图片数:   {total_images:,}")
    print(f"   平均每类:   {total_images//len(found_classes):,} 张")
    
    print(f"\n📊 各类别图片数量:")
    for cls, cnt in sorted(class_counts.items()):
        info = get_disease_info(cls)
        bar = "█" * (cnt // 100)
        print(f"   {info['zh_name']:20s} {cnt:5d} 张  {bar}")

    # 检查是否有缺失类
    missing = set(CLASS_NAMES) - set(found_classes)
    if missing:
        print(f"\n⚠️  缺失 {len(missing)} 个类别:")
        for cls in sorted(missing):
            print(f"   - {cls}")
    else:
        print(f"\n✅ 所有 {len(CLASS_NAMES)} 个类别均已找到")
    
    return True


def analyze_dataset():
    """分析数据集分布，生成统计报告"""
    if not check_dataset():
        return

    print("\n📊 生成数据集统计报告...")
    
    # 统计各植物类型的病害分布
    plant_stats = {}
    for cls_name in os.listdir(Config.DATA_DIR):
        cls_path = os.path.join(Config.DATA_DIR, cls_name)
        if not os.path.isdir(cls_path):
            continue
        info = get_disease_info(cls_name)
        plant = info["plant"]
        count = len([f for f in os.listdir(cls_path) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        
        if plant not in plant_stats:
            plant_stats[plant] = {"total": 0, "healthy": 0, "diseased": 0, "classes": []}
        plant_stats[plant]["total"] += count
        plant_stats[plant]["classes"].append({"name": cls_name, "count": count})
        if info["is_healthy"]:
            plant_stats[plant]["healthy"] += count
        else:
            plant_stats[plant]["diseased"] += count

    # 输出报告
    print("\n🌿 各植物类型统计:")
    for plant, stats in sorted(plant_stats.items()):
        print(f"\n   [{plant}]")
        print(f"   总计: {stats['total']:,} | 健康: {stats['healthy']:,} | 患病: {stats['diseased']:,}")

    # 保存统计结果
    stats_file = os.path.join(os.path.dirname(__file__), "dataset_stats.json")
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(plant_stats, f, ensure_ascii=False, indent=2)
    print(f"\n📁 统计结果已保存: {stats_file}")


def create_sample_demo():
    """
    从数据集中随机抽取样本创建演示数据集（每类10张）
    用于快速验证系统功能
    """
    if not os.path.exists(Config.DATA_DIR):
        print("❌ 原始数据集不存在，无法创建演示集")
        return

    demo_dir = os.path.join(os.path.dirname(Config.DATA_DIR), "PlantVillage_demo")
    os.makedirs(demo_dir, exist_ok=True)
    
    print(f"📦 创建演示数据集: {demo_dir}")
    total = 0

    for cls_name in os.listdir(Config.DATA_DIR):
        src_dir = os.path.join(Config.DATA_DIR, cls_name)
        if not os.path.isdir(src_dir):
            continue
        
        dst_dir = os.path.join(demo_dir, cls_name)
        os.makedirs(dst_dir, exist_ok=True)
        
        images = [f for f in os.listdir(src_dir) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        sample = random.sample(images, min(10, len(images)))
        
        for img in sample:
            shutil.copy2(os.path.join(src_dir, img), os.path.join(dst_dir, img))
        
        total += len(sample)

    print(f"✅ 演示数据集创建完成: {total} 张图片")
    print(f"   路径: {demo_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="数据集管理工具")
    parser.add_argument("--check", action="store_true", help="检查数据集完整性")
    parser.add_argument("--analyze", action="store_true", help="分析数据集分布")
    parser.add_argument("--demo", action="store_true", help="创建演示数据集（每类10张）")
    args = parser.parse_args()

    if args.check:
        check_dataset()
    elif args.analyze:
        analyze_dataset()
    elif args.demo:
        create_sample_demo()
    else:
        check_dataset()
