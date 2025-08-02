#!/usr/bin/env python3
"""
Swarm MongoDB MCP Client
Swarm框架的MongoDB MCP客户端，用于连接和使用MongoDB MCP服务器

功能:
- 连接到MongoDB MCP服务器
- 提供Swarm代理使用的MongoDB操作接口
- 处理MCP协议通信
- 数据格式转换和错误处理
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: requests is required. Install with: pip install requests")
    sys.exit(1)

class SwarmMongoDBClient:
    """
    Swarm MongoDB MCP客户端
    为Swarm代理提供MongoDB数据库访问功能
    """
    
    def __init__(self, mcp_server_url: str = "http://localhost:8080", 
                 mongodb_url: Optional[str] = None, 
                 default_database: str = "default"):
        self.mcp_server_url = mcp_server_url.rstrip('/')
        self.mongodb_url = mongodb_url or os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
        self.default_database = default_database
        self.connected = False
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 会话配置
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Swarm-MongoDB-MCP-Client/1.0'
        })
    
    def _call_mcp_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        调用MCP服务器工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
        
        Returns:
            工具执行结果
        """
        try:
            url = f"{self.mcp_server_url}/tools/{tool_name}"
            response = self.session.post(url, json=kwargs, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"MCP tool call failed: {e}")
            return {
                "success": False,
                "error": f"MCP communication error: {str(e)}"
            }
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response: {e}")
            return {
                "success": False,
                "error": f"Invalid response format: {str(e)}"
            }
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def _get_mcp_resource(self, resource_uri: str) -> Dict[str, Any]:
        """
        获取MCP服务器资源
        
        Args:
            resource_uri: 资源URI
        
        Returns:
            资源内容
        """
        try:
            url = f"{self.mcp_server_url}/resources"
            response = self.session.get(url, params={'uri': resource_uri}, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"MCP resource request failed: {e}")
            return {
                "success": False,
                "error": f"MCP communication error: {str(e)}"
            }
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    # === 连接管理 ===
    
    def connect(self, database_name: Optional[str] = None) -> Dict[str, Any]:
        """
        连接到MongoDB数据库
        
        Args:
            database_name: 数据库名称，默认使用初始化时指定的数据库
        
        Returns:
            连接结果
        """
        db_name = database_name or self.default_database
        result = self._call_mcp_tool("connect_database", database_name=db_name)
        
        if result.get("success"):
            self.connected = True
            self.current_database = db_name
            self.logger.info(f"Connected to MongoDB database: {db_name}")
        
        return result
    
    def get_connection_status(self) -> Dict[str, Any]:
        """
        获取连接状态
        
        Returns:
            连接状态信息
        """
        return self._get_mcp_resource("mongodb://status")
    
    def list_databases(self) -> Dict[str, Any]:
        """
        获取数据库列表
        
        Returns:
            数据库列表
        """
        return self._get_mcp_resource("mongodb://databases")
    
    # === CRUD操作 ===
    
    def insert_document(self, collection_name: str, document: Union[Dict, List[Dict]], 
                       many: bool = False) -> Dict[str, Any]:
        """
        插入文档
        
        Args:
            collection_name: 集合名称
            document: 要插入的文档或文档列表
            many: 是否批量插入
        
        Returns:
            插入结果
        """
        if not self.connected:
            return {"success": False, "error": "Not connected to database"}
        
        return self._call_mcp_tool(
            "insert_document",
            collection_name=collection_name,
            document=document,
            many=many
        )
    
    def find_documents(self, collection_name: str, query: Optional[Dict] = None,
                      projection: Optional[Dict] = None, limit: int = 100,
                      skip: int = 0, sort: Optional[Dict] = None) -> Dict[str, Any]:
        """
        查找文档
        
        Args:
            collection_name: 集合名称
            query: 查询条件
            projection: 投影字段
            limit: 限制数量
            skip: 跳过数量
            sort: 排序条件
        
        Returns:
            查询结果
        """
        if not self.connected:
            return {"success": False, "error": "Not connected to database"}
        
        return self._call_mcp_tool(
            "find_documents",
            collection_name=collection_name,
            query=query or {},
            projection=projection,
            limit=limit,
            skip=skip,
            sort=sort
        )
    
    def update_document(self, collection_name: str, query: Dict, update: Dict,
                       many: bool = False) -> Dict[str, Any]:
        """
        更新文档
        
        Args:
            collection_name: 集合名称
            query: 查询条件
            update: 更新操作
            many: 是否批量更新
        
        Returns:
            更新结果
        """
        if not self.connected:
            return {"success": False, "error": "Not connected to database"}
        
        return self._call_mcp_tool(
            "update_document",
            collection_name=collection_name,
            query=query,
            update=update,
            many=many
        )
    
    def delete_document(self, collection_name: str, query: Dict,
                       many: bool = False) -> Dict[str, Any]:
        """
        删除文档
        
        Args:
            collection_name: 集合名称
            query: 查询条件
            many: 是否批量删除
        
        Returns:
            删除结果
        """
        if not self.connected:
            return {"success": False, "error": "Not connected to database"}
        
        return self._call_mcp_tool(
            "delete_document",
            collection_name=collection_name,
            query=query,
            many=many
        )
    
    # === 高级查询 ===
    
    def aggregate(self, collection_name: str, pipeline: List[Dict]) -> Dict[str, Any]:
        """
        执行聚合查询
        
        Args:
            collection_name: 集合名称
            pipeline: 聚合管道
        
        Returns:
            聚合结果
        """
        if not self.connected:
            return {"success": False, "error": "Not connected to database"}
        
        return self._call_mcp_tool(
            "aggregate_query",
            collection_name=collection_name,
            pipeline=pipeline
        )
    
    # === 数据库管理 ===
    
    def list_collections(self) -> Dict[str, Any]:
        """
        列出所有集合
        
        Returns:
            集合列表
        """
        if not self.connected:
            return {"success": False, "error": "Not connected to database"}
        
        return self._call_mcp_tool("list_collections")
    
    def create_index(self, collection_name: str, index_spec: Dict,
                    unique: bool = False, background: bool = True) -> Dict[str, Any]:
        """
        创建索引
        
        Args:
            collection_name: 集合名称
            index_spec: 索引规范
            unique: 是否唯一索引
            background: 是否后台创建
        
        Returns:
            创建结果
        """
        if not self.connected:
            return {"success": False, "error": "Not connected to database"}
        
        return self._call_mcp_tool(
            "create_index",
            collection_name=collection_name,
            index_spec=index_spec,
            unique=unique,
            background=background
        )
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """
        获取集合统计信息
        
        Args:
            collection_name: 集合名称
        
        Returns:
            统计信息
        """
        if not self.connected:
            return {"success": False, "error": "Not connected to database"}
        
        return self._call_mcp_tool(
            "get_collection_stats",
            collection_name=collection_name
        )
    
    # === Swarm代理专用方法 ===
    
    def swarm_query(self, collection_name: str, natural_language_query: str) -> str:
        """
        Swarm代理专用的自然语言查询接口
        
        Args:
            collection_name: 集合名称
            natural_language_query: 自然语言查询描述
        
        Returns:
            格式化的查询结果字符串
        """
        try:
            # 这里可以集成NLP处理，将自然语言转换为MongoDB查询
            # 目前简化处理，直接执行基本查询
            
            result = self.find_documents(collection_name, limit=10)
            
            if result.get("success"):
                documents = result.get("documents", [])
                if documents:
                    formatted_result = f"Found {len(documents)} documents in '{collection_name}':\n"
                    for i, doc in enumerate(documents[:5], 1):  # 只显示前5个
                        formatted_result += f"{i}. {json.dumps(doc, indent=2, ensure_ascii=False)}\n"
                    
                    if len(documents) > 5:
                        formatted_result += f"... and {len(documents) - 5} more documents\n"
                    
                    return formatted_result
                else:
                    return f"No documents found in collection '{collection_name}'"
            else:
                return f"Query failed: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def swarm_insert(self, collection_name: str, data_description: str, 
                    document: Union[Dict, List[Dict]]) -> str:
        """
        Swarm代理专用的插入接口
        
        Args:
            collection_name: 集合名称
            data_description: 数据描述
            document: 要插入的文档
        
        Returns:
            格式化的插入结果字符串
        """
        try:
            many = isinstance(document, list)
            result = self.insert_document(collection_name, document, many=many)
            
            if result.get("success"):
                if many:
                    count = result.get("count", 0)
                    return f"Successfully inserted {count} documents into '{collection_name}'. Description: {data_description}"
                else:
                    inserted_id = result.get("inserted_id")
                    return f"Successfully inserted document with ID {inserted_id} into '{collection_name}'. Description: {data_description}"
            else:
                return f"Insert failed: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            return f"Error inserting data: {str(e)}"
    
    def swarm_update(self, collection_name: str, update_description: str,
                    query: Dict, update: Dict) -> str:
        """
        Swarm代理专用的更新接口
        
        Args:
            collection_name: 集合名称
            update_description: 更新描述
            query: 查询条件
            update: 更新操作
        
        Returns:
            格式化的更新结果字符串
        """
        try:
            result = self.update_document(collection_name, query, update)
            
            if result.get("success"):
                matched = result.get("matched_count", 0)
                modified = result.get("modified_count", 0)
                return f"Update completed: {matched} documents matched, {modified} documents modified in '{collection_name}'. Description: {update_description}"
            else:
                return f"Update failed: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            return f"Error updating data: {str(e)}"
    
    def swarm_stats(self, collection_name: Optional[str] = None) -> str:
        """
        Swarm代理专用的统计信息接口
        
        Args:
            collection_name: 集合名称，如果为None则返回数据库概览
        
        Returns:
            格式化的统计信息字符串
        """
        try:
            if collection_name:
                # 获取特定集合的统计信息
                result = self.get_collection_stats(collection_name)
                if result.get("success"):
                    stats = result
                    return f"""Collection '{collection_name}' Statistics:
- Document Count: {stats.get('document_count', 0):,}
- Size: {stats.get('size_bytes', 0):,} bytes
- Storage Size: {stats.get('storage_size_bytes', 0):,} bytes
- Indexes: {stats.get('index_count', 0)}"""
                else:
                    return f"Failed to get stats for '{collection_name}': {result.get('error', 'Unknown error')}"
            else:
                # 获取数据库概览
                collections_result = self.list_collections()
                status_result = self.get_connection_status()
                
                if collections_result.get("success") and status_result.get("connected"):
                    collections = collections_result.get("collections", [])
                    db_name = status_result.get("current_database", "Unknown")
                    
                    stats_text = f"""Database '{db_name}' Overview:
- Total Collections: {len(collections)}
- Collections: {', '.join(collections) if collections else 'None'}
- Server Version: {status_result.get('server_info', {}).get('version', 'Unknown')}"""
                    
                    return stats_text
                else:
                    return "Failed to get database overview"
                    
        except Exception as e:
            return f"Error getting statistics: {str(e)}"
    
    def close(self):
        """
        关闭客户端连接
        """
        self.session.close()
        self.connected = False
        self.logger.info("MongoDB MCP client closed")


