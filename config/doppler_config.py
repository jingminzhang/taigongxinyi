#!/usr/bin/env python3
"""
Doppler配置管理模块
安全地从Doppler获取配置和密钥
"""

import os
from typing import Optional, Dict, Any

def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    从Doppler或环境变量获取密钥
    
    Args:
        key: 密钥名称
        default: 默认值
        
    Returns:
        密钥值或默认值
    """
    # 首先尝试从环境变量获取（Doppler会注入到环境变量）
    value = os.getenv(key, default)
    
    if not value and default is None:
        raise ValueError(f"Required secret '{key}' not found in environment variables")
    
    return value

def get_rapidapi_key() -> str:
    """
    获取RapidAPI密钥
    
    Returns:
        RapidAPI密钥
        
    Raises:
        ValueError: 如果密钥未找到
    """
    return get_secret('RAPIDAPI_KEY')

def get_openrouter_key() -> str:
    """
    获取OpenRouter API密钥
    
    Returns:
        OpenRouter API密钥
        
    Raises:
        ValueError: 如果密钥未找到
    """
    return get_secret('OPENROUTER_API_KEY_1')

def get_database_config() -> Dict[str, str]:
    """
    获取数据库配置
    
    Returns:
        数据库配置字典
    """
    return {
        'postgres_url': get_secret('POSTGRES_URL', ''),
        'mongodb_url': get_secret('MONGODB_URL', ''),
        'zilliz_url': get_secret('ZILLIZ_URL', ''),
        'zilliz_token': get_secret('ZILLIZ_TOKEN', '')
    }

def validate_config() -> bool:
    """
    验证必要的配置是否存在
    
    Returns:
        配置是否有效
    """
    required_keys = [
        'RAPIDAPI_KEY',
        'OPENROUTER_API_KEY_1'
    ]
    
    missing_keys = []
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ 缺少必要的配置: {', '.join(missing_keys)}")
        print("请确保已正确配置Doppler或环境变量")
        return False
    
    print("✅ 配置验证通过")
    return True

if __name__ == "__main__":
    # 配置验证脚本
    print("🔧 验证配置...")
    validate_config()