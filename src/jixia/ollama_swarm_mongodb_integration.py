#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Swarm + MongoDB RSS 集成示例
展示如何使用基于 Ollama 的 Swarm 调用 MongoDB 中的 RSS 数据
包含向量化搜索的实现方案
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from swarm import Swarm, Agent
from openai import OpenAI

# 导入 MongoDB MCP 客户端
try:
    from src.mcp.swarm_mongodb_client import SwarmMongoDBClient
except ImportError:
    print("警告: 无法导入 SwarmMongoDBClient，将使用模拟客户端")
    SwarmMongoDBClient = None

class OllamaSwarmMongoDBIntegration:
    """
    Ollama Swarm + MongoDB RSS 集成系统
    
    功能:
    1. 使用 Ollama 本地模型进行 AI 推理
    2. 通过 MCP 连接 MongoDB 获取 RSS 数据
    3. 支持向量化搜索（可选）
    4. 四仙辩论系统集成
    """
    
    def __init__(self):
        # Ollama 配置
        self.ollama_base_url = "http://100.99.183.38:11434"
        self.model_name = "qwen3:8b"  # 使用支持工具调用的模型     
        # 初始化 OpenAI 客户端（连接到 Ollama）
        self.openai_client = OpenAI(
            api_key="ollama",  # Ollama 不需要真实 API 密钥
            base_url=f"{self.ollama_base_url}/v1"
        )
        
        # 初始化 Swarm
        self.swarm = Swarm(client=self.openai_client)
        
        # 初始化 MongoDB 客户端
        self.mongodb_client = None
        self.init_mongodb_client()
        
        # 创建代理
        self.agents = self.create_agents()
        
        print(f"🦙 Ollama 服务: {self.ollama_base_url}")
        print(f"🤖 使用模型: {self.model_name}")
        print(f"📊 MongoDB 连接: {'已连接' if self.mongodb_client else '未连接'}")
    
    def init_mongodb_client(self):
        """初始化 MongoDB 客户端"""
        try:
            if SwarmMongoDBClient:
                self.mongodb_client = SwarmMongoDBClient(
                    mcp_server_url="http://localhost:8080",
                    default_database="taigong"
                )
                # 连接到数据库
                result = self.mongodb_client.connect("taigong")
                if result.get("success"):
                    print("✅ MongoDB MCP 连接成功")
                else:
                    print(f"❌ MongoDB MCP 连接失败: {result.get('error')}")
                    self.mongodb_client = None
            else:
                print("⚠️ 使用模拟 MongoDB 客户端")
                self.mongodb_client = MockMongoDBClient()
        except Exception as e:
            print(f"❌ MongoDB 初始化失败: {e}")
            self.mongodb_client = MockMongoDBClient()
    
    def get_rss_articles(self, query: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """获取 RSS 文章数据"""
        if not self.mongodb_client:
            return []
        
        try:
            # 构建查询条件
            filter_query = {}
            if query:
                # 简单的文本搜索
                filter_query = {
                    "$or": [
                        {"title": {"$regex": query, "$options": "i"}},
                        {"description": {"$regex": query, "$options": "i"}}
                    ]
                }
            
            # 查询文档
            result = self.mongodb_client.find_documents(
                collection_name="articles",
                query=filter_query,
                limit=limit,
                sort={"published_time": -1}  # 按发布时间倒序
            )
            
            if result.get("success"):
                return result.get("documents", [])
            else:
                print(f"查询失败: {result.get('error')}")
                return []
                
        except Exception as e:
            print(f"获取 RSS 文章失败: {e}")
            return []
    
    def create_agents(self) -> Dict[str, Agent]:
        """创建四仙代理"""
        
        def get_rss_news(query: str = "", limit: int = 5) -> str:
            """获取 RSS 新闻的工具函数"""
            articles = self.get_rss_articles(query, limit)
            if not articles:
                return "未找到相关新闻文章"
            
            result = f"找到 {len(articles)} 篇相关文章:\n\n"
            for i, article in enumerate(articles, 1):
                title = article.get('title', '无标题')
                published = article.get('published_time', '未知时间')
                result += f"{i}. {title}\n   发布时间: {published}\n\n"
            
            return result
        
        def analyze_market_sentiment(topic: str) -> str:
            """分析市场情绪的工具函数"""
            articles = self.get_rss_articles(topic, 10)
            if not articles:
                return f"未找到关于 '{topic}' 的相关新闻"
            
            # 简单的情绪分析（实际应用中可以使用更复杂的 NLP 模型）
            positive_keywords = ['上涨', '增长', '利好', '突破', '创新高']
            negative_keywords = ['下跌', '下降', '利空', '暴跌', '风险']
            
            positive_count = 0
            negative_count = 0
            
            for article in articles:
                title = article.get('title', '').lower()
                for keyword in positive_keywords:
                    if keyword in title:
                        positive_count += 1
                for keyword in negative_keywords:
                    if keyword in title:
                        negative_count += 1
            
            sentiment = "中性"
            if positive_count > negative_count:
                sentiment = "偏乐观"
            elif negative_count > positive_count:
                sentiment = "偏悲观"
            
            return f"基于 {len(articles)} 篇新闻分析，'{topic}' 的市场情绪: {sentiment}\n" \
                   f"正面信号: {positive_count}, 负面信号: {negative_count}"
        
        # 创建四仙代理
        agents = {
            "吕洞宾": Agent(
                name="吕洞宾",
                model=self.model_name,
                instructions="""
                你是吕洞宾，技术分析专家。
                - 专长：技术分析和图表解读
                - 性格：犀利直接，一剑封喉
                - 立场：偏向积极乐观
                - 使用 get_rss_news 获取最新财经新闻
                - 使用 analyze_market_sentiment 分析市场情绪
                """,
                functions=[get_rss_news, analyze_market_sentiment]
            ),
            
            "何仙姑": Agent(
                name="何仙姑",
                model=self.model_name,
                instructions="""
                你是何仙姑，风险控制专家。
                - 专长：风险评估和资金管理
                - 性格：温和坚定，关注风险
                - 立场：偏向谨慎保守
                - 使用 get_rss_news 获取风险相关新闻
                - 使用 analyze_market_sentiment 评估市场风险
                """,
                functions=[get_rss_news, analyze_market_sentiment]
            ),
            
            "张果老": Agent(
                name="张果老",
                model=self.model_name,
                instructions="""
                你是张果老，历史数据分析师。
                - 专长：历史数据分析和趋势预测
                - 性格：博学深沉，引经据典
                - 立场：基于历史数据的客观分析
                - 使用 get_rss_news 获取历史相关新闻
                - 使用 analyze_market_sentiment 分析长期趋势
                """,
                functions=[get_rss_news, analyze_market_sentiment]
            ),
            
            "铁拐李": Agent(
                name="铁拐李",
                model=self.model_name,
                instructions="""
                你是铁拐李，逆向思维大师。
                - 专长：逆向思维和另类观点
                - 性格：特立独行，敢于质疑
                - 立场：挑战主流观点
                - 使用 get_rss_news 寻找被忽视的信息
                - 使用 analyze_market_sentiment 提出反向观点
                """,
                functions=[get_rss_news, analyze_market_sentiment]
            )
        }
        
        return agents
    
    async def start_debate(self, topic: str, rounds: int = 3) -> Dict[str, Any]:
        """开始四仙辩论"""
        print(f"\n🎭 开始四仙辩论: {topic}")
        print("=" * 50)
        
        debate_history = []
        
        # 获取相关新闻作为背景
        background_articles = self.get_rss_articles(topic, 5)
        background_info = "\n".join([f"- {article.get('title', '')}" for article in background_articles])
        
        agent_names = list(self.agents.keys())
        
        for round_num in range(rounds):
            print(f"\n📢 第 {round_num + 1} 轮辩论")
            print("-" * 30)
            
            for agent_name in agent_names:
                agent = self.agents[agent_name]
                
                # 构建消息
                if round_num == 0:
                    message = f"""请基于以下背景信息对 '{topic}' 发表你的观点：
                    
背景新闻：
{background_info}
                    
请使用你的专业工具获取更多信息并给出分析。"""
                else:
                    # 后续轮次包含之前的辩论历史
                    history_summary = "\n".join([f"{h['agent']}: {h['response'][:100]}..." for h in debate_history[-3:]])
                    message = f"""基于之前的辩论内容，请继续阐述你对 '{topic}' 的观点：
                    
之前的观点：
{history_summary}
                    
请使用工具获取最新信息并回应其他仙友的观点。"""
                
                try:
                    # 调用代理
                    response = self.swarm.run(
                        agent=agent,
                        messages=[{"role": "user", "content": message}]
                    )
                    
                    agent_response = response.messages[-1]["content"]
                    
                    print(f"\n{agent_name}: {agent_response}")
                    
                    debate_history.append({
                        "round": round_num + 1,
                        "agent": agent_name,
                        "response": agent_response,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    print(f"❌ {agent_name} 发言失败: {e}")
                    continue
        
        return {
            "topic": topic,
            "rounds": rounds,
            "debate_history": debate_history,
            "background_articles": background_articles
        }
    
    def get_vector_search_recommendation(self) -> str:
        """获取向量化搜索的建议"""
        return """
🔍 向量化搜索建议：

当前 RSS 数据结构：
- _id: ObjectId
- title: String
- published_time: String

向量化增强方案：

1. 数据预处理：
   - 提取文章摘要/描述字段
   - 清理和标准化文本内容
   - 添加分类标签

2. 向量化实现：
   - 使用 Ollama 本地嵌入模型（如 nomic-embed-text）
   - 为每篇文章生成 768 维向量
   - 存储向量到 MongoDB 的 vector 字段

3. 索引创建：
   ```javascript
   db.articles.createIndex(
     { "vector": "2dsphere" },
     { "name": "vector_index" }
   )
   ```

4. 语义搜索：
   - 将用户查询转换为向量
   - 使用 $vectorSearch 进行相似度搜索
   - 结合传统关键词搜索提高准确性

5. Swarm 集成：
   - 为代理添加语义搜索工具
   - 支持概念级别的新闻检索
   - 提高辩论质量和相关性

实施优先级：
1. 先完善基础文本搜索
2. 添加文章摘要字段
3. 集成 Ollama 嵌入模型
4. 实现向量搜索功能
        """

class MockMongoDBClient:
    """模拟 MongoDB 客户端（用于测试）"""
    
    def __init__(self):
        self.mock_articles = [
            {
                "_id": "mock_1",
                "title": "滨江服务，还能涨价的物业",
                "published_time": "2025-06-13T04:58:00.000Z",
                "description": "房地产市场分析"
            },
            {
                "_id": "mock_2",
                "title": "中国汽车行业在内卷什么？",
                "published_time": "2025-06-11T05:07:00.000Z",
                "description": "汽车行业竞争分析"
            }
        ]
    
    def find_documents(self, collection_name: str, query: Optional[Dict] = None, 
                      limit: int = 100, **kwargs) -> Dict[str, Any]:
        """模拟文档查询"""
        return {
            "success": True,
            "documents": self.mock_articles[:limit]
        }
    
    def connect(self, database_name: str) -> Dict[str, Any]:
        """模拟连接"""
        return {"success": True}

async def main():
    """主函数"""
    # 创建集成系统
    system = OllamaSwarmMongoDBIntegration()
    
    # 显示向量化建议
    print(system.get_vector_search_recommendation())
    
    # 测试 RSS 数据获取
    print("\n📰 测试 RSS 数据获取:")
    articles = system.get_rss_articles(limit=3)
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article.get('title', '无标题')}")
    
    # 开始辩论（可选）
    user_input = input("\n是否开始辩论？(y/n): ")
    if user_input.lower() == 'y':
        topic = input("请输入辩论主题（默认：房地产市场）: ") or "房地产市场"
        result = await system.start_debate(topic, rounds=2)
        
        print("\n📊 辩论总结:")
        print(f"主题: {result['topic']}")
        print(f"轮次: {result['rounds']}")
        print(f"发言次数: {len(result['debate_history'])}")

if __name__ == "__main__":
    asyncio.run(main())