# === Swarm代理函数 ===

def create_mongodb_functions(client: SwarmMongoDBClient) -> List[Dict[str, Any]]:
    """
    为Swarm代理创建MongoDB操作函数
    
    Args:
        client: MongoDB MCP客户端实例
    
    Returns:
        Swarm函数列表
    """
    
    def mongodb_query(collection_name: str, query_description: str = "查询所有文档") -> str:
        """查询MongoDB集合中的文档"""
        return client.swarm_query(collection_name, query_description)
    
    def mongodb_insert(collection_name: str, document: Union[Dict, str], 
                      description: str = "插入新文档") -> str:
        """向MongoDB集合插入文档"""
        if isinstance(document, str):
            try:
                document = json.loads(document)
            except json.JSONDecodeError:
                return f"Error: Invalid JSON format in document: {document}"
        
        return client.swarm_insert(collection_name, description, document)
    
    def mongodb_update(collection_name: str, query: Union[Dict, str], 
                      update: Union[Dict, str], description: str = "更新文档") -> str:
        """更新MongoDB集合中的文档"""
        try:
            if isinstance(query, str):
                query = json.loads(query)
            if isinstance(update, str):
                update = json.loads(update)
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON format: {str(e)}"
        
        return client.swarm_update(collection_name, description, query, update)
    
    def mongodb_stats(collection_name: str = None) -> str:
        """获取MongoDB数据库或集合的统计信息"""
        return client.swarm_stats(collection_name)
    
    def mongodb_collections() -> str:
        """列出数据库中的所有集合"""
        result = client.list_collections()
        if result.get("success"):
            collections = result.get("collections", [])
            if collections:
                return f"Available collections: {', '.join(collections)}"
            else:
                return "No collections found in the database"
        else:
            return f"Error listing collections: {result.get('error', 'Unknown error')}"
    
    # 返回函数定义列表
    return [
        {
            "name": "mongodb_query",
            "description": "查询MongoDB集合中的文档",
            "function": mongodb_query
        },
        {
            "name": "mongodb_insert",
            "description": "向MongoDB集合插入文档",
            "function": mongodb_insert
        },
        {
            "name": "mongodb_update",
            "description": "更新MongoDB集合中的文档",
            "function": mongodb_update
        },
        {
            "name": "mongodb_stats",
            "description": "获取MongoDB数据库或集合的统计信息",
            "function": mongodb_stats
        },
        {
            "name": "mongodb_collections",
            "description": "列出数据库中的所有集合",
            "function": mongodb_collections
        }
    ]


