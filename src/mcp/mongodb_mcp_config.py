#!/usr/bin/env python3
"""
MongoDB MCP Configuration for Swarm
Swarm框架的MongoDB MCP配置文件

功能:
- 配置MongoDB MCP服务器
- 集成到Swarm代理中
- 提供完整的使用示例
- 环境变量管理
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class MongoDBMCPConfig:
    """
    MongoDB MCP配置类
    """
    # MCP服务器配置
    mcp_server_host: str = "localhost"
    mcp_server_port: int = 8080
    mcp_server_url: Optional[str] = None
    
    # MongoDB配置
    mongodb_url: str = "mongodb://localhost:27017"
    default_database: str = "swarm_data"
    
    # Swarm集成配置
    enable_auto_connect: bool = True
    max_query_limit: int = 1000
    default_query_limit: int = 100
    
    # 日志配置
    log_level: str = "INFO"
    enable_query_logging: bool = True
    
    def __post_init__(self):
        """初始化后处理"""
        if not self.mcp_server_url:
            self.mcp_server_url = f"http://{self.mcp_server_host}:{self.mcp_server_port}"
        
        # 从环境变量覆盖配置
        self.mongodb_url = os.getenv('MONGODB_URL', self.mongodb_url)
        self.default_database = os.getenv('MONGODB_DEFAULT_DB', self.default_database)
        self.mcp_server_host = os.getenv('MCP_SERVER_HOST', self.mcp_server_host)
        self.mcp_server_port = int(os.getenv('MCP_SERVER_PORT', str(self.mcp_server_port)))
        
        # 重新构建URL
        if not os.getenv('MCP_SERVER_URL'):
            self.mcp_server_url = f"http://{self.mcp_server_host}:{self.mcp_server_port}"
        else:
            self.mcp_server_url = os.getenv('MCP_SERVER_URL')
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'mcp_server_host': self.mcp_server_host,
            'mcp_server_port': self.mcp_server_port,
            'mcp_server_url': self.mcp_server_url,
            'mongodb_url': self.mongodb_url,
            'default_database': self.default_database,
            'enable_auto_connect': self.enable_auto_connect,
            'max_query_limit': self.max_query_limit,
            'default_query_limit': self.default_query_limit,
            'log_level': self.log_level,
            'enable_query_logging': self.enable_query_logging
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MongoDBMCPConfig':
        """从字典创建配置"""
        return cls(**data)
    
    @classmethod
    def from_env(cls) -> 'MongoDBMCPConfig':
        """从环境变量创建配置"""
        return cls()
    
    def save_to_file(self, filepath: str):
        """保存配置到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'MongoDBMCPConfig':
        """从文件加载配置"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


class SwarmMongoDBIntegration:
    """
    Swarm MongoDB集成类
    负责将MongoDB MCP服务器集成到Swarm框架中
    """
    
    def __init__(self, config: MongoDBMCPConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 设置日志级别
        logging.basicConfig(
            level=getattr(logging, config.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def create_swarm_agent_config(self) -> Dict[str, Any]:
        """
        创建Swarm代理配置
        
        Returns:
            Swarm代理配置字典
        """
        return {
            "name": "mongodb_agent",
            "description": "MongoDB数据库操作代理，支持CRUD操作、聚合查询和数据库管理",
            "instructions": self._get_agent_instructions(),
            "functions": self._get_agent_functions(),
            "mcp_config": {
                "server_url": self.config.mcp_server_url,
                "mongodb_url": self.config.mongodb_url,
                "default_database": self.config.default_database
            }
        }
    
    def _get_agent_instructions(self) -> str:
        """
        获取代理指令
        
        Returns:
            代理指令字符串
        """
        return f"""
你是一个MongoDB数据库操作专家代理。你的主要职责是：

1. **数据查询**: 帮助用户查询MongoDB集合中的数据
   - 支持自然语言查询描述
   - 自动限制查询结果数量（默认{self.config.default_query_limit}条，最大{self.config.max_query_limit}条）
   - 提供清晰的查询结果格式

