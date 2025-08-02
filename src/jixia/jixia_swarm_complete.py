#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
稷下学宫完整版 - 基于OpenAI Swarm的八仙辩论系统
实现完整的八仙论道 + 三清决策
"""

import os
import asyncio
import json
import subprocess
from datetime import datetime
from swarm import Swarm, Agent
from typing import Dict, List, Any, Optional
import random

class JixiaSwarmAcademy:
    """稷下学宫 - 完整的八仙辩论系统"""
    
    def __init__(self):
        # 从Doppler获取API密钥
        self.api_key = self.get_secure_api_key()
        
        # 设置环境变量
        if self.api_key:
            os.environ["OPENAI_API_KEY"] = self.api_key
            os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
            
            # 初始化Swarm客户端，传入配置
            from openai import OpenAI
            openai_client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "https://github.com/ben/cauldron",
                    "X-Title": "Jixia Academy Debate System"  # 避免中文字符
                }
            )
            self.client = Swarm(client=openai_client)
        else:
            print("❌ 无法获取有效的API密钥")
            self.client = None
        
        # 八仙配置 - 完整版
        self.immortals_config = {
            '吕洞宾': {
                'role': '剑仙投资顾问',
                'gua_position': '乾☰',
                'specialty': '技术分析',
                'stance': 'positive',
                'style': '一剑封喉，直指要害',
                'personality': '犀利直接，善于识破市场迷雾',
                'weapon': '纯阳剑',
                'next': '何仙姑'
            },
            '何仙姑': {
                'role': '慈悲风控专家',
                'gua_position': '坤☷',
                'specialty': '风险控制',
                'stance': 'negative',
                'style': '荷花在手，全局在胸',
                'personality': '温和坚定，关注风险控制',
                'weapon': '荷花',
                'next': '张果老'
            },
            '张果老': {
                'role': '历史数据分析师',
                'gua_position': '艮☶',
                'specialty': '历史回测',
                'stance': 'positive',
                'style': '倒骑毛驴，逆向思维',
                'personality': '博古通今，从历史中寻找规律',
                'weapon': '鱼鼓',
                'next': '韩湘子'
            },
            '韩湘子': {
                'role': '市场情绪分析师',
                'gua_position': '兑☱',
                'specialty': '情绪分析',
                'stance': 'negative',
                'style': '笛声悠扬，感知人心',
                'personality': '敏感细腻，善于捕捉市场情绪',
                'weapon': '洞箫',
                'next': '汉钟离'
            },
            '汉钟离': {
                'role': '宏观经济分析师',
                'gua_position': '离☲',
                'specialty': '宏观分析',
                'stance': 'positive',
                'style': '扇子一挥，大局明了',
                'personality': '气度恢宏，关注宏观大势',
                'weapon': '芭蕉扇',
                'next': '蓝采和'
            },
            '蓝采和': {
                'role': '量化交易专家',
                'gua_position': '巽☴',
                'specialty': '量化模型',
                'stance': 'negative',
                'style': '花篮一抛，数据飞舞',
                'personality': '逻辑严密，依赖数学模型',
                'weapon': '花篮',
                'next': '曹国舅'
            },
            '曹国舅': {
                'role': '价值投资专家',
                'gua_position': '坎☵',
                'specialty': '基本面分析',
                'stance': 'positive',
                'style': '玉板一敲，价值显现',
                'personality': '稳重踏实，注重内在价值',
                'weapon': '玉板',
                'next': '铁拐李'
            },
            '铁拐李': {
                'role': '逆向投资大师',
                'gua_position': '震☳',
                'specialty': '逆向投资',
                'stance': 'negative',
                'style': '铁拐一点，危机毕现',
                'personality': '不拘一格，挑战主流观点',
                'weapon': '铁拐杖',
                'next': 'summary'
            }
        }
        
        # 三清决策层配置
        self.sanqing_config = {
            '元始天尊': {
                'role': '最终决策者',
                'specialty': '综合决策',
                'style': '无极生太极，一言定乾坤'
            },
            '灵宝天尊': {
                'role': '风险评估师',
                'specialty': '风险量化',
                'style': '太极生两仪，阴阳定风险'
            },
            '道德天尊': {
                'role': '合规审查员',
                'specialty': '合规检查',
                'style': '两仪生四象，四象定规矩'
            }
        }
        
        # 创建智能体
        self.immortal_agents = self.create_immortal_agents()
        self.sanqing_agents = self.create_sanqing_agents()
        
        # 辩论历史
        self.debate_history = []
        self.current_round = 0
        self.max_rounds = 2  # 每个仙人最多发言2轮
    
    def get_secure_api_key(self):
        """获取API密钥 - 支持多种方式"""
        # 从环境变量获取API密钥
        available_keys = [
            os.getenv("OPENROUTER_API_KEY_1"),
            os.getenv("OPENROUTER_API_KEY_2"), 
            os.getenv("OPENROUTER_API_KEY_3"),
            os.getenv("OPENROUTER_API_KEY_4")
        ]
        # 过滤掉None值
        available_keys = [key for key in available_keys if key]
        
        # 直接使用第一个密钥进行测试
        test_key = available_keys[0]
        print(f"🔑 直接使用测试密钥: {test_key[:20]}...")
        return test_key
        

    
    def create_immortal_agents(self) -> Dict[str, Agent]:
        """创建八仙智能体"""
        agents = {}
        
        for name, config in self.immortals_config.items():
            # 创建转换函数 - 使用英文名称避免特殊字符问题
            next_immortal = config['next']
            if next_immortal == 'summary':
                transfer_func = self.transfer_to_sanqing
            else:
                # 创建一个简单的转换函数，避免lambda的问题
                def create_transfer_func(next_name):
                    def transfer():
                        return self.transfer_to_immortal(next_name)
                    transfer.__name__ = f"transfer_to_{self.get_english_name(next_name)}"
                    return transfer
                transfer_func = create_transfer_func(next_immortal)
            
            # 构建详细的指令
            instructions = self.build_immortal_instructions(name, config)
            
            agents[name] = Agent(
                name=name,
                instructions=instructions,
                functions=[transfer_func]
            )
        
        return agents
    
    def create_sanqing_agents(self) -> Dict[str, Agent]:
        """创建三清决策层智能体"""
        agents = {}
        
        # 元始天尊 - 最终决策者
        agents['元始天尊'] = Agent(
            name="元始天尊",
            instructions="""
            你是元始天尊，道教三清之首，稷下学宫的最终决策者。
            
            你的使命：
            1. 综合八仙的所有观点，做出最终投资决策
            2. 平衡正反两方的观点，寻找最优解
            3. 给出具体的投资建议和操作指导
            4. 评估决策的风险等级和预期收益
            
            你的风格：
            - 高屋建瓴，统揽全局
            - 言简意赅，一锤定音
            - 既不偏向乐观，也不偏向悲观
            - 以数据和逻辑为准绳
            
            请以"元始天尊曰"开头，给出最终决策。
            决策格式：
            - 投资建议：买入/持有/卖出
            - 风险等级：低/中/高
            - 预期收益：具体百分比
            - 操作建议：具体的操作指导
            - 决策依据：主要的决策理由
            """,
            functions=[]
        )
        
        return agents
    
    def build_immortal_instructions(self, name: str, config: Dict) -> str:
        """构建仙人的详细指令"""
        stance_desc = "看涨派，倾向于发现投资机会" if config['stance'] == 'positive' else "看跌派，倾向于发现投资风险"
        
        instructions = f"""
        你是{name}，八仙之一，{config['role']}。
        
        你的身份特征：
        - 位居{config['gua_position']}之位，代表{self.get_gua_meaning(config['gua_position'])}
        - 持有{config['weapon']}，{config['style']}
        - 擅长{config['specialty']}，{config['personality']}
        - 立场倾向：{stance_desc}
        
        在稷下学宫辩论中，你要：
        
        1. **专业分析**：从{config['specialty']}角度深入分析
        2. **立场鲜明**：作为{stance_desc}，要有明确的观点
        3. **数据支撑**：用具体的数据、图表、历史案例支撑观点
        4. **互动辩论**：可以质疑前面仙人的观点，但要有理有据
        5. **仙风道骨**：保持古雅的表达风格，但不影响专业性
        6. **承上启下**：总结前面的观点，为后面的仙人铺垫
        
        发言格式：
        - 以"{name}曰："开头
        - 先简要回应前面仙人的观点（如果有）
        - 然后从你的专业角度进行分析
        - 最后明确表达你的投资倾向
        - 结尾时说"请{config['next']}仙长继续论道"（如果不是最后一个）
        
        记住：你是{stance_desc}，要体现这个立场，但也要保持专业和客观。
        """
        
        return instructions
    
    def get_gua_meaning(self, gua: str) -> str:
        """获取卦象含义"""
        meanings = {
            '乾☰': '天行健，自强不息',
            '坤☷': '地势坤，厚德载物',
            '艮☶': '艮为山，止于至善',
            '兑☱': '兑为泽，和悦致祥',
            '离☲': '离为火，光明磊落',
            '巽☴': '巽为风，随风而化',
            '坎☵': '坎为水，智慧如水',
            '震☳': '震为雷，威震四方'
        }
        return meanings.get(gua, '神秘莫测')
    
    def transfer_to_hexiangu(self):
        """转到何仙姑"""
        return self.immortal_agents.get('何仙姑')
    
    def transfer_to_zhangguolao(self):
        """转到张果老"""
        return self.immortal_agents.get('张果老')
    
    def transfer_to_hanxiangzi(self):
        """转到韩湘子"""
        return self.immortal_agents.get('韩湘子')
    
    def transfer_to_hanzhongli(self):
        """转到汉钟离"""
        return self.immortal_agents.get('汉钟离')
    
    def transfer_to_lancaihe(self):
        """转到蓝采和"""
        return self.immortal_agents.get('蓝采和')
    
    def transfer_to_caoguojiu(self):
        """转到曹国舅"""
        return self.immortal_agents.get('曹国舅')
    
    def transfer_to_tieguaili(self):
        """转到铁拐李"""
        return self.immortal_agents.get('铁拐李')
    
    def transfer_to_sanqing(self):
        """转到三清决策层"""
        return self.sanqing_agents['元始天尊']
    
    async def conduct_full_debate(self, topic: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """进行完整的稷下学宫辩论"""
        if not self.api_key or not self.client:
            print("❌ 无法获取API密钥或初始化客户端，无法进行论道")
            return None
        
        print("🏛️ 稷下学宫八仙论道正式开始！")
        print("=" * 80)
        print(f"🎯 论道主题: {topic}")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 构建初始提示
        initial_prompt = self.build_debate_prompt(topic, context)
        
        try:
            # 从吕洞宾开始论道
            print("⚔️ 吕洞宾仙长请先发言...")
            print("-" * 60)
            
            response = self.client.run(
                agent=self.immortal_agents['吕洞宾'],
                messages=[{"role": "user", "content": initial_prompt}],
                max_turns=20  # 允许多轮对话
            )
            
            print("\n" + "=" * 80)
            print("🎊 稷下学宫八仙论道圆满结束！")
            print("📊 三清决策已生成")
            
            # 处理辩论结果
            debate_result = self.process_debate_result(response, topic, context)
            
            # 显示辩论总结
            self.display_debate_summary(debate_result)
            
            return debate_result
            
        except Exception as e:
            print(f"❌ 论道过程中出错: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def build_debate_prompt(self, topic: str, context: Dict[str, Any] = None) -> str:
        """构建辩论提示"""
        context_str = ""
        if context:
            context_str = f"\n📊 市场背景:\n{json.dumps(context, indent=2, ensure_ascii=False)}\n"
        
        # 随机选择一些市场数据作为背景
        market_context = self.generate_market_context(topic)
        
        prompt = f"""
        🏛️ 稷下学宫八仙论道正式开始！
        
        📜 论道主题: {topic}
        {context_str}
        📈 当前市场环境:
        {market_context}
        
        🎭 论道规则:
        1. 八仙按序发言：吕洞宾 → 何仙姑 → 张果老 → 韩湘子 → 汉钟离 → 蓝采和 → 曹国舅 → 铁拐李
        2. 正反方交替：正方(看涨) vs 反方(看跌)
        3. 每位仙人从专业角度分析，必须提供数据支撑
        4. 可以质疑前面仙人的观点，但要有理有据
        5. 保持仙风道骨的表达风格
        6. 最后由三清做出最终决策
        
        🗡️ 请吕洞宾仙长首先发言，展现剑仙的犀利分析！
        记住：你是看涨派，要从技术分析角度找到投资机会！
        """
        return prompt
    
    def generate_market_context(self, topic: str) -> str:
        """生成模拟的市场背景数据"""
        # 这里可以集成真实的市场数据，现在先用模拟数据
        contexts = {
            "英伟达": "NVDA当前价格$120，P/E比率65，市值$3T，AI芯片需求旺盛",
            "比特币": "BTC当前价格$43,000，24h涨幅+2.3%，机构持续买入",
            "美联储": "联邦基金利率5.25%，通胀率3.2%，就业数据强劲",
            "中国股市": "上证指数3100点，外资流入放缓，政策支持预期"
        }
        
        # 根据主题选择相关背景
        for key, context in contexts.items():
            if key in topic:
                return context
        
        return "市场情绪谨慎，波动率上升，投资者观望情绪浓厚"
    
    def process_debate_result(self, response, topic: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """处理辩论结果"""
        # 提取所有消息
        all_messages = response.messages if hasattr(response, 'messages') else []
        
        # 分析发言者和内容
        debate_messages = []
        speakers = []
        
        for msg in all_messages:
            if msg.get('role') == 'assistant' and msg.get('content'):
                content = msg['content']
                speaker = self.extract_speaker_from_content(content)
                
                debate_messages.append({
                    'speaker': speaker,
                    'content': content,
                    'timestamp': datetime.now().isoformat(),
                    'stance': self.get_speaker_stance(speaker)
                })
                
                if speaker not in speakers:
                    speakers.append(speaker)
        
        # 提取最终决策（通常是最后一条消息）
        final_decision = ""
        if debate_messages:
            final_decision = debate_messages[-1]['content']
        
        # 构建结果
        result = {
            "debate_id": f"jixia_debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "topic": topic,
            "context": context,
            "participants": speakers,
            "messages": debate_messages,
            "final_decision": final_decision,
            "summary": self.generate_debate_summary(debate_messages),
            "timestamp": datetime.now().isoformat(),
            "framework": "OpenAI Swarm",
            "academy": "稷下学宫"
        }
        
        self.debate_history.append(result)
        return result
    
    def extract_speaker_from_content(self, content: str) -> str:
        """从内容中提取发言者"""
        for name in list(self.immortals_config.keys()) + list(self.sanqing_config.keys()):
            if f"{name}曰" in content or name in content[:20]:
                return name
        return "未知仙人"
    
    def get_speaker_stance(self, speaker: str) -> str:
        """获取发言者立场"""
        if speaker in self.immortals_config:
            return self.immortals_config[speaker]['stance']
        elif speaker in self.sanqing_config:
            return 'neutral'
        return 'unknown'
    
    def generate_debate_summary(self, messages: List[Dict]) -> str:
        """生成辩论摘要"""
        positive_count = len([m for m in messages if m.get('stance') == 'positive'])
        negative_count = len([m for m in messages if m.get('stance') == 'negative'])
        
        summary = f"""
        📊 辩论统计:
        - 参与仙人: {len(set(m['speaker'] for m in messages))}位
        - 看涨观点: {positive_count}条
        - 看跌观点: {negative_count}条
        - 总发言数: {len(messages)}条
        
        🎯 观点倾向: {'偏向看涨' if positive_count > negative_count else '偏向看跌' if negative_count > positive_count else '观点平衡'}
        """
        
        return summary
    
    def display_debate_summary(self, result: Dict[str, Any]):
        """显示辩论总结"""
        print("\n🌟 稷下学宫辩论总结")
        print("=" * 80)
        print(f"📜 主题: {result['topic']}")
        print(f"🎭 参与仙人: {', '.join(result['participants'])}")
        print(f"⏰ 辩论时间: {result['timestamp']}")
        print(f"🔧 技术框架: {result['framework']}")
        
        print(result['summary'])
        
        print("\n🏆 最终决策:")
        print("-" * 40)
        print(result['final_decision'])
        
        print("\n✨ 稷下学宫辩论特色:")
        print("🗡️ 八仙各展所长，观点多元化")
        print("⚖️ 正反方交替发言，辩论更激烈")
        print("🧠 三清最终决策，权威性更强")
        print("🔄 基于Swarm框架，性能更优越")

# 主函数和测试
async def main():
    """主函数 - 演示完整的稷下学宫辩论"""
    print("🏛️ 稷下学宫 - OpenAI Swarm完整版")
    print("🔐 使用Doppler安全管理API密钥")
    print("🚀 八仙论道 + 三清决策的完整体验")
    print()
    
    # 创建学宫
    academy = JixiaSwarmAcademy()
    
    if not academy.api_key:
        print("❌ 无法获取API密钥，请检查Doppler配置或环境变量")
        return
    
    # 辩论主题列表
    topics = [
        "英伟达股价走势：AI泡沫还是技术革命？",
        "美联储2024年货币政策：加息还是降息？",
        "比特币vs黄金：谁是更好的避险资产？",
        "中国房地产市场：触底反弹还是继续下行？",
        "特斯拉股价：马斯克效应还是基本面支撑？"
    ]
    
    # 随机选择主题
    topic = random.choice(topics)
    
    # 构建市场背景
    context = {
        "market_sentiment": "谨慎乐观",
        "volatility": "中等",
        "major_events": ["美联储会议", "财报季", "地缘政治紧张"],
        "technical_indicators": {
            "RSI": 65,
            "MACD": "金叉",
            "MA20": "上穿"
        }
    }
    
    # 开始辩论
    result = await academy.conduct_full_debate(topic, context)
    
    if result:
        print(f"\n🎉 辩论成功完成！辩论ID: {result['debate_id']}")
    else:
        print("❌ 辩论失败")

if __name__ == "__main__":
    asyncio.run(main())