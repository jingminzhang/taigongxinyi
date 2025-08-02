# MCP Manager - 完整独立包

## 📁 文件结构和内容

### 1. README.md
```markdown
# MCP Service Manager

> 🧙‍♂️ 统一管理stdio、SSE、HTTP类型的MCP服务，解决依赖管理和服务发现痛点

## 🎯 解决的问题

- **多协议混合管理**: stdio/SSE/HTTP服务统一管理
- **依赖检查复杂**: 自动检查Python、Node.js、uv等依赖
- **缺乏监控界面**: Web Dashboard实时监控服务状态
- **配置分散**: 单一YAML文件集中配置
- **批量操作困难**: 服务组批量启停

## 🚀 快速开始

### 安装
```bash
pip install mcp-service-manager
# 或
git clone https://github.com/your-username/mcp-service-manager
cd mcp-service-manager
pip install -e .
```

### 使用
```bash
# 初始化配置
mcp-manager init

# 启动管理器
mcp-manager start

# 访问Web界面
open http://localhost:8090
```

## 📋 支持的MCP类型

### stdio类型
```yaml
- name: my-stdio-service
  type: stdio
  command: python
  args: ["-m", "my_mcp_server"]
  dependencies: ["python>=3.9"]
```

### HTTP类型
```yaml
- name: my-http-service
  type: http
  url: "https://api.example.com/mcp"
  health_check: "https://api.example.com/health"
```

### SSE类型
```yaml
- name: my-sse-service
  type: sse
  url: "https://sse.example.com/events"
```

## 🎮 功能特性

- ✅ Web界面管理
- ✅ 实时状态监控
- ✅ 自动依赖检查
- ✅ 批量服务操作
- ✅ 健康状态检查
- ✅ Docker部署支持
- ✅ 服务组管理
- ✅ API接口

## 📖 文档

- [安装指南](docs/installation.md)
- [配置说明](docs/configuration.md)
- [API文档](docs/api.md)
- [Docker部署](docs/docker.md)

## 🤝 贡献

欢迎提交Issue和PR！

## 📄 许可证

MIT License
```

### 2. setup.py
```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mcp-service-manager",
    version="1.0.0",
    author="MCP Manager Team",
    author_email="contact@mcpmanager.dev",
    description="Universal MCP service manager for stdio, SSE, and HTTP protocols",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/mcp-service-manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mcp-manager=mcp_manager.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mcp_manager": [
            "templates/*.html",
            "static/*",
            "config/*.yml",
        ],
    },
)
```

### 3. requirements.txt
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pyyaml>=6.0
httpx>=0.25.0
jinja2>=3.1.0
python-multipart>=0.0.6
aiofiles>=23.0.0
psutil>=5.9.0
```

### 4. mcp_manager/__init__.py
```python
"""
MCP Service Manager

Universal manager for stdio, SSE, and HTTP MCP services.
"""

__version__ = "1.0.0"
__author__ = "MCP Manager Team"

from .manager import MCPManager
from .config import MCPConfig, MCPService

__all__ = ["MCPManager", "MCPConfig", "MCPService"]
```

### 5. mcp_manager/cli.py
```python
#!/usr/bin/env python3
"""
MCP Manager CLI
"""

import argparse
import asyncio
import sys
from pathlib import Path
from .manager import MCPManager
from .config import create_default_config

def main():
    parser = argparse.ArgumentParser(description="MCP Service Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize configuration")
    init_parser.add_argument("--config", "-c", default="mcp_services.yml",
                           help="Configuration file path")
    
    # start command
    start_parser = subparsers.add_parser("start", help="Start MCP manager")
    start_parser.add_argument("--config", "-c", default="mcp_services.yml",
                            help="Configuration file path")
    start_parser.add_argument("--port", "-p", type=int, default=8090,
                            help="Manager port")
    start_parser.add_argument("--host", default="0.0.0.0",
                            help="Bind address")
    start_parser.add_argument("--start-all", action="store_true",
                            help="Start all services automatically")
    start_parser.add_argument("--group", "-g",
                            help="Start specific service group")
    
    # list command
    list_parser = subparsers.add_parser("list", help="List services")
    list_parser.add_argument("--config", "-c", default="mcp_services.yml",
                           help="Configuration file path")
    
    # status command
    status_parser = subparsers.add_parser("status", help="Show service status")
    status_parser.add_argument("--config", "-c", default="mcp_services.yml",
                             help="Configuration file path")
    status_parser.add_argument("service", nargs="?", help="Service name")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "init":
        init_config(args.config)
    elif args.command == "start":
        start_manager(args)
    elif args.command == "list":
        list_services(args.config)
    elif args.command == "status":
        show_status(args.config, args.service)

def init_config(config_path):
    """Initialize configuration file"""
    if Path(config_path).exists():
        print(f"❌ Configuration file already exists: {config_path}")
        return
    
    create_default_config(config_path)
    print(f"✅ Created configuration file: {config_path}")
    print(f"💡 Edit {config_path} to configure your MCP services")

