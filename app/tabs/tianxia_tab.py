"""
天下体系 - 儒门天下观资本生态分析Tab
基于"天命树"结构模型分析全球资本市场权力结构

重构版本：
- 移除硬编码API密钥
- 使用统一配置管理
- 改进数据结构
- 增强错误处理
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# 导入配置管理
try:
    from config.doppler_config import get_rapidapi_key
except ImportError:
    # 如果配置模块不可用，使用环境变量
    import os
    def get_rapidapi_key():
        return os.getenv('RAPIDAPI_KEY', '')

@dataclass
class StockEntity:
    """股票实体数据类"""
    symbol: str
    name: str
    role: str
    dependency: Optional[str] = None
    serves: Optional[str] = None
    type: Optional[str] = None

@dataclass
class EcosystemData:
    """生态系统数据类"""
    tianzi: Dict[str, str]
    dafu: List[StockEntity]
    shi: List[StockEntity]
    jiajie: List[StockEntity]

class TianxiaAnalyzer:
    """天下体系分析器 - 天命树结构分析"""
    
    def __init__(self):
        """初始化分析器"""
        try:
            self.rapidapi_key = get_rapidapi_key()
        except Exception:
            self.rapidapi_key = ""
            st.warning("⚠️ 未配置RapidAPI密钥，将使用模拟数据")
        
        # 定义三大天命树生态系统
        self.ecosystems = self._initialize_ecosystems()
    
    def _initialize_ecosystems(self) -> Dict[str, EcosystemData]:
        """初始化生态系统数据"""
        return {
            'AI': EcosystemData(
                tianzi={'symbol': 'NVDA', 'name': 'NVIDIA', 'tianming': 'CUDA + GPU硬件，定义AI计算范式'},
                dafu=[
                    StockEntity('TSM', 'TSMC', '芯片代工', '高端芯片唯一代工厂'),
                    StockEntity('000660.SZ', 'SK Hynix', 'HBM内存', 'GPU性能关键'),
                    StockEntity('MU', 'Micron', 'HBM内存', 'GPU性能关键'),
                    StockEntity('SMCI', 'Supermicro', '服务器集成', 'GPU转化为计算能力')
                ],
                shi=[
                    StockEntity('ASML', 'ASML', '光刻设备', serves='TSMC'),
                    StockEntity('AMAT', 'Applied Materials', '半导体设备', serves='TSMC')
                ],
                jiajie=[
                    StockEntity('AMD', 'AMD', '竞争对手', type='竞争天子'),
                    StockEntity('GOOGL', 'Google', '云计算', type='云计算天子'),
                    StockEntity('AMZN', 'Amazon', '云计算', type='云计算天子')
                ]
            ),
            'EV': EcosystemData(
                tianzi={'symbol': 'TSLA', 'name': 'Tesla', 'tianming': '软件定义汽车 + 超级充电网络'},
                dafu=[
                    StockEntity('300750.SZ', 'CATL', '动力电池', '动力系统基石'),
                    StockEntity('6752.T', 'Panasonic', '动力电池', '动力系统基石'),
                    StockEntity('ALB', 'Albemarle', '锂矿', '源头命脉'),
                    StockEntity('002460.SZ', 'Ganfeng Lithium', '锂矿', '源头命脉')
                ],
                shi=[
                    StockEntity('002497.SZ', 'Yahua Industrial', '氢氧化锂', serves='CATL'),
                    StockEntity('002850.SZ', 'Kedali', '精密结构件', serves='CATL')
                ],
                jiajie=[
                    StockEntity('002594.SZ', 'BYD', '电动车', type='诸侯'),
                    StockEntity('VWAGY', 'Volkswagen', '传统车企', type='诸侯'),
                    StockEntity('F', 'Ford', '传统车企', type='诸侯')
                ]
            ),
            'Consumer_Electronics': EcosystemData(
                tianzi={'symbol': 'AAPL', 'name': 'Apple', 'tianming': 'iOS + App Store生态系统'},
                dafu=[
                    StockEntity('2317.TW', 'Foxconn', '代工制造', '物理执行者'),
                    StockEntity('TSM', 'TSMC', '芯片代工', '性能优势保障'),
                    StockEntity('005930.KS', 'Samsung Display', '屏幕供应', '显示技术'),
                    StockEntity('QCOM', 'Qualcomm', '基带芯片', '通信命脉')
                ],
                shi=[
                    StockEntity('002475.SZ', 'Luxshare', '精密制造', serves='Foxconn'),
                    StockEntity('002241.SZ', 'Goertek', '声学器件', serves='Foxconn')
                ],
                jiajie=[
                    StockEntity('005930.KS', 'Samsung', '手机制造', type='亦敌亦友天子'),
                    StockEntity('1810.HK', 'Xiaomi', '手机制造', type='诸侯'),
                    StockEntity('NVDA', 'NVIDIA', 'AI芯片', type='跨生态天子')
                ]
            )
        }
    
    def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        """
        获取股票数据
        
        Args:
            symbol: 股票代码
            
        Returns:
            股票数据字典
        """
        # TODO: 实现真实API调用
        # 目前使用模拟数据
        try:
            return {
                'price': round(random.uniform(50, 500), 2),
                'change_pct': round(random.uniform(-5, 5), 2),
                'market_cap': f"{random.randint(100, 3000)}B",
                'volume': random.randint(1000000, 100000000)
            }
        except Exception:
            return {
                'price': 'N/A', 
                'change_pct': 0, 
                'market_cap': 'N/A', 
                'volume': 'N/A'
            }
    
    def create_tianming_card(self, ecosystem_name: str, ecosystem_data: EcosystemData) -> None:
        """
        创建天命卡片
        
        Args:
            ecosystem_name: 生态系统名称
            ecosystem_data: 生态系统数据
        """
        tianzi = ecosystem_data.tianzi
        stock_data = self.get_stock_data(tianzi['symbol'])
        
        st.markdown(f"### 👑 {ecosystem_name} 天命树")
        
        # 天子信息
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown("#### 🌟 天子")
            st.markdown(f"**{tianzi['name']}** ({tianzi['symbol']})")
        
        with col2:
            st.markdown("#### 📜 天命")
            st.info(tianzi['tianming'])
        
        with col3:
            st.metric(
                label="股价",
                value=f"${stock_data['price']}",
                delta=f"{stock_data['change_pct']:+.2f}%"
            )
        
        # 大夫层级
        if ecosystem_data.dafu:
            st.markdown("#### 🏛️ 大夫 (核心依赖)")
            dafu_cols = st.columns(min(len(ecosystem_data.dafu), 4))
            
            for i, dafu in enumerate(ecosystem_data.dafu):
                col_index = i % 4
                with dafu_cols[col_index]:
                    data = self.get_stock_data(dafu.symbol)
                    st.metric(
                        label=f"{dafu.name}",
                        value=f"${data['price']}",
                        delta=f"{data['change_pct']:+.2f}%"
                    )
                    st.caption(f"**{dafu.role}**: {dafu.dependency}")
        
        # 士层级
        if ecosystem_data.shi:
            st.markdown("#### ⚔️ 士 (专业供应商)")
            shi_cols = st.columns(min(len(ecosystem_data.shi), 3))
            
            for i, shi in enumerate(ecosystem_data.shi):
                col_index = i % 3
                with shi_cols[col_index]:
                    data = self.get_stock_data(shi.symbol)
                    st.metric(
                        label=f"{shi.name}",
                        value=f"${data['price']}",
                        delta=f"{data['change_pct']:+.2f}%"
                    )
                    st.caption(f"**{shi.role}** → 服务于{shi.serves}")
        
        # 嫁接关系
        if ecosystem_data.jiajie:
            st.markdown("#### 🔗 嫁接关系 (跨生态链接)")
            jiajie_cols = st.columns(min(len(ecosystem_data.jiajie), 4))
            
            for i, jiajie in enumerate(ecosystem_data.jiajie):
                col_index = i % 4
                with jiajie_cols[col_index]:
                    data = self.get_stock_data(jiajie.symbol)
                    st.metric(
                        label=f"{jiajie.name}",
                        value=f"${data['price']}",
                        delta=f"{data['change_pct']:+.2f}%"
                    )
                    st.caption(f"**{jiajie.type}**")
        
        st.markdown("---")
    
    def create_tianming_tree_table(self) -> pd.DataFrame:
        """
        创建天命树完整表格 - 用于投资组合去相关性分析
        
        Returns:
            包含所有股票信息的DataFrame
        """
        st.markdown("### 📋 天命树完整表格 - 投资组合去相关性分析")
        st.markdown("**核心理念**: 投资组合的本质是去相关性 - 从不同root下的不同spine下的不同leaf进行配置")

        all_stocks = []

        for eco_name, eco_data in self.ecosystems.items():
            # 天子
            tianzi = eco_data.tianzi
            stock_data = self.get_stock_data(tianzi['symbol'])
            all_stocks.append({
                'Root': eco_name,
                'Level': '👑 天子',
                'Symbol': tianzi['symbol'],
                'Company': tianzi['name'],
                'Role': '定义范式',
                'Dependency_Path': f"{eco_name}",
                'Price': stock_data['price'],
                'Change%': stock_data['change_pct'],
                'Market_Cap': stock_data['market_cap'],
                'Correlation_Risk': '极高 - 生态核心'
            })

            # 大夫
            for dafu in eco_data.dafu:
                stock_data = self.get_stock_data(dafu.symbol)
                all_stocks.append({
                    'Root': eco_name,
                    'Level': '🏛️ 大夫',
                    'Symbol': dafu.symbol,
                    'Company': dafu.name,
                    'Role': dafu.role,
                    'Dependency_Path': f"{eco_name} → {tianzi['name']} → {dafu.name}",
                    'Price': stock_data['price'],
                    'Change%': stock_data['change_pct'],
                    'Market_Cap': stock_data['market_cap'],
                    'Correlation_Risk': '高 - 深度绑定天子'
                })

            # 士
            for shi in eco_data.shi:
                stock_data = self.get_stock_data(shi.symbol)
                all_stocks.append({
                    'Root': eco_name,
                    'Level': '⚔️ 士',
                    'Symbol': shi.symbol,
                    'Company': shi.name,
                    'Role': shi.role,
                    'Dependency_Path': f"{eco_name} → {shi.serves} → {shi.name}",
                    'Price': stock_data['price'],
                    'Change%': stock_data['change_pct'],
                    'Market_Cap': stock_data['market_cap'],
                    'Correlation_Risk': '中 - 专业供应商'
                })

            # 嫁接
            for jiajie in eco_data.jiajie:
                stock_data = self.get_stock_data(jiajie.symbol)
                all_stocks.append({
                    'Root': '🔗 跨生态',
                    'Level': '🔗 嫁接',
                    'Symbol': jiajie.symbol,
                    'Company': jiajie.name,
                    'Role': jiajie.type or jiajie.role,
                    'Dependency_Path': f"多生态嫁接 → {jiajie.name}",
                    'Price': stock_data['price'],
                    'Change%': stock_data['change_pct'],
                    'Market_Cap': stock_data['market_cap'],
                    'Correlation_Risk': '低 - 多元化依赖'
                })

        df = pd.DataFrame(all_stocks)

        # 显示表格
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Root": st.column_config.TextColumn("生态根节点", width="small"),
                "Level": st.column_config.TextColumn("层级", width="small"),
                "Symbol": st.column_config.TextColumn("代码", width="small"),
                "Company": st.column_config.TextColumn("公司", width="medium"),
                "Role": st.column_config.TextColumn("角色", width="medium"),
                "Dependency_Path": st.column_config.TextColumn("依赖路径", width="large"),
                "Price": st.column_config.NumberColumn("股价", format="$%.2f"),
                "Change%": st.column_config.NumberColumn("涨跌幅", format="%.2f%%"),
                "Market_Cap": st.column_config.TextColumn("市值", width="small"),
                "Correlation_Risk": st.column_config.TextColumn("相关性风险", width="medium")
            }
        )

        return df

def render_tianxia_tab() -> None:
    """渲染天下体系Tab"""
    
    # 页面标题
    st.markdown("### 🏛️ 天下体系 - 儒门天下观资本生态分析")
    st.markdown("**基于'天命树'结构模型，穿透市场表象，绘制全球资本市场真实的权力结构**")
    st.markdown("---")
    
    # 初始化分析器
    analyzer = TianxiaAnalyzer()
    
    # 控制面板
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        auto_refresh = st.checkbox("🔄 自动刷新", value=False, key="tianxia_auto_refresh")
    with col2:
        if st.button("🏛️ 扫描天下", type="primary", key="tianxia_scan_btn"):
            st.session_state.trigger_tianxia_scan = True
    with col3:
        st.markdown("*正在分析全球资本生态权力结构...*")
    
    # 理论介绍
    with st.expander("📚 天命树理论基础"):
        st.markdown("""
        ### 🏛️ 儒门天下观核心思想
        
        **两大哲学基石：**
        1. **结构非平权**: 资本宇宙本质是不平权的、层级森严的树状结构
        2. **天命与脉络**: 每个生态都有唯一的"根节点"(天子)，拥有定义整个生态的"天命"
        
        **四层架构：**
        - **👑 天子**: 定义范式的平台型公司 (如Apple, NVIDIA, Tesla)
        - **🏛️ 大夫**: 深度绑定天子的核心供应商 (如TSMC, CATL)
        - **⚔️ 士**: 专业供应商和服务商 (如ASML, Luxshare)
        - **🔗 嫁接**: 跨生态的策略性链接关系
        """)
    
    # 自动刷新逻辑
    if auto_refresh:
        time.sleep(60)
        st.rerun()
    
    # 触发扫描或显示数据
    if st.session_state.get('trigger_tianxia_scan', False) or 'tianxia_scan_time' not in st.session_state:
        with st.spinner("🏛️ 正在扫描天下体系..."):
            st.session_state.tianxia_scan_time = datetime.now()
        st.session_state.trigger_tianxia_scan = False
    
    # 显示扫描时间
    if 'tianxia_scan_time' in st.session_state:
        st.info(f"📅 最后扫描时间: {st.session_state.tianxia_scan_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 显示三大生态系统
    st.markdown("## 🌍 三大天命树生态系统")
    
    # 分析模式选择
    analysis_mode = st.selectbox(
        "选择分析模式",
        ["生态系统分析", "投资组合去相关性分析"],
        key="tianxia_analysis_mode"
    )

    if analysis_mode == "生态系统分析":
        # 生态系统选择
        selected_ecosystem = st.selectbox(
            "选择要分析的生态系统",
            ["全部", "AI", "EV", "Consumer_Electronics"],
            format_func=lambda x: {
                "全部": "🌍 全部生态系统",
                "AI": "🤖 AI人工智能生态",
                "EV": "⚡ 电动汽车生态",
                "Consumer_Electronics": "📱 消费电子生态"
            }[x],
            key="tianxia_ecosystem_select"
        )

        if selected_ecosystem == "全部":
            # 显示所有生态系统
            for eco_name, eco_data in analyzer.ecosystems.items():
                analyzer.create_tianming_card(eco_name, eco_data)
        else:
            # 显示选定的生态系统
            analyzer.create_tianming_card(selected_ecosystem, analyzer.ecosystems[selected_ecosystem])

    else:  # 投资组合去相关性分析
        st.markdown("## 🎯 投资组合去相关性分析")
        st.info("**核心理念**: 真正的分散投资是从不同的root（天子）下的不同spine（大夫）下的不同leaf（士）进行配置")

        # 创建完整天命树表格
        df = analyzer.create_tianming_tree_table()
    
    # 页面底部说明
    st.markdown("---")
    st.markdown("""
    ### 🎯 天下体系核心洞察
    
    **权力结构分析**：
    - **AI生态**: NVIDIA通过CUDA平台统治AI计算，TSMC是关键"嫁接"节点
    - **电动车生态**: Tesla定义软件汽车范式，CATL掌握电池命脉
    - **消费电子生态**: Apple建立iOS护城河，供应链高度集中化
    
    **投资策略启示**：
    1. **投资天子**: 寻找定义范式的平台型公司
    2. **关注大夫**: 深度绑定天子的核心供应商往往被低估
    3. **警惕嫁接**: 被多个天子"嫁接"的公司风险与机会并存
    4. **避开士层**: 缺乏议价能力的专业供应商投资价值有限
    
    ⚠️ **免责声明**: 天下体系分析仅供参考，投资有风险，决策需谨慎！
    """)