2. **数据操作**: 执行数据的增删改操作
   - 插入新文档或批量插入
   - 更新现有文档
   - 删除不需要的文档
   - 确保操作安全性

3. **数据库管理**: 提供数据库管理功能
   - 查看集合列表
   - 获取集合统计信息
   - 创建索引优化查询性能
   - 监控数据库状态

4. **最佳实践**:
   - 在执行删除或更新操作前，先确认影响范围
   - 对于大量数据操作，提供进度反馈
   - 遇到错误时，提供清晰的错误说明和解决建议
   - 保护敏感数据，避免泄露

当前连接的数据库: {self.config.default_database}
MongoDB服务器: {self.config.mongodb_url.replace(self.config.mongodb_url.split('@')[0].split('//')[1] + '@', '***@') if '@' in self.config.mongodb_url else self.config.mongodb_url}

请始终以友好、专业的方式协助用户完成MongoDB相关任务。
""".strip()
    
    def _get_agent_functions(self) -> List[str]:
        """
        获取代理函数列表
        
        Returns:
            函数名称列表
        """
        return [
            "mongodb_query",
            "mongodb_insert", 
            "mongodb_update",
            "mongodb_stats",
            "mongodb_collections"
        ]
    
    def create_mcp_server_config(self) -> Dict[str, Any]:
        """
        创建MCP服务器配置
        
        Returns:
            MCP服务器配置字典
        """
        return {
            "name": "mongodb-mcp-server",
            "description": "MongoDB MCP服务器，为Swarm提供MongoDB数据库访问功能",
            "version": "1.0.0",
            "server": {
                "host": self.config.mcp_server_host,
                "port": self.config.mcp_server_port,
                "url": self.config.mcp_server_url
            },
            "mongodb": {
                "url": self.config.mongodb_url,
                "default_database": self.config.default_database
            },
            "tools": [
                {
                    "name": "connect_database",
                    "description": "连接到MongoDB数据库",
                    "parameters": {
                        "database_name": {"type": "string", "description": "数据库名称"}
                    }
                },
                {
                    "name": "insert_document",
                    "description": "插入文档到集合",
                    "parameters": {
                        "collection_name": {"type": "string", "description": "集合名称"},
                        "document": {"type": "object", "description": "要插入的文档"},
                        "many": {"type": "boolean", "description": "是否批量插入"}
                    }
                },
                {
                    "name": "find_documents",
                    "description": "查找文档",
                    "parameters": {
                        "collection_name": {"type": "string", "description": "集合名称"},
                        "query": {"type": "object", "description": "查询条件"},
                        "limit": {"type": "integer", "description": "限制数量"}
                    }
                },
                {
                    "name": "update_document",
                    "description": "更新文档",
                    "parameters": {
                        "collection_name": {"type": "string", "description": "集合名称"},
                        "query": {"type": "object", "description": "查询条件"},
                        "update": {"type": "object", "description": "更新操作"}
                    }
                },
                {
                    "name": "delete_document",
                    "description": "删除文档",
                    "parameters": {
                        "collection_name": {"type": "string", "description": "集合名称"},
                        "query": {"type": "object", "description": "查询条件"}
                    }
                },
                {
                    "name": "aggregate_query",
                    "description": "执行聚合查询",
                    "parameters": {
                        "collection_name": {"type": "string", "description": "集合名称"},
                        "pipeline": {"type": "array", "description": "聚合管道"}
                    }
                },
                {
                    "name": "list_collections",
                    "description": "列出所有集合",
                    "parameters": {}
                },
                {
                    "name": "create_index",
                    "description": "创建索引",
                    "parameters": {
                        "collection_name": {"type": "string", "description": "集合名称"},
                        "index_spec": {"type": "object", "description": "索引规范"}
                    }
                },
                {
                    "name": "get_collection_stats",
                    "description": "获取集合统计信息",
                    "parameters": {
                        "collection_name": {"type": "string", "description": "集合名称"}
                    }
                }
            ],
            "resources": [
                {
                    "uri": "mongodb://status",
                    "name": "MongoDB连接状态",
                    "description": "获取MongoDB连接状态和基本信息"
                },
                {
                    "uri": "mongodb://databases",
                    "name": "数据库列表",
                    "description": "获取所有可用数据库的列表"
                }
            ]
        }
    
    def generate_docker_compose(self) -> str:
        """
        生成Docker Compose配置
        
        Returns:
            Docker Compose YAML字符串
        """
        return f"""
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    container_name: swarm_mongodb
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
      MONGO_INITDB_DATABASE: {self.config.default_database}
    volumes:
      - mongodb_data:/data/db
      - ./mongo-init:/docker-entrypoint-initdb.d
    networks:
      - swarm_network

  mongodb-mcp-server:
    build:
      context: .
      dockerfile: Dockerfile.mongodb-mcp
    container_name: swarm_mongodb_mcp
    restart: unless-stopped
    ports:
      - "{self.config.mcp_server_port}:{self.config.mcp_server_port}"
    environment:
      MONGODB_URL: [REDACTED - 从Doppler获取MONGODB_URL]
      MCP_SERVER_PORT: {self.config.mcp_server_port}
      LOG_LEVEL: {self.config.log_level}
    depends_on:
      - mongodb
    networks:
      - swarm_network

