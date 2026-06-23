# -*- coding: utf-8 -*-
"""
农作物病害智能识别与诊断系统 - 主程序
基于 EfficientNet + 大语言模型 (LLM) 的 Streamlit 可视化应用
"""

import os
import sys
import json
import time
import base64
import datetime
import io
import random

import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import Config
from models.model import get_predictor
from llm.llm_api import get_llm_client
from utils.class_info import DISEASE_INFO, PLANT_TYPES, get_severity_color

# ============================================================
#  页面初始化配置
# ============================================================
st.set_page_config(
    page_title="农作物病害智能识别系统",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
#  自定义 CSS 样式（深绿农业主题）
# ============================================================
st.markdown("""
<style>
/* 主色调 */
:root {
    --primary: #2E7D32;
    --primary-light: #4CAF50;
    --accent: #FF6F00;
    --bg-card: #F9FBF9;
    --border-light: #C8E6C9;
}

/* 顶部标题栏 */
.main-header {
    background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #388E3C 100%);
    color: white;
    padding: 20px 30px;
    border-radius: 12px;
    margin-bottom: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(46,125,50,0.3);
}
.main-header h1 { font-size: 2.0rem; margin: 0; font-weight: 700; }
.main-header p  { font-size: 0.95rem; margin: 6px 0 0; opacity: 0.9; }

/* 结果卡片 */
.result-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-left: 5px solid var(--primary-light);
    border-radius: 10px;
    padding: 18px 22px;
    margin: 10px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* 危害等级标签 */
.severity-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-left: 8px;
}
.severity-none     { background: #E8F5E9; color: #2E7D32; }
.severity-moderate { background: #FFF8E1; color: #F57F17; }
.severity-severe   { background: #FBE9E7; color: #BF360C; }
.severity-fatal    { background: #FCE4EC; color: #880E4F; }

/* 置信度进度条自定义 */
.confidence-bar { 
    height: 8px; 
    border-radius: 4px; 
    background: linear-gradient(90deg, #4CAF50, #8BC34A); 
}

/* Demo 模式警告条 */
.demo-banner {
    background: linear-gradient(90deg, #FF6F00, #FFA000);
    color: white;
    padding: 8px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    font-size: 0.88rem;
    text-align: center;
}

/* 指标卡片 */
.metric-card {
    background: white;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-top: 3px solid var(--primary-light);
}
.metric-value { font-size: 1.8rem; font-weight: 700; color: var(--primary); }
.metric-label { font-size: 0.82rem; color: #666; margin-top: 4px; }

/* 上传区域美化 */
section[data-testid="stFileUploader"] > div {
    border: 2px dashed #A5D6A7 !important;
    border-radius: 12px !important;
    background: #F1F8E9 !important;
}

/* 侧边栏 */
.sidebar-title { color: #2E7D32; font-weight: 700; font-size: 1.1rem; }

/* 按钮样式 */
.stButton > button {
    background: linear-gradient(135deg, #2E7D32, #4CAF50);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    transition: all 0.3s;
}
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(46,125,50,0.4); }
</style>
""", unsafe_allow_html=True)


# ============================================================
#  工具函数
# ============================================================
def load_history() -> list:
    """加载历史记录"""
    if os.path.exists(Config.HISTORY_FILE):
        try:
            with open(Config.HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(history: list):
    """保存历史记录"""
    os.makedirs(os.path.dirname(Config.HISTORY_FILE), exist_ok=True)
    with open(Config.HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-Config.MAX_HISTORY:], f, ensure_ascii=False, indent=2)


def add_history_record(record: dict):
    """添加一条历史记录"""
    history = load_history()
    history.append(record)
    save_history(history)


def pil_to_base64(img: Image.Image) -> str:
    """PIL 图像转 base64（用于内嵌显示）"""
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def get_severity_class(severity: str) -> str:
    """获取危害等级 CSS 类名"""
    mapping = {
        "无": "severity-none",
        "中度": "severity-moderate",
        "重度": "severity-severe",
        "毁灭性": "severity-fatal"
    }
    return mapping.get(severity, "severity-moderate")


def draw_confidence_chart(results: list) -> go.Figure:
    """绘制置信度水平柱状图"""
    zh_names = [r["zh_name"] for r in results]
    confidences = [r["confidence"] * 100 for r in results]
    colors = [r.get("color", "#4CAF50") for r in results]

    fig = go.Figure(go.Bar(
        x=confidences,
        y=zh_names,
        orientation="h",
        marker=dict(
            color=confidences,
            colorscale=[[0, "#A5D6A7"], [0.5, "#4CAF50"], [1, "#1B5E20"]],
            showscale=False,
            line=dict(width=0)
        ),
        text=[f"{c:.1f}%" for c in confidences],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>置信度: %{x:.2f}%<extra></extra>"
    ))
    fig.update_layout(
        title=dict(text="🔬 预测置信度分布", font=dict(size=14)),
        xaxis=dict(title="置信度 (%)", range=[0, 115], gridcolor="#E8F5E9"),
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=280,
        margin=dict(l=10, r=40, t=40, b=30),
        font=dict(family="Microsoft YaHei, Arial", size=12)
    )
    return fig


def draw_history_trend(history: list) -> go.Figure:
    """绘制历史检测趋势图"""
    if not history:
        return None

    df = pd.DataFrame(history[-30:])  # 最近30条
    if "timestamp" not in df.columns:
        return None

    disease_counts = df["zh_name"].value_counts().head(10)
    
    fig = go.Figure(go.Bar(
        x=disease_counts.values,
        y=disease_counts.index,
        orientation="h",
        marker_color="#4CAF50",
        hovertemplate="<b>%{y}</b><br>检测次数: %{x}<extra></extra>"
    ))
    fig.update_layout(
        title=dict(text="📊 历史检测病害统计（最近30次）", font=dict(size=14)),
        xaxis=dict(title="检测次数", gridcolor="#E8F5E9"),
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=350,
        margin=dict(l=10, r=20, t=40, b=30),
        font=dict(family="Microsoft YaHei, Arial", size=12)
    )
    return fig


# ============================================================
#  Session State 初始化
# ============================================================
if "predictor" not in st.session_state:
    with st.spinner("🔄 正在加载 AI 模型..."):
        st.session_state["predictor"] = get_predictor()

if "llm_client" not in st.session_state:
    with st.spinner("🤖 正在初始化大语言模型..."):
        st.session_state["llm_client"] = get_llm_client()

if "history" not in st.session_state:
    st.session_state["history"] = load_history()

if "last_results" not in st.session_state:
    st.session_state["last_results"] = None

if "current_context_disease" not in st.session_state:
    st.session_state["current_context_disease"] = None

predictor  = st.session_state["predictor"]
llm_client = st.session_state["llm_client"]


# ============================================================
#  顶部标题
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🌿 农作物病害智能识别与诊断系统</h1>
    <p>基于 EfficientNet + 大语言模型 (LLM) | PlantVillage 数据集 | 38类 · 87,000+ 样本</p>
</div>
""", unsafe_allow_html=True)

# 演示模式提示
if predictor.demo_mode:
    st.markdown("""
    <div class="demo-banner">
        ⚠️ <b>当前运行在演示模式</b>：未检测到训练好的模型权重，预测结果为模拟数据，仅供界面功能展示。
        如需使用真实模型，请运行 <code>py models/train.py</code> 进行训练。
    </div>
    """, unsafe_allow_html=True)


# ============================================================
#  侧边栏配置
# ============================================================
with st.sidebar:
    st.markdown('<p class="sidebar-title">⚙️ 系统设置</p>', unsafe_allow_html=True)
    st.divider()

    # LLM API 配置
    st.markdown("**🤖 大模型 API 配置**")
    api_key_input = st.text_input(
        "通义千问 API Key",
        value=Config.LLM_API_KEY,
        type="password",
        placeholder="sk-xxxxxxxxxxxxxxxxxx",
        help="填入后即可启用 AI 智能诊断报告生成"
    )
    if api_key_input and api_key_input != Config.LLM_API_KEY:
        Config.LLM_API_KEY = api_key_input
        st.session_state["llm_client"] = None  # 重置客户端
        llm_client = get_llm_client()
        st.session_state["llm_client"] = llm_client
        st.success("✅ API Key 已更新")

    st.divider()

    # 检测参数
    st.markdown("**🎯 检测参数**")
    top_k = st.slider("显示前 K 个预测结果", 3, 8, 5)
    conf_threshold = st.slider("置信度显示阈值", 0.0, 1.0, 0.05, step=0.05,
                                help="低于此阈值的预测结果不显示")
    
    st.divider()

    # 植物过滤器
    st.markdown("**🌱 植物种类筛选**")
    selected_plant = st.selectbox(
        "仅显示特定植物",
        ["全部"] + PLANT_TYPES
    )
    
    st.divider()

    # 统计信息
    st.markdown("**📈 本次会话统计**")
    col1, col2 = st.columns(2)
    col1.metric("检测次数", len(st.session_state["history"]))
    col2.metric("AI 报告", "已启用" if llm_client.provider != "mock" else "演示中")

    st.divider()
    st.markdown("**ℹ️ 关于本系统**")
    st.markdown("""
- 🤖 模型: EfficientNet-B0
- 📊 数据集: PlantVillage
- 🌿 覆盖作物: 14种
- 🦠 病害类别: 38类
- 🎓 《人工智能基础B》期末项目
""")


# ============================================================
#  主内容区 — 标签页
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["🔍 病害识别", "📊 历史记录", "📖 病害知识库", "❓ AI 问诊"]
)


# ──────────────────────────────────────────────────────────
#  TAB 1: 病害识别
# ──────────────────────────────────────────────────────────
with tab1:
    col_upload, col_result = st.columns([1, 1.4], gap="large")

    with col_upload:
        st.subheader("📤 上传植物叶片图片")
        
        # 上传方式选择
        upload_mode = st.radio("输入方式", ["📁 本地上传", "📷 摄像头拍摄"], horizontal=True)
        
        image = None
        
        if upload_mode == "📁 本地上传":
            uploaded_file = st.file_uploader(
                "拖拽或点击上传图片",
                type=["jpg", "jpeg", "png", "bmp", "webp"],
                help="支持 JPG/PNG/BMP/WEBP 格式，建议图片清晰、叶片完整可见"
            )
            if uploaded_file:
                image = Image.open(uploaded_file).convert("RGB")
        else:
            camera_photo = st.camera_input("📸 拍摄叶片照片")
            if camera_photo:
                image = Image.open(camera_photo).convert("RGB")

        if image:
            # 显示上传的图片
            st.image(image, caption="📷 待检测图片", use_container_width=True)
            
            # 图片基本信息
            with st.expander("🔍 图片详情"):
                w, h = image.size
                st.markdown(f"""
                | 属性 | 值 |
                |------|------|
                | 尺寸 | {w} × {h} 像素 |
                | 模式 | {image.mode} |
                | 大小 | {w*h/1024:.1f} K像素 |
                """)
            
            # 检测按钮
            if st.button("🚀 开始智能识别", use_container_width=True):
                with st.spinner("🔬 AI 模型分析中..."):
                    start_time = time.time()
                    results = predictor.predict(image, top_k=top_k)
                    elapsed = time.time() - start_time
                
                # 过滤置信度和植物种类
                filtered = [r for r in results if r["confidence"] >= conf_threshold]
                if selected_plant != "全部":
                    filtered = [r for r in filtered if r["plant"] == selected_plant] or results[:1]
                
                st.session_state["last_results"] = filtered
                st.session_state["inference_time"] = elapsed
                st.session_state["current_context_disease"] = filtered[0]["zh_name"] if filtered else None
                
                # 保存历史
                record = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "zh_name": filtered[0]["zh_name"] if filtered else "未知",
                    "class_name": filtered[0]["class_name"] if filtered else "unknown",
                    "plant": filtered[0]["plant"] if filtered else "未知",
                    "confidence": filtered[0]["confidence"] if filtered else 0,
                    "is_healthy": filtered[0]["is_healthy"] if filtered else False,
                    "is_demo": filtered[0].get("demo_mode", False)
                }
                add_history_record(record)
                st.session_state["history"] = load_history()
                
                st.success(f"✅ 识别完成！推理耗时: {elapsed*1000:.1f} ms")
                st.rerun()

    # ──── 右侧结果区 ────
    with col_result:
        st.subheader("📋 识别结果")
        
        if st.session_state.get("last_results") is None:
            st.info("👈 请在左侧上传植物叶片图片，点击「开始智能识别」查看结果")
            
            # 显示示例效果
            st.markdown("---")
            st.markdown("**📌 支持的植物种类：**")
            plant_cols = st.columns(4)
            emoji_map = {"苹果":"🍎","蓝莓":"🫐","樱桃":"🍒","玉米":"🌽","葡萄":"🍇",
                        "柑橘/橙":"🍊","桃":"🍑","甜椒":"🫑","马铃薯":"🥔","覆盆子":"🍓",
                        "大豆":"🫘","南瓜":"🎃","草莓":"🍓","番茄":"🍅"}
            for i, plant in enumerate(PLANT_TYPES):
                emoji = emoji_map.get(plant, "🌿")
                plant_cols[i % 4].markdown(f"{emoji} {plant}")
        
        else:
            results = st.session_state["last_results"]
            top_result = results[0]
            
            # ── 主要结果卡片 ──
            sev_class = get_severity_class(top_result.get("severity", "中度"))
            
            if top_result["is_healthy"]:
                st.success(f"✅ **检测结论：该植株健康，无明显病害**")
                st.markdown(f"""
                <div class="result-card">
                    <h3>🌿 {top_result['zh_name']}</h3>
                    <p>植物种类：{top_result['plant']} &nbsp;|&nbsp; 
                       置信度：<b style="color:#2E7D32">{top_result['confidence']:.1%}</b> &nbsp;|&nbsp;
                       状态：<span class="severity-badge severity-none">健康</span></p>
                    <p style="color:#555;">{top_result.get('description','植株生长正常，建议保持常规管理。')}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"⚠️ **检测到植物病害：{top_result['zh_name']}**")
                st.markdown(f"""
                <div class="result-card">
                    <h3>🦠 {top_result['zh_name']}</h3>
                    <p>植物种类：{top_result['plant']} &nbsp;|&nbsp; 
                       置信度：<b style="color:#C62828">{top_result['confidence']:.1%}</b> &nbsp;|&nbsp;
                       危害：<span class="severity-badge {sev_class}">{top_result.get('severity','中度')}</span></p>
                    <p><b>典型症状：</b>{top_result.get('symptoms','请参见病害知识库')}</p>
                </div>
                """, unsafe_allow_html=True)

            # ── 置信度图表 ──
            fig = draw_confidence_chart(results)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # ── 前K结果详细列表 ──
            with st.expander(f"📊 查看前 {len(results)} 项预测详情"):
                for i, r in enumerate(results, 1):
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    col_a.markdown(f"**{i}. {r['zh_name']}**")
                    col_b.progress(r["confidence"], text=f"{r['confidence']:.1%}")
                    status = "🟢 健康" if r["is_healthy"] else "🔴 患病"
                    col_c.markdown(status)

            # ── LLM 诊断报告 ──
            st.markdown("---")
            st.subheader("🤖 AI 智能诊断报告")
            
            gen_col1, gen_col2 = st.columns([1, 1])
            
            if gen_col1.button("📝 生成诊断报告", use_container_width=True):
                with st.spinner("🤖 大语言模型正在分析，请稍候..."):
                    report = llm_client.generate_diagnosis(
                        zh_name=top_result["zh_name"],
                        plant=top_result["plant"],
                        confidence=top_result["confidence"],
                        symptoms=top_result.get("symptoms", ""),
                        is_healthy=top_result["is_healthy"]
                    )
                st.session_state["last_report"] = report
            
            if gen_col2.button("🔬 多病害对比分析", use_container_width=True):
                with st.spinner("🤖 对比分析中..."):
                    analysis = llm_client.analyze_predictions(results[:5])
                st.session_state["last_report"] = analysis

            if "last_report" in st.session_state and st.session_state["last_report"]:
                st.markdown(st.session_state["last_report"])
                
                # 导出报告
                st.download_button(
                    label="💾 下载诊断报告 (.md)",
                    data=st.session_state["last_report"].encode("utf-8"),
                    file_name=f"诊断报告_{top_result['zh_name']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown"
                )


