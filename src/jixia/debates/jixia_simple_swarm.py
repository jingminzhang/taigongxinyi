#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
稷下学宫简化版 - 基于OpenAI Swarm的四仙辩论系统
避免复杂的函数名称问题，专注于辩论效果
"""

import os
import asyncio
import json
from datetime import datetime
from swarm import Swarm, Agent
from typing import Dict, List, Any, Optional
import random

class JixiaSimpleSwarm:
    """稷下学宫简化版 - 四仙辩论系统"""
    
    def __init__(self):
        # 使用Doppler配置
        try:
            from config.doppler_config import get_doppler_manager
            manager = get_doppler_manager()
            manager.load_config(force_doppler=True)
            print("🔐 使用Doppler配置")
        except Exception as e:
            print(f"❌ Doppler配置失败: {e}")
            raise
        
        # 获取API密钥
        self.api_key = self.get_api_key()
        
        if self.api_key:
            # 初始化Swarm客户端
            from openai import OpenAI
            openai_client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "https://github.com/ben/cauldron",
                    "X-Title": "Jixia Academy"
                }
            )
            self.client = Swarm(client=openai_client)
        else:
            self.client = None
        
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
        
    def get_api_key(self):
        """获取API密钥"""
        api_keys = [
            os.getenv('OPENROUTER_API_KEY_1'),
            os.getenv('OPENROUTER_API_KEY_2'), 
            os.getenv('OPENROUTER_API_KEY_3'),
            os.getenv('OPENROUTER_API_KEY_4')
        ]
        
        for key in api_keys:
            if key and key.startswith('sk-'):
                print(f"✅ 找到API密钥: {key[:20]}...")
                return key
        
        print("❌ 未找到有效的API密钥")
        return None
    
    def create_agents(self) -> Dict[str, Agent]:
        """创建四仙智能体"""
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
            
            在辩论中：
            1. 从技术分析角度分析市场
            2. 使用具体的技术指标支撑观点
            3. 保持看涨的乐观态度
            4. 发言以"吕洞宾曰："开头
            5. 发言完毕后说"请何仙姑继续论道"
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
            2. 指出潜在的投资风险
            3. 保持谨慎的态度
            4. 发言以"何仙姑曰："开头
            5. 发言完毕后说"请张果老继续论道"
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
            2. 引用历史案例和数据
            3. 保持乐观的投资态度
            4. 发言以"张果老曰："开头
            5. 发言完毕后说"请铁拐李继续论道"
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
            2. 挑战前面仙人的观点
            3. 寻找市场的潜在危机
            4. 发言以"铁拐李曰："开头
            5. 作为最后发言者，要总结四仙观点并给出结论
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
        if not self.client:
            print("❌ 客户端未初始化，无法进行辩论")
            return None
        
        print("🏛️ 稷下学宫四仙论道开始！")
        print("=" * 60)
        print(f"🎯 论道主题: {topic}")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
                max_turns=10,
                model_override="openai/gpt-3.5-turbo"  # 使用稳定的模型
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
        4. 可以质疑前面仙人的观点
        5. 保持仙风道骨的表达风格
        6. 铁拐李作为最后发言者要总结观点
        
        🗡️ 请吕洞宾仙长首先发言！
        记住：你是技术分析专家，要从技术面找到投资机会！
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
                    'timestamp': datetime.now().isoformat()
                })
        
        return {
            "debate_id": f"jixia_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "topic": topic,
            "context": context,
            "messages": debate_messages,
            "final_output": debate_messages[-1]['content'] if debate_messages else "",
            "timestamp": datetime.now().isoformat(),
            "framework": "OpenAI Swarm (Simplified)"
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
        print(f"💬 发言数: {len(result['messages'])}条")
        
        print("\n🏆 最终总结:")
        print("-" * 40)
        if result['messages']:
            print(result['final_output'])
        
        print("\n✨ 辩论特色:")
        print("🗡️ 四仙各展所长，观点多元")
        print("⚖️ 正反方交替，辩论激烈")
        print("🚀 基于Swarm，性能优越")

# 主函数
async def main():
    """主函数"""
    print("🏛️ 稷下学宫简化版 - OpenAI Swarm")
    print("🚀 四仙论道，简洁高效")
    print()
    
    # 创建辩论系统
    academy = JixiaSimpleSwarm()
    
    if not academy.client:
        print("❌ 系统初始化失败")
        return
    
    # 辩论主题
    topics = [
        "英伟达股价走势：AI泡沫还是技术革命？",
        "美联储2024年货币政策：加息还是降息？", 
        "比特币vs黄金：谁是更好的避险资产？",
        "中国房地产市场：触底反弹还是继续下行？"
    ]
    
    # 随机选择主题
    topic = random.choice(topics)
    
    # 市场背景
    context = {
        "market_sentiment": "谨慎乐观",
        "volatility": "中等",
        "key_events": ["财报季", "央行会议", "地缘政治"]
    }
    
    # 开始辩论
    result = await academy.conduct_debate(topic, context)
    
    if result:
        print(f"\n🎉 辩论成功！ID: {result['debate_id']}")
    else:
        print("❌ 辩论失败")

if __name__ == "__main__":
    asyncio.run(main())