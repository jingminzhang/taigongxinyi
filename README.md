# 🏛️ 炼妖壶 (Lianyaohu) - 稷下学宫AI辩论系统

基于中国哲学传统的多AI智能体辩论平台，重构版本。

## ✨ 核心特性

- **🎭 稷下学宫八仙论道**: 基于中国传统八仙文化的多AI智能体辩论系统
- **🌍 天下体系分析**: 基于儒门天下观的资本生态"天命树"分析模型
- **🔒 安全配置管理**: 使用Doppler进行统一的密钥和配置管理
- **📊 智能数据源**: 基于17个RapidAPI订阅的永动机数据引擎
- **🎨 现代化界面**: 基于Streamlit的响应式Web界面

## 🏗️ 项目结构

```
liurenchaxin/
├── app/                    # 应用入口
│   ├── streamlit_app.py   # 主Streamlit应用
│   └── tabs/              # 功能模块
│       └── tianxia_tab.py # 天下体系分析
├── src/                   # 核心业务逻辑
│   └── jixia/            # 稷下学宫系统
│       └── engines/      # 核心引擎
│           └── perpetual_engine.py # 永动机引擎
├── config/               # 配置管理
│   └── doppler_config.py # Doppler配置接口
├── scripts/              # 工具脚本
│   └── test_openrouter_api.py # API连接测试
├── tests/                # 测试代码
├── .kiro/               # Kiro AI助手配置
│   └── steering/        # AI指导规则
└── requirements.txt     # 依赖清单
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置管理

项目使用Doppler进行安全的配置管理。需要配置以下环境变量：

```bash
# 必需配置
RAPIDAPI_KEY=your_rapidapi_key
OPENROUTER_API_KEY_1=your_openrouter_key

# 可选配置
POSTGRES_URL=your_postgres_url
MONGODB_URL=your_mongodb_url
ZILLIZ_URL=your_zilliz_url
ZILLIZ_TOKEN=your_zilliz_token
```

### 3. 启动应用

```bash
# 启动Streamlit应用
streamlit run app/streamlit_app.py

# 或指定端口
streamlit run app/streamlit_app.py --server.port 8501
```

### 4. 安装Swarm (可选)

如果要使用Swarm八仙论道功能：

```bash
# 安装OpenAI Swarm
python scripts/install_swarm.py

# 或手动安装
pip install git+https://github.com/openai/swarm.git
```

### 5. 测试连接

```bash
# 测试API连接
python scripts/test_openrouter_api.py

# 验证配置
python config/doppler_config.py

# 测试Swarm辩论 (可选)
python src/jixia/debates/swarm_debate.py
```

## 🎭 稷下学宫八仙论道

### 传统模式 (RapidAPI数据驱动)
基于中国传统八仙文化，每位仙人都有专属的投资哲学和数据源：

- **🧙‍♂️ 吕洞宾** (乾): 主动投资，综合分析
- **👸 何仙姑** (坤): 被动ETF，稳健跟踪
- **👴 张果老** (兑): 传统价值，基本面分析
- **🎵 韩湘子** (艮): 新兴资产，趋势捕捉
- **⚡ 汉钟离** (离): 热点追踪，实时数据
- **🎭 蓝采和** (坎): 潜力股，价值发现
- **👑 曹国舅** (震): 机构视角，专业分析
- **🦯 铁拐李** (巽): 逆向投资，反向思维

### Swarm模式 (AI智能体辩论)
基于OpenAI Swarm框架的四仙智能体辩论系统：

- **🗡️ 吕洞宾** (乾卦): 技术分析专家，看涨派，犀利直接
- **🌸 何仙姑** (坤卦): 风险控制专家，看跌派，温和坚定
- **📚 张果老** (兑卦): 历史数据分析师，看涨派，博古通今
- **⚡ 铁拐李** (巽卦): 逆向投资大师，看跌派，挑战共识

#### 支持两种运行模式：
- **OpenRouter模式**: 使用云端AI服务，模型选择丰富
- **Ollama模式**: 使用本地AI服务，完全离线运行

## 🌍 天下体系分析

基于儒门天下观的"天命树"结构模型：

### 四层架构
- **👑 天子**: 定义范式的平台型公司 (如NVIDIA, Tesla, Apple)
- **🏛️ 大夫**: 深度绑定天子的核心供应商 (如TSMC, CATL)
- **⚔️ 士**: 专业供应商和服务商 (如ASML, Luxshare)
- **🔗 嫁接**: 跨生态的策略性链接关系

### 三大生态
- **🤖 AI生态**: NVIDIA统治的AI计算生态
- **⚡ EV生态**: Tesla定义的电动汽车生态
- **📱 消费电子生态**: Apple建立的iOS生态

## 🔧 开发指南

### 代码规范
- 使用Python类型注解
- 遵循PEP 8编码规范
- 所有公共函数必须有文档字符串
- 使用dataclass定义数据结构

### 安全要求
- **零硬编码密钥**: 所有敏感信息通过Doppler或环境变量获取
- **环境隔离**: 开发、测试、生产环境严格分离
- **自动化扫描**: 所有提交必须通过安全检查

### 测试要求
- 所有核心功能必须有单元测试
- API调用必须有集成测试
- 配置管理必须有验证测试

## 📊 API使用统计

项目基于17个RapidAPI订阅构建永动机数据引擎：

- **智能故障转移**: 主API失败时自动切换备用API
- **负载均衡**: 智能分配API调用，避免单点过载
- **使用统计**: 实时监控API使用情况和成本优化

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## ⚠️ 免责声明

本系统仅供学习和研究使用。所有投资分析和建议仅供参考，不构成投资建议。投资有风险，决策需谨慎。

---

**炼妖壶 - 让AI辩论照亮投资智慧** 🏛️✨