def main():
    """测试客户端功能"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Swarm MongoDB MCP Client")
    parser.add_argument(
        "--mcp-server",
        default="http://localhost:8080",
        help="MCP服务器URL"
    )
    parser.add_argument(
        "--database",
        default="test",
        help="数据库名称"
    )
    
    args = parser.parse_args()
    
    # 创建客户端
    client = SwarmMongoDBClient(
        mcp_server_url=args.mcp_server,
        default_database=args.database
    )
    
    print(f"🔗 Connecting to MongoDB MCP Server: {args.mcp_server}")
    
    # 测试连接
    result = client.connect(args.database)
    if result.get("success"):
        print(f"✅ Connected to database: {args.database}")
        
        # 测试基本操作
        print("\n📊 Testing basic operations...")
        
        # 列出集合
        collections = client.list_collections()
        print(f"Collections: {collections}")
        
        # 获取状态
        status = client.get_connection_status()
        print(f"Status: {status}")
        
        # 创建Swarm函数
        functions = create_mongodb_functions(client)
        print(f"\n🔧 Created {len(functions)} Swarm functions:")
        for func in functions:
            print(f"  - {func['name']}: {func['description']}")
        
    else:
        print(f"❌ Connection failed: {result.get('error')}")
    
    client.close()


if __name__ == "__main__":
    main()