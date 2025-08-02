#!/usr/bin/env python3
"""
炼妖壶 (Lianyaohu) - 稷下学宫AI辩论系统
主Streamlit应用入口

重构版本：
- 清晰的模块化结构
- 统一的配置管理
- 安全的密钥处理
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def configure_page():
    """配置页面基本设置"""
    st.set_page_config(
        page_title="炼妖壶 - 稷下学宫AI辩论系统",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def show_header():
    """显示页面头部"""
    st.title("🏛️ 炼妖壶 - 稷下学宫AI辩论系统")
    st.markdown("**基于中国哲学传统的多AI智能体辩论平台**")
    
    # 显示系统状态
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("系统状态", "🟢 运行中")
    with col2:
        st.metric("AI模型", "OpenRouter")
    with col3:
        st.metric("数据源", "RapidAPI")

def show_sidebar():
    """显示侧边栏"""
    with st.sidebar:
        st.markdown("## 🎛️ 控制面板")
        
        # 系统信息
        st.markdown("### 📊 系统信息")
        st.info("**版本**: v2.0 (重构版)")
        st.info("**状态**: 迁移完成")
        
        # 配置检查
        st.markdown("### 🔧 配置状态")
        try:
            from config.doppler_config import validate_config
            if validate_config():
                st.success("✅ 配置正常")
            else:
                st.error("❌ 配置异常")
        except Exception as e:
            st.warning(f"⚠️ 配置检查失败: {str(e)}")
        
        # 快速操作
        st.markdown("### ⚡ 快速操作")
        if st.button("🧪 测试API连接"):
            test_api_connections()
        
        if st.button("🏛️ 启动八仙论道"):
            start_jixia_debate()
        
        if st.button("🚀 启动Swarm论道"):
            start_swarm_debate()

def test_api_connections():
    """测试API连接"""
    with st.spinner("正在测试API连接..."):
        try:
            from scripts.test_openrouter_api import test_openrouter_api, test_rapidapi_connection
            
            openrouter_ok = test_openrouter_api()
            rapidapi_ok = test_rapidapi_connection()
            
            if openrouter_ok and rapidapi_ok:
                st.success("✅ 所有API连接正常")
            else:
                st.error("❌ 部分API连接失败")
        except Exception as e:
            st.error(f"❌ API测试异常: {str(e)}")

def start_jixia_debate():
    """启动稷下学宫辩论"""
    with st.spinner("正在启动稷下学宫八仙论道..."):
        try:
            from config.doppler_config import get_rapidapi_key
            from src.jixia.engines.perpetual_engine import JixiaPerpetualEngine
            
            api_key = get_rapidapi_key()
            engine = JixiaPerpetualEngine(api_key)
            
            # 运行辩论
            results = engine.simulate_jixia_debate('TSLA')
            
            st.success("✅ 八仙论道完成")
            st.json(results)
        except Exception as e:
            st.error(f"❌ 辩论启动失败: {str(e)}")

def start_swarm_debate():
    """启动Swarm八仙论道"""
    with st.spinner("正在启动Swarm八仙论道..."):
        try:
            import asyncio
            from src.jixia.debates.swarm_debate import start_ollama_debate, start_openrouter_debate
            
            # 选择模式
            mode = st.session_state.get('swarm_mode', 'ollama')
            topic = st.session_state.get('swarm_topic', 'TSLA股价走势分析')
            
            # 构建上下文
            context = {
                "market_sentiment": "谨慎乐观",
                "volatility": "中等",
                "technical_indicators": {
                    "RSI": 65,
                    "MACD": "金叉",
                    "MA20": "上穿"
                }
            }
            
            # 运行辩论
            if mode == 'ollama':
                result = asyncio.run(start_ollama_debate(topic, context))
            else:
                result = asyncio.run(start_openrouter_debate(topic, context))
            
            if result:
                st.success("✅ Swarm八仙论道完成")
                st.json(result)
            else:
                st.error("❌ Swarm辩论失败")
                
        except Exception as e:
            st.error(f"❌ Swarm辩论启动失败: {str(e)}")

def main():
    """主函数"""
    configure_page()
    show_header()
    show_sidebar()
    
    # 主内容区域
    st.markdown("---")
    
    # 选项卡
    tab1, tab2, tab3 = st.tabs(["🏛️ 稷下学宫", "🌍 天下体系", "📊 数据分析"])
    
    with tab1:
        st.markdown("### 🏛️ 稷下学宫 - 八仙论道")
        st.markdown("**多AI智能体辩论系统，基于中国传统八仙文化**")
        
        # 辩论模式选择
        debate_mode = st.selectbox(
            "选择辩论模式",
            ["传统模式 (RapidAPI数据)", "Swarm模式 (AI智能体)"],
            key="debate_mode_select"
        )
        
        if debate_mode == "Swarm模式 (AI智能体)":
            # Swarm模式配置
            col1, col2 = st.columns(2)
            with col1:
                swarm_mode = st.selectbox(
                    "AI服务模式",
                    ["ollama", "openrouter"],
                    key="swarm_mode_select"
                )
                st.session_state.swarm_mode = swarm_mode
            
            with col2:
                swarm_topic = st.text_input(
                    "辩论主题", 
                    value="英伟达股价走势：AI泡沫还是技术革命？", 
                    key="swarm_topic_input"
                )
                st.session_state.swarm_topic = swarm_topic
            
            if st.button("🚀 启动Swarm八仙论道", type="primary"):
                start_swarm_debate()
        
        else:
            # 传统模式
            col1, col2 = st.columns([2, 1])
            with col1:
                topic = st.text_input("辩论主题 (股票代码)", value="TSLA", key="debate_topic")
            with col2:
                if st.button("🎭 开始辩论", type="primary"):
                    start_debate_session(topic)
        
        # 显示辩论历史
        if 'debate_history' in st.session_state:
            st.markdown("#### 📜 辩论记录")
            for record in st.session_state.debate_history[-3:]:  # 显示最近3次
                with st.expander(f"🎭 {record['topic']} - {record['time']}"):
                    st.json(record['results'])
    
    with tab2:
        st.markdown("### 🌍 天下体系分析")
        try:
            from app.tabs.tianxia_tab import render_tianxia_tab
            render_tianxia_tab()
        except Exception as e:
            st.error(f"❌ 天下体系模块加载失败: {str(e)}")
    
    with tab3:
        st.markdown("### 📊 数据分析")
        st.info("🚧 数据分析模块开发中...")
        
        # 显示系统统计
        try:
            from config.doppler_config import get_rapidapi_key
            from src.jixia.engines.perpetual_engine import JixiaPerpetualEngine
            
            api_key = get_rapidapi_key()
            engine = JixiaPerpetualEngine(api_key)
            stats = engine.get_usage_stats()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("API调用总数", stats['total_calls'])
            with col2:
                st.metric("活跃API数", f"{stats['active_apis']}/{stats['total_apis']}")
            with col3:
                st.metric("未使用API", stats['unused_count'])
                
        except Exception as e:
            st.warning(f"⚠️ 无法加载统计数据: {str(e)}")

def start_debate_session(topic: str):
    """启动辩论会话"""
    if not topic:
        st.error("请输入辩论主题")
        return
    
    with st.spinner(f"🏛️ 八仙正在就 {topic} 展开论道..."):
        try:
            from config.doppler_config import get_rapidapi_key
            from src.jixia.engines.perpetual_engine import JixiaPerpetualEngine
            from datetime import datetime
            
            api_key = get_rapidapi_key()
            engine = JixiaPerpetualEngine(api_key)
            
            # 运行辩论
            results = engine.simulate_jixia_debate(topic)
            
            # 保存到会话状态
            if 'debate_history' not in st.session_state:
                st.session_state.debate_history = []
            
            st.session_state.debate_history.append({
                'topic': topic,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'results': {name: {'success': result.success, 'api_used': result.api_used} 
                           for name, result in results.items()}
            })
            
            st.success(f"✅ 八仙论道完成！共有 {len(results)} 位仙人参与")
            
            # 显示结果摘要
            successful_debates = sum(1 for result in results.values() if result.success)
            st.info(f"📊 成功获取数据: {successful_debates}/{len(results)} 位仙人")
            
        except Exception as e:
            st.error(f"❌ 辩论启动失败: {str(e)}")

if __name__ == "__main__":
    main()