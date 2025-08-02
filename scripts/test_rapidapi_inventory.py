#!/usr/bin/env python3
"""
RapidAPI库存测试脚本
自动测试所有订阅的API服务，生成可用性报告
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import os

class RapidAPITester:
    """RapidAPI测试器"""
    
    def __init__(self):
        """初始化测试器"""
        # 从环境变量获取API密钥
        self.api_key = os.getenv('RAPIDAPI_KEY')
        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY环境变量未设置")
        
        # API配置 - 基于永动机引擎的配置
        self.api_configs = {
            'alpha_vantage': 'alpha-vantage.p.rapidapi.com',
            'yahoo_finance_1': 'yahoo-finance15.p.rapidapi.com',
            'yh_finance_complete': 'yh-finance.p.rapidapi.com',
            'yahoo_finance_api_data': 'yahoo-finance-api1.p.rapidapi.com',
            'yahoo_finance_realtime': 'yahoo-finance-low-latency.p.rapidapi.com',
            'yh_finance': 'yh-finance-complete.p.rapidapi.com',
            'yahoo_finance_basic': 'yahoo-finance127.p.rapidapi.com',
            'seeking_alpha': 'seeking-alpha.p.rapidapi.com',
            'webull': 'webull.p.rapidapi.com',
            'morning_star': 'morningstar1.p.rapidapi.com',
            'tradingview': 'tradingview-ta.p.rapidapi.com',
            'investing_com': 'investing-cryptocurrency-markets.p.rapidapi.com',
            'finance_api': 'real-time-finance-data.p.rapidapi.com',
            'ms_finance': 'ms-finance.p.rapidapi.com',
            'sec_filings': 'sec-filings.p.rapidapi.com',
            'exchangerate_api': 'exchangerate-api.p.rapidapi.com',
            'crypto_news': 'cryptocurrency-news2.p.rapidapi.com'
        }
        
        # 测试端点配置
        self.test_endpoints = {
            'alpha_vantage': '/query?function=GLOBAL_QUOTE&symbol=AAPL',
            'yahoo_finance_1': '/api/yahoo/qu/quote/AAPL',
            'yh_finance_complete': '/stock/v2/get-summary?symbol=AAPL',
            'yahoo_finance_api_data': '/v8/finance/chart/AAPL',
            'yahoo_finance_realtime': '/stock/v2/get-summary?symbol=AAPL',
            'yh_finance': '/stock/v2/get-summary?symbol=AAPL',
            'yahoo_finance_basic': '/api/yahoo/qu/quote/AAPL',
            'seeking_alpha': '/symbols/get-profile?symbols=AAPL',
            'webull': '/stock/search?keyword=AAPL',
            'morning_star': '/market/v2/get-movers?performanceId=0P0000OQN8',
            'tradingview': '/get-analysis?symbol=AAPL&screener=america&exchange=NASDAQ',
            'investing_com': '/coins/get-overview',
            'finance_api': '/stock-price?symbol=AAPL',
            'ms_finance': '/stock/v2/get-summary?symbol=AAPL',
            'sec_filings': '/search?query=AAPL',
            'exchangerate_api': '/latest?base=USD',
            'crypto_news': '/v1/cryptonews'
        }
        
        self.results = {}
    
    def test_api(self, api_name: str) -> Dict[str, Any]:
        """
        测试单个API
        
        Args:
            api_name: API名称
            
        Returns:
            测试结果
        """
        if api_name not in self.api_configs:
            return {
                'success': False,
                'error': 'API not configured',
                'status_code': None,
                'response_time': 0
            }
        
        host = self.api_configs[api_name]
        endpoint = self.test_endpoints.get(api_name, '/')
        
        headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': host,
            'Content-Type': 'application/json'
        }
        
        url = f"https://{host}{endpoint}"
        
        print(f"🧪 测试 {api_name} ({host})")
        print(f"   URL: {url}")
        
        start_time = time.time()
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response_time = time.time() - start_time
            
            result = {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response_time': round(response_time, 2),
                'response_size': len(response.text),
                'error': None if response.status_code == 200 else response.text[:200]
            }
            
            if response.status_code == 200:
                print(f"   ✅ 成功 - {response_time:.2f}s - {len(response.text)} bytes")
                # 尝试解析JSON
                try:
                    data = response.json()
                    result['has_data'] = bool(data)
                    result['data_keys'] = list(data.keys()) if isinstance(data, dict) else []
                except:
                    result['has_data'] = False
                    result['data_keys'] = []
            else:
                print(f"   ❌ 失败 - HTTP {response.status_code}")
                print(f"   错误: {response.text[:100]}...")
            
            return result
            
        except requests.exceptions.Timeout:
            print(f"   ⏰ 超时")
            return {
                'success': False,
                'error': 'Request timeout',
                'status_code': None,
                'response_time': 10.0
            }
        except requests.exceptions.RequestException as e:
            print(f"   ❌ 请求异常: {str(e)}")
            return {
                'success': False,
                'error': f'Request error: {str(e)}',
                'status_code': None,
                'response_time': time.time() - start_time
            }
        except Exception as e:
            print(f"   ❌ 未知异常: {str(e)}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'status_code': None,
                'response_time': time.time() - start_time
            }
    
    def test_all_apis(self) -> Dict[str, Any]:
        """测试所有API"""
        print("🚀 开始测试所有RapidAPI服务")
        print("=" * 60)
        
        for api_name in self.api_configs.keys():
            result = self.test_api(api_name)
            self.results[api_name] = result
            time.sleep(1)  # 避免请求过快
            print()
        
        return self.results
    
    def generate_report(self) -> str:
        """生成测试报告"""
        if not self.results:
            return "没有测试结果"
        
        # 统计
        total_apis = len(self.results)
        successful_apis = len([r for r in self.results.values() if r['success']])
        failed_apis = total_apis - successful_apis
        
        # 按状态分类
        success_list = []
        failed_list = []
        
        for api_name, result in self.results.items():
            if result['success']:
                success_list.append({
                    'name': api_name,
                    'host': self.api_configs[api_name],
                    'response_time': result['response_time'],
                    'data_keys': result.get('data_keys', [])
                })
            else:
                failed_list.append({
                    'name': api_name,
                    'host': self.api_configs[api_name],
                    'error': result['error'],
                    'status_code': result['status_code']
                })
        
        # 生成报告
        report = f"""# RapidAPI 测试报告

