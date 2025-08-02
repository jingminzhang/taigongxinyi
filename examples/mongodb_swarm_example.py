#!/usr/bin/env python3
"""
MongoDB Swarm Integration Example
MongoDB与Swarm集成的完整使用示例

这个示例展示了如何:
1. 设置MongoDB MCP服务器
2. 创建Swarm代理
3. 执行各种数据库操作
4. 处理错误和异常情况
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Any

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.mcp.swarm_mongodb_client import SwarmMongoDBClient, create_mongodb_functions
    from src.mcp.mongodb_mcp_config import MongoDBMCPConfig, SwarmMongoDBIntegration
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所需依赖: pip install pymongo requests")
    sys.exit(1)

# 模拟Swarm框架（如果没有实际的Swarm库）
class MockSwarm:
    """模拟Swarm客户端"""
    
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, agent):
        """注册代理"""
        self.agents[agent.name] = agent
        print(f"✅ 注册代理: {agent.name}")
    
    def run(self, agent_name: str, message: str) -> str:
        """运行代理"""
        if agent_name not in self.agents:
            return f"错误: 代理 '{agent_name}' 不存在"
        
        agent = self.agents[agent_name]
        return agent.process_message(message)

class MockAgent:
    """模拟Swarm代理"""
    
    def __init__(self, name: str, instructions: str, functions: List[callable]):
        self.name = name
        self.instructions = instructions
        self.functions = {func.__name__: func for func in functions}
        self.conversation_history = []
    
    def process_message(self, message: str) -> str:
        """处理用户消息"""
        self.conversation_history.append({"role": "user", "content": message})
        
        # 简单的意图识别和函数调用
        response = self._analyze_and_execute(message)
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
    
    def _analyze_and_execute(self, message: str) -> str:
        """分析消息并执行相应函数"""
        message_lower = message.lower()
        
        try:
            # 查询操作
            if any(keyword in message_lower for keyword in ['查询', '查找', '搜索', 'find', 'query', '显示']):
                if '集合' in message_lower or 'collection' in message_lower:
                    return self.functions['mongodb_collections']()
                else:
                    # 提取集合名称（简化处理）
                    collection_name = self._extract_collection_name(message)
                    return self.functions['mongodb_query'](collection_name, message)
            
            # 插入操作
            elif any(keyword in message_lower for keyword in ['插入', '添加', '创建', 'insert', 'add', 'create']):
                collection_name = self._extract_collection_name(message)
                # 这里需要更复杂的解析来提取文档内容
                sample_doc = {"message": message, "timestamp": datetime.now().isoformat()}
                return self.functions['mongodb_insert'](collection_name, sample_doc, "用户请求插入")
            
            # 统计操作
            elif any(keyword in message_lower for keyword in ['统计', '状态', 'stats', 'status', '信息']):
                collection_name = self._extract_collection_name(message)
                return self.functions['mongodb_stats'](collection_name)
            
            # 更新操作
            elif any(keyword in message_lower for keyword in ['更新', '修改', 'update', 'modify']):
                collection_name = self._extract_collection_name(message)
                query = {"message": {"$regex": "test"}}
                update = {"$set": {"updated_at": datetime.now().isoformat()}}
                return self.functions['mongodb_update'](collection_name, query, update, "用户请求更新")
            
            else:
                return f"我理解您想要进行数据库操作，但需要更具体的指令。\n\n可用操作:\n- 查询数据: '查询users集合'\n- 插入数据: '向users集合插入数据'\n- 查看统计: '显示users集合统计信息'\n- 列出集合: '显示所有集合'"
        
        except Exception as e:
            return f"执行操作时出错: {str(e)}"
    
    def _extract_collection_name(self, message: str) -> str:
        """从消息中提取集合名称（简化实现）"""
        # 简单的关键词匹配
        common_collections = ['users', 'products', 'orders', 'logs', 'test', 'data']
        
        for collection in common_collections:
            if collection in message.lower():
                return collection
        
        # 默认返回test集合
        return 'test'


class MongoDBSwarmDemo:
    """MongoDB Swarm集成演示"""
    
    def __init__(self):
        self.config = MongoDBMCPConfig.from_env()
        self.mongodb_client = None
        self.swarm = MockSwarm()
        self.setup_complete = False
    
    def setup(self) -> bool:
        """设置演示环境"""
        print("🚀 开始设置MongoDB Swarm集成演示...")
        
        try:
            # 1. 创建MongoDB客户端
            print(f"📊 连接到MongoDB MCP服务器: {self.config.mcp_server_url}")
            self.mongodb_client = SwarmMongoDBClient(
                mcp_server_url=self.config.mcp_server_url,
                default_database=self.config.default_database
            )
            
            # 2. 测试连接
            print(f"🔗 连接到数据库: {self.config.default_database}")
            result = self.mongodb_client.connect(self.config.default_database)
            
            if not result.get("success"):
                print(f"❌ 数据库连接失败: {result.get('error')}")
                print("💡 请确保MongoDB MCP服务器正在运行")
                return False
            
            print(f"✅ 数据库连接成功")
            
            # 3. 创建MongoDB函数
            mongodb_functions = create_mongodb_functions(self.mongodb_client)
            print(f"🔧 创建了 {len(mongodb_functions)} 个MongoDB函数")
            
            # 4. 创建Swarm代理
            agent = MockAgent(
                name="MongoDB助手",
                instructions="你是一个MongoDB数据库专家，帮助用户管理和查询数据库。",
                functions=[func["function"] for func in mongodb_functions]
            )
            
            self.swarm.register_agent(agent)
            
            self.setup_complete = True
            print("✅ 设置完成！")
            return True
            
        except Exception as e:
            print(f"❌ 设置失败: {str(e)}")
            return False
    
    def run_demo_scenarios(self):
        """运行演示场景"""
        if not self.setup_complete:
            print("❌ 请先完成设置")
            return
        
        print("\n" + "="*60)
        print("🎯 开始运行MongoDB Swarm演示场景")
        print("="*60)
        
        scenarios = [
            {
                "name": "查看数据库状态",
                "message": "显示数据库连接状态和统计信息",
                "description": "检查数据库连接和基本信息"
            },
            {
                "name": "列出所有集合",
                "message": "显示所有集合",
                "description": "查看数据库中的所有集合"
            },
            {
                "name": "插入测试数据",
                "message": "向test集合插入一些测试数据",
                "description": "创建示例文档"
            },
            {
                "name": "查询测试数据",
                "message": "查询test集合中的数据",
                "description": "检索刚插入的数据"
            },
            {
                "name": "获取集合统计",
                "message": "显示test集合的统计信息",
                "description": "查看集合的详细统计"
            },
            {
                "name": "更新数据",
                "message": "更新test集合中的数据",
                "description": "修改现有文档"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n📋 场景 {i}: {scenario['name']}")
            print(f"📝 描述: {scenario['description']}")
            print(f"💬 用户消息: {scenario['message']}")
            print("-" * 40)
            
            try:
                response = self.swarm.run("MongoDB助手", scenario['message'])
                print(f"🤖 代理响应:\n{response}")
            except Exception as e:
                print(f"❌ 场景执行失败: {str(e)}")
            
            print("-" * 40)
            time.sleep(1)  # 短暂暂停
    
    def interactive_mode(self):
        """交互模式"""
        if not self.setup_complete:
            print("❌ 请先完成设置")
            return
        
        print("\n" + "="*60)
        print("🎮 进入交互模式")
        print("💡 输入 'quit' 或 'exit' 退出")
        print("💡 输入 'help' 查看可用命令")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n👤 您: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("👋 再见！")
                    break
                
                if user_input.lower() in ['help', '帮助']:
                    self._show_help()
                    continue
                
                if not user_input:
                    continue
                
                print("🤖 MongoDB助手: ", end="")
                response = self.swarm.run("MongoDB助手", user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 错误: {str(e)}")
    
    def _show_help(self):
        """显示帮助信息"""
        help_text = """
