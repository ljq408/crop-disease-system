# -*- coding: utf-8 -*-
"""
模型训练脚本
基于 PlantVillage 数据集的迁移学习训练
支持数据增强、学习率调度、早停、断点续训
"""

import os
import sys
import json
import time
import argparse
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import ReduceLROnPlateau

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from models.model import build_model


# ============ 数据增强配置 ============
def get_train_transform():
    """训练集数据增强变换"""
    return transforms.Compose([
        transforms.RandomResizedCrop(Config.IMG_SIZE, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.2),
        transforms.RandomRotation(30),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
        transforms.RandomGrayscale(p=0.05),
        transforms.ToTensor(),
        transforms.Normalize(mean=Config.NORMALIZE_MEAN, std=Config.NORMALIZE_STD)
    ])

def get_val_transform():
    """验证/测试集变换（不做数据增强）"""
    return transforms.Compose([
        transforms.Resize((Config.IMG_SIZE, Config.IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=Config.NORMALIZE_MEAN, std=Config.NORMALIZE_STD)
    ])


# ============ 数据集加载 ============
def load_datasets():
    """
    加载并划分 PlantVillage 数据集
    训练集:验证集:测试集 = 70%:15%:15%
    """
    print(f"📂 加载数据集: {Config.DATA_DIR}")
    if not os.path.exists(Config.DATA_DIR):
        raise FileNotFoundError(
            f"数据集路径不存在: {Config.DATA_DIR}\n"
            "请参考 data/README.md 下载 PlantVillage 数据集"
        )

    # 先用验证变换加载完整数据集（后续对训练集单独应用增强）
    full_dataset = datasets.ImageFolder(Config.DATA_DIR, transform=get_val_transform())
    total_size = len(full_dataset)
    train_size = int(total_size * Config.TRAIN_RATIO)
    val_size = int(total_size * Config.VAL_RATIO)
    test_size = total_size - train_size - val_size

    train_dataset, val_dataset, test_dataset = random_split(
        full_dataset, [train_size, val_size, test_size],
        generator=torch.Generator().manual_seed(42)
    )

    # 为训练集单独设置数据增强
    train_dataset.dataset = datasets.ImageFolder(Config.DATA_DIR, transform=get_train_transform())

    print(f"✅ 数据集加载完成:")
    print(f"   总样本数:  {total_size:,}")
    print(f"   训练集:    {train_size:,} ({Config.TRAIN_RATIO*100:.0f}%)")
    print(f"   验证集:    {val_size:,} ({Config.VAL_RATIO*100:.0f}%)")
    print(f"   测试集:    {test_size:,} ({Config.TEST_RATIO*100:.0f}%)")
    print(f"   类别数量:  {len(full_dataset.classes)}")

    return train_dataset, val_dataset, test_dataset, full_dataset.classes


# ============ 训练函数 ============
def train_epoch(model, loader, criterion, optimizer, device):
    """训练一个 epoch"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (images, labels) in enumerate(loader):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()

        # 梯度裁剪，防止梯度爆炸
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

        if (batch_idx + 1) % 50 == 0:
            print(f"   Batch [{batch_idx+1}/{len(loader)}] "
                  f"Loss: {running_loss/(batch_idx+1):.4f} "
                  f"Acc: {100.*correct/total:.2f}%")

    return running_loss / len(loader), 100. * correct / total


def evaluate(model, loader, criterion, device):
    """验证/测试评估"""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    avg_loss = running_loss / len(loader)
    accuracy = 100. * correct / total
    return avg_loss, accuracy, all_preds, all_labels


# ============ 主训练流程 ============
def train(args):
    """完整训练流程"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥️  训练设备: {device}")
    if torch.cuda.is_available():
        print(f"   GPU: {torch.cuda.get_device_name(0)}")

    # 创建保存目录
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    os.makedirs(Config.LOG_DIR, exist_ok=True)

    # 加载数据集
    train_dataset, val_dataset, test_dataset, classes = load_datasets()
    train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE,
                              shuffle=True, num_workers=4, pin_memory=True)
    val_loader   = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE,
                              shuffle=False, num_workers=4, pin_memory=True)
    test_loader  = DataLoader(test_dataset, batch_size=Config.BATCH_SIZE,
                              shuffle=False, num_workers=4, pin_memory=True)

    # 构建模型
    print(f"\n🏗️  构建模型: {Config.MODEL_NAME}")
    model = build_model(Config.MODEL_NAME, Config.NUM_CLASSES, pretrained=True)
    model = model.to(device)

    # 损失函数与优化器
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = optim.AdamW(model.parameters(),
                            lr=Config.LEARNING_RATE,
                            weight_decay=Config.WEIGHT_DECAY)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5,
                                   patience=Config.LR_PATIENCE, verbose=True)

    # 断点续训
    start_epoch = 0
    best_val_acc = 0.0
    history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}

    checkpoint_path = os.path.join(Config.MODEL_DIR, "checkpoint.pth")
    if args.resume and os.path.exists(checkpoint_path):
        print(f"🔄 恢复训练: {checkpoint_path}")
        ckpt = torch.load(checkpoint_path, map_location=device)
        model.load_state_dict(ckpt["model_state_dict"])
        optimizer.load_state_dict(ckpt["optimizer_state_dict"])
        start_epoch = ckpt["epoch"] + 1
        best_val_acc = ckpt.get("best_val_acc", 0.0)
        history = ckpt.get("history", history)
        print(f"   从第 {start_epoch} 轮继续训练，最佳验证准确率: {best_val_acc:.2f}%")

    # 开始训练
    early_stop_counter = 0
    print(f"\n🚀 开始训练 ({Config.NUM_EPOCHS} 轮)\n" + "=" * 60)

    for epoch in range(start_epoch, Config.NUM_EPOCHS):
        epoch_start = time.time()
        print(f"\n📌 Epoch [{epoch+1}/{Config.NUM_EPOCHS}]")

        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc, _, _ = evaluate(model, val_loader, criterion, device)
        scheduler.step(val_loss)

        epoch_time = time.time() - epoch_start
        print(f"   ⏱️  耗时: {epoch_time:.1f}s  "
              f"Train Loss: {train_loss:.4f}  Train Acc: {train_acc:.2f}%  "
              f"Val Loss: {val_loss:.4f}  Val Acc: {val_acc:.2f}%")

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["train_acc"].append(train_acc)
        history["val_acc"].append(val_acc)

        # 保存最佳模型
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                "model_state_dict": model.state_dict(),
                "val_acc": val_acc,
                "epoch": epoch,
                "model_name": Config.MODEL_NAME,
                "num_classes": Config.NUM_CLASSES,
                "class_names": classes
            }, Config.MODEL_PATH)
            print(f"   ✅ 保存最佳模型 (Val Acc: {best_val_acc:.2f}%)")
            early_stop_counter = 0
        else:
            early_stop_counter += 1

        # 保存断点
        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "best_val_acc": best_val_acc,
            "history": history
        }, checkpoint_path)

        # 早停判断
        if early_stop_counter >= Config.EARLY_STOP_PATIENCE:
            print(f"\n⏹️  早停：{Config.EARLY_STOP_PATIENCE} 轮内验证准确率未提升，停止训练")
            break

    # 在测试集上最终评估
    print(f"\n{'='*60}\n📊 加载最佳模型进行测试集评估...")
    ckpt = torch.load(Config.MODEL_PATH, map_location=device)
    model.load_state_dict(ckpt["model_state_dict"])
    test_loss, test_acc, preds, labels = evaluate(model, test_loader, criterion, device)

    print(f"🎯 最终测试集结果:")
    print(f"   Test Loss: {test_loss:.4f}")
    print(f"   Test Accuracy: {test_acc:.2f}%")
    print(f"   Best Val Accuracy: {best_val_acc:.2f}%")

    # 保存训练历史
    with open(os.path.join(Config.LOG_DIR, "training_history.json"), "w") as f:
        json.dump(history, f, indent=2)
    print(f"\n📁 训练历史已保存至 logs/training_history.json")
    print(f"📁 最佳模型已保存至 {Config.MODEL_PATH}")


# ============ 命令行入口 ============
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="农作物病害识别模型训练")
    parser.add_argument("--resume", action="store_true", help="从断点恢复训练")
    parser.add_argument("--epochs", type=int, default=Config.NUM_EPOCHS, help="训练轮数")
    parser.add_argument("--lr", type=float, default=Config.LEARNING_RATE, help="学习率")
    parser.add_argument("--batch", type=int, default=Config.BATCH_SIZE, help="批量大小")
    args = parser.parse_args()

    Config.NUM_EPOCHS = args.epochs
    Config.LEARNING_RATE = args.lr
    Config.BATCH_SIZE = args.batch

    train(args)
