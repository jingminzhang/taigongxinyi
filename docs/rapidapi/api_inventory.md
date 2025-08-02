# RapidAPI 订阅清单

## 📋 概览

基于Doppler配置和实际测试，记录当前RapidAPI订阅的API服务及其可用性。

**API密钥**: `6731900a13msh816fbe854209ac2p1bded2jsn1538144d52a4`  
**总订阅数**: 17个API服务  
**最后更新**: 2025-08-02

## ✅ 已验证可用的API (4个)

### 1. Alpha Vantage (`alpha-vantage.p.rapidapi.com`) ⚡
- **状态**: ✅ 可用 (响应时间: 1.26s)
- **用途**: 股票基本面数据、财报数据
- **测试结果**: 成功获取AAPL全球报价数据
- **数据字段**: Global Quote
- **端点**:
  - `/query?function=GLOBAL_QUOTE&symbol={symbol}` - 实时报价
  - `/query?function=OVERVIEW&symbol={symbol}` - 公司概览
  - `/query?function=EARNINGS&symbol={symbol}` - 财报数据

### 2. Webull (`webull.p.rapidapi.com`) ⚡
- **状态**: ✅ 可用 (响应时间: 1.56s)
- **用途**: 股票搜索、报价
- **测试结果**: 成功获取AAPL搜索数据
- **数据字段**: stocks, busiModel
- **端点**:
  - `/stock/search?keyword={symbol}` - 股票搜索
  - `/market/get-active-gainers` - 活跃涨幅股

### 3. Yahoo Finance 15 (`yahoo-finance15.p.rapidapi.com`)
- **状态**: ✅ 可用 (响应时间: 2.07s)
- **用途**: 实时股价、市场数据
- **测试结果**: 成功获取AAPL报价数据
- **数据字段**: meta, body
- **端点**:
  - `/api/yahoo/qu/quote/{symbol}` - 股票报价
  - `/api/yahoo/co/collections/day_gainers` - 涨幅榜
  - `/api/yahoo/co/collections/day_losers` - 跌幅榜

### 4. Seeking Alpha (`seeking-alpha.p.rapidapi.com`)
- **状态**: ✅ 可用 (响应时间: 3.32s)
- **用途**: 股票分析、新闻
- **测试结果**: 成功获取AAPL分析数据
- **数据字段**: data
- **端点**:
  - `/symbols/get-profile?symbols={symbol}` - 股票档案
  - `/news/list?category=market-news` - 市场新闻

## ❌ 未订阅或失败的API (13个)

### 权限问题 (403 Forbidden)
以下API显示"You are not subscribed to this API"，表示未订阅：

- **yahoo_finance_api_data** (`yahoo-finance-api1.p.rapidapi.com`)
- **yahoo_finance_basic** (`yahoo-finance127.p.rapidapi.com`) 
- **morning_star** (`morningstar1.p.rapidapi.com`)
- **investing_com** (`investing-cryptocurrency-markets.p.rapidapi.com`)
- **finance_api** (`real-time-finance-data.p.rapidapi.com`)

### API不存在 (404 Not Found)
以下API显示"API doesn't exists"，可能已下线：

- **yahoo_finance_realtime** (`yahoo-finance-low-latency.p.rapidapi.com`)
- **tradingview** (`tradingview-ta.p.rapidapi.com`)
- **sec_filings** (`sec-filings.p.rapidapi.com`)

### 端点错误 (404 Endpoint Not Found)
以下API存在但端点路径不正确：

- **yh_finance** (`yh-finance-complete.p.rapidapi.com`)
- **ms_finance** (`ms-finance.p.rapidapi.com`)
- **exchangerate_api** (`exchangerate-api.p.rapidapi.com`)
- **crypto_news** (`cryptocurrency-news2.p.rapidapi.com`)

### 无响应数据 (204 No Content)
- **yh_finance_complete** (`yh-finance.p.rapidapi.com`) - 返回空响应

## 🔄 需要进一步测试的API

### 8. YH Finance Complete (`yh-finance.p.rapidapi.com`)
- **状态**: 🟡 待测试
- **用途**: 完整的Yahoo Finance数据

