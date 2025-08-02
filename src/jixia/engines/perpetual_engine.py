#!/usr/bin/env python3
"""
稷下学宫永动机引擎
为八仙论道提供无限数据支撑

重构版本：
- 移除硬编码密钥
- 添加类型注解
- 改进错误处理
- 统一配置管理
"""

import requests
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ImmortalConfig:
    """八仙配置数据类"""
    primary: str
    backup: List[str]
    specialty: str

@dataclass
class APIResult:
    """API调用结果数据类"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    api_used: Optional[str] = None
    usage_count: Optional[int] = None
    error: Optional[str] = None

class JixiaPerpetualEngine:
    """稷下学宫永动机引擎"""
    
    def __init__(self, rapidapi_key: str):
        """
        初始化永动机引擎
        
        Args:
            rapidapi_key: RapidAPI密钥，从环境变量或Doppler获取
        """
        if not rapidapi_key:
            raise ValueError("RapidAPI密钥不能为空")
        
        self.rapidapi_key = rapidapi_key
        
        # 八仙专属API分配 - 基于4个可用API优化
        self.immortal_apis: Dict[str, ImmortalConfig] = {
            '吕洞宾': ImmortalConfig(  # 乾-技术分析专家
                primary='alpha_vantage',
                backup=['yahoo_finance_1'],
                specialty='comprehensive_analysis'
            ),
            '何仙姑': ImmortalConfig(  # 坤-风险控制专家
                primary='yahoo_finance_1',
                backup=['webull'],
                specialty='risk_management'
            ),
            '张果老': ImmortalConfig(  # 兑-历史数据分析师
                primary='seeking_alpha',
                backup=['alpha_vantage'],
                specialty='fundamental_analysis'
            ),
            '韩湘子': ImmortalConfig(  # 艮-新兴资产专家
                primary='webull',
                backup=['yahoo_finance_1'],
                specialty='emerging_trends'
            ),
            '汉钟离': ImmortalConfig(  # 离-热点追踪
                primary='yahoo_finance_1',
                backup=['webull'],
                specialty='hot_trends'
            ),
            '蓝采和': ImmortalConfig(  # 坎-潜力股发现
                primary='webull',
                backup=['alpha_vantage'],
                specialty='undervalued_stocks'
            ),
            '曹国舅': ImmortalConfig(  # 震-机构分析
                primary='seeking_alpha',
                backup=['alpha_vantage'],
                specialty='institutional_analysis'
            ),
            '铁拐李': ImmortalConfig(  # 巽-逆向投资
                primary='alpha_vantage',
                backup=['seeking_alpha'],
                specialty='contrarian_analysis'
            )
        }
        
        # API池配置 - 只保留4个可用的API
        self.api_configs: Dict[str, str] = {
            'alpha_vantage': 'alpha-vantage.p.rapidapi.com',        # 1.26s ⚡
            'webull': 'webull.p.rapidapi.com',                     # 1.56s ⚡
            'yahoo_finance_1': 'yahoo-finance15.p.rapidapi.com',   # 2.07s
            'seeking_alpha': 'seeking-alpha.p.rapidapi.com'        # 3.32s
        }
        
        # 使用统计
        self.usage_tracker: Dict[str, int] = {api: 0 for api in self.api_configs.keys()}
        
    def get_immortal_data(self, immortal_name: str, data_type: str, symbol: str = 'AAPL') -> APIResult:
        """
        为特定八仙获取专属数据
        
        Args:
            immortal_name: 八仙名称
            data_type: 数据类型
            symbol: 股票代码
            
        Returns:
            API调用结果
        """
        if immortal_name not in self.immortal_apis:
            return APIResult(success=False, error=f'Unknown immortal: {immortal_name}')
        
        immortal_config = self.immortal_apis[immortal_name]
        
        print(f"🧙‍♂️ {immortal_name} 请求 {data_type} 数据 (股票: {symbol})")
        
        # 尝试主要API
        result = self._call_api(immortal_config.primary, data_type, symbol)
        if result.success:
            print(f"   ✅ 使用主要API: {immortal_config.primary}")
            return result
        
        # 故障转移到备用API
        for backup_api in immortal_config.backup:
            print(f"   🔄 故障转移到: {backup_api}")
            result = self._call_api(backup_api, data_type, symbol)
            if result.success:
                print(f"   ✅ 备用API成功: {backup_api}")
                return result
        
        print(f"   ❌ 所有API都失败了")
        return APIResult(success=False, error='All APIs failed')
    
    def _call_api(self, api_name: str, data_type: str, symbol: str) -> APIResult:
        """
        调用指定API
        
        Args:
            api_name: API名称
            data_type: 数据类型
            symbol: 股票代码
            
        Returns:
            API调用结果
        """
        if api_name not in self.api_configs:
            return APIResult(success=False, error=f'API {api_name} not configured')
        
        host = self.api_configs[api_name]
        headers = {
            'X-RapidAPI-Key': self.rapidapi_key,
            'X-RapidAPI-Host': host,
            'Content-Type': 'application/json'
        }
        
        endpoint = self._get_endpoint(api_name, data_type, symbol)
        if not endpoint:
            return APIResult(success=False, error=f'No endpoint for {data_type} on {api_name}')
        
        url = f"https://{host}{endpoint}"
        
        try:
            response = requests.get(url, headers=headers, timeout=8)
            self.usage_tracker[api_name] += 1
            
            if response.status_code == 200:
                return APIResult(
                    success=True,
                    data=response.json(),
                    api_used=api_name,
                    usage_count=self.usage_tracker[api_name]
                )
            else:
                return APIResult(
                    success=False,
                    error=f'HTTP {response.status_code}: {response.text[:100]}'
                )
        except requests.exceptions.Timeout:
            return APIResult(success=False, error='Request timeout')
        except requests.exceptions.RequestException as e:
            return APIResult(success=False, error=f'Request error: {str(e)}')
        except Exception as e:
            return APIResult(success=False, error=f'Unexpected error: {str(e)}')
    
    def _get_endpoint(self, api_name: str, data_type: str, symbol: str) -> Optional[str]:
        """
        根据API和数据类型返回合适的端点
        
        Args:
            api_name: API名称
            data_type: 数据类型
            symbol: 股票代码
            
        Returns:
            API端点路径
        """
        endpoint_mapping = {
            'alpha_vantage': {
                'quote': f'/query?function=GLOBAL_QUOTE&symbol={symbol}',
                'overview': f'/query?function=OVERVIEW&symbol={symbol}',
                'earnings': f'/query?function=EARNINGS&symbol={symbol}',
                'profile': f'/query?function=OVERVIEW&symbol={symbol}',
                'analysis': f'/query?function=OVERVIEW&symbol={symbol}'
            },
            'yahoo_finance_1': {
                'quote': f'/api/yahoo/qu/quote/{symbol}',
                'gainers': '/api/yahoo/co/collections/day_gainers',
                'losers': '/api/yahoo/co/collections/day_losers',
                'search': f'/api/yahoo/qu/quote/{symbol}',
                'analysis': f'/api/yahoo/qu/quote/{symbol}',
                'profile': f'/api/yahoo/qu/quote/{symbol}'
            },
            'seeking_alpha': {
                'profile': f'/symbols/get-profile?symbols={symbol}',
                'news': '/news/list?category=market-news',
                'analysis': f'/symbols/get-profile?symbols={symbol}',
                'quote': f'/symbols/get-profile?symbols={symbol}'
            },
            'webull': {
                'search': f'/stock/search?keyword={symbol}',
                'quote': f'/stock/search?keyword={symbol}',
                'analysis': f'/stock/search?keyword={symbol}',
                'gainers': '/market/get-active-gainers',
                'profile': f'/stock/search?keyword={symbol}'
            }
        }
        
        api_endpoints = endpoint_mapping.get(api_name, {})
        return api_endpoints.get(data_type, api_endpoints.get('quote'))
    
    def simulate_jixia_debate(self, topic_symbol: str = 'TSLA') -> Dict[str, APIResult]:
        """
        模拟稷下学宫八仙论道
        
        Args:
            topic_symbol: 辩论主题股票代码
            
        Returns:
            八仙辩论结果
        """
        print(f"🏛️ 稷下学宫八仙论道 - 主题: {topic_symbol}")
        print("=" * 60)
        
        debate_results: Dict[str, APIResult] = {}
        
        # 数据类型映射
        data_type_mapping = {
            'comprehensive_analysis': 'overview',
            'etf_tracking': 'quote',
            'fundamental_analysis': 'profile',
            'emerging_trends': 'news',
            'hot_trends': 'gainers',
            'undervalued_stocks': 'search',
            'institutional_analysis': 'profile',
            'contrarian_analysis': 'analysis'
        }
        
        # 八仙依次发言
        for immortal_name, config in self.immortal_apis.items():
            print(f"\n🎭 {immortal_name} ({config.specialty}) 发言:")
            
            data_type = data_type_mapping.get(config.specialty, 'quote')
            result = self.get_immortal_data(immortal_name, data_type, topic_symbol)
            
            if result.success:
                debate_results[immortal_name] = result
                print(f"   💬 观点: 基于{result.api_used}数据的{config.specialty}分析")
            else:
                print(f"   😔 暂时无法获取数据: {result.error}")
            
            time.sleep(0.5)  # 避免过快请求
        
        return debate_results
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        获取使用统计信息
        
        Returns:
            统计信息字典
        """
        total_calls = sum(self.usage_tracker.values())
        active_apis = len([api for api, count in self.usage_tracker.items() if count > 0])
        unused_apis = [api for api, count in self.usage_tracker.items() if count == 0]
        
        return {
            'total_calls': total_calls,
            'active_apis': active_apis,
            'total_apis': len(self.api_configs),
            'average_calls_per_api': total_calls / len(self.api_configs) if self.api_configs else 0,
            'usage_by_api': {api: count for api, count in self.usage_tracker.items() if count > 0},
            'unused_apis': unused_apis,
            'unused_count': len(unused_apis)
        }
    
    def print_perpetual_stats(self) -> None:
        """打印永动机统计信息"""
        stats = self.get_usage_stats()
        
        print(f"\n📊 永动机运行统计:")
        print("=" * 60)
        print(f"总API调用次数: {stats['total_calls']}")
        print(f"活跃API数量: {stats['active_apis']}/{stats['total_apis']}")
        print(f"平均每API调用: {stats['average_calls_per_api']:.1f}次")
        
        if stats['usage_by_api']:
            print(f"\n各API使用情况:")
            for api, count in stats['usage_by_api'].items():
                print(f"  {api}: {count}次")
        
        print(f"\n🎯 未使用的API储备: {stats['unused_count']}个")
        if stats['unused_apis']:
            unused_display = ', '.join(stats['unused_apis'][:5])
            if len(stats['unused_apis']) > 5:
                unused_display += '...'
            print(f"储备API: {unused_display}")
        
        print(f"\n💡 永动机效果:")
        print(f"  • {stats['total_apis']}个API订阅，智能调度")
        print(f"  • 智能故障转移，永不断线")
        print(f"  • 八仙专属API，个性化数据")
        print(f"  • 成本优化，效果最大化！")