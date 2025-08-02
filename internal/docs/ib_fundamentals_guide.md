# 💎 六壬察心 - IB基本面数据抓取指南

## 概述

六壬察心是炼妖壶系统的降魔杵专属功能，通过Interactive Brokers (IB) API获取深度基本面数据，实现对市场情绪面的精准洞察。

## 功能特性

### 🎯 核心功能
- **实时基本面数据**：PE/PB比率、ROE、负债权益比等关键指标
- **财务报表分析**：营收增长、EPS增长等财务健康度指标
- **分析师观点**：评级、目标价、预测数据
- **市场情绪指标**：内部持股、空头比例、社交情绪
- **多股票对比**：批量分析，可视化对比
- **数据导出**：支持CSV、Excel、JSON格式

### 🏛️ 神器等级对应
- **🆓 炼妖壶**: 基础功能，仅展示演示数据
- **💎 降魔杵**: 完整功能，实时IB数据访问
- **👑 打神鞭**: 增强功能，高频分析和预测模型

## 环境配置

### 1. IB Gateway/TWS 设置

#### 安装IB Gateway
1. 下载并安装 [IB Gateway](https://www.interactivebrokers.com/en/index.php?f=16457)
2. 启动IB Gateway并登录您的账户
3. 配置API设置：
   - 启用API连接
   - 设置端口号（推荐4002用于模拟账户）
   - 允许本地连接

#### API配置
```
Socket Port: 4002 (模拟账户) / 4001 (实盘账户)
Enable ActiveX and Socket Clients: ✓
Read-Only API: ✓ (推荐用于数据获取)
Download open orders on connection: ✓
```

### 2. 环境变量配置

复制 `.env.example` 为 `.env` 并配置：

```bash
# IB 连接配置
IB_HOST=127.0.0.1
IB_PORT=4002          # 4002=模拟, 4001=实盘
IB_CLIENT_ID=10       # 唯一客户端ID
```

### 3. Python依赖安装

```bash
# 安装IB相关依赖
pip install ib-insync pandas plotly

# 或使用项目依赖
pip install -r requirements.txt
```

## 使用方法

### 1. 命令行测试

```bash
# 测试IB连接和基本面数据抓取
python scripts/test_ib_fundamentals.py
```

### 2. Streamlit界面

```bash
# 启动Web界面
streamlit run streamlit_app.py
```

在界面中：
1. 选择"💎 六壬察心"标签页
2. 确保会员等级为"降魔杵"或以上
3. 使用各种功能模块

### 3. 编程接口

```python
import asyncio
from src.data.ib_fundamentals_fetcher import IBFundamentalsFetcher

async def get_stock_data():
    fetcher = IBFundamentalsFetcher()
    
    try:
        # 获取单只股票数据
        aapl_data = await fetcher.get_stock_fundamentals('AAPL')
        print(f"AAPL PE比率: {aapl_data.pe_ratio}")
        
        # 获取多只股票数据
        symbols = ['AAPL', 'MSFT', 'GOOGL']
        data_dict = await fetcher.get_multiple_stocks_fundamentals(symbols)
        
        # 转换为DataFrame
        df = fetcher.to_dataframe(data_dict)
        print(df[['symbol', 'pe_ratio', 'market_cap']])
        
    finally:
        await fetcher.disconnect()

# 运行
asyncio.run(get_stock_data())
```

## 数据结构

### FundamentalData 对象

```python
@dataclass
class FundamentalData:
    symbol: str                    # 股票代码
    company_name: str              # 公司名称
    sector: str                    # 行业
    market_cap: float              # 市值
    pe_ratio: Optional[float]      # PE比率
    pb_ratio: Optional[float]      # PB比率
    roe: Optional[float]           # 净资产收益率
    debt_to_equity: Optional[float] # 负债权益比
    revenue_growth: Optional[float] # 营收增长率
    eps_growth: Optional[float]    # EPS增长率
    dividend_yield: Optional[float] # 股息率
    analyst_rating: Optional[str]  # 分析师评级
    price_target: Optional[float]  # 目标价
    insider_ownership: Optional[float] # 内部持股比例
    short_interest: Optional[float]    # 空头比例
    social_sentiment: Optional[float]  # 社交情绪
    last_updated: datetime         # 最后更新时间
```

## 支持的市场

### 美股 (US)
- 交易所：SMART, NYSE, NASDAQ
- 货币：USD
- 数据类型：完整基本面数据

### 港股 (HK)
- 交易所：SEHK
- 货币：HKD
- 数据类型：基础基本面数据

### 其他市场
- 根据IB数据订阅情况而定
- 部分市场可能需要额外的数据订阅

## 故障排除

### 常见问题

#### 1. 连接失败
```
❌ IB连接失败: Connection refused
```

**解决方案：**
- 确保IB Gateway/TWS正在运行
- 检查端口号是否正确
- 确认API设置已启用
- 检查防火墙设置

#### 2. 数据获取失败
```
❌ 无法获取基本面数据
```

**解决方案：**
- 检查股票代码是否正确
- 确认市场数据订阅状态
- 验证交易时间（某些数据仅在交易时间可用）
- 检查IB账户权限

#### 3. API限制
```
⚠️ API请求频率过高
```

**解决方案：**
- 增加请求间隔时间
- 使用批量请求减少API调用
- 检查IB API限制政策

### 调试模式

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 测试连接

```bash
# 快速连接测试
python -c "
import asyncio
from src.data.ib_fundamentals_fetcher import IBFundamentalsFetcher

async def test():
    fetcher = IBFundamentalsFetcher()
    success = await fetcher.connect()
    print('✅ 连接成功' if success else '❌ 连接失败')
    await fetcher.disconnect()

asyncio.run(test())
"
```

## 性能优化

### 1. 连接池管理
- 复用IB连接，避免频繁连接/断开
- 使用连接池管理多个并发请求

### 2. 数据缓存
- 缓存基本面数据，避免重复请求
- 设置合理的缓存过期时间

### 3. 批量处理
- 使用批量API减少网络开销
- 合理控制并发请求数量

## 扩展开发

### 自定义数据处理

```python
class CustomFundamentalsFetcher(IBFundamentalsFetcher):
    async def get_custom_metrics(self, symbol: str):
        """自定义指标计算"""
        data = await self.get_stock_fundamentals(symbol)
        
        # 自定义计算
        if data.pe_ratio and data.eps_growth:
            peg_ratio = data.pe_ratio / data.eps_growth
            return {'peg_ratio': peg_ratio}
        
        return {}
```

### 数据存储

```python
async def save_to_database(data: FundamentalData):
    """保存到数据库"""
    # 实现数据库存储逻辑
    pass
```

## 注意事项

### 1. 数据订阅
- 某些基本面数据需要额外的市场数据订阅
- 免费账户可能有数据延迟或限制

### 2. 使用限制
- 遵守IB API使用条款
- 注意API调用频率限制
- 不要用于高频交易

### 3. 数据准确性
- 基本面数据可能有延迟
- 建议与其他数据源交叉验证
- 注意财报发布时间对数据的影响

## 技术支持

如有问题，请：
1. 查看日志文件获取详细错误信息
2. 运行测试脚本验证配置
3. 检查IB官方文档和API说明
4. 在项目GitHub提交Issue

---

*太公心易BI系统 - 降魔杵专属功能*  
*版本：v1.0*  
*更新时间：2025-01-15*
