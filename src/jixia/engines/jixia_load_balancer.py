#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
稷下学宫负载均衡器
实现八仙论道的API负载分担策略
"""

import time
import random
import requests
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import json
import os

@dataclass
class APIResult:
    """API调用结果"""
    success: bool
    data: Dict[str, Any]
    api_used: str
    response_time: float
    error: Optional[str] = None
    cached: bool = False

class RateLimiter:
    """速率限制器"""
    
    def __init__(self):
        self.api_calls = defaultdict(list)
        self.limits = {
            'alpha_vantage': {'per_minute': 500, 'per_month': 500000},
            'yahoo_finance_15': {'per_minute': 500, 'per_month': 500000},
            'webull': {'per_minute': 500, 'per_month': 500000},
            'seeking_alpha': {'per_minute': 500, 'per_month': 500000}
        }
    
    def is_rate_limited(self, api_name: str) -> bool:
        """检查是否达到速率限制"""
        now = time.time()
        calls = self.api_calls[api_name]
        
        # 清理1分钟前的记录
        self.api_calls[api_name] = [call_time for call_time in calls if now - call_time < 60]
        
        # 检查每分钟限制
        if len(self.api_calls[api_name]) >= self.limits[api_name]['per_minute'] * 0.9:  # 90%阈值
            return True
        
        return False
    
    def record_call(self, api_name: str):
        """记录API调用"""
        self.api_calls[api_name].append(time.time())

class APIHealthChecker:
    """API健康检查器"""
    
    def __init__(self):
        self.health_status = {
            'alpha_vantage': {'healthy': True, 'last_check': 0, 'consecutive_failures': 0},
            'yahoo_finance_15': {'healthy': True, 'last_check': 0, 'consecutive_failures': 0},
            'webull': {'healthy': True, 'last_check': 0, 'consecutive_failures': 0},
            'seeking_alpha': {'healthy': True, 'last_check': 0, 'consecutive_failures': 0}
        }
        self.check_interval = 300  # 5分钟检查一次
    
    def is_healthy(self, api_name: str) -> bool:
        """检查API是否健康"""
        status = self.health_status[api_name]
        now = time.time()
        
        # 如果距离上次检查超过间隔时间，进行健康检查
        if now - status['last_check'] > self.check_interval:
            self._perform_health_check(api_name)
        
        return status['healthy']
    
    def _perform_health_check(self, api_name: str):
        """执行健康检查"""
        # 这里可以实现具体的健康检查逻辑
        # 暂时简化为基于连续失败次数判断
        status = self.health_status[api_name]
        status['last_check'] = time.time()
        
        # 如果连续失败超过3次，标记为不健康
        if status['consecutive_failures'] > 3:
            status['healthy'] = False
        else:
            status['healthy'] = True
    
    def record_success(self, api_name: str):
        """记录成功调用"""
        self.health_status[api_name]['consecutive_failures'] = 0
        self.health_status[api_name]['healthy'] = True
    
    def record_failure(self, api_name: str):
        """记录失败调用"""
        self.health_status[api_name]['consecutive_failures'] += 1

class DataNormalizer:
    """数据标准化处理器"""
    
    def normalize_stock_quote(self, raw_data: dict, api_source: str) -> dict:
        """将不同API的股票报价数据标准化"""
        try:
            if api_source == 'alpha_vantage':
                return self._normalize_alpha_vantage_quote(raw_data)
            elif api_source == 'yahoo_finance_15':
                return self._normalize_yahoo_quote(raw_data)
            elif api_source == 'webull':
                return self._normalize_webull_quote(raw_data)
            elif api_source == 'seeking_alpha':
                return self._normalize_seeking_alpha_quote(raw_data)
            else:
                return {'error': f'Unknown API source: {api_source}'}
        except Exception as e:
            return {'error': f'Data normalization failed: {str(e)}'}
    
    def _normalize_alpha_vantage_quote(self, data: dict) -> dict:
        """标准化Alpha Vantage数据格式"""
        global_quote = data.get('Global Quote', {})
        return {
            'symbol': global_quote.get('01. symbol'),
            'price': float(global_quote.get('05. price', 0)),
            'change': float(global_quote.get('09. change', 0)),
            'change_percent': global_quote.get('10. change percent', '0%'),
            'volume': int(global_quote.get('06. volume', 0)),
            'high': float(global_quote.get('03. high', 0)),
            'low': float(global_quote.get('04. low', 0)),
            'source': 'alpha_vantage',
            'timestamp': global_quote.get('07. latest trading day')
        }
    
    def _normalize_yahoo_quote(self, data: dict) -> dict:
        """标准化Yahoo Finance数据格式"""
        body = data.get('body', {})
        return {
            'symbol': body.get('symbol'),
            'price': float(body.get('regularMarketPrice', 0)),
            'change': float(body.get('regularMarketChange', 0)),
            'change_percent': f"{body.get('regularMarketChangePercent', 0):.2f}%",
            'volume': int(body.get('regularMarketVolume', 0)),
            'high': float(body.get('regularMarketDayHigh', 0)),
            'low': float(body.get('regularMarketDayLow', 0)),
            'source': 'yahoo_finance_15',
            'timestamp': body.get('regularMarketTime')
        }
    
    def _normalize_webull_quote(self, data: dict) -> dict:
        """标准化Webull数据格式"""
        if 'stocks' in data and len(data['stocks']) > 0:
            stock = data['stocks'][0]
            return {
                'symbol': stock.get('symbol'),
                'price': float(stock.get('close', 0)),
                'change': float(stock.get('change', 0)),
                'change_percent': f"{stock.get('changeRatio', 0):.2f}%",
                'volume': int(stock.get('volume', 0)),
                'high': float(stock.get('high', 0)),
                'low': float(stock.get('low', 0)),
                'source': 'webull',
                'timestamp': stock.get('timeStamp')
            }
        return {'error': 'No stock data found in Webull response'}
    
    def _normalize_seeking_alpha_quote(self, data: dict) -> dict:
        """标准化Seeking Alpha数据格式"""
        if 'data' in data and len(data['data']) > 0:
            stock_data = data['data'][0]
            attributes = stock_data.get('attributes', {})
            return {
                'symbol': attributes.get('slug'),
                'price': float(attributes.get('lastPrice', 0)),
                'change': float(attributes.get('dayChange', 0)),
                'change_percent': f"{attributes.get('dayChangePercent', 0):.2f}%",
                'volume': int(attributes.get('volume', 0)),
                'source': 'seeking_alpha',
                'market_cap': attributes.get('marketCap'),
                'pe_ratio': attributes.get('peRatio')
            }
        return {'error': 'No data found in Seeking Alpha response'}

class JixiaLoadBalancer:
    """稷下学宫负载均衡器"""
    
    def __init__(self, rapidapi_key: str):
        self.rapidapi_key = rapidapi_key
        self.rate_limiter = RateLimiter()
        self.health_checker = APIHealthChecker()
        self.data_normalizer = DataNormalizer()
        self.cache = {}  # 简单的内存缓存
        self.cache_ttl = 300  # 5分钟缓存
        
        # API配置
        self.api_configs = {
            'alpha_vantage': {
                'host': 'alpha-vantage.p.rapidapi.com',
                'endpoints': {
                    'stock_quote': '/query?function=GLOBAL_QUOTE&symbol={symbol}',
                    'company_overview': '/query?function=OVERVIEW&symbol={symbol}',
                    'earnings': '/query?function=EARNINGS&symbol={symbol}'
                }
            },
            'yahoo_finance_15': {
                'host': 'yahoo-finance15.p.rapidapi.com',
                'endpoints': {
                    'stock_quote': '/api/yahoo/qu/quote/{symbol}',
                    'market_movers': '/api/yahoo/co/collections/day_gainers',
                    'market_news': '/api/yahoo/ne/news'
                }
            },
            'webull': {
                'host': 'webull.p.rapidapi.com',
                'endpoints': {
                    'stock_quote': '/stock/search?keyword={symbol}',
                    'market_movers': '/market/get-active-gainers'
                }
            },
            'seeking_alpha': {
                'host': 'seeking-alpha.p.rapidapi.com',
                'endpoints': {
                    'company_overview': '/symbols/get-profile?symbols={symbol}',
                    'market_news': '/news/list?category=market-news'
                }
            }
        }
        
        # 八仙API分配策略
        self.immortal_api_mapping = {
            'stock_quote': {
                '吕洞宾': 'alpha_vantage',      # 主力剑仙用最快的API
                '何仙姑': 'yahoo_finance_15',   # 风控专家用稳定的API
                '张果老': 'webull',            # 技术分析师用搜索强的API
                '韩湘子': 'alpha_vantage',      # 基本面研究用专业API
                '汉钟离': 'yahoo_finance_15',   # 量化专家用市场数据API
                '蓝采和': 'webull',            # 情绪分析师用活跃数据API
                '曹国舅': 'seeking_alpha',      # 宏观分析师用分析API
                '铁拐李': 'alpha_vantage'       # 逆向投资用基础数据API
            },
            'company_overview': {
                '吕洞宾': 'alpha_vantage',
                '何仙姑': 'seeking_alpha',
                '张果老': 'alpha_vantage',
                '韩湘子': 'seeking_alpha',
                '汉钟离': 'alpha_vantage',
                '蓝采和': 'seeking_alpha',
                '曹国舅': 'seeking_alpha',
                '铁拐李': 'alpha_vantage'
            },
            'market_movers': {
                '吕洞宾': 'yahoo_finance_15',
                '何仙姑': 'webull',
                '张果老': 'yahoo_finance_15',
                '韩湘子': 'webull',
                '汉钟离': 'yahoo_finance_15',
                '蓝采和': 'webull',
                '曹国舅': 'yahoo_finance_15',
                '铁拐李': 'webull'
            },
            'market_news': {
                '吕洞宾': 'yahoo_finance_15',
                '何仙姑': 'seeking_alpha',
                '张果老': 'yahoo_finance_15',
                '韩湘子': 'seeking_alpha',
                '汉钟离': 'yahoo_finance_15',
                '蓝采和': 'seeking_alpha',
                '曹国舅': 'seeking_alpha',
                '铁拐李': 'yahoo_finance_15'
            }
        }
        
        # 故障转移优先级
        self.failover_priority = {
            'alpha_vantage': ['webull', 'yahoo_finance_15'],
            'yahoo_finance_15': ['webull', 'alpha_vantage'],
            'webull': ['alpha_vantage', 'yahoo_finance_15'],
            'seeking_alpha': ['yahoo_finance_15', 'alpha_vantage']
        }
    
    def get_data_for_immortal(self, immortal_name: str, data_type: str, symbol: str = None) -> APIResult:
        """为特定仙人获取数据"""
        print(f"🎭 {immortal_name} 正在获取 {data_type} 数据...")
        
        # 检查缓存
        cache_key = f"{immortal_name}_{data_type}_{symbol}"
        cached_result = self._get_cached_data(cache_key)
        if cached_result:
            print(f"   📦 使用缓存数据")
            return cached_result
        
        # 获取该仙人的首选API
        if data_type not in self.immortal_api_mapping:
            return APIResult(False, {}, '', 0, f"Unsupported data type: {data_type}")
        
        preferred_api = self.immortal_api_mapping[data_type][immortal_name]
        
        # 尝试首选API
        result = self._try_api(preferred_api, data_type, symbol)
        if result.success:
            self._cache_data(cache_key, result)
            print(f"   ✅ 成功从 {preferred_api} 获取数据 (响应时间: {result.response_time:.2f}s)")
            return result
        
        # 故障转移到备用API
        print(f"   ⚠️ {preferred_api} 不可用，尝试备用API...")
        backup_apis = self.failover_priority.get(preferred_api, [])
        
        for backup_api in backup_apis:
            if data_type in self.api_configs[backup_api]['endpoints']:
                result = self._try_api(backup_api, data_type, symbol)
                if result.success:
                    self._cache_data(cache_key, result)
                    print(f"   ✅ 成功从备用API {backup_api} 获取数据 (响应时间: {result.response_time:.2f}s)")
                    return result
        
        # 所有API都失败
        print(f"   ❌ 所有API都不可用")
        return APIResult(False, {}, '', 0, "All APIs failed")
    
    def _try_api(self, api_name: str, data_type: str, symbol: str = None) -> APIResult:
        """尝试调用指定API"""
        # 检查API健康状态和速率限制
        if not self.health_checker.is_healthy(api_name):
            return APIResult(False, {}, api_name, 0, "API is unhealthy")
        
        if self.rate_limiter.is_rate_limited(api_name):
            return APIResult(False, {}, api_name, 0, "Rate limited")
        
        # 构建请求
        config = self.api_configs[api_name]
        if data_type not in config['endpoints']:
            return APIResult(False, {}, api_name, 0, f"Endpoint {data_type} not supported")
        
        endpoint = config['endpoints'][data_type]
        if symbol and '{symbol}' in endpoint:
            endpoint = endpoint.format(symbol=symbol)
        
        url = f"https://{config['host']}{endpoint}"
        headers = {
            'X-RapidAPI-Key': self.rapidapi_key,
            'X-RapidAPI-Host': config['host']
        }
        
        # 发起请求
        start_time = time.time()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response_time = time.time() - start_time
            
            self.rate_limiter.record_call(api_name)
            
            if response.status_code == 200:
                data = response.json()
                
                # 数据标准化
                if data_type == 'stock_quote':
                    normalized_data = self.data_normalizer.normalize_stock_quote(data, api_name)
                else:
                    normalized_data = data
                
                self.health_checker.record_success(api_name)
                return APIResult(True, normalized_data, api_name, response_time)
            else:
                error_msg = f"HTTP {response.status_code}: {response.text[:200]}"
                self.health_checker.record_failure(api_name)
                return APIResult(False, {}, api_name, response_time, error_msg)
                
        except Exception as e:
            response_time = time.time() - start_time
            self.health_checker.record_failure(api_name)
            return APIResult(False, {}, api_name, response_time, str(e))
    
    def _get_cached_data(self, cache_key: str) -> Optional[APIResult]:
        """获取缓存数据"""
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            if time.time() - cached_item['timestamp'] < self.cache_ttl:
                result = cached_item['result']
                result.cached = True
                return result
            else:
                # 缓存过期，删除
                del self.cache[cache_key]
        return None
    
    def _cache_data(self, cache_key: str, result: APIResult):
        """缓存数据"""
        self.cache[cache_key] = {
            'result': result,
            'timestamp': time.time()
        }
    
    def get_load_distribution(self) -> dict:
        """获取负载分布统计"""
        api_calls = {}
        total_calls = 0
        
        for api_name, calls in self.rate_limiter.api_calls.items():
            call_count = len(calls)
            api_calls[api_name] = call_count
            total_calls += call_count
        
        if total_calls == 0:
            return {}
        
        distribution = {}
        for api_name, call_count in api_calls.items():
            health_status = self.health_checker.health_status[api_name]
            distribution[api_name] = {
                'calls': call_count,
                'percentage': (call_count / total_calls) * 100,
                'healthy': health_status['healthy'],
                'consecutive_failures': health_status['consecutive_failures']
            }
        
        return distribution
    
    def conduct_immortal_debate(self, topic_symbol: str) -> Dict[str, APIResult]:
        """进行八仙论道，每个仙人获取不同的数据"""
        print(f"\n🏛️ 稷下学宫八仙论道开始 - 主题: {topic_symbol}")
        print("=" * 60)
        
        immortals = ['吕洞宾', '何仙姑', '张果老', '韩湘子', '汉钟离', '蓝采和', '曹国舅', '铁拐李']
        debate_results = {}
        
        # 每个仙人获取股票报价数据
        for immortal in immortals:
            result = self.get_data_for_immortal(immortal, 'stock_quote', topic_symbol)
            debate_results[immortal] = result
            
            if result.success:
                data = result.data
                if 'price' in data:
                    print(f"   💰 {immortal}: ${data['price']:.2f} ({data.get('change_percent', 'N/A')}) via {result.api_used}")
            
            time.sleep(0.2)  # 避免过快请求
        
        print("\n📊 负载分布统计:")
        distribution = self.get_load_distribution()
        for api_name, stats in distribution.items():
            print(f"   {api_name}: {stats['calls']} 次调用 ({stats['percentage']:.1f}%) - {'健康' if stats['healthy'] else '异常'}")
        
        return debate_results

# 使用示例
if __name__ == "__main__":
    # 从环境变量获取API密钥
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    if not rapidapi_key:
        print("❌ 请设置RAPIDAPI_KEY环境变量")
        exit(1)
    
    # 创建负载均衡器
    load_balancer = JixiaLoadBalancer(rapidapi_key)
    
    # 进行八仙论道
    results = load_balancer.conduct_immortal_debate('TSLA')
    
    print("\n🎉 八仙论道完成！")