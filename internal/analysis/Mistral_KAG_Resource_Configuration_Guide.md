# Mistral + KAG 资源配置完整指南

## 🎯 资源配置策略概览

### 配置原则
```
资源配置策略:
├── 成本优化 (免费资源优先)
├── 性能平衡 (避免瓶颈)
├── 扩展性 (支持业务增长)
└── 可靠性 (生产级稳定)
```

## 💰 免费资源配置方案

### 1. Mistral模型资源

#### OpenRouter免费额度
```yaml
# OpenRouter Mistral配置
mistral_config:
  provider: "openrouter"
  models:
    free_tier:
      - model: "mistralai/mistral-7b-instruct:free"
        limit: "200 requests/day"
        context: "32k tokens"
        cost: "$0"
      - model: "mistralai/mixtral-8x7b-instruct:free" 
        limit: "20 requests/day"
        context: "32k tokens"
        cost: "$0"
    
  api_config:
    base_url: "https://openrouter.ai/api/v1"
    api_key: "${OPENROUTER_API_KEY}"
    headers:
      HTTP-Referer: "https://your-domain.com"
      X-Title: "太公心易系统"
```

#### 官方Mistral免费层
```yaml
# Mistral官方免费配置
mistral_official:
  provider: "mistral"
  free_tier:
    model: "mistral-small-latest"
    limit: "1M tokens/month"
    context: "32k tokens"
    cost: "$0"
  
  api_config:
    base_url: "https://api.mistral.ai/v1"
    api_key: "${MISTRAL_API_KEY}"
```

### 2. KAG部署资源

#### 轻量级部署配置
```yaml
# KAG轻量级配置
kag_config:
  deployment_mode: "lightweight"
  
  # 计算资源
  compute:
    cpu: "4 cores"
    memory: "8GB RAM"
    storage: "50GB SSD"
    gpu: "optional (CPU推理)"
  
  # 组件配置
  components:
    knowledge_extractor:
      model: "BAAI/bge-large-zh-v1.5"  # 免费开源
      device: "cpu"
      batch_size: 16
    
    graph_builder:
      backend: "networkx"  # 轻量级图库
      storage: "sqlite"    # 本地存储
    
    reasoning_engine:
      type: "hybrid"
      symbolic_engine: "owlready2"  # 开源
      neural_engine: "mistral"     # 通过API
```

## 🏗️ 资源架构设计

### 分层资源配置
```
资源分层架构:
┌─────────────────────────────────────┐
│  应用层资源                          │
│  - N8N: 1GB RAM                    │
│  - 太公心易UI: 512MB RAM             │
├─────────────────────────────────────┤
│  智能体层资源                        │
│  - AutoGen: 2GB RAM                │
│  - 11仙智能体: 共享Mistral API       │
├─────────────────────────────────────┤
│  认知中间件层资源                    │
│  - KAG服务: 4GB RAM, 4 CPU         │
│  - 知识图谱: 2GB存储                │
├─────────────────────────────────────┤
│  模型层资源                         │
│  - Mistral API: 免费额度            │
│  - BGE嵌入: 本地CPU推理             │
├─────────────────────────────────────┤
│  数据层资源                         │
│  - Milvus: 4GB RAM, 20GB存储       │
│  - MongoDB: 2GB RAM, 10GB存储      │
└─────────────────────────────────────┘

总计: 16GB RAM, 8 CPU, 80GB存储
```

## 🐳 Docker Compose配置

### 完整的容器化部署
```yaml
# docker-compose.yml
version: '3.8'

services:
  # KAG知识中间件
  kag-service:
    image: kag:latest
    container_name: taigong-kag
    ports:
      - "8080:8080"
    environment:
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - KAG_MODE=lightweight
    volumes:
      - ./kag_data:/app/data
      - ./kag_config:/app/config
    mem_limit: 4g
    cpus: 2.0
    restart: unless-stopped
    depends_on:
      - milvus
      - mongodb

  # Milvus向量数据库
  milvus:
    image: milvusdb/milvus:latest
    container_name: taigong-milvus
    ports:
      - "19530:19530"
    environment:
      - ETCD_ENDPOINTS=etcd:2379
      - MINIO_ADDRESS=minio:9000
    volumes:
      - ./milvus_data:/var/lib/milvus
    mem_limit: 4g
    cpus: 2.0
    restart: unless-stopped

  # MongoDB文档数据库
  mongodb:
    image: mongo:latest
    container_name: taigong-mongodb
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_PASSWORD}
    volumes:
      - ./mongo_data:/data/db
    mem_limit: 2g
    cpus: 1.0
    restart: unless-stopped

  # N8N工作流
  n8n:
    image: n8nio/n8n:latest
    container_name: taigong-n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - WEBHOOK_URL=https://your-domain.com
    volumes:
      - ./n8n_data:/home/node/.n8n
    mem_limit: 1g
    cpus: 1.0
    restart: unless-stopped

  # 太公心易应用
  taigong-app:
    build: ./app
    container_name: taigong-xinyi
    ports:
      - "8501:8501"
    environment:
      - KAG_API_URL=http://kag-service:8080
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
    volumes:
      - ./app_data:/app/data
    mem_limit: 1g
    cpus: 1.0
    restart: unless-stopped
    depends_on:
      - kag-service

  # Redis缓存
  redis:
    image: redis:alpine
    container_name: taigong-redis
    ports:
      - "6379:6379"
    volumes:
      - ./redis_data:/data
    mem_limit: 512m
    cpus: 0.5
    restart: unless-stopped

# 网络配置
networks:
  default:
    name: taigong-network
    driver: bridge

# 数据卷
volumes:
  kag_data:
  milvus_data:
  mongo_data:
  n8n_data:
  app_data:
  redis_data:
```