# ──────────────────────────────────────────────────────────
#  TAB 2: 历史记录
# ──────────────────────────────────────────────────────────
with tab2:
    st.subheader("📊 检测历史记录")
    
    history = st.session_state["history"]
    
    if not history:
        st.info("📭 暂无历史记录，请先进行病害检测")
    else:
        # 统计摘要
        df_history = pd.DataFrame(history)
        total_scans = len(df_history)
        healthy_count = df_history["is_healthy"].sum() if "is_healthy" in df_history else 0
        diseased_count = total_scans - healthy_count
        
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f"""<div class="metric-card"><div class="metric-value">{total_scans}</div>
                        <div class="metric-label">总检测次数</div></div>""", unsafe_allow_html=True)
        m2.markdown(f"""<div class="metric-card"><div class="metric-value" style="color:#2E7D32">{healthy_count}</div>
                        <div class="metric-label">健康植株</div></div>""", unsafe_allow_html=True)
        m3.markdown(f"""<div class="metric-card"><div class="metric-value" style="color:#C62828">{diseased_count}</div>
                        <div class="metric-label">发现病害</div></div>""", unsafe_allow_html=True)
        avg_conf = df_history["confidence"].mean() if "confidence" in df_history else 0
        m4.markdown(f"""<div class="metric-card"><div class="metric-value">{avg_conf:.1%}</div>
                        <div class="metric-label">平均置信度</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 趋势图
        trend_fig = draw_history_trend(history)
        if trend_fig:
            st.plotly_chart(trend_fig, use_container_width=True, config={"displayModeBar": False})
        
        # 历史数据表格
        st.markdown("**📋 详细记录**")
        display_df = df_history[["timestamp", "zh_name", "plant", "confidence", "is_healthy"]].copy()
        display_df.columns = ["检测时间", "识别结果", "植物种类", "置信度", "是否健康"]
        display_df["置信度"] = display_df["置信度"].apply(lambda x: f"{x:.1%}")
        display_df["是否健康"] = display_df["是否健康"].apply(lambda x: "✅ 健康" if x else "⚠️ 患病")
        st.dataframe(
            display_df.iloc[::-1].reset_index(drop=True),
            use_container_width=True,
            height=350
        )
        
        # 导出和清空
        col_exp, col_clr = st.columns([1, 1])
        if col_exp.button("📥 导出历史记录 (CSV)"):
            csv = display_df.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                "点击下载",
                data=csv.encode("utf-8-sig"),
                file_name=f"检测历史_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        if col_clr.button("🗑️ 清空历史记录", type="secondary"):
            if os.path.exists(Config.HISTORY_FILE):
                os.remove(Config.HISTORY_FILE)
            st.session_state["history"] = []
            st.success("历史记录已清空")
            st.rerun()


# ──────────────────────────────────────────────────────────
#  TAB 3: 病害知识库
# ──────────────────────────────────────────────────────────
with tab3:
    st.subheader("📖 农作物病害知识库")
    st.markdown("覆盖 **14种作物** · **38类病害**，含症状、防治方案、危害等级")
    
    # 搜索和过滤
    search_col, plant_col, status_col = st.columns([2, 1, 1])
    search_kw = search_col.text_input("🔍 搜索病害名称或植物种类", placeholder="例：番茄、白粉病、晚疫病...")
    filter_plant = plant_col.selectbox("植物种类", ["全部"] + PLANT_TYPES, key="kb_plant")
    filter_status = status_col.selectbox("健康状态", ["全部", "病害", "健康"], key="kb_status")
    
    # 过滤结果
    filtered_diseases = {}
    for cls_name, info in DISEASE_INFO.items():
        if search_kw and search_kw.lower() not in info["zh_name"].lower() and \
           search_kw.lower() not in info["plant"].lower():
            continue
        if filter_plant != "全部" and info["plant"] != filter_plant:
            continue
        if filter_status == "病害" and info["is_healthy"]:
            continue
        if filter_status == "健康" and not info["is_healthy"]:
            continue
        filtered_diseases[cls_name] = info

    st.markdown(f"**共找到 {len(filtered_diseases)} 个结果**")
    
    # 按植物分组显示
    plant_groups = {}
    for cls_name, info in filtered_diseases.items():
        plant = info["plant"]
        if plant not in plant_groups:
            plant_groups[plant] = []
        plant_groups[plant].append((cls_name, info))
    
    for plant, items in sorted(plant_groups.items()):
        with st.expander(f"🌿 {plant}（{len(items)} 条）", expanded=len(plant_groups) == 1):
            for cls_name, info in items:
                col_info, col_detail = st.columns([1, 2])
                with col_info:
                    status_icon = "✅" if info["is_healthy"] else "⚠️"
                    sev_class = get_severity_class(info.get("severity", "中度"))
                    st.markdown(f"""
                    **{status_icon} {info['zh_name']}**
                    <span class="severity-badge {sev_class}">{info.get('severity','')}</span>
                    """, unsafe_allow_html=True)
                    if not info["is_healthy"]:
                        st.caption(f"🦠 病原: {info.get('pathogen','未知')[:30]}...")
                
                with col_detail:
                    if not info["is_healthy"]:
                        st.markdown(f"**症状：** {info.get('symptoms','—')[:80]}...")
                        st.markdown(f"**防治：** {info.get('treatment','—')[:80]}...")
                    else:
                        st.markdown(f"**描述：** {info.get('description','—')[:100]}...")
                
                st.divider()


# ──────────────────────────────────────────────────────────
#  TAB 4: AI 问诊
# ──────────────────────────────────────────────────────────
with tab4:
    st.subheader("❓ AI 农业智能问诊")
    st.markdown("由大语言模型驱动，可回答农作物病害识别、防治、种植管理等问题")
    
    # 快捷问题按钮
    st.markdown("**💡 快捷提问：**")
    quick_q_cols = st.columns(3)
    quick_questions = [
        "番茄晚疫病如何快速识别？",
        "马铃薯黄龙病能治好吗？",
        "有机农业如何防治白粉病？",
        "什么农药对玉米大斑病效果好？",
        "叶片出现黄色斑点是什么病？",
        "如何预防果树常见病害？"
    ]
    
    for i, q in enumerate(quick_questions):
        if quick_q_cols[i % 3].button(q, key=f"quick_{i}"):
            st.session_state["qa_input"] = q
    
    # 问题输入
    user_question = st.text_area(
        "输入您的问题",
        value=st.session_state.get("qa_input", ""),
        height=100,
        placeholder="例：番茄叶片出现褐色斑点，中间灰白色，四周有黄圈，请问是什么病？该如何防治？",
        key="qa_text_area"
    )
    
    # 上下文关联
    context = st.session_state.get("current_context_disease")
    if context:
        st.info(f"💡 当前检测到的病害：**{context}**，AI 将结合此背景回答您的问题")
    
    if st.button("🤖 提交问题", use_container_width=True, type="primary"):
        if user_question.strip():
            with st.spinner("🤔 AI 正在思考..."):
                answer = llm_client.answer_question(user_question, context)
            
            st.markdown("---")
            st.markdown("**🤖 AI 诊断建议：**")
            st.markdown(answer)
            
            # 清除快捷问题
            if "qa_input" in st.session_state:
                del st.session_state["qa_input"]
        else:
            st.warning("请输入您的问题")

    st.markdown("---")
    st.markdown("""
    > ⚠️ **免责声明**：本系统的 AI 诊断建议仅供参考，不能替代专业农业技术人员的现场诊断。
    > 对于重要农作物的病害防治，建议联系当地农业技术推广站或植保专家确认。
    """)


# ============================================================
#  底部版权信息
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#9E9E9E; font-size:0.82rem; padding:10px 0;">
    🌿 农作物病害智能识别与诊断系统 &nbsp;|&nbsp; 
    基于 EfficientNet-B0 + LLM &nbsp;|&nbsp;
    《人工智能基础B》期末大作业 &nbsp;|&nbsp; 2026
</div>
""", unsafe_allow_html=True)
