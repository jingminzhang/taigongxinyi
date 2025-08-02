#!/usr/bin/env python3
"""
测试OpenRouter API连接
重构版本：使用统一配置管理
"""

import requests
from typing import Dict, Any

def test_openrouter_api() -> bool:
    """
    测试OpenRouter API连接
    
    Returns:
        测试是否成功
    """
    # 使用统一配置管理
    try:
        from config.doppler_config import get_openrouter_key
        api_key = get_openrouter_key()
    except ImportError:
        # 如果配置模块不可用，使用环境变量
        import os
        api_key = os.getenv('OPENROUTER_API_KEY_1')
    except Exception as e:
        print(f"❌ 无法获取API密钥: {e}")
        return False
    
    if not api_key:
        print("❌ 未找到OpenRouter API密钥")
        print("请确保已配置 OPENROUTER_API_KEY_1 环境变量")
        return False
    
    print(f"🔑 使用API密钥: {api_key[:20]}...")
    
    # 测试API调用
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/ben/liurenchaxin",
        "X-Title": "Jixia Academy Debate System",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "你好，请简单回复一下测试连接"}
        ],
        "max_tokens": 50
    }
    
    try:
        print("📡 正在测试API连接...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"📡 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ OpenRouter API连接成功!")
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"📝 AI回复: {content}")
            else:
                print("📝 API响应格式异常，但连接成功")
            return True
        else:
            print(f"❌ API调用失败: HTTP {response.status_code}")
            print(f"错误详情: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求异常: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知异常: {e}")
        return False

def test_rapidapi_connection() -> bool:
    """
    测试RapidAPI连接
    
    Returns:
        测试是否成功
    """
    try:
        from config.doppler_config import get_rapidapi_key
        api_key = get_rapidapi_key()
    except ImportError:
        import os
        api_key = os.getenv('RAPIDAPI_KEY')
    except Exception as e:
        print(f"❌ 无法获取RapidAPI密钥: {e}")
        return False
    
    if not api_key:
        print("❌ 未找到RapidAPI密钥")
        return False
    
    print(f"🔑 测试RapidAPI连接...")
    
    # 测试一个简单的API端点
    url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/AAPL"
    headers = {
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': 'yahoo-finance15.p.rapidapi.com'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ RapidAPI连接成功!")
            return True
        else:
            print(f"❌ RapidAPI连接失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ RapidAPI连接异常: {e}")
        return False

def main():
    """主函数 - 运行所有API连接测试"""
    print("🧪 API连接测试套件")
    print("=" * 50)
    
    # 测试配置验证
    try:
        from config.doppler_config import validate_config
        print("\n🔧 验证配置...")
        config_valid = validate_config()
    except ImportError:
        print("⚠️ 配置模块不可用，跳过配置验证")
        config_valid = True
    
    # 测试OpenRouter API
    print("\n🤖 测试OpenRouter API...")
    openrouter_success = test_openrouter_api()
    
    # 测试RapidAPI
    print("\n📊 测试RapidAPI...")
    rapidapi_success = test_rapidapi_api()
    
    # 总结测试结果
    print("\n" + "=" * 50)
    print("📋 测试结果总结:")
    print(f"  配置验证: {'✅ 通过' if config_valid else '❌ 失败'}")
    print(f"  OpenRouter API: {'✅ 通过' if openrouter_success else '❌ 失败'}")
    print(f"  RapidAPI: {'✅ 通过' if rapidapi_success else '❌ 失败'}")
    
    all_passed = config_valid and openrouter_success and rapidapi_success
    if all_passed:
        print("\n🎉 所有API连接测试通过！系统已准备就绪。")
    else:
        print("\n⚠️ 部分测试失败，请检查配置和网络连接。")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)