volumes:
  mongodb_data:

networks:
  swarm_network:
    driver: bridge
""".strip()
    
    def generate_dockerfile(self) -> str:
        """
        生成Dockerfile
        
        Returns:
            Dockerfile内容字符串
        """
        return """
# Dockerfile.mongodb-mcp
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements-mongodb-mcp.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements-mongodb-mcp.txt

# 复制源代码
COPY src/mcp/ ./src/mcp/

# 设置环境变量
ENV PYTHONPATH=/app
ENV MONGODB_URL=mongodb://localhost:27017
ENV MCP_SERVER_PORT=8080

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "src/mcp/mongodb_mcp_server.py", "--port", "8080"]
""".strip()
    
    def generate_requirements(self) -> str:
        """
        生成requirements文件
        
        Returns:
            requirements.txt内容
        """
        return """
# MongoDB MCP Server Requirements
pymongo>=4.5.0
requests>=2.31.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.4.0
aiofiles>=23.2.1
python-multipart>=0.0.6
""".strip()
    
    def create_env_template(self) -> str:
        """
        创建环境变量模板
        
        Returns:
            .env模板内容
        """
        return f"""
# MongoDB MCP Configuration
# MongoDB连接配置
MONGODB_URL={self.config.mongodb_url}
MONGODB_DEFAULT_DB={self.config.default_database}

# MCP服务器配置
MCP_SERVER_HOST={self.config.mcp_server_host}
MCP_SERVER_PORT={self.config.mcp_server_port}
MCP_SERVER_URL={self.config.mcp_server_url}

# 日志配置
LOG_LEVEL={self.config.log_level}
ENABLE_QUERY_LOGGING={str(self.config.enable_query_logging).lower()}

# Swarm集成配置
ENABLE_AUTO_CONNECT={str(self.config.enable_auto_connect).lower()}
MAX_QUERY_LIMIT={self.config.max_query_limit}
DEFAULT_QUERY_LIMIT={self.config.default_query_limit}
""".strip()


def create_complete_setup(output_dir: str = "./mongodb_mcp_setup"):
    """
    创建完整的MongoDB MCP设置
    
    Args:
        output_dir: 输出目录
    """
    import os
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建配置
    config = MongoDBMCPConfig.from_env()
    integration = SwarmMongoDBIntegration(config)
    
    # 保存配置文件
    config.save_to_file(os.path.join(output_dir, "mongodb_mcp_config.json"))
    
    # 生成Swarm代理配置
    agent_config = integration.create_swarm_agent_config()
    with open(os.path.join(output_dir, "swarm_agent_config.json"), 'w', encoding='utf-8') as f:
        json.dump(agent_config, f, indent=2, ensure_ascii=False)
    
    # 生成MCP服务器配置
    server_config = integration.create_mcp_server_config()
    with open(os.path.join(output_dir, "mcp_server_config.json"), 'w', encoding='utf-8') as f:
        json.dump(server_config, f, indent=2, ensure_ascii=False)
    
    # 生成Docker配置
    with open(os.path.join(output_dir, "docker-compose.yml"), 'w', encoding='utf-8') as f:
        f.write(integration.generate_docker_compose())
    
    with open(os.path.join(output_dir, "Dockerfile.mongodb-mcp"), 'w', encoding='utf-8') as f:
        f.write(integration.generate_dockerfile())
    
    # 生成requirements
    with open(os.path.join(output_dir, "requirements-mongodb-mcp.txt"), 'w', encoding='utf-8') as f:
        f.write(integration.generate_requirements())
    
    # 生成环境变量模板
    with open(os.path.join(output_dir, ".env.template"), 'w', encoding='utf-8') as f:
        f.write(integration.create_env_template())
    
    # 生成README
    readme_content = f"""
