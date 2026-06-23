# -*- coding: utf-8 -*-
"""
项目全局配置文件
农作物病害智能识别与诊断系统
"""

import os


def _get_secret(key: str, env_var: str, default: str = "") -> str:
    """从 Streamlit Secrets 或环境变量读取配置"""
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(env_var, default)


class Config:
    """系统全局配置类"""

    # ============ 模型配置 ============
    MODEL_NAME = "efficientnet_b0"      # 可选: resnet50, efficientnet_b0, efficientnet_b3
    NUM_CLASSES = 38                     # PlantVillage 数据集类别数
    IMG_SIZE = 224                       # 输入图像尺寸
    BATCH_SIZE = 32                      # 训练批量大小
    NUM_EPOCHS = 30                      # 训练轮数
    LEARNING_RATE = 1e-4                 # 初始学习率
    WEIGHT_DECAY = 1e-5                  # 权重衰减
    LR_PATIENCE = 5                      # 学习率调度耐心值
    EARLY_STOP_PATIENCE = 8             # 早停耐心值

    # ============ 路径配置 ============
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data", "PlantVillage")
    MODEL_DIR = os.path.join(BASE_DIR, "models", "weights")
    MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pth")
    LOG_DIR = os.path.join(BASE_DIR, "logs")

    # ============ LLM 大模型配置 ============
    # 优先级: Streamlit Secrets > 环境变量 > 默认值
    # Streamlit Cloud 部署时通过 .streamlit/secrets.toml 配置密钥

    # 方案1: 阿里云通义千问 API (推荐)
    LLM_PROVIDER = "qwen"                       # qwen / openai / ollama / mock
    LLM_API_KEY = _get_secret("DASHSCOPE_API_KEY", "DASHSCOPE_API_KEY")
    LLM_MODEL = _get_secret("LLM_MODEL", "LLM_MODEL", "qwen-plus")
    LLM_BASE_URL = _get_secret("LLM_BASE_URL", "LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

    # 方案2: OpenAI 兼容接口
    OPENAI_API_KEY = _get_secret("OPENAI_API_KEY", "OPENAI_API_KEY")
    OPENAI_BASE_URL = _get_secret("OPENAI_BASE_URL", "OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL = _get_secret("OPENAI_MODEL", "OPENAI_MODEL", "gpt-4o-mini")

    # 方案3: 本地 Ollama 离线模型
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "qwen2:7b"

    # ============ 应用配置 ============
    CONFIDENCE_THRESHOLD = 0.5          # 置信度阈值
    TOP_K = 5                           # 显示前 K 个预测结果
    MAX_HISTORY = 50                    # 最大历史记录数量
    HISTORY_FILE = os.path.join(BASE_DIR, "assets", "history.json")

    # ============ 演示模式 ============
    # 若无模型权重文件，自动进入演示模式（使用随机模拟预测）
    @classmethod
    def is_demo_mode(cls):
        return not os.path.exists(cls.MODEL_PATH)

    # ============ 数据增强配置 ============
    TRAIN_AUG = True
    NORMALIZE_MEAN = [0.485, 0.456, 0.406]
    NORMALIZE_STD  = [0.229, 0.224, 0.225]

    # ============ 训练集/验证集/测试集划分 ============
    TRAIN_RATIO = 0.7
    VAL_RATIO   = 0.15
    TEST_RATIO  = 0.15
