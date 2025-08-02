#!/usr/bin/env python3
"""
Alpha Vantage API 测试脚本 - Meta (META) 财报和分析师评级
"""

import os
import requests
import json
from datetime import datetime

def get_alpha_vantage_key():
    """从环境变量获取 Alpha Vantage API Key"""
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        raise ValueError("未找到 ALPHA_VANTAGE_API_KEY 环境变量")
    return api_key

def get_company_overview(symbol, api_key):
    """获取公司基本信息和财务概览"""
    url = f"https://www.alphavantage.co/query"
    params = {
        'function': 'OVERVIEW',
        'symbol': symbol,
        'apikey': api_key
    }
    
    response = requests.get(url, params=params)
    return response.json()

def get_earnings_data(symbol, api_key):
    """获取财报数据"""
    url = f"https://www.alphavantage.co/query"
    params = {
        'function': 'EARNINGS',
        'symbol': symbol,
        'apikey': api_key
    }
    
    response = requests.get(url, params=params)
    return response.json()

def get_analyst_ratings(symbol, api_key):
    """获取分析师评级（需要付费版本，这里尝试调用看是否有数据）"""
    url = f"https://www.alphavantage.co/query"
    params = {
        'function': 'ANALYST_RECOMMENDATIONS',
        'symbol': symbol,
        'apikey': api_key
    }
    
    response = requests.get(url, params=params)
    return response.json()

def get_income_statement(symbol, api_key):
    """获取损益表"""
    url = f"https://www.alphavantage.co/query"
    params = {
        'function': 'INCOME_STATEMENT',
        'symbol': symbol,
        'apikey': api_key
    }
    
    response = requests.get(url, params=params)
    return response.json()

def format_financial_data(data, title):
    """格式化财务数据输出"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    
    if isinstance(data, dict):
        if 'Error Message' in data:
            print(f"❌ 错误: {data['Error Message']}")
        elif 'Note' in data:
            print(f"⚠️  注意: {data['Note']}")
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(data)

def main():
    """主函数"""
    try:
        # 获取 API Key
        api_key = get_alpha_vantage_key()
        print(f"✅ 成功获取 Alpha Vantage API Key: {api_key[:8]}...")
        
        symbol = "META"  # Meta Platforms Inc.
        print(f"\n🔍 正在获取 {symbol} 的财务数据...")
        
        # 1. 公司概览
        print("\n📊 获取公司概览...")
        overview = get_company_overview(symbol, api_key)
        format_financial_data(overview, f"{symbol} - 公司概览")
        
        # 2. 财报数据
        print("\n📈 获取财报数据...")
        earnings = get_earnings_data(symbol, api_key)
        format_financial_data(earnings, f"{symbol} - 财报数据")
        
        # 3. 分析师评级
        print("\n⭐ 获取分析师评级...")
        ratings = get_analyst_ratings(symbol, api_key)
        format_financial_data(ratings, f"{symbol} - 分析师评级")
        
        # 4. 损益表
        print("\n💰 获取损益表...")
        income_statement = get_income_statement(symbol, api_key)
        format_financial_data(income_statement, f"{symbol} - 损益表")
        
        print(f"\n✅ {symbol} 数据获取完成!")
        print(f"⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())