## 📊 测试概览

- **测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **总API数**: {total_apis}
- **成功数**: {successful_apis} ({successful_apis/total_apis*100:.1f}%)
- **失败数**: {failed_apis} ({failed_apis/total_apis*100:.1f}%)

## ✅ 可用的API ({len(success_list)}个)

"""
        
        for api in sorted(success_list, key=lambda x: x['response_time']):
            report += f"### {api['name']}\n"
            report += f"- **主机**: `{api['host']}`\n"
            report += f"- **响应时间**: {api['response_time']}s\n"
            if api['data_keys']:
                report += f"- **数据字段**: {', '.join(api['data_keys'][:5])}\n"
            report += "\n"
        
        report += f"## ❌ 失败的API ({len(failed_list)}个)\n\n"
        
        for api in failed_list:
            report += f"### {api['name']}\n"
            report += f"- **主机**: `{api['host']}`\n"
            report += f"- **状态码**: {api['status_code']}\n"
            report += f"- **错误**: {api['error'][:100] if api['error'] else 'Unknown'}...\n"
            report += "\n"
        
        # 建议
        report += """## 🔧 优化建议

### 立即可用的API
"""
        
        fast_apis = [api for api in success_list if api['response_time'] < 2.0]
        if fast_apis:
            report += "以下API响应快速，建议优先使用：\n"
            for api in fast_apis:
                report += f"- **{api['name']}**: {api['response_time']}s\n"
        
        report += """
### 需要修复的API
"""
        
        if failed_list:
            report += "以下API需要检查端点配置或权限：\n"
            for api in failed_list[:5]:  # 只显示前5个
                report += f"- **{api['name']}**: {api['error'][:50] if api['error'] else 'Unknown error'}...\n"
        
        return report
    
    def save_report(self, filename: str = None):
        """保存报告到文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"docs/rapidapi/test_report_{timestamp}.md"
        
        report = self.generate_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 报告已保存到: {filename}")
        return filename

def main():
    """主函数"""
    print("🧪 RapidAPI库存测试工具")
    print("=" * 40)
    
    try:
        tester = RapidAPITester()
        
        # 测试所有API
        results = tester.test_all_apis()
        
        # 生成并显示报告
        print("\n" + "=" * 60)
        print("📊 测试完成，生成报告...")
        
        report = tester.generate_report()
        print(report)
        
        # 保存报告
        filename = tester.save_report()
        
        # 更新库存文档
        print(f"\n💡 建议更新 docs/rapidapi/api_inventory.md")
        print(f"📁 详细报告: {filename}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()