# MongoDB MCP for Swarm

这是一个完整的MongoDB MCP服务器设置，用于与Swarm框架集成。

## 文件说明

- `mongodb_mcp_config.json`: MongoDB MCP配置文件
- `swarm_agent_config.json`: Swarm代理配置
- `mcp_server_config.json`: MCP服务器配置
- `docker-compose.yml`: Docker Compose配置
- `Dockerfile.mongodb-mcp`: MCP服务器Docker镜像
- `requirements-mongodb-mcp.txt`: Python依赖
- `.env.template`: 环境变量模板

## 快速开始

1. 复制环境变量模板:
   ```bash
   cp .env.template .env
   ```

2. 编辑 `.env` 文件，设置你的MongoDB连接信息

3. 启动服务:
   ```bash
   docker-compose up -d
   ```

4. 验证服务:
   ```bash
   curl http://localhost:{config.mcp_server_port}/health
   ```

## 在Swarm中使用

```python
from src.mcp.swarm_mongodb_client import SwarmMongoDBClient, create_mongodb_functions
from swarm import Swarm, Agent

# 创建MongoDB客户端
mongodb_client = SwarmMongoDBClient(
    mcp_server_url="http://localhost:{config.mcp_server_port}",
    default_database="{config.default_database}"
)

# 连接数据库
mongodb_client.connect()

# 创建MongoDB函数
mongodb_functions = create_mongodb_functions(mongodb_client)

# 创建Swarm代理
agent = Agent(
    name="MongoDB助手",
    instructions="你是一个MongoDB数据库专家，帮助用户管理和查询数据库。",
    functions=[func["function"] for func in mongodb_functions]
)

# 使用Swarm
client = Swarm()
response = client.run(
    agent=agent,
    messages=[{{"role": "user", "content": "查询users集合中的所有数据"}}]
)

print(response.messages[-1]["content"])
```

## 可用功能

- `mongodb_query`: 查询集合中的文档
- `mongodb_insert`: 插入新文档
- `mongodb_update`: 更新现有文档
- `mongodb_stats`: 获取统计信息
- `mongodb_collections`: 列出所有集合

## 配置说明

### MongoDB连接
- `MONGODB_URL`: MongoDB连接字符串
- `MONGODB_DEFAULT_DB`: 默认数据库名称

### MCP服务器
- `MCP_SERVER_HOST`: 服务器主机
- `MCP_SERVER_PORT`: 服务器端口

### 查询限制
- `MAX_QUERY_LIMIT`: 最大查询数量限制
- `DEFAULT_QUERY_LIMIT`: 默认查询数量限制

## 故障排除

1. **连接失败**: 检查MongoDB服务是否运行，连接字符串是否正确
2. **权限错误**: 确保MongoDB用户有足够的权限
3. **端口冲突**: 修改 `MCP_SERVER_PORT` 环境变量

## 安全注意事项

- 不要在生产环境中使用默认密码
- 限制MongoDB的网络访问
- 定期备份数据库
- 监控查询性能和资源使用
""".strip()
    
    with open(os.path.join(output_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ MongoDB MCP设置已创建在: {output_dir}")
    print(f"📁 包含以下文件:")
    for file in os.listdir(output_dir):
        print(f"   - {file}")


if __name__ == "__main__":
    # 创建完整设置
    create_complete_setup()
