# 炼妖壶调用OpenManus集成方案

## 🎯 架构设计

```
炼妖壶 (Cauldron) ←→ OpenManus (爬虫服务)
    ↓                      ↓
太公心易分析系统        Playwright爬虫引擎
    ↓                      ↓
八仙论道辩论           Seeking Alpha数据
```

## 🔌 集成方式

### 1. **HTTP API调用** (推荐)

#### OpenManus端提供RESTful API
```python
# OpenManus项目中
from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.post("/scrape/seekingalpha")
async def scrape_seeking_alpha(request: ScrapeRequest):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 设置反检测
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
        
        await page.goto(request.url)
        content = await page.content()
        await browser.close()
        
        return {"content": content, "status": "success"}
```

#### 炼妖壶端调用
```python
# 在你的炼妖壶项目中
import httpx

class OpenManusClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.client = httpx.AsyncClient()
    
    async def scrape_seeking_alpha(self, url: str):
        """调用OpenManus爬取Seeking Alpha"""
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        response = await self.client.post(
            f"{self.base_url}/scrape/seekingalpha",
            json={"url": url},
            headers=headers
        )
        return response.json()

# 使用示例
openmanus = OpenManusClient("https://openmanus.your-domain.com")
result = await openmanus.scrape_seeking_alpha(
    "https://seekingalpha.com/pr/20162773-ai-device-startup..."
)
```

### 2. **MCP协议集成** (最优雅)

#### OpenManus作为MCP服务
```python
# OpenManus项目中实现MCP服务器
from mcp import MCPServer

class OpenManusMCPServer(MCPServer):
    def __init__(self):
        super().__init__("openmanus-scraper")
        self.register_tool("scrape_seeking_alpha", self.scrape_seeking_alpha)
    
    async def scrape_seeking_alpha(self, url: str, extract_type: str = "article"):
        """MCP工具：爬取Seeking Alpha内容"""
        # Playwright爬虫逻辑
        return {
            "url": url,
            "title": extracted_title,
            "content": extracted_content,
            "metadata": metadata
        }
```

#### 炼妖壶端配置
```yaml
# mcp_services.yml中添加
services:
  - name: openmanus-scraper
    type: stdio  # 或 http
    command: python
    args: ["-m", "openmanus.mcp_server"]
    env:
      OPENMANUS_API_URL: "https://openmanus.your-domain.com"
      OPENMANUS_API_KEY: "${OPENMANUS_API_KEY}"
    dependencies: ["python>=3.9", "playwright"]
    description: "OpenManus网页爬虫服务"
```

### 3. **消息队列异步调用**

#### 使用Redis/RabbitMQ
```python
# 炼妖壶端发送任务
import redis
import json

class OpenManusQueue:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
    
    async def submit_scrape_task(self, url: str, callback_url: str = None):
        """提交爬虫任务到队列"""
        task = {
            "id": generate_task_id(),
            "url": url,
            "type": "seeking_alpha",
            "callback_url": callback_url,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.redis.lpush("openmanus:tasks", json.dumps(task))
        return task["id"]
    
    async def get_result(self, task_id: str):
        """获取爬虫结果"""
        result = self.redis.get(f"openmanus:result:{task_id}")
        return json.loads(result) if result else None
```

### 4. **gRPC高性能调用**

#### OpenManus gRPC服务
```protobuf
// openmanus.proto
service OpenManusService {
    rpc ScrapeSeekingAlpha(ScrapeRequest) returns (ScrapeResponse);
    rpc GetTaskStatus(TaskRequest) returns (TaskResponse);
}

message ScrapeRequest {
    string url = 1;
    string extract_type = 2;
    map<string, string> options = 3;
}
```

#### 炼妖壶gRPC客户端
```python
import grpc
from openmanus_pb2_grpc import OpenManusServiceStub

class OpenManusGRPCClient:
    def __init__(self, server_address: str):
        self.channel = grpc.aio.insecure_channel(server_address)
        self.stub = OpenManusServiceStub(self.channel)
    
    async def scrape_seeking_alpha(self, url: str):
        request = ScrapeRequest(url=url, extract_type="article")
        response = await self.stub.ScrapeSeekingAlpha(request)
        return response
```

