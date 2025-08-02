#!/usr/bin/env python3
"""
四仙论道 - 基于OpenAI Swarm的辩论系统
使用OpenRouter API，四仙轮流论道
"""

import os
import asyncio
import json
import subprocess
from datetime import datetime
from swarm import Swarm, Agent
from typing import Dict, List, Any

class BaxianSwarmDebate:
    """基于Swarm的四仙论道系统"""
    
    def __init__(self):
        # 从Doppler获取API密钥
        self.api_key = self.get_secure_api_key()
        
        # 初始化Swarm客户端，使用OpenRouter
        self.client = Swarm()
        # 设置OpenRouter配置
        os.environ["OPENAI_API_KEY"] = self.api_key
        os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
        
        # 四仙配置
        self.immortals_config = {
            '吕洞宾': {
                'role': '剑仙投资顾问',
                'gua_position': '乾☰',
                'specialty': '技术分析',
                'style': '一剑封喉，直指要害',
                'personality': '犀利直接，善于识破市场迷雾'
            },
            '何仙姑': {
                'role': '慈悲风控专家',
                'gua_position': '坤☷',
                'specialty': '风险控制',
                'style': '荷花在手，全局在胸',
                'personality': '温和坚定，关注风险控制'
            },
            '铁拐李': {
                'role': '逆向思维大师',
                'gua_position': '震☳',
                'specialty': '逆向投资',
                'style': '铁拐一点，危机毕现',
                'personality': '不拘一格，挑战主流观点'
            },
            '蓝采和': {
                'role': '情绪分析师',
                'gua_position': '巽☴',
                'specialty': '市场情绪',
                'style': '花篮一抛，情绪明了',
                'personality': '敏锐活泼，感知市场情绪'
            }
        }
        
        # 创建四仙代理
        self.agents = self.create_agents()
        self.debate_history = []
    
    def get_secure_api_key(self):
        """从Doppler安全获取API密钥"""
        try:
            result = subprocess.run(
                ['doppler', 'secrets', 'get', 'OPENROUTER_API_KEY_1', '--json'],
                capture_output=True,
                text=True,
                check=True
            )
            secret_data = json.loads(result.stdout)
            return secret_data['OPENROUTER_API_KEY_1']['computed']
        except Exception as e:
            print(f"❌ 从Doppler获取密钥失败: {e}")
            return None
    
    def create_agents(self) -> Dict[str, Agent]:
        """创建四仙Swarm代理"""
        agents = {}
        
        # 吕洞宾 - 剑仙投资顾问
        agents['吕洞宾'] = Agent(
            name="吕洞宾",
            instructions=f"""
            你是吕洞宾，八仙之首，剑仙投资顾问。
            
            你的特点：
            - 位居{self.immortals_config['吕洞宾']['gua_position']}之位，代表天行健
            - 以剑气纵横的气势分析市场，{self.immortals_config['吕洞宾']['style']}
            - 擅长{self.immortals_config['吕洞宾']['specialty']}，善于识破市场迷雾
            - 性格{self.immortals_config['吕洞宾']['personality']}
            
            在辩论中，你要：
            1. 提出犀利的技术分析观点
            2. 用数据和图表支撑论断
            3. 挑战其他仙人的观点
            4. 保持仙风道骨的表达风格
            5. 论道完毕后，建议下一位仙人发言
            
            请用古雅的语言风格，结合现代金融分析。
            """,
            functions=[self.transfer_to_hexiangu]
        )
        
        # 何仙姑 - 慈悲风控专家
        agents['何仙姑'] = Agent(
            name="何仙姑",
            instructions=f"""
            你是何仙姑，八仙中唯一的女仙，慈悲风控专家。
            
            你的特点：
            - 位居{self.immortals_config['何仙姑']['gua_position']}之位，代表厚德载物
            - {self.immortals_config['何仙姑']['style']}，以母性关怀关注投资风险
            - 擅长{self.immortals_config['何仙姑']['specialty']}，善于发现隐藏危险
            - 性格{self.immortals_config['何仙姑']['personality']}
            
            在辩论中，你要：
            1. 重点关注风险控制和投资安全
            2. 提醒其他仙人注意潜在危险
            3. 提供稳健的投资建议
            4. 平衡激进与保守的观点
            5. 论道完毕后，建议下一位仙人发言
            
            请用温和但坚定的语调，体现女性的细致和关怀。
            """,
            functions=[self.transfer_to_tieguaili]
        )
        
        # 铁拐李 - 逆向思维大师
        agents['铁拐李'] = Agent(
            name="铁拐李",
            instructions=f"""
            你是铁拐李，八仙中的逆向思维大师。
            
            你的特点：
            - 位居{self.immortals_config['铁拐李']['gua_position']}之位，代表雷动风行
            - {self.immortals_config['铁拐李']['style']}，总是从反面角度思考
            - 擅长{self.immortals_config['铁拐李']['specialty']}，发现逆向机会
            - 性格{self.immortals_config['铁拐李']['personality']}，敢于挑战共识
            
            在辩论中，你要：
            1. 提出与众不同的逆向观点
            2. 挑战市场共识和主流观点
            3. 寻找逆向投资机会
            4. 用数据证明反向逻辑
            5. 论道完毕后，建议下一位仙人发言
            
            请用直率犀利的语言，体现逆向思维的独特视角。
            """,
            functions=[self.transfer_to_lancaihe]
        )
        
        # 蓝采和 - 情绪分析师
        agents['蓝采和'] = Agent(
            name="蓝采和",
            instructions=f"""
            你是蓝采和，八仙中的情绪分析师。
            
            你的特点：
            - 位居{self.immortals_config['蓝采和']['gua_position']}之位，代表风行草偃
            - {self.immortals_config['蓝采和']['style']}，敏锐感知市场情绪
            - 擅长{self.immortals_config['蓝采和']['specialty']}，分析投资者心理
            - 性格{self.immortals_config['蓝采和']['personality']}
            
            在辩论中，你要：
            1. 分析市场情绪和投资者心理
            2. 关注社交媒体和舆论趋势
            3. 提供情绪面的投资建议
            4. 用生动的比喻说明观点
            5. 作为最后发言者，要总结四仙观点
            
            请用轻松活泼的语调，体现对市场情绪的敏锐洞察。
            """,
            functions=[self.summarize_debate]
        )
        
        return agents
    
    def transfer_to_hexiangu(self):
        """转到何仙姑"""
        return self.agents['何仙姑']
    
    def transfer_to_tieguaili(self):
        """转到铁拐李"""
        return self.agents['铁拐李']
    
    def transfer_to_lancaihe(self):
        """转到蓝采和"""
        return self.agents['蓝采和']
    
    def summarize_debate(self):
        """蓝采和总结辩论"""
        # 这里可以返回一个特殊的总结agent，或者标记辩论结束
        return None
    
    async def conduct_debate(self, topic: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """进行四仙论道"""
        if not self.api_key:
            print("❌ 无法获取API密钥，无法进行论道")
            return None
            
        print("🎭 四仙论道开始！")
        print("=" * 80)
        print(f"🎯 论道主题: {topic}")
        print()
        
        # 构建初始提示
        initial_prompt = self.build_debate_prompt(topic, context)
        
        try:
            # 从吕洞宾开始论道
            print("⚔️  吕洞宾仙长请先发言...")
            response = self.client.run(
                agent=self.agents['吕洞宾'],
                messages=[{"role": "user", "content": initial_prompt}]
            )
            
            print("\n🎊 四仙论道圆满结束！")
            print("📊 论道结果已生成")
            
            # 生成论道结果
            debate_result = {
                "debate_id": f"swarm_debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "topic": topic,
                "participants": list(self.agents.keys()),
                "messages": response.messages if hasattr(response, 'messages') else [],
                "final_output": response.messages[-1]["content"] if response.messages else "",
                "timestamp": datetime.now().isoformat(),
                "framework": "OpenAI Swarm"
            }
            
            self.debate_history.append(debate_result)
            return debate_result
            
        except Exception as e:
            print(f"❌ 论道过程中出错: {e}")
            return None
    
    def build_debate_prompt(self, topic: str, context: Dict[str, Any] = None) -> str:
        """构建论道提示"""
        context_str = ""
        if context:
            context_str = f"\n背景信息:\n{json.dumps(context, indent=2, ensure_ascii=False)}\n"
        
        prompt = f"""
        🎭 四仙论道正式开始！
        
        论道主题: {topic}
        {context_str}
        论道规则:
        1. 四仙按序发言：吕洞宾 → 何仙姑 → 铁拐李 → 蓝采和
        2. 每位仙人从自己的专业角度分析
        3. 必须提供具体的数据或逻辑支撑
        4. 可以质疑前面仙人的观点
        5. 保持仙风道骨的表达风格
        6. 蓝采和作为最后发言者要综合总结
        
        请吕洞宾仙长首先发言，展现剑仙的犀利分析！
        """
        return prompt
    
    def print_debate_summary(self, debate_result: Dict[str, Any]):
        """打印论道总结"""
        print("\n🌟 四仙论道总结")
        print("=" * 60)
        print(f"主题: {debate_result['topic']}")
        print(f"参与仙人: {', '.join(debate_result['participants'])}")
        print(f"框架: {debate_result['framework']}")
        print(f"时间: {debate_result['timestamp']}")
        print("\n最终结论:")
        print(debate_result['final_output'])
        print("\n🔗 使用Swarm handoff机制实现自然的仙人交接")
        print("✅ 相比AutoGen，配置更简洁，性能更优")

async def main():
    """主函数"""
    print("🐝 四仙论道 - OpenAI Swarm版本")
    print("🔐 使用Doppler安全管理API密钥")
    print("🚀 基于OpenRouter的轻量级多智能体系统")
    print()
    
    # 创建论道系统
    debate_system = BaxianSwarmDebate()
    
    if not debate_system.api_key:
        print("❌ 无法获取API密钥，请检查Doppler配置")
        return
    
    # 论道主题
    topics = [
        "英伟达股价走势：AI泡沫还是技术革命？",
        "美联储政策转向：2024年降息预期分析",
        "比特币vs黄金：谁是更好的避险资产？",
        "中国房地产市场：触底反弹还是继续下行？"
    ]
    
    # 随机选择主题（这里选第一个作为示例）
    topic = topics[0]
    
    # 构建市场背景
    context = {
        "market_data": "英伟达当前股价$120，市值$3T，P/E比率65",
        "recent_news": ["ChatGPT-5即将发布", "中国AI芯片突破", "美国对华芯片制裁升级"],
        "analyst_consensus": "买入评级占70%，目标价$150"
    }
    
    # 进行论道
    result = await debate_system.conduct_debate(topic, context)
    
    if result:
        debate_system.print_debate_summary(result)
    else:
        print("❌ 论道失败")

if __name__ == "__main__":
    asyncio.run(main())
