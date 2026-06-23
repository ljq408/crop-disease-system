# -*- coding: utf-8 -*-
"""
深度学习模型定义与推理模块
使用 EfficientNet-B0 迁移学习进行农作物病害分类
支持 EfficientNet-B0/B3, ResNet50 等主干网络
"""

import os
import sys
import random

# 条件导入 torch —— 未安装时自动进入演示模式
try:
    import torch
    import torch.nn as nn
    import torchvision.models as tv_models
    from torchvision import transforms
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None
    nn = None
    tv_models = None
    transforms = None

from PIL import Image
import numpy as np

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from utils.class_info import CLASS_NAMES, get_disease_info


def build_model(model_name: str = "efficientnet_b0", num_classes: int = 38,
                pretrained: bool = True):
    """
    构建迁移学习模型（仅在 torch 可用时调用）
    """
    if not TORCH_AVAILABLE:
        raise RuntimeError("PyTorch 未安装，无法构建模型。请安装 torch 和 torchvision。")

    weights_flag = "DEFAULT" if pretrained else None

    if model_name == "efficientnet_b0":
        model = tv_models.efficientnet_b0(weights=weights_flag)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(in_features, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.2),
            nn.Linear(512, num_classes)
        )

    elif model_name == "efficientnet_b3":
        model = tv_models.efficientnet_b3(weights=weights_flag)
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(in_features, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.2),
            nn.Linear(512, num_classes)
        )

    elif model_name == "resnet50":
        model = tv_models.resnet50(weights=weights_flag)
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(in_features, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.2),
            nn.Linear(512, num_classes)
        )
    else:
        raise ValueError(f"不支持的模型名称: {model_name}，请选择 efficientnet_b0/b3 或 resnet50")

    return model


# ============ 图像预处理变换 ============
def get_inference_transform():
    """获取推理时的图像变换（仅在 torch 可用时调用）"""
    if not TORCH_AVAILABLE:
        return None
    return transforms.Compose([
        transforms.Resize((Config.IMG_SIZE, Config.IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=Config.NORMALIZE_MEAN, std=Config.NORMALIZE_STD)
    ])


# ============ 推理引擎 ============
class DiseasePredictor:
    """农作物病害识别推理引擎（支持真实模型与演示模式）"""

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if TORCH_AVAILABLE else "cpu"
        self.transform = get_inference_transform()
        self.model = None
        self.demo_mode = not TORCH_AVAILABLE or Config.is_demo_mode()
        self._load_model()

    def _load_model(self):
        """加载模型权重"""
        if self.demo_mode:
            print("⚠️  未检测到模型权重，进入演示模式（使用模拟预测）")
            print(f"   权重文件路径: {Config.MODEL_PATH}")
            print("   如需使用真实模型，请运行 models/train.py 训练后将权重放入 models/weights/")
            return

        try:
            print(f"🔄 加载模型权重: {Config.MODEL_PATH}")
            self.model = build_model(
                model_name=Config.MODEL_NAME,
                num_classes=Config.NUM_CLASSES,
                pretrained=False
            )
            checkpoint = torch.load(Config.MODEL_PATH, map_location=self.device)
            # 兼容多种保存格式
            if "model_state_dict" in checkpoint:
                self.model.load_state_dict(checkpoint["model_state_dict"])
            else:
                self.model.load_state_dict(checkpoint)
            self.model.to(self.device)
            self.model.eval()
            print(f"✅ 模型加载成功，运行设备: {self.device}")
        except Exception as e:
            print(f"❌ 模型加载失败: {e}，切换到演示模式")
            self.demo_mode = True
            self.model = None

    def predict(self, image: Image.Image, top_k: int = 5) -> list:
        """
        对单张图片进行病害预测
        Args:
            image: PIL Image 对象
            top_k: 返回前 K 个预测结果
        Returns:
            results: [{"class_name": str, "zh_name": str, "confidence": float, ...}, ...]
        """
        if self.demo_mode:
            return self._demo_predict(top_k)

        # 图像预处理
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(img_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            top_probs, top_indices = probabilities.topk(top_k, dim=1)

        results = []
        for prob, idx in zip(top_probs[0].cpu().numpy(), top_indices[0].cpu().numpy()):
            class_name = CLASS_NAMES[idx]
            info = get_disease_info(class_name)
            results.append({
                "class_name": class_name,
                "class_idx": int(idx),
                "confidence": float(prob),
                "zh_name": info["zh_name"],
                "plant": info["plant"],
                "is_healthy": info["is_healthy"],
                "severity": info.get("severity", "未知"),
                "description": info.get("description", ""),
                "symptoms": info.get("symptoms", ""),
                "treatment": info.get("treatment", ""),
                "prevention": info.get("prevention", ""),
                "color": info.get("color", "#6C757D")
            })
        return results

    def _demo_predict(self, top_k: int = 5) -> list:
        """
        演示模式：生成模拟预测结果（用于无模型权重时的功能演示）
        使用符合真实分布的随机预测，首个结果置信度较高
        """
        # 从所有38类中随机选取 top_k 个不重复的类
        selected_indices = random.sample(range(len(CLASS_NAMES)), top_k)

        # 生成符合 softmax 分布特征的置信度（第一名明显高于其他）
        raw_scores = sorted([random.random() for _ in range(top_k)], reverse=True)
        # 对最高分做加权使其更突出
        raw_scores[0] = raw_scores[0] * 2.5
        total = sum(raw_scores)
        confidences = [s / total for s in raw_scores]

        results = []
        for conf, idx in zip(confidences, selected_indices):
            class_name = CLASS_NAMES[idx]
            info = get_disease_info(class_name)
            results.append({
                "class_name": class_name,
                "class_idx": idx,
                "confidence": conf,
                "zh_name": info["zh_name"],
                "plant": info["plant"],
                "is_healthy": info["is_healthy"],
                "severity": info.get("severity", "未知"),
                "description": info.get("description", ""),
                "symptoms": info.get("symptoms", ""),
                "treatment": info.get("treatment", ""),
                "prevention": info.get("prevention", ""),
                "color": info.get("color", "#6C757D"),
                "demo_mode": True  # 标记为演示模式结果
            })
        return results


# ============ 全局单例 ============
_predictor_instance = None

def get_predictor() -> DiseasePredictor:
    """获取推理引擎单例（避免重复加载模型）"""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = DiseasePredictor()
    return _predictor_instance