def start_manager(args):
    """Start MCP manager"""
    if not Path(args.config).exists():
        print(f"❌ Configuration file not found: {args.config}")
        print("💡 Run 'mcp-manager init' to create default configuration")
        sys.exit(1)
    
    print("🚀 Starting MCP Manager...")
    print(f"📁 Config: {args.config}")
    print(f"🌐 Web UI: http://{args.host}:{args.port}")
    print(f"📊 API: http://{args.host}:{args.port}/docs")
    
    manager = MCPManager(args.config)
    
    if args.group:
        asyncio.run(start_service_group(manager, args.group))
    elif args.start_all:
        asyncio.run(start_all_services(manager))
    
    try:
        manager.run(host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\n🛑 Stopping MCP Manager...")
        asyncio.run(stop_all_services(manager))

def list_services(config_path):
    """List configured services"""
    if not Path(config_path).exists():
        print(f"❌ Configuration file not found: {config_path}")
        return
    
    manager = MCPManager(config_path)
    print("📋 Configured MCP Services:")
    print("-" * 50)
    
    for name, service in manager.services.items():
        print(f"🔧 {name}")
        print(f"   Type: {service.type}")
        print(f"   Status: {service.status}")
        if service.command:
            print(f"   Command: {service.command}")
        if service.url:
            print(f"   URL: {service.url}")
        print()

def show_status(config_path, service_name=None):
    """Show service status"""
    if not Path(config_path).exists():
        print(f"❌ Configuration file not found: {config_path}")
        return
    
    manager = MCPManager(config_path)
    
    if service_name:
        if service_name not in manager.services:
            print(f"❌ Service not found: {service_name}")
            return
        
        status = asyncio.run(manager.get_service_status(service_name))
        print(f"📊 Status for {service_name}:")
        print(f"   Status: {status.get('status', 'unknown')}")
        print(f"   Health: {status.get('health', 'unknown')}")
    else:
        print("📊 All Services Status:")
        print("-" * 30)
        for name in manager.services.keys():
            status = asyncio.run(manager.get_service_status(name))
            print(f"🔧 {name}: {status.get('status', 'unknown')}")

async def start_service_group(manager, group_name):
    """Start service group"""
    # Service groups would be loaded from config
    service_groups = {
        'core': ['basic-service'],
        'all': list(manager.services.keys())
    }
    
    services = service_groups.get(group_name, [])
    if not services:
        print(f"❌ Unknown service group: {group_name}")
        return
    
    print(f"🔄 Starting service group: {group_name}")
    for service_name in services:
        if service_name in manager.services:
            await manager.start_service(service_name)

async def start_all_services(manager):
    """Start all services"""
    print("🔄 Starting all services...")
    for service_name in manager.services.keys():
        await manager.start_service(service_name)

async def stop_all_services(manager):
    """Stop all services"""
    for service_name in manager.services.keys():
        await manager.stop_service(service_name)

if __name__ == "__main__":
    main()
```

### 6. mcp_manager/config.py
```python
"""
Configuration management for MCP Manager
"""

import os
import yaml
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from pathlib import Path

@dataclass
class MCPService:
    """MCP服务配置"""
    name: str
    type: str  # stdio, sse, http
    command: Optional[str] = None
    args: Optional[List[str]] = None
    env: Optional[Dict[str, str]] = None
    url: Optional[str] = None
    port: Optional[int] = None
    health_check: Optional[str] = None
    dependencies: Optional[List[str]] = None
    auto_restart: bool = True
    description: Optional[str] = None
    status: str = "stopped"
    process: Optional[Any] = None

@dataclass
class MCPConfig:
    """MCP管理器配置"""
    services: List[MCPService]
    global_config: Dict[str, Any]
    service_groups: Dict[str, List[str]]

def create_default_config(config_path: str):
    """创建默认配置文件"""
    default_config = {
        'services': [
            {
                'name': 'example-stdio',
                'type': 'stdio',
                'command': 'python',
                'args': ['-m', 'my_mcp_server'],
                'env': {'PYTHONPATH': '.'},
                'dependencies': ['python>=3.9'],
                'auto_restart': True,
                'description': 'Example stdio MCP service'
            },
            {
                'name': 'example-http',
                'type': 'http',
                'url': 'https://api.example.com/mcp',
                'health_check': 'https://api.example.com/health',
                'auto_restart': False,
                'description': 'Example HTTP MCP service'
            },
            {
                'name': 'example-sse',
                'type': 'sse',
                'url': 'https://sse.example.com/events',
                'auto_restart': False,
                'description': 'Example SSE MCP service'
            }
        ],
        'global': {
            'manager_port': 8090,
            'log_level': 'INFO',
            'health_check_interval': 30,
            'restart_delay': 5,
            'max_restart_attempts': 3
        },
        'service_groups': {
            'core': ['example-stdio', 'example-http'],
            'all': ['example-stdio', 'example-http', 'example-sse']
        }
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)

def load_config(config_path: str) -> MCPConfig:
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    services = []
    for service_config in config_data.get('services', []):
        service = MCPService(**service_config)
        services.append(service)
    
    return MCPConfig(
        services=services,
        global_config=config_data.get('global', {}),
        service_groups=config_data.get('service_groups', {})
    )
```

### 7. 复制现有文件
- 将之前创建的 `mcp_manager.py` 重命名为 `mcp_manager/manager.py`
- 将 `templates/mcp_dashboard.html` 复制到 `mcp_manager/templates/dashboard.html`
- 将 `docker-compose.mcp.yml` 复制到 `docker/docker-compose.yml`

### 8. docs/installation.md
```markdown
# 安装指南

## 系统要求

- Python 3.9+
- pip

## 安装方式

### 1. 从PyPI安装 (推荐)
```bash
pip install mcp-service-manager
```

### 2. 从源码安装
```bash
git clone https://github.com/your-username/mcp-service-manager
cd mcp-service-manager
pip install -e .
```

### 3. Docker安装
```bash
docker pull mcpmanager/mcp-service-manager
```

## 验证安装

```bash
mcp-manager --help
```

## 快速开始

```bash
# 创建配置文件
mcp-manager init

# 启动管理器
mcp-manager start
```
```

这个完整的包可以直接作为独立项目发布，完全脱离太公心易项目。要我继续创建其他文件吗？