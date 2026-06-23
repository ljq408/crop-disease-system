# -*- coding: utf-8 -*-
"""
大语言模型 (LLM) API 集成模块
支持多种 LLM 提供商：阿里云通义千问、OpenAI 兼容接口、本地 Ollama
"""

import os
import sys
import json
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from llm.prompts import SYSTEM_PROMPT, get_diagnosis_prompt, get_qa_prompt, get_comparison_prompt


class LLMClient:
    """
    大语言模型客户端，支持多种后端
    优先级: Qwen API > OpenAI API > Ollama 本地 > Mock 演示
    """

    def __init__(self):
        self.provider = self._detect_provider()
        print(f"🤖 LLM 服务已就绪，使用提供商: {self.provider}")

    def _detect_provider(self) -> str:
        """自动检测可用的 LLM 提供商"""
        # 1. 检测通义千问 API
        if Config.LLM_API_KEY and Config.LLM_API_KEY != "":
            return "qwen"

        # 2. 检测 OpenAI 兼容接口
        if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != "":
            return "openai"

        # 3. 检测本地 Ollama
        try:
            import requests
            resp = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=2)
            if resp.status_code == 200:
                return "ollama"
        except Exception:
            pass

        # 4. 回退到演示模式
        print("⚠️  未检测到可用的 LLM 配置，使用演示文本（Mock 模式）")
        print("   如需启用 LLM：")
        print("   方案1: 设置环境变量 DASHSCOPE_API_KEY=你的通义千问密钥")
        print("   方案2: 设置 OPENAI_API_KEY=你的OpenAI密钥")
        print("   方案3: 本地安装并启动 Ollama (https://ollama.com)")
        return "mock"

    def chat(self, user_message: str, system_message: str = None,
             stream: bool = False) -> str:
        """
        发送消息到 LLM 并获取回复
        Args:
            user_message: 用户消息
            system_message: 系统提示词（可选）
            stream: 是否使用流式输出（暂未完整实现）
        Returns:
            回复文本
        """
        sys_msg = system_message or SYSTEM_PROMPT

        if self.provider == "qwen":
            return self._call_qwen(sys_msg, user_message)
        elif self.provider == "openai":
            return self._call_openai(sys_msg, user_message)
        elif self.provider == "ollama":
            return self._call_ollama(sys_msg, user_message)
        else:
            return self._mock_response(user_message)

    def _call_qwen(self, system_message: str, user_message: str) -> str:
        """调用阿里云通义千问 API"""
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=Config.LLM_API_KEY,
                base_url=Config.LLM_BASE_URL
            )
            response = client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except ImportError:
            return "❌ 请安装 openai 包: pip install openai"
        except Exception as e:
            return f"❌ 通义千问 API 调用失败: {str(e)}\n\n{self._mock_response(user_message)}"

    def _call_openai(self, system_message: str, user_message: str) -> str:
        """调用 OpenAI 兼容接口"""
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=Config.OPENAI_API_KEY,
                base_url=Config.OPENAI_BASE_URL
            )
            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ OpenAI API 调用失败: {str(e)}\n\n{self._mock_response(user_message)}"

    def _call_ollama(self, system_message: str, user_message: str) -> str:
        """调用本地 Ollama 模型"""
        try:
            import requests
            payload = {
                "model": Config.OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                "stream": False
            }
            response = requests.post(
                f"{Config.OLLAMA_BASE_URL}/api/chat",
                json=payload, timeout=120
            )
            if response.status_code == 200:
                return response.json()["message"]["content"]
            else:
                return f"❌ Ollama 调用失败 (状态码: {response.status_code})"
        except Exception as e:
            return f"❌ Ollama 连接失败: {str(e)}"

    def _mock_response(self, user_message: str) -> str:
        """演示模式：返回预设的模拟诊断报告"""
        return """
> ⚠️ **演示模式**：当前未配置 LLM API，以下为示例报告

---

## 🌱 病害诊断分析报告

**一、病害诊断结论**

根据深度学习模型的图像识别结果，结合植株叶片表现出的典型病征，初步诊断为真菌性叶部病害。该诊断基于叶片病斑形态、颜色分布及扩展规律等关键特征综合判断，置信度较高，建议结合田间实际情况进行核实。

**二、病害危害分析**

- 🔴 该病害属于**中度危害**等级，在适宜条件下（高温高湿）扩展迅速
- 📊 可造成叶面积损失30-50%，显著降低光合效率，影响产量10-30%
- 🌊 病原菌可通过气流、雨水飞溅进行传播，需注意邻株感染

**三、⚡ 紧急处理措施**

- ⚡ **立即摘除**发病严重的叶片，装袋带出田间集中销毁（勿随地丢弃）
- ⚡ **停止大水漫灌**，改为小水勤灌或滴灌，降低田间湿度
- ⚡ **尽快施药**：选用对应杀菌剂全株均匀喷雾，重点喷施叶片背面

**四、系统防治方案**

**化学防治（推荐）：**
1. 苯醚甲环唑（10%水分散粒剂）1000倍液，7天一次
2. 嘧菌酯（250g/L悬浮剂）1500倍液，10天一次  
3. 代森锰锌（80%可湿性粉剂）600倍液，保护性施药

**生物防治：**
1. 枯草芽孢杆菌制剂（100亿芽孢/g）500倍液喷施
2. 木霉菌制剂叶面喷施，增强植株免疫力

**农业防治：**
- 合理密植，改善通风透光条件
- 增施磷钾肥，减少氮肥，增强植株抗病能力
- 收获后彻底清除田间病残体，深翻土壤

**五、防治注意事项**

⚠️ 同一种类药剂不要连续使用3次以上，应轮换使用不同作用机制的药剂，以防病原产生抗药性

⚠️ 施药应在晴天上午10点前或下午4点后进行，避免高温时段，施药后4小时内下雨需补喷

**六、预后展望**

在采取上述防治措施后，若环境条件改善（气温下降、减少雨水），7-14天内病情可有效控制，新叶可正常生长。完全恢复约需3-4周。若处理及时到位，本季产量损失可控制在10%以内。

---

💡 *如需启用智能AI诊断，请配置 DASHSCOPE_API_KEY 环境变量（通义千问）或 OPENAI_API_KEY*
"""

    # ============ 业务方法封装 ============
    def generate_diagnosis(self, zh_name: str, plant: str, confidence: float,
                           symptoms: str, is_healthy: bool) -> str:
        """生成病害诊断报告"""
        prompt = get_diagnosis_prompt(zh_name, plant, confidence, symptoms, is_healthy)
        return self.chat(prompt)

    def answer_question(self, question: str, context_disease: str = None) -> str:
        """回答农业问题"""
        prompt = get_qa_prompt(question, context_disease)
        return self.chat(prompt)

    def analyze_predictions(self, diseases: list) -> str:
        """分析多个预测结果"""
        prompt = get_comparison_prompt(diseases)
        return self.chat(prompt)


# ============ 全局单例 ============
_llm_client_instance = None

def get_llm_client() -> LLMClient:
    """获取 LLM 客户端单例"""
    global _llm_client_instance
    if _llm_client_instance is None:
        _llm_client_instance = LLMClient()
    return _llm_client_instance
