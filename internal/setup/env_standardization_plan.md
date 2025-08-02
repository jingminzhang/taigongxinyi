# 炼妖壶环境变量标准化方案

## 🎯 命名规范

### **标准格式**
```
{SERVICE}_{CATEGORY}_{SPECIFIC}
```

### **分类说明**
- `API_KEY` - API密钥
- `URL` - 服务地址
- `TOKEN` - 访问令牌
- `CONFIG` - 配置参数
- `DB` - 数据库相关

## 📋 需要修改的变量

### **AI服务类**
```bash
# 当前 → 标准化
ANTHROPIC_AUTH_TOKEN → ANTHROPIC_API_KEY
ANTHROPIC_BASE_URL → ANTHROPIC_API_URL
OPENROUTER_API_KEY_1 → OPENROUTER_API_KEY_PRIMARY
OPENROUTER_API_KEY_2 → OPENROUTER_API_KEY_SECONDARY  
OPENROUTER_API_KEY_3 → OPENROUTER_API_KEY_TERTIARY
OPENROUTER_API_KEY_4 → OPENROUTER_API_KEY_QUATERNARY
HUGGINGFACE_API_TOKEN → HUGGINGFACE_API_KEY
HF_TOKEN → HUGGINGFACE_TOKEN (保留作为别名)
```

### **数据库类**
```bash
# 当前 → 标准化
DATABASE_URL → POSTGRES_DATABASE_URL
SUPABASE_URL → SUPABASE_DATABASE_URL
SUPABASE_ANON_KEY → SUPABASE_API_KEY_ANON
SUPABASE_SECRET_KEY → SUPABASE_API_KEY_SECRET
SUPABASE_PUBLISHABLE_KEY → SUPABASE_API_KEY_PUBLIC
SUPABASE_PERSONAL_TOKEN → SUPABASE_API_TOKEN
NEON_DB_URL → NEON_DATABASE_URL
NEON_API → NEON_API_KEY
```

### **向量数据库类**
```bash
# 当前 → 标准化
ZILLIZ_ENDPOINT → ZILLIZ_API_URL
ZILLIZ_USER → ZILLIZ_USERNAME
ZILLIZ_PASSWD → ZILLIZ_PASSWORD
ZILLIZ_TOKEN → ZILLIZ_API_KEY
ZILLIZ_CLOUD_TOKEN → ZILLIZ_CLOUD_API_KEY
MILVUS_URI → MILVUS_API_URL
MILVUS_TOKEN → MILVUS_API_KEY
```

### **金融数据类**
```bash
# 当前 → 标准化
ALPHA_VANTAGE_API → ALPHA_VANTAGE_API_KEY
RAPIDAPI_KEY → RAPIDAPI_API_KEY
COINGECKO_PRO_API_KEY → COINGECKO_API_KEY_PRO
POLYGON_API_KEY → POLYGON_API_KEY (保持不变)
```

### **社交媒体类**
```bash
# 当前 → 标准化
MASTODON_APP_ID → MASTODON_CLIENT_ID
MASTODON_APP_SECRET → MASTODON_CLIENT_SECRET
MASTODON_ACCESS_TOKEN → MASTODON_API_TOKEN
```

### **缓存和队列类**
```bash
# 当前 → 标准化
UPSTASH_REDIS_URL → UPSTASH_REDIS_DATABASE_URL
UPSTASH_REDIS_REST_URL → UPSTASH_REDIS_API_URL
UPSTASH_REDIS_REST_TOKEN → UPSTASH_REDIS_API_TOKEN
QSTASH_URL → QSTASH_API_URL
QSTASH_TOKEN → QSTASH_API_TOKEN
```

### **Interactive Brokers类**
```bash
# 当前 → 标准化
IB_HOST → IBKR_API_HOST
IB_PORT → IBKR_API_PORT
IB_CLIENT_ID → IBKR_CLIENT_ID
IB_TIMEOUT → IBKR_API_TIMEOUT
IB_RETRY_COUNT → IBKR_API_RETRY_COUNT
IB_MARKET_DATA_TYPE → IBKR_MARKET_DATA_TYPE
IB_REQUEST_TIMEOUT → IBKR_REQUEST_TIMEOUT
```

### **其他服务类**
```bash
# 当前 → 标准化
TAVILY_API_KEY → TAVILY_API_KEY (保持不变)
LANCEDB_API → LANCEDB_API_KEY
KOREAN_MCP_SERVER_URL → KOREAN_MCP_API_URL
KOREAN_MCP_API_KEY → KOREAN_MCP_API_KEY (保持不变)
KOREAN_MCP_TIMEOUT → KOREAN_MCP_API_TIMEOUT
```

## 🔧 项目内部引用修改

