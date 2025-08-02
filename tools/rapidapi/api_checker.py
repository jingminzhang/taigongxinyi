#!/usr/bin/env python3
"""
RapidAPI检查工具
从cauldron_new迁移的简化版本
"""

import requests
import time
from typing import Dict, List, Any
from config.doppler_config import get_rapidapi_key

class RapidAPIChecker:
    """RapidAPI服务检查器"""
    
    def __init__(self):
        """初始化检查器"""
        try:
            self.api_key = get_rapidapi_key()
        except Exception as e:
            print(f"❌ 无法获取RapidAPI密钥: {e}")
            self.api_key = ""
        
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def test_api(self, host: str, endpoint: str, params: Dict = None, method: str = 'GET') -> Dict[str, Any]:
        """
        测试特定的RapidAPI服务
        
        Args:
            host: API主机名
            endpoint: API端点
            params: 请求参数
            method: HTTP方法
            
        Returns:
            测试结果
        """
        self.headers['X-RapidAPI-Host'] = host
        url = f"https://{host}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, params=params, timeout=8)
            else:
                response = requests.post(url, headers=self.headers, json=params, timeout=8)
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response_size': len(response.text),
                'response_time': response.elapsed.total_seconds(),
                'error': None if response.status_code == 200 else response.text[:200]
            }
        except Exception as e:
            return {
                'success': False,
                'status_code': None,
                'response_size': 0,
                'response_time': 0,
                'error': str(e)
            }
    
    def check_common_apis(self) -> Dict[str, Dict[str, Any]]:
        """检查常用的RapidAPI服务"""
        print("🔍 检查RapidAPI订阅状态")
        
        # 常用API列表
        apis_to_check = [
            {
                'name': 'Yahoo Finance',
                'host': 'yahoo-finance15.p.rapidapi.com',
                'endpoint': '/api/yahoo/qu/quote/AAPL'
            },
            {
                'name': 'Alpha Vantage',
                'host': 'alpha-vantage.p.rapidapi.com',
                'endpoint': '/query?function=GLOBAL_QUOTE&symbol=AAPL'
            },
            {
                'name': 'Seeking Alpha',
                'host': 'seeking-alpha.p.rapidapi.com',
                'endpoint': '/symbols/get-profile?symbols=AAPL'
            }
        ]
        
        results = {}
        for api in apis_to_check:
            print(f"  测试 {api['name']}...")
            result = self.test_api(api['host'], api['endpoint'])
            results[api['name']] = result
            
            status = "✅ 可用" if result['success'] else "❌ 不可用"
            print(f"    {status} - {result.get('response_time', 0):.2f}s")
            
            time.sleep(0.5)  # 避免请求过快
        
        return results

def main():
    """主函数"""
    checker = RapidAPIChecker()
    results = checker.check_common_apis()
    
    print("\n📊 检查结果总结:")
    available_count = sum(1 for result in results.values() if result['success'])
    print(f"可用API: {available_count}/{len(results)}")

if __name__ == "__main__":
    main()