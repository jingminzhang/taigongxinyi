#!/usr/bin/env python3
"""
MongoDB MCP Server
为Swarm提供MongoDB数据库访问的MCP服务器

功能:
- 连接MongoDB数据库
- 执行CRUD操作
- 聚合查询
- 索引管理
- 数据库统计
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError, ConnectionFailure
    from bson import ObjectId, json_util
except ImportError:
    print("Error: pymongo is required. Install with: pip install pymongo")
    sys.exit(1)

# MCP协议相关导入
try:
    from mcp import MCPServer, Tool, Resource
    from mcp.types import TextContent, ImageContent, EmbeddedResource
except ImportError:
    # 如果没有mcp库，我们创建一个简单的兼容层
    class MCPServer:
        def __init__(self, name: str):
            self.name = name
            self.tools = {}
            self.resources = {}
        
        def add_tool(self, name: str, description: str, handler):
            self.tools[name] = {
                'description': description,
                'handler': handler
            }
        
        def add_resource(self, uri: str, name: str, description: str, handler):
            self.resources[uri] = {
                'name': name,
                'description': description,
                'handler': handler
            }

class MongoDBMCPServer:
    """
    MongoDB MCP服务器
    提供MongoDB数据库访问功能
    """
    
    def __init__(self, mongodb_url: Optional[str] = None):
        self.mongodb_url = mongodb_url or os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
        self.client = None
        self.db = None
        self.server = MCPServer("mongodb-mcp")
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 注册工具
        self._register_tools()
        self._register_resources()
    
    def _register_tools(self):
        """注册MCP工具"""
        
        # 数据库连接工具
        self.server.add_tool(
            "connect_database",
            "连接到MongoDB数据库",
            self.connect_database
        )
        
        # CRUD操作工具
        self.server.add_tool(
            "insert_document",
            "向集合中插入文档",
            self.insert_document
        )
        
        self.server.add_tool(
            "find_documents",
            "查找文档",
            self.find_documents
        )
        
        self.server.add_tool(
            "update_document",
            "更新文档",
            self.update_document
        )
        
        self.server.add_tool(
            "delete_document",
            "删除文档",
            self.delete_document
        )
        
        # 聚合查询工具
        self.server.add_tool(
            "aggregate_query",
            "执行聚合查询",
            self.aggregate_query
        )
        
        # 数据库管理工具
        self.server.add_tool(
            "list_collections",
            "列出数据库中的所有集合",
            self.list_collections
        )
        
        self.server.add_tool(
            "create_index",
            "创建索引",
            self.create_index
        )
        
        self.server.add_tool(
            "get_collection_stats",
            "获取集合统计信息",
            self.get_collection_stats
        )
    
    def _register_resources(self):
        """注册MCP资源"""
        
        self.server.add_resource(
            "mongodb://status",
            "MongoDB连接状态",
            "获取MongoDB连接状态和基本信息",
            self.get_connection_status
        )
        
        self.server.add_resource(
            "mongodb://databases",
            "数据库列表",
            "获取所有可用数据库的列表",
            self.get_databases_list
        )
    
    async def connect_database(self, database_name: str = "default") -> Dict[str, Any]:
        """连接到MongoDB数据库"""
        try:
            if not self.client:
                self.client = MongoClient(self.mongodb_url)
                # 测试连接
                self.client.admin.command('ping')
                self.logger.info(f"Connected to MongoDB at {self.mongodb_url}")
            
            self.db = self.client[database_name]
            
            return {
                "success": True,
                "message": f"Successfully connected to database '{database_name}'",
                "database_name": database_name,
                "connection_url": self.mongodb_url.replace(self.mongodb_url.split('@')[0].split('//')[1] + '@', '***@') if '@' in self.mongodb_url else self.mongodb_url
            }
            
        except ConnectionFailure as e:
            error_msg = f"Failed to connect to MongoDB: {str(e)}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    async def insert_document(self, collection_name: str, document: Union[Dict, str], many: bool = False) -> Dict[str, Any]:
        """插入文档到集合"""
        try:
            if not self.db:
                return {"success": False, "error": "Database not connected"}
            
            # 如果document是字符串，尝试解析为JSON
            if isinstance(document, str):
                document = json.loads(document)
            
            collection = self.db[collection_name]
            
            if many and isinstance(document, list):
                result = collection.insert_many(document)
                return {
                    "success": True,
                    "inserted_ids": [str(id) for id in result.inserted_ids],
                    "count": len(result.inserted_ids)
                }
            else:
                result = collection.insert_one(document)
                return {
                    "success": True,
                    "inserted_id": str(result.inserted_id)
                }
                
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON: {str(e)}"}
        except PyMongoError as e:
            return {"success": False, "error": f"MongoDB error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def find_documents(self, collection_name: str, query: Union[Dict, str] = None, 
                           projection: Union[Dict, str] = None, limit: int = 100, 
                           skip: int = 0, sort: Union[Dict, str] = None) -> Dict[str, Any]:
        """查找文档"""
        try:
            if not self.db:
                return {"success": False, "error": "Database not connected"}
            
            # 解析参数
            if isinstance(query, str):
                query = json.loads(query) if query else {}
            elif query is None:
                query = {}
            
            if isinstance(projection, str):
                projection = json.loads(projection) if projection else None
            
            if isinstance(sort, str):
                sort = json.loads(sort) if sort else None
            
            collection = self.db[collection_name]
            cursor = collection.find(query, projection)
            
            if sort:
                cursor = cursor.sort(list(sort.items()))
            
            cursor = cursor.skip(skip).limit(limit)
            
            documents = list(cursor)
            
            # 转换ObjectId为字符串
            for doc in documents:
                if '_id' in doc and isinstance(doc['_id'], ObjectId):
                    doc['_id'] = str(doc['_id'])
            
            return {
                "success": True,
                "documents": documents,
                "count": len(documents),
                "query": query,
                "limit": limit,
                "skip": skip
            }
            
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON: {str(e)}"}
        except PyMongoError as e:
            return {"success": False, "error": f"MongoDB error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def update_document(self, collection_name: str, query: Union[Dict, str], 
                            update: Union[Dict, str], many: bool = False) -> Dict[str, Any]:
        """更新文档"""
        try:
            if not self.db:
                return {"success": False, "error": "Database not connected"}
            
            # 解析参数
            if isinstance(query, str):
                query = json.loads(query)
            if isinstance(update, str):
                update = json.loads(update)
            
            collection = self.db[collection_name]
            
            if many:
                result = collection.update_many(query, update)
                return {
                    "success": True,
                    "matched_count": result.matched_count,
                    "modified_count": result.modified_count
                }
            else:
                result = collection.update_one(query, update)
                return {
                    "success": True,
                    "matched_count": result.matched_count,
                    "modified_count": result.modified_count
                }
                
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON: {str(e)}"}
        except PyMongoError as e:
            return {"success": False, "error": f"MongoDB error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def delete_document(self, collection_name: str, query: Union[Dict, str], 
                            many: bool = False) -> Dict[str, Any]:
        """删除文档"""
        try:
            if not self.db:
                return {"success": False, "error": "Database not connected"}
            
            # 解析参数
            if isinstance(query, str):
                query = json.loads(query)
            
            collection = self.db[collection_name]
            
            if many:
                result = collection.delete_many(query)
                return {
                    "success": True,
                    "deleted_count": result.deleted_count
                }
            else:
                result = collection.delete_one(query)
                return {
                    "success": True,
                    "deleted_count": result.deleted_count
                }
                
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON: {str(e)}"}
        except PyMongoError as e:
            return {"success": False, "error": f"MongoDB error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def aggregate_query(self, collection_name: str, pipeline: Union[List, str]) -> Dict[str, Any]:
        """执行聚合查询"""
        try:
            if not self.db:
                return {"success": False, "error": "Database not connected"}
            
            # 解析参数
            if isinstance(pipeline, str):
                pipeline = json.loads(pipeline)
            
            collection = self.db[collection_name]
            result = list(collection.aggregate(pipeline))
            
            # 转换ObjectId为字符串
            for doc in result:
                if '_id' in doc and isinstance(doc['_id'], ObjectId):
                    doc['_id'] = str(doc['_id'])
            
            return {
                "success": True,
                "result": result,
                "count": len(result),
                "pipeline": pipeline
            }
            
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON: {str(e)}"}
        except PyMongoError as e:
            return {"success": False, "error": f"MongoDB error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def list_collections(self) -> Dict[str, Any]:
        """列出数据库中的所有集合"""
        try:
            if not self.db:
                return {"success": False, "error": "Database not connected"}
            
            collections = self.db.list_collection_names()
            
            return {
                "success": True,
                "collections": collections,
                "count": len(collections)
            }
            
        except PyMongoError as e:
            return {"success": False, "error": f"MongoDB error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def create_index(self, collection_name: str, index_spec: Union[Dict, str], 
                          unique: bool = False, background: bool = True) -> Dict[str, Any]:
        """创建索引"""
        try:
            if not self.db:
                return {"success": False, "error": "Database not connected"}
            
            # 解析参数
            if isinstance(index_spec, str):
                index_spec = json.loads(index_spec)
            
            collection = self.db[collection_name]
            
            # 转换为pymongo格式
            index_list = [(key, value) for key, value in index_spec.items()]
            
            result = collection.create_index(
                index_list,
                unique=unique,
                background=background
            )
            
            return {
                "success": True,
                "index_name": result,
                "index_spec": index_spec
            }
            
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON: {str(e)}"}
        except PyMongoError as e:
            return {"success": False, "error": f"MongoDB error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """获取集合统计信息"""
        try:
            if not self.db:
                return {"success": False, "error": "Database not connected"}
            
            collection = self.db[collection_name]
            
            # 获取基本统计
            stats = self.db.command("collStats", collection_name)
            
            # 获取文档数量
            count = collection.count_documents({})
            
            # 获取索引信息
            indexes = list(collection.list_indexes())
            
            return {
                "success": True,
                "collection_name": collection_name,
                "document_count": count,
                "size_bytes": stats.get('size', 0),
                "storage_size_bytes": stats.get('storageSize', 0),
                "indexes": [{
                    "name": idx.get('name'),
                    "key": idx.get('key'),
                    "unique": idx.get('unique', False)
                } for idx in indexes],
                "index_count": len(indexes)
            }
            
        except PyMongoError as e:
            return {"success": False, "error": f"MongoDB error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def get_connection_status(self) -> Dict[str, Any]:
        """获取连接状态"""
        try:
            if not self.client:
                return {
                    "connected": False,
                    "message": "Not connected to MongoDB"
                }
            
            # 测试连接
            self.client.admin.command('ping')
            
            # 获取服务器信息
            server_info = self.client.server_info()
            
            return {
                "connected": True,
                "server_version": server_info.get('version'),
                "connection_url": self.mongodb_url.replace(self.mongodb_url.split('@')[0].split('//')[1] + '@', '***@') if '@' in self.mongodb_url else self.mongodb_url,
                "current_database": self.db.name if self.db else None,
                "server_info": {
                    "version": server_info.get('version'),
                    "git_version": server_info.get('gitVersion'),
                    "platform": server_info.get('platform')
                }
            }
            
        except Exception as e:
            return {
                "connected": False,
                "error": str(e)
            }
    
    async def get_databases_list(self) -> Dict[str, Any]:
        """获取数据库列表"""
        try:
            if not self.client:
                return {"success": False, "error": "Not connected to MongoDB"}
            
            databases = self.client.list_database_names()
            
            return {
                "success": True,
                "databases": databases,
                "count": len(databases)
            }
            
        except PyMongoError as e:
            return {"success": False, "error": f"MongoDB error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    def close_connection(self):
        """关闭数据库连接"""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            self.logger.info("MongoDB connection closed")


def main():
    """主函数 - 启动MCP服务器"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MongoDB MCP Server")
    parser.add_argument(
        "--mongodb-url",
        default=os.getenv('MONGODB_URL', 'mongodb://localhost:27017'),
        help="MongoDB连接URL"
    )
    parser.add_argument(
        "--database",
        default="default",
        help="默认数据库名称"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="MCP服务器端口"
    )
    
    args = parser.parse_args()
    
    # 创建MCP服务器
    mcp_server = MongoDBMCPServer(args.mongodb_url)
    
    print(f"🚀 Starting MongoDB MCP Server...")
    print(f"📊 MongoDB URL: {args.mongodb_url}")
    print(f"🗄️  Default Database: {args.database}")
    print(f"🌐 Port: {args.port}")
    print(f"")
    print(f"Available tools:")
    for tool_name, tool_info in mcp_server.server.tools.items():
        print(f"  - {tool_name}: {tool_info['description']}")
    print(f"")
    print(f"Available resources:")
    for resource_uri, resource_info in mcp_server.server.resources.items():
        print(f"  - {resource_uri}: {resource_info['description']}")
    
    try:
        # 自动连接到默认数据库
        asyncio.run(mcp_server.connect_database(args.database))
        
        # 这里应该启动实际的MCP服务器
        # 由于我们没有完整的MCP库，这里只是演示
        print(f"\n✅ MongoDB MCP Server is ready!")
        print(f"💡 Use this server with Swarm MCP client to access MongoDB")
        
        # 保持服务器运行
        try:
            while True:
                asyncio.run(asyncio.sleep(1))
        except KeyboardInterrupt:
            print("\n🛑 Shutting down MongoDB MCP Server...")
            mcp_server.close_connection()
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()