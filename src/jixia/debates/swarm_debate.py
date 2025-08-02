#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
稷下学宫Swarm辩论系统 - 统一版本
支持OpenRouter和Ollama两种模式的八仙论道
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import random
import os

try:
    from swarm import Swarm, Agent
    SWARM_AVAILABLE = True
except ImportError:
    print("⚠️ OpenAI Swarm未安装，请运行: pip install git+https://github.com/openai/swarm.git")
    SWARM_AVAILABLE = False

class JixiaSwarmDebate:
    """稷下学宫Swarm辩论系统 - 统一版本"""
    
    def __init__(self, mode: str = "openrouter", ollama_url: str = "http://100.99.183.38:11434", model: str = "qwen3:8b"):
        """
        初始化辩论系统
        
        Args:
            mode: 运行模式 ("openrouter" 或 "ollama")
            ollama_url: Ollama服务地址
            model: 使用的模型名称
        """
        if not SWARM_AVAILABLE:
            raise ImportError("OpenAI Swarm未安装")
        
        self.mode = mode
        self.ollama_url = ollama_url
        self.model = model
        
        # 初始化客户端
        self.client = self._initialize_client()
        
        # 八仙配置
        self.immortals = {
            '吕洞宾': {
                'role': '技术分析专家',
                'stance': 'positive',
                'specialty': '技术分析和图表解读',
                'style': '犀利直接，一剑封喉',
                'bagua': '乾卦 - 主动进取'
            },
            '何仙姑': {
                'role': '风险控制专家', 
                'stance': 'negative',
                'specialty': '风险评估和资金管理',
                'style': '温和坚定，关注风险',
                'bagua': '坤卦 - 稳健保守'
            },
            '张果老': {
                'role': '历史数据分析师',
                'stance': 'positive', 
                'specialty': '历史回测和趋势分析',
                'style': '博古通今，从历史找规律',
                'bagua': '兑卦 - 传统价值'
            },
            '铁拐李': {
                'role': '逆向投资大师',
                'stance': 'negative',
                'specialty': '逆向思维和危机发现', 
                'style': '不拘一格，挑战共识',
                'bagua': '巽卦 - 逆向思维'
            }
        }
        
        # 创建智能体
        self.agents = self._create_agents()
        
    def _initialize_client(self) -> Optional[Swarm]:
        """初始化Swarm客户端"""
        try:
            from openai import OpenAI
            
            if self.mode == "ollama":
                # Ollama模式
                openai_client = OpenAI(
                    api_key="ollama",  # Ollama不需要真实的API密钥
                    base_url=f"{self.ollama_url}/v1"
                )
                print(f"🦙 使用本地Ollama服务: {self.ollama_url}")
                print(f"🤖 使用模型: {self.model}")
                
            else:
                # OpenRouter模式
                api_key = self._get_openrouter_key()
                if not api_key:
                    print("❌ 未找到OpenRouter API密钥")
                    return None
                
                openai_client = OpenAI(
                    api_key=api_key,
                    base_url="https://openrouter.ai/api/v1",
                    default_headers={
                        "HTTP-Referer": "https://github.com/ben/liurenchaxin",
                        "X-Title": "Jixia Academy Swarm Debate"
                    }
                )
                print(f"🌐 使用OpenRouter服务")
                print(f"🔑 API密钥: {api_key[:20]}...")
            
            return Swarm(client=openai_client)
            
        except Exception as e:
            print(f"❌ 客户端初始化失败: {e}")
            return None
    
    def _get_openrouter_key(self) -> Optional[str]:
        """获取OpenRouter API密钥"""
        # 尝试从配置管理获取
        try:
            from config.doppler_config import get_openrouter_key
            return get_openrouter_key()
        except ImportError:
            pass
        
        # 尝试从环境变量获取
        api_keys = [
            os.getenv('OPENROUTER_API_KEY_1'),
            os.getenv('OPENROUTER_API_KEY_2'), 
            os.getenv('OPENROUTER_API_KEY_3'),
            os.getenv('OPENROUTER_API_KEY_4')
        ]
        
        for key in api_keys:
            if key and key.startswith('sk-'):
                return key
        
        return None
    
    def _create_agents(self) -> Dict[str, Agent]:
        """创建八仙智能体"""
        if not self.client:
            return {}
            
        agents = {}
        
        # 吕洞宾 - 技术分析专家
        agents['吕洞宾'] = Agent(
            name="LuDongbin",
            instructions="""
            你是吕洞宾，八仙之首，技术分析专家。
            
            你的特点：
            - 擅长技术分析和图表解读
            - 立场：看涨派，善于发现投资机会
            - 风格：犀利直接，一剑封喉
            - 八卦：乾卦 - 主动进取
            
            在辩论中：
            1. 从技术分析角度分析市场
            2. 使用具体的技术指标支撑观点（如RSI、MACD、均线等）
            3. 保持看涨的乐观态度
            4. 发言以"吕洞宾曰："开头
            5. 发言控制在100字以内，简洁有力
            6. 发言完毕后说"请何仙姑继续论道"
            
            请用古雅但现代的语言风格，结合专业的技术分析。
            """,
            functions=[self._to_hexiangu]
        )
        
        # 何仙姑 - 风险控制专家
        agents['何仙姑'] = Agent(
            name="HeXiangu", 
            instructions="""
            你是何仙姑，八仙中唯一的女仙，风险控制专家。
            
            你的特点：
            - 擅长风险评估和资金管理
            - 立场：看跌派，关注投资风险
            - 风格：温和坚定，关注风险控制
            - 八卦：坤卦 - 稳健保守
            
            在辩论中：
            1. 从风险控制角度分析市场
            2. 指出潜在的投资风险和危险信号
            3. 保持谨慎的态度，强调风险管理
            4. 发言以"何仙姑曰："开头
            5. 发言控制在100字以内，温和但坚定
            6. 发言完毕后说"请张果老继续论道"
            
            请用温和但专业的语调，体现女性的细致和关怀。
            """,
            functions=[self._to_zhangguolao]
        )
        
        # 张果老 - 历史数据分析师
        agents['张果老'] = Agent(
            name="ZhangGuoLao",
            instructions="""
            你是张果老，历史数据分析师。
            
            你的特点：
            - 擅长历史回测和趋势分析
            - 立场：看涨派，从历史中寻找机会
            - 风格：博古通今，从历史中找规律
            - 八卦：兑卦 - 传统价值
            
            在辩论中：
            1. 从历史数据角度分析市场
            2. 引用具体的历史案例和数据
            3. 保持乐观的投资态度
            4. 发言以"张果老曰："开头
            5. 发言控制在100字以内，引经据典
            6. 发言完毕后说"请铁拐李继续论道"
            
            请用博学的语调，多引用历史数据和案例。
            """,
            functions=[self._to_tieguaili]
        )
        
        # 铁拐李 - 逆向投资大师
        agents['铁拐李'] = Agent(
            name="TieGuaiLi",
            instructions="""
            你是铁拐李，逆向投资大师。
            
            你的特点：
            - 擅长逆向思维和危机发现
            - 立场：看跌派，挑战主流观点
            - 风格：不拘一格，敢于质疑
            - 八卦：巽卦 - 逆向思维
            
            在辩论中：
            1. 从逆向投资角度分析市场
            2. 挑战前面三位仙人的观点
            3. 寻找市场的潜在危机和泡沫
            4. 发言以"铁拐李曰："开头
            5. 作为最后发言者，要总结四仙观点并给出结论
            6. 发言控制在150字以内，包含总结
            
            请用直率犀利的语言，体现逆向思维的独特视角。
            """,
            functions=[]  # 最后一个，不需要转换
        )
        
        return agents
    
    def _to_hexiangu(self):
        """转到何仙姑"""
        return self.agents['何仙姑']
    
    def _to_zhangguolao(self):
        """转到张果老"""
        return self.agents['张果老']
    
    def _to_tieguaili(self):
        """转到铁拐李"""
        return self.agents['铁拐李']
    
    async def conduct_debate(self, topic: str, context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        进行八仙辩论
        
        Args:
            topic: 辩论主题
            context: 市场背景信息
            
        Returns:
            辩论结果
        """
        if not self.client:
            print("❌ 客户端未初始化，无法进行辩论")
            return None
        
        print("🏛️ 稷下学宫八仙论道开始！")
        print("=" * 60)
        print(f"🎯 论道主题: {topic}")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔧 运行模式: {self.mode.upper()}")
        if self.mode == "ollama":
            print(f"🦙 Ollama服务: {self.ollama_url}")
        print()
        
        # 构建初始提示
        prompt = self._build_prompt(topic, context)
        
        try:
            print("⚔️ 吕洞宾仙长请先发言...")
            print("-" * 40)
            
            # 开始辩论
            model_override = self.model if self.mode == "ollama" else "openai/gpt-3.5-turbo"
            
            response = self.client.run(
                agent=self.agents['吕洞宾'],
                messages=[{"role": "user", "content": prompt}],
                max_turns=10,
                model_override=model_override
            )
            
            print("\n" + "=" * 60)
            print("🎊 八仙论道圆满结束！")
            
            # 处理结果
            result = self._process_result(response, topic, context)
            self._display_summary(result)
            
            return result
            
        except Exception as e:
            print(f"❌ 论道过程中出错: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _build_prompt(self, topic: str, context: Dict[str, Any] = None) -> str:
        """构建辩论提示"""
        context_str = ""
        if context:
            context_str = f"\n📊 市场背景:\n{json.dumps(context, indent=2, ensure_ascii=False)}\n"
        
        prompt = f"""
        🏛️ 稷下学宫八仙论道正式开始！
        
        📜 论道主题: {topic}
        {context_str}
        
        🎭 论道规则:
        1. 四仙按序发言：吕洞宾 → 何仙姑 → 张果老 → 铁拐李
        2. 正反方交替：吕洞宾(看涨) → 何仙姑(看跌) → 张果老(看涨) → 铁拐李(看跌)
        3. 每位仙人从专业角度分析，提供具体数据支撑
        4. 可以质疑前面仙人的观点，但要有理有据
        5. 保持仙风道骨的表达风格，但要专业
        6. 每次发言简洁有力，控制在100字以内
        7. 铁拐李作为最后发言者要总结观点
        8. 体现各自的八卦属性和投资哲学
        
        🗡️ 请吕洞宾仙长首先发言！
        记住：你是技术分析专家，要从技术面找到投资机会！
        发言要简洁有力，一剑封喉！
        """
        return prompt
    
    def _process_result(self, response, topic: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """处理辩论结果"""
        messages = response.messages if hasattr(response, 'messages') else []
        
        debate_messages = []
        for msg in messages:
            if msg.get('role') == 'assistant' and msg.get('content'):
                content = msg['content']
                speaker = self._extract_speaker(content)
                
                debate_messages.append({
                    'speaker': speaker,
                    'content': content,
                    'timestamp': datetime.now().isoformat(),
                    'stance': self.immortals.get(speaker, {}).get('stance', 'unknown'),
                    'specialty': self.immortals.get(speaker, {}).get('specialty', ''),
                    'bagua': self.immortals.get(speaker, {}).get('bagua', '')
                })
        
        return {
            "debate_id": f"jixia_swarm_{self.mode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "topic": topic,
            "context": context,
            "messages": debate_messages,
            "final_output": debate_messages[-1]['content'] if debate_messages else "",
            "timestamp": datetime.now().isoformat(),
            "framework": f"OpenAI Swarm + {self.mode.upper()}",
            "model": self.model,
            "mode": self.mode,
            "participants": list(self.immortals.keys())
        }
    
    def _extract_speaker(self, content: str) -> str:
        """从内容中提取发言者"""
        for name in self.immortals.keys():
            if f"{name}曰" in content:
                return name
        return "未知仙人"
    
    def _display_summary(self, result: Dict[str, Any]):
        """显示辩论总结"""
        print("\n🌟 八仙论道总结")
        print("=" * 60)
        print(f"📜 主题: {result['topic']}")
        print(f"⏰ 时间: {result['timestamp']}")
        print(f"🔧 框架: {result['framework']}")
        print(f"🤖 模型: {result['model']}")
        print(f"💬 发言数: {len(result['messages'])}条")
        
        # 统计正反方观点
        positive_count = len([m for m in result['messages'] if m.get('stance') == 'positive'])
        negative_count = len([m for m in result['messages'] if m.get('stance') == 'negative'])
        
        print(f"📊 观点分布: 看涨{positive_count}条, 看跌{negative_count}条")
        
        # 显示参与者
        participants = ", ".join(result['participants'])
        print(f"🎭 参与仙人: {participants}")
        
        print("\n🏆 最终总结:")
        print("-" * 40)
        if result['messages']:
            print(result['final_output'])
        
        print("\n✨ Swarm辩论特色:")
        if self.mode == "ollama":
            print("🦙 使用本地Ollama，无需API密钥")
            print("🔒 完全本地运行，数据安全")
        else:
            print("🌐 使用OpenRouter，模型选择丰富")
            print("☁️ 云端运行，性能强劲")
        print("🗡️ 八仙各展所长，观点多元")
        print("⚖️ 正反方交替，辩论激烈")
        print("🚀 基于Swarm，智能体协作")
        print("🎯 八卦哲学，投资智慧")

# 便捷函数
async def start_openrouter_debate(topic: str, context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    """启动OpenRouter模式的辩论"""
    debate = JixiaSwarmDebate(mode="openrouter")
    return await debate.conduct_debate(topic, context)

async def start_ollama_debate(topic: str, context: Dict[str, Any] = None, 
                             ollama_url: str = "http://100.99.183.38:11434", 
                             model: str = "qwen3:8b") -> Optional[Dict[str, Any]]:
    """启动Ollama模式的辩论"""
    debate = JixiaSwarmDebate(mode="ollama", ollama_url=ollama_url, model=model)
    return await debate.conduct_debate(topic, context)

# 主函数
async def main():
    """主函数 - 演示八仙论道"""
    print("🏛️ 稷下学宫Swarm辩论系统")
    print("🚀 支持OpenRouter和Ollama两种模式")
    print()
    
    # 选择运行模式
    mode = input("请选择运行模式 (openrouter/ollama) [默认: ollama]: ").strip().lower()
    if not mode:
        mode = "ollama"
    
    # 辩论主题
    topics = [
        "英伟达股价走势：AI泡沫还是技术革命？",
        "美联储2024年货币政策：加息还是降息？", 
        "比特币vs黄金：谁是更好的避险资产？",
        "中国房地产市场：触底反弹还是继续下行？",
        "特斯拉股价：马斯克效应还是基本面支撑？"
    ]
    
    # 随机选择主题
    topic = random.choice(topics)
    
    # 市场背景
    context = {
        "market_sentiment": "谨慎乐观",
        "volatility": "中等",
        "key_events": ["财报季", "央行会议", "地缘政治"],
        "technical_indicators": {
            "RSI": 65,
            "MACD": "金叉",
            "MA20": "上穿"
        }
    }
    
    # 开始辩论
    if mode == "ollama":
        result = await start_ollama_debate(topic, context)
    else:
        result = await start_openrouter_debate(topic, context)
    
    if result:
        print(f"\n🎉 辩论成功！ID: {result['debate_id']}")
        print(f"📁 使用模式: {result['mode']}")
        print(f"🤖 使用模型: {result['model']}")
    else:
        print("❌ 辩论失败")

if __name__ == "__main__":
    asyncio.run(main())