### **Python代码中的引用**
```python
# 需要修改的文件和引用
src/core/xinyi_api.py:
  - os.getenv('ANTHROPIC_AUTH_TOKEN') → os.getenv('ANTHROPIC_API_KEY')
  - os.getenv('ANTHROPIC_BASE_URL') → os.getenv('ANTHROPIC_API_URL')

src/core/enhanced_jixia_academy.py:
  - os.getenv('OPENROUTER_API_KEY_1') → os.getenv('OPENROUTER_API_KEY_PRIMARY')

app/services/api_client.py:
  - os.getenv('DATABASE_URL') → os.getenv('POSTGRES_DATABASE_URL')

scripts/mcp/yahoo-finance-mcp/server.py:
  - os.getenv('RAPIDAPI_KEY') → os.getenv('RAPIDAPI_API_KEY')
```

### **配置文件中的引用**
```yaml
# .github/workflows/claude.yml
env:
  ANTHROPIC_AUTH_TOKEN: ${{ secrets.ANTHROPIC_API_KEY }}
  ANTHROPIC_BASE_URL: ${{ secrets.ANTHROPIC_API_URL }}

# docker-compose.yml
environment:
  - DATABASE_URL=${POSTGRES_DATABASE_URL}
  - ZILLIZ_TOKEN=${ZILLIZ_API_KEY}
```

### **文档中的引用**
```markdown
# README.md, docs/等文件中需要更新
- ANTHROPIC_AUTH_TOKEN → ANTHROPIC_API_KEY
- DATABASE_URL → POSTGRES_DATABASE_URL
```

## 📝 注释规范

### **分组注释**
```bash
# ===========================================
# AI服务配置
# ===========================================
ANTHROPIC_API_KEY=sk-xxx                    # Claude AI API密钥
ANTHROPIC_API_URL=https://anyrouter.top     # Claude API代理地址
OPENROUTER_API_KEY_PRIMARY=sk-or-v1-xxx     # OpenRouter主要API密钥
OPENROUTER_API_KEY_SECONDARY=sk-or-v1-xxx   # OpenRouter备用API密钥

# ===========================================
# 数据库配置
# ===========================================
POSTGRES_DATABASE_URL=postgresql://xxx      # 主数据库连接
SUPABASE_DATABASE_URL=postgresql://xxx      # Supabase数据库连接
SUPABASE_API_KEY_ANON=xxx                   # Supabase匿名访问密钥

# ===========================================
# 向量数据库配置
# ===========================================
ZILLIZ_API_URL=https://xxx                  # Zilliz向量数据库地址
ZILLIZ_API_KEY=xxx                          # Zilliz API密钥
MILVUS_API_URL=xxx                          # Milvus向量数据库地址

# ===========================================
# 金融数据API
# ===========================================
RAPIDAPI_API_KEY=xxx                        # RapidAPI统一密钥
ALPHA_VANTAGE_API_KEY=xxx                   # Alpha Vantage股票数据
POLYGON_API_KEY=xxx                         # Polygon金融数据

# ===========================================
# Interactive Brokers配置
# ===========================================
IBKR_API_HOST=127.0.0.1                    # IB API主机地址
IBKR_API_PORT=4002                         # IB API端口
IBKR_CLIENT_ID=1                           # IB客户端ID
```

## 🚀 迁移步骤

### **Step 1: 备份现有配置**
```bash
cp .env .env.backup.$(date +%Y%m%d)
```

### **Step 2: 批量替换**
```bash
# 使用sed批量替换
sed -i.bak 's/ANTHROPIC_AUTH_TOKEN/ANTHROPIC_API_KEY/g' .env
sed -i.bak 's/ANTHROPIC_BASE_URL/ANTHROPIC_API_URL/g' .env
# ... 其他替换
```

### **Step 3: 更新代码引用**
```bash
# 在所有Python文件中替换
find . -name "*.py" -exec sed -i.bak 's/ANTHROPIC_AUTH_TOKEN/ANTHROPIC_API_KEY/g' {} \;
find . -name "*.py" -exec sed -i.bak 's/DATABASE_URL/POSTGRES_DATABASE_URL/g' {} \;
```

### **Step 4: 更新配置文件**
```bash
# 更新GitHub Actions
sed -i.bak 's/ANTHROPIC_AUTH_TOKEN/ANTHROPIC_API_KEY/g' .github/workflows/*.yml
```

### **Step 5: 同步到Doppler**
```bash
# 上传标准化后的环境变量
doppler secrets upload .env
```

## ✅ 验证清单

- [ ] 所有环境变量遵循命名规范
- [ ] 添加了清晰的分组注释
- [ ] 更新了所有代码引用
- [ ] 更新了配置文件
- [ ] 更新了文档
- [ ] 同步到Doppler
- [ ] 测试所有功能正常

## 🎯 最终效果

标准化后的.env文件将具有：
- 🏷️ **一致的命名规范**
- 📝 **清晰的分组和注释**
- 🔍 **易于搜索和维护**
- 🔄 **与Doppler完美同步**