## ⚙️ 环境变量配置

### .env文件
```bash
# .env
# API密钥
MISTRAL_API_KEY=your_mistral_api_key
OPENROUTER_API_KEY=your_openrouter_key
COHERE_API_KEY=your_cohere_key

# 数据库配置
MONGO_PASSWORD=your_mongo_password
REDIS_PASSWORD=your_redis_password

# N8N配置
N8N_USER=admin
N8N_PASSWORD=your_n8n_password

# KAG配置
KAG_MODE=lightweight
KAG_LOG_LEVEL=INFO

# Milvus配置
MILVUS_HOST=milvus
MILVUS_PORT=19530

# 应用配置
APP_ENV=production
APP_DEBUG=false
```

## 📊 资源监控配置

### Prometheus + Grafana监控
```yaml
# monitoring/docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: taigong-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    mem_limit: 1g
    cpus: 0.5

  grafana:
    image: grafana/grafana:latest
    container_name: taigong-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    mem_limit: 512m
    cpus: 0.5

volumes:
  prometheus_data:
  grafana_data:
```

## 💡 成本优化策略

### 免费资源最大化利用
```python
# 智能API路由配置
class APIResourceManager:
    def __init__(self):
        self.providers = {
            "openrouter_free": {
                "daily_limit": 200,
                "current_usage": 0,
                "models": ["mistral-7b-instruct:free"]
            },
            "mistral_free": {
                "monthly_limit": 1000000,  # tokens
                "current_usage": 0,
                "models": ["mistral-small-latest"]
            },
            "local_models": {
                "unlimited": True,
                "models": ["bge-large-zh-v1.5"]
            }
        }
    
    def get_best_provider(self, task_type, complexity):
        """智能选择最佳提供商"""
        if task_type == "embedding":
            return "local_models"
        
        if complexity == "simple" and self.providers["openrouter_free"]["current_usage"] < 180:
            return "openrouter_free"
        
        if self.providers["mistral_free"]["current_usage"] < 900000:
            return "mistral_free"
        
        # 降级到本地模型
        return "local_models"
```

## 🚀 部署脚本

### 一键部署脚本
```bash
#!/bin/bash
# deploy.sh

echo "🚀 开始部署太公心易 + KAG + Mistral系统..."

# 1. 检查依赖
echo "📋 检查系统依赖..."
command -v docker >/dev/null 2>&1 || { echo "请先安装Docker"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "请先安装Docker Compose"; exit 1; }

# 2. 创建目录结构
echo "📁 创建目录结构..."
mkdir -p {kag_data,milvus_data,mongo_data,n8n_data,app_data,redis_data}
mkdir -p {kag_config,monitoring}

# 3. 检查环境变量
echo "🔑 检查环境变量..."
if [ ! -f .env ]; then
    echo "请先配置.env文件"
    exit 1
fi

# 4. 启动服务
echo "🐳 启动Docker服务..."
docker-compose up -d

# 5. 等待服务就绪
echo "⏳ 等待服务启动..."
sleep 30

# 6. 健康检查
echo "🏥 执行健康检查..."
curl -f http://localhost:8080/health || echo "KAG服务未就绪"
curl -f http://localhost:19530/health || echo "Milvus服务未就绪"
curl -f http://localhost:5678/healthz || echo "N8N服务未就绪"

echo "✅ 部署完成！"
echo "🌐 访问地址："
echo "  - 太公心易应用: http://localhost:8501"
echo "  - N8N工作流: http://localhost:5678"
echo "  - KAG API: http://localhost:8080"
echo "  - 监控面板: http://localhost:3000"
```

## 📈 扩展配置

### 生产环境扩展
```yaml
# 生产环境资源配置
production_config:
  compute:
    cpu: "16 cores"
    memory: "64GB RAM"
    storage: "500GB SSD"
    gpu: "NVIDIA T4 (可选)"
  
  high_availability:
    replicas: 3
    load_balancer: "nginx"
    failover: "automatic"
  
  monitoring:
    metrics: "prometheus"
    logging: "elasticsearch"
    alerting: "alertmanager"
```

## 🎯 总结

**推荐的资源配置策略：**

1. **开发/测试**: 使用免费API + 轻量级部署
2. **小规模生产**: 混合免费+付费API + 中等资源
3. **大规模生产**: 私有化部署 + 充足资源

**关键配置要点：**
- ✅ 充分利用免费API额度
- ✅ 智能路由避免超限
- ✅ 容器化部署便于扩展
- ✅ 监控资源使用情况

想要我帮你根据你的具体需求调整这个配置方案吗？🤔