🔧 可用命令示例:

📊 查询操作:
  - "查询users集合"
  - "显示test集合中的数据"
  - "搜索products集合"

➕ 插入操作:
  - "向users集合插入数据"
  - "添加新记录到test集合"

📈 统计信息:
  - "显示users集合统计信息"
  - "查看数据库状态"

📋 管理操作:
  - "显示所有集合"
  - "列出集合"

🔄 更新操作:
  - "更新test集合中的数据"
  - "修改users集合"

💡 提示: 请在命令中包含集合名称，如 'users', 'test', 'products' 等
"""
        print(help_text)
    
    def cleanup(self):
        """清理资源"""
        if self.mongodb_client:
            self.mongodb_client.close()
            print("🧹 已清理MongoDB客户端连接")


def main():
    """主函数"""
    print("🎯 MongoDB Swarm集成演示")
    print("=" * 50)
    
    demo = MongoDBSwarmDemo()
    
    try:
        # 设置演示环境
        if not demo.setup():
            print("\n❌ 演示设置失败，请检查:")
            print("1. MongoDB服务是否运行")
            print("2. MongoDB MCP服务器是否启动")
            print("3. 网络连接是否正常")
            return
        
        # 选择运行模式
        print("\n🎮 选择运行模式:")
        print("1. 自动演示场景")
        print("2. 交互模式")
        print("3. 两者都运行")
        
        try:
            choice = input("\n请选择 (1/2/3): ").strip()
        except KeyboardInterrupt:
            print("\n👋 再见！")
            return
        
        if choice == "1":
            demo.run_demo_scenarios()
        elif choice == "2":
            demo.interactive_mode()
        elif choice == "3":
            demo.run_demo_scenarios()
            demo.interactive_mode()
        else:
            print("❌ 无效选择，运行自动演示")
            demo.run_demo_scenarios()
    
    except KeyboardInterrupt:
        print("\n👋 用户中断，正在退出...")
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {str(e)}")
    finally:
        demo.cleanup()


if __name__ == "__main__":
    main()