### 9. Yahoo Finance API Data (`yahoo-finance-api1.p.rapidapi.com`)
- **状态**: 🟡 待测试
- **用途**: Yahoo Finance API数据

### 10. Yahoo Finance Low Latency (`yahoo-finance-low-latency.p.rapidapi.com`)
- **状态**: 🟡 待测试
- **用途**: 低延迟实时数据

### 11. YH Finance Complete (`yh-finance-complete.p.rapidapi.com`)
- **状态**: 🟡 待测试
- **用途**: 完整金融数据

### 12. Yahoo Finance 127 (`yahoo-finance127.p.rapidapi.com`)
- **状态**: 🟡 待测试
- **用途**: Yahoo Finance基础数据

### 13. Real Time Finance Data (`real-time-finance-data.p.rapidapi.com`)
- **状态**: 🟡 待测试
- **用途**: 实时金融数据

### 14. MS Finance (`ms-finance.p.rapidapi.com`)
- **状态**: 🟡 待测试
- **用途**: 微软金融数据

### 15. SEC Filings (`sec-filings.p.rapidapi.com`)
- **状态**: 🟡 待测试
- **用途**: SEC文件数据

### 16. ExchangeRate API (`exchangerate-api.p.rapidapi.com`)
- **状态**: 🟡 待测试
- **用途**: 汇率数据

### 17. Cryptocurrency News 2 (`cryptocurrency-news2.p.rapidapi.com`)
- **状态**: 🟡 待测试
- **用途**: 加密货币新闻

## 📊 使用统计

### 成功率分析
- **可用API**: 4/17 (23.5%)
- **未订阅API**: 5/17 (29.4%)
- **API不存在**: 3/17 (17.6%)
- **端点错误**: 4/17 (23.5%)
- **其他问题**: 1/17 (5.9%)

### 八仙论道中的API使用情况
- **吕洞宾**: Alpha Vantage ✅
- **何仙姑**: Yahoo Finance 15 ✅
- **张果老**: Seeking Alpha ✅
- **韩湘子**: 多个API失败 ❌
- **汉钟离**: 多个API失败 ❌
- **蓝采和**: Webull ✅
- **曹国舅**: Seeking Alpha ✅
- **铁拐李**: 多个API失败 ❌

## 🔧 优化建议

### 1. 端点配置优化
- 需要为每个API配置正确的端点路径
- 研究各API的具体参数要求
- 添加更多数据类型的端点映射

### 2. 故障转移策略
- 优先使用已验证可用的API
- 将Yahoo Finance系列API作为主要数据源
- Alpha Vantage作为基本面数据的首选

### 3. API测试计划
- 逐个测试待测试的API
- 记录每个API的具体用法和限制
- 建立API健康检查机制

## 📝 测试记录

### 2025-08-02 全面测试记录
```
✅ alpha_vantage: 1.26s - 成功获取AAPL全球报价
✅ webull: 1.56s - 成功获取AAPL搜索数据
✅ yahoo_finance_1: 2.07s - 成功获取AAPL报价数据  
✅ seeking_alpha: 3.32s - 成功获取AAPL分析数据

❌ yahoo_finance_api_data: 403 - 未订阅
❌ yahoo_finance_basic: 403 - 未订阅
❌ morning_star: 403 - 未订阅
❌ investing_com: 403 - 未订阅
❌ finance_api: 403 - 未订阅

❌ yahoo_finance_realtime: 404 - API不存在
❌ tradingview: 404 - API不存在
❌ sec_filings: 404 - API不存在

❌ yh_finance: 404 - 端点不存在
❌ ms_finance: 404 - 端点不存在
❌ exchangerate_api: 404 - 端点不存在
❌ crypto_news: 404 - 端点不存在

❌ yh_finance_complete: 204 - 无响应数据
```

## 🚀 下一步行动

1. **完善端点配置**: 为所有API添加正确的端点映射
2. **批量测试**: 使用自动化脚本测试所有待测试API
3. **文档更新**: 根据测试结果更新此文档
4. **性能优化**: 基于可用性调整八仙论道的API分配策略

---

**维护者**: Ben  
**联系方式**: 通过Doppler配置管理API密钥  
**更新频率**: 每次API测试后更新