## 🔧 炼妖壶中的具体集成

### 1. **在N8N工作流中集成**
```javascript
// N8N自定义节点
{
  "name": "OpenManus Scraper",
  "type": "http-request",
  "url": "https://openmanus.your-domain.com/scrape/seekingalpha",
  "method": "POST",
  "body": {
    "url": "{{$json.article_url}}",
    "extract_type": "full_article"
  }
}
```

### 2. **在八仙论道中使用**
```python
# jixia_academy_clean/core/enhanced_jixia_agents.py
from openmanus_client import OpenManusClient

class EnhancedJixiaAgent:
    def __init__(self):
        self.openmanus = OpenManusClient(
            base_url=os.getenv("OPENMANUS_API_URL"),
            api_key=os.getenv("OPENMANUS_API_KEY")
        )
    
    async def research_topic(self, topic: str):
        """研究特定话题，使用OpenManus获取最新资讯"""
        # 搜索相关文章
        search_urls = await self.search_seeking_alpha(topic)
        
        # 批量爬取内容
        articles = []
        for url in search_urls[:5]:  # 限制数量
            content = await self.openmanus.scrape_seeking_alpha(url)
            articles.append(content)
        
        # 分析内容并生成辩论观点
        return self.generate_debate_points(articles)
```

### 3. **在太公心易系统中集成**
```python
# src/core/xinyi_system.py
class XinyiAnalysisEngine:
    def __init__(self):
        self.openmanus = OpenManusClient(
            base_url=os.getenv("OPENMANUS_API_URL")
        )
    
    async def analyze_market_sentiment(self, symbol: str):
        """分析市场情绪，结合爬虫数据"""
        # 获取Seeking Alpha上的相关分析
        articles = await self.get_symbol_analysis(symbol)
        
        # 结合太公心易的卦象分析
        sentiment_score = self.calculate_sentiment(articles)
        hexagram = self.generate_hexagram(sentiment_score)
        
        return {
            "symbol": symbol,
            "sentiment": sentiment_score,
            "hexagram": hexagram,
            "articles": articles
        }
```

## 🚀 部署和配置

### 1. **环境变量配置**
```bash
# .env文件中添加
OPENMANUS_API_URL=https://openmanus.your-domain.com
OPENMANUS_API_KEY=your-secret-api-key
OPENMANUS_TIMEOUT=30
OPENMANUS_RETRY_COUNT=3
```

### 2. **Docker Compose集成**
```yaml
# docker-compose.yml
version: '3.8'
services:
  cauldron:
    build: .
    environment:
      - OPENMANUS_API_URL=http://openmanus:8000
    depends_on:
      - openmanus
  
  openmanus:
    image: your-registry/openmanus:latest
    ports:
      - "8001:8000"
    environment:
      - PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
```

### 3. **监控和日志**
```python
# 添加监控
import logging
from prometheus_client import Counter, Histogram

openmanus_requests = Counter('openmanus_requests_total', 'Total OpenManus requests')
openmanus_duration = Histogram('openmanus_request_duration_seconds', 'OpenManus request duration')

class MonitoredOpenManusClient(OpenManusClient):
    async def scrape_seeking_alpha(self, url: str):
        openmanus_requests.inc()
        
        with openmanus_duration.time():
            try:
                result = await super().scrape_seeking_alpha(url)
                logging.info(f"Successfully scraped: {url}")
                return result
            except Exception as e:
                logging.error(f"Failed to scrape {url}: {e}")
                raise
```

## 💡 推荐方案

基于你的项目特点，我推荐：

1. **主要方案**: HTTP API + MCP协议
2. **备用方案**: 消息队列（处理大量任务时）
3. **监控**: Prometheus + Grafana
4. **缓存**: Redis缓存爬虫结果

这样既保持了架构的清晰分离，又能充分利用OpenManus的爬虫能力！