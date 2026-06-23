# 农作物病害智能识别与诊断系统

> 基于深度学习（EfficientNet-B0）与大语言模型（LLM）的农业病害辅助诊断平台

![Python](https://img.shields.io/badge/Python-3.10+-blue) 
![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-orange) 
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![Classes](https://img.shields.io/badge/病害类别-38类-green)

---

## 📋 项目概述

本系统是《人工智能基础B》课程期末大作业，实现了一个完整的农作物病害智能识别与诊断平台。

**核心功能：**
- 🔬 上传/拍摄叶片图片 → AI 自动识别病害类型（38类）
- 📊 置信度可视化展示，显示前 K 个预测结果
- 🤖 大语言模型（通义千问/GPT）生成专业诊断报告
- 💬 AI 问答系统，支持农业技术咨询
- 📖 内置病害知识库，包含症状描述、防治方案
- 📈 历史检测记录统计与导出

---

## 🗂️ 项目结构

```
crop_disease_system/
├── data/
│   ├── preprocess.py        # 数据集处理工具
│   ├── dataset_stats.json   # 数据集统计（自动生成）
│   └── README.md            # 数据集下载说明
├── models/
│   ├── model.py             # EfficientNet 模型定义与推理引擎
│   ├── train.py             # 完整训练脚本
│   └── weights/             # 模型权重目录（训练后生成）
│       └── best_model.pth   # 最佳模型权重
├── llm/
│   ├── llm_api.py           # LLM API 集成（支持Qwen/OpenAI/Ollama）
│   └── prompts.py           # 提示词模板
├── utils/
│   └── class_info.py        # 38类病害详细信息字典
├── assets/
│   └── history.json         # 历史检测记录（自动生成）
├── logs/                    # 训练日志（自动生成）
├── app.py                   # 主程序（Streamlit Web 应用）
├── config.py                # 全局配置文件
├── requirements.txt         # Python 依赖包清单
├── run.bat                  # Windows 一键启动脚本
└── run.sh                   # Linux/macOS 一键启动脚本
```

---

## ⚡ 快速开始

### 方法一：双击运行（推荐）

**Windows：**
```
双击 run.bat
```

**Linux/macOS：**
```bash
chmod +x run.sh && ./run.sh
```

### 方法二：命令行手动运行

```bash
# 1. 进入项目目录
cd crop_disease_system

# 2. 安装依赖（首次运行）
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 3. 启动应用
py -m streamlit run app.py
# 或
python3 -m streamlit run app.py
```

浏览器自动打开 http://localhost:8501

---

## 🎯 演示模式

**无需下载数据集或训练模型即可运行！**

- 未检测到 `models/weights/best_model.pth` 时自动进入**演示模式**
- 演示模式使用模拟预测数据，完整展示所有界面功能
- 所有 LLM 诊断报告功能均正常可用

---

## 📥 数据集下载（训练真实模型）

1. 访问 Kaggle：https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
2. 下载并解压到 `data/PlantVillage/` 目录
3. 验证数据集：`py data/preprocess.py --check`

---

## 🏋️ 模型训练

```bash
# 基础训练（30轮）
py models/train.py

# 自定义参数
py models/train.py --epochs 50 --lr 0.0001 --batch 32

# 断点续训
py models/train.py --resume
```

训练完成后，最佳权重自动保存到 `models/weights/best_model.pth`。

---

## 🤖 启用 AI 诊断报告

**方案1：通义千问（推荐，免费额度）**
```bash
# Windows
set DASHSCOPE_API_KEY=你的API密钥
run.bat

# 或在应用侧边栏直接填入 API Key
```

**方案2：本地 Ollama（离线）**
```bash
# 安装 Ollama: https://ollama.com
ollama pull qwen2:7b
# 启动后系统自动检测
```

---

## 📊 模型性能（训练完成后）

| 指标 | 值 |
|------|-----|
| 测试集准确率 | ≥ 93% |
| 训练数据量 | 60,900+ 张 |
| 推理速度（CPU）| ~150 ms/张 |
| 推理速度（GPU）| ~15 ms/张 |
| 模型大小 | ~21 MB |

---

## 🔧 环境要求

| 组件 | 最低要求 |
|------|---------|
| Python | 3.10+ |
| 内存 (RAM) | 4 GB+ |
| 磁盘空间 | 500 MB+（含依赖） |
| GPU（可选）| CUDA 11.8+ |
| 操作系统 | Windows 10/11, Ubuntu 20.04+, macOS 12+ |

---

## 👥 团队分工

| 成员 | 职责 |
|------|------|
| 成员1（组长）| 方案设计、技术架构、报告撰写 |
| 成员2 | 深度学习模型训练与优化、数据处理 |
| 成员3 | Streamlit界面开发、LLM集成、视频录制 |

---

*《人工智能基础B》期末大作业 · 2026*
