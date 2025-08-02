#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
稷下学宫本地版 - 基于Ollama的四仙辩论系统
使用本地Ollama服务，无需API密钥
"""

import asyncio
import json
from datetime import datetime
from swarm import Swarm, Agent
from typing import Dict, List, Any, Optional
import random

class JixiaOllamaSwarm:
    """稷下学宫本地版 - 使用Ollama的四仙辩论系统"""
    
    def __init__(self):
        # Ollama配置
        self.ollama_base_url = "http://100.99.183.38:11434"
        self.model_name = "gemma3n:e4b"  # 使用你指定的模型
        
        # 初始化Swarm客户端，使用Ollama
        from openai import OpenAI
        openai_client = OpenAI(
            api_key="ollama",  # Ollama不需要真实的API密钥
            base_url=f"{self.ollama_base_url}/v1"
        )
        self.client = Swarm(client=openai_client)
        
        print(f"🦙 使用本地Ollama服务: {self.ollama_base_url}")
        print(f"🤖 使用模型: {self.model_name}")
        
        # 四仙配置
        self.immortals = {
            '吕洞宾': {
                'role': '技术分析专家',
                'stance': 'positive',
                'specialty': '技术分析和图表解读',
                'style': '犀利直接，一剑封喉'
            },
            '何仙姑': {
                'role': '风险控制专家', 
                'stance': 'negative',
                'specialty': '风险评估和资金管理',
                'style': '温和坚定，关注风险'
            },
            '张果老': {
                'role': '历史数据分析师',
                'stance': 'positive', 
                'specialty': '历史回测和趋势分析',
                'style': '博古通今，从历史找规律'
            },
            '铁拐李': {
                'role': '逆向投资大师',
                'stance': 'negative',
                'specialty': '逆向思维和危机发现', 
                'style': '不拘一格，挑战共识'
            }
        }
        
        # 创建智能体
        self.agents = self.create_agents()
        
    def create_agents(self) -> Dict[str, Agent]:
        """创建四仙智能体"""
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
            
            在辩论中：
            1. 从技术分析角度分析市场
            2. 使用具体的技术指标支撑观点（如RSI、MACD、均线等）
            3. 保持看涨的乐观态度
            4. 发言以"吕洞宾曰："开头
            5. 发言控制在100字以内，简洁有力
            6. 发言完毕后说"请何仙姑继续论道"
            
            请用古雅但现代的语言风格，结合专业的技术分析。
            """,
            functions=[self.to_hexiangu]
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
            
            在辩论中：
            1. 从风险控制角度分析市场
            2. 指出潜在的投资风险和危险信号
            3. 保持谨慎的态度，强调风险管理
            4. 发言以"何仙姑曰："开头
            5. 发言控制在100字以内，温和但坚定
            6. 发言完毕后说"请张果老继续论道"
            
            请用温和但专业的语调，体现女性的细致和关怀。
            """,
            functions=[self.to_zhangguolao]
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
            
            在辩论中：
            1. 从历史数据角度分析市场
            2. 引用具体的历史案例和数据
            3. 保持乐观的投资态度
            4. 发言以"张果老曰："开头
            5. 发言控制在100字以内，引经据典
            6. 发言完毕后说"请铁拐李继续论道"
            
            请用博学的语调，多引用历史数据和案例。
            """,
            functions=[self.to_tieguaili]
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
    
    def to_hexiangu(self):
        """转到何仙姑"""
        return self.agents['何仙姑']
    
    def to_zhangguolao(self):
        """转到张果老"""
        return self.agents['张果老']
    
    def to_tieguaili(self):
        """转到铁拐李"""
        return self.agents['铁拐李']
    
    async def conduct_debate(self, topic: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """进行四仙辩论"""
        print("🏛️ 稷下学宫四仙论道开始！")
        print("=" * 60)
        print(f"🎯 论道主题: {topic}")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🦙 使用本地Ollama: {self.ollama_base_url}")
        print()
        
        # 构建初始提示
        prompt = self.build_prompt(topic, context)
        
        try:
            print("⚔️ 吕洞宾仙长请先发言...")
            print("-" * 40)
            
            # 开始辩论
            response = self.client.run(
                agent=self.agents['吕洞宾'],
                messages=[{"role": "user", "content": prompt}],
                max_turns=8,  # 四仙各发言一次，加上可能的交互
                model_override=self.model_name
            )
            
            print("\n" + "=" * 60)
            print("🎊 四仙论道圆满结束！")
            
            # 处理结果
            result = self.process_result(response, topic, context)
            self.display_summary(result)
            
            return result
            
        except Exception as e:
            print(f"❌ 论道过程中出错: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def build_prompt(self, topic: str, context: Dict[str, Any] = None) -> str:
        """构建辩论提示"""
        context_str = ""
        if context:
            context_str = f"\n📊 市场背景:\n{json.dumps(context, indent=2, ensure_ascii=False)}\n"
        
        prompt = f"""
        🏛️ 稷下学宫四仙论道正式开始！
        
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
        
        🗡️ 请吕洞宾仙长首先发言！
        记住：你是技术分析专家，要从技术面找到投资机会！
        发言要简洁有力，一剑封喉！
        """
        return prompt
    
    def process_result(self, response, topic: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """处理辩论结果"""
        messages = response.messages if hasattr(response, 'messages') else []
        
        debate_messages = []
        for msg in messages:
            if msg.get('role') == 'assistant' and msg.get('content'):
                content = msg['content']
                speaker = self.extract_speaker(content)
                
                debate_messages.append({
                    'speaker': speaker,
                    'content': content,
                    'timestamp': datetime.now().isoformat(),
                    'stance': self.immortals.get(speaker, {}).get('stance', 'unknown')
                })
        
        return {
            "debate_id": f"jixia_ollama_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "topic": topic,
            "context": context,
            "messages": debate_messages,
            "final_output": debate_messages[-1]['content'] if debate_messages else "",
            "timestamp": datetime.now().isoformat(),
            "framework": "OpenAI Swarm + Ollama",
            "model": self.model_name,
            "ollama_url": self.ollama_base_url
        }
    
    def extract_speaker(self, content: str) -> str:
        """从内容中提取发言者"""
        for name in self.immortals.keys():
            if f"{name}曰" in content:
                return name
        return "未知仙人"
    
    def display_summary(self, result: Dict[str, Any]):
        """显示辩论总结"""
        print("\n🌟 四仙论道总结")
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
        
        print("\n🏆 最终总结:")
        print("-" * 40)
        if result['messages']:
            print(result['final_output'])
        
        print("\n✨ 本地辩论特色:")
        print("🦙 使用本地Ollama，无需API密钥")
        print("🗡️ 四仙各展所长，观点多元")
        print("⚖️ 正反方交替，辩论激烈")
        print("🚀 基于Swarm，性能优越")
        print("🔒 完全本地运行，数据安全")

# 主函数
async def main():
    """主函数"""
    print("🏛️ 稷下学宫本地版 - Ollama + Swarm")
    print("🦙 使用本地Ollama服务，无需API密钥")
    print("🚀 四仙论道，完全本地运行")
    print()
    
    # 创建辩论系统
    academy = JixiaOllamaSwarm()
    
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
    result = await academy.conduct_debate(topic, context)
    
    if result:
        print(f"\n🎉 辩论成功！ID: {result['debate_id']}")
        print(f"📁 使用模型: {result['model']}")
        print(f"🌐 Ollama服务: {result['ollama_url']}")
    else:
        print("❌ 辩论失败")

if __name__ == "__main__":
    asyncio.run(main())