#!/usr/bin/env python3
"""
MongoDB Swarm集成使用示例

这个示例展示了如何将MongoDB MCP服务器与Swarm框架集成使用。
"""

import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime

# 模拟Swarm框架（实际使用时导入真实的Swarm）
class MockSwarm:
    def __init__(self):
        self.agents = {}
    
    def add_agent(self, agent):
        self.agents[agent.name] = agent
        print(f"✅ 代理 '{agent.name}' 已添加到Swarm")
    
    async def run(self, agent_name: str, message: str) -> str:
        if agent_name not in self.agents:
            return f"❌ 代理 '{agent_name}' 不存在"
        
        agent = self.agents[agent_name]
        print(f"🤖 代理 '{agent_name}' 正在处理: {message}")
        
        # 模拟代理处理逻辑
        if "查询" in message or "查找" in message:
            return await agent.handle_query(message)
        elif "插入" in message or "添加" in message:
            return await agent.handle_insert(message)
        elif "统计" in message:
            return await agent.handle_stats(message)
        else:
            return f"📝 代理 '{agent_name}' 收到消息: {message}"

class MockMongoDBAgent:
    def __init__(self, name: str, mongodb_client):
        self.name = name
        self.mongodb_client = mongodb_client
        self.functions = [
            "mongodb_query",
            "mongodb_insert", 
            "mongodb_update",
            "mongodb_delete",
            "mongodb_stats",
            "mongodb_collections"
        ]
    
    async def handle_query(self, message: str) -> str:
        try:
            # 模拟查询操作
            result = await self.mongodb_client.query_documents(
                collection="users",
                filter_query={},
                limit=5
            )
            return f"📊 查询结果: 找到 {len(result.get('documents', []))} 条记录"
        except Exception as e:
            return f"❌ 查询失败: {str(e)}"
    
    async def handle_insert(self, message: str) -> str:
        try:
            # 模拟插入操作
            sample_doc = {
                "name": "示例用户",
                "email": "user@example.com",
                "created_at": datetime.now().isoformat(),
                "tags": ["swarm", "mongodb"]
            }
            result = await self.mongodb_client.insert_document(
                collection="users",
                document=sample_doc
            )
            return f"✅ 插入成功: 文档ID {result.get('inserted_id', 'unknown')}"
        except Exception as e:
            return f"❌ 插入失败: {str(e)}"
    
    async def handle_stats(self, message: str) -> str:
        try:
            # 模拟统计操作
            result = await self.mongodb_client.get_database_stats()
            return f"📈 数据库统计: {json.dumps(result, indent=2, ensure_ascii=False)}"
        except Exception as e:
            return f"❌ 获取统计失败: {str(e)}"

# 模拟MongoDB MCP客户端
class MockMongoDBClient:
    def __init__(self, mcp_server_url: str, default_database: str):
        self.mcp_server_url = mcp_server_url
        self.default_database = default_database
        self.connected = False
    
    async def connect(self) -> bool:
        print(f"🔌 连接到MongoDB MCP服务器: {self.mcp_server_url}")
        print(f"📁 默认数据库: {self.default_database}")
        self.connected = True
        return True
    
    async def query_documents(self, collection: str, filter_query: Dict, limit: int = 100) -> Dict[str, Any]:
        if not self.connected:
            raise Exception("未连接到MongoDB服务器")
        
        print(f"🔍 查询集合 '{collection}', 过滤条件: {filter_query}, 限制: {limit}")
        # 模拟查询结果
        return {
            "documents": [
                {"_id": "507f1f77bcf86cd799439011", "name": "用户1", "email": "user1@example.com"},
                {"_id": "507f1f77bcf86cd799439012", "name": "用户2", "email": "user2@example.com"},
                {"_id": "507f1f77bcf86cd799439013", "name": "用户3", "email": "user3@example.com"}
            ],
            "count": 3
        }
    
    async def insert_document(self, collection: str, document: Dict[str, Any]) -> Dict[str, Any]:
        if not self.connected:
            raise Exception("未连接到MongoDB服务器")
        
        print(f"📝 向集合 '{collection}' 插入文档: {json.dumps(document, ensure_ascii=False, indent=2)}")
        # 模拟插入结果
        return {
            "inserted_id": "507f1f77bcf86cd799439014",
            "acknowledged": True
        }
    
    async def get_database_stats(self) -> Dict[str, Any]:
        if not self.connected:
            raise Exception("未连接到MongoDB服务器")
        
        print(f"📊 获取数据库 '{self.default_database}' 统计信息")
        # 模拟统计结果
        return {
            "database": self.default_database,
            "collections": 5,
            "documents": 1250,
            "avgObjSize": 512,
            "dataSize": 640000,
            "storageSize": 1024000,
            "indexes": 8,
            "indexSize": 32768
        }
    
    async def disconnect(self):
        print("🔌 断开MongoDB MCP连接")
        self.connected = False

async def main():
    print("🚀 MongoDB Swarm集成示例")
    print("=" * 50)
    
    # 1. 创建MongoDB MCP客户端
    print("\n📋 步骤1: 创建MongoDB MCP客户端")
    mongodb_client = MockMongoDBClient(
        mcp_server_url="http://localhost:8080",
        default_database="swarm_data"
    )
    
    # 2. 连接到MongoDB
    print("\n📋 步骤2: 连接到MongoDB")
    await mongodb_client.connect()
    
    # 3. 创建Swarm实例
    print("\n📋 步骤3: 创建Swarm实例")
    swarm = MockSwarm()
    
    # 4. 创建MongoDB代理
    print("\n📋 步骤4: 创建MongoDB代理")
    mongodb_agent = MockMongoDBAgent("mongodb_agent", mongodb_client)
    swarm.add_agent(mongodb_agent)
    
    # 5. 演示各种操作
    print("\n📋 步骤5: 演示MongoDB操作")
    print("-" * 30)
    
    # 查询操作
    print("\n🔍 演示查询操作:")
    result = await swarm.run("mongodb_agent", "查询所有用户数据")
    print(f"结果: {result}")
    
    # 插入操作
    print("\n📝 演示插入操作:")
    result = await swarm.run("mongodb_agent", "插入一个新用户")
    print(f"结果: {result}")
    
    # 统计操作
    print("\n📊 演示统计操作:")
    result = await swarm.run("mongodb_agent", "获取数据库统计信息")
    print(f"结果: {result}")
    
    # 6. 清理资源
    print("\n📋 步骤6: 清理资源")
    await mongodb_client.disconnect()
    
    print("\n✅ 示例完成!")
    print("\n💡 实际使用说明:")
    print("1. 启动MongoDB和MCP服务器: docker-compose up -d")
    print("2. 使用真实的SwarmMongoDBClient替换MockMongoDBClient")
    print("3. 导入真实的Swarm框架")
    print("4. 根据需要配置代理的instructions和functions")

if __name__ == "__main__":
    asyncio.run(main())