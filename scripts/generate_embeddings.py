#!/usr/bin/env python3
"""
为MongoDB中的文章生成向量embeddings
用于swarm辩论系统的语义搜索和内容聚类
"""

import os
import openai
from pymongo import MongoClient
from typing import List, Dict
import time

def get_mongodb_client():
    """从Doppler获取MongoDB连接"""
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        raise ValueError("MONGODB_URI not found in environment variables")
    return MongoClient(mongodb_uri)

def generate_embedding(text: str) -> List[float]:
    """使用OpenAI API生成文本embedding"""
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"生成embedding失败: {e}")
        return None

def update_articles_with_embeddings():
    """为所有文章添加embedding字段"""
    client = get_mongodb_client()
    db = client.taigong
    collection = db.articles
    
    # 获取所有没有embedding的文章
    articles = collection.find({"embedding": {"$exists": False}})
    
    count = 0
    for article in articles:
        title = article.get('title', '')
        if not title:
            continue
            
        print(f"处理文章: {title[:50]}...")
        
        # 生成embedding
        embedding = generate_embedding(title)
        if embedding:
            # 更新文档
            collection.update_one(
                {"_id": article["_id"]},
                {"$set": {"embedding": embedding}}
            )
            count += 1
            print(f"✓ 已更新 {count} 篇文章")
            
            # 避免API rate limit
            time.sleep(0.1)
        else:
            print(f"× 跳过文章: {title[:50]}")
    
    print(f"\n完成！共处理 {count} 篇文章")
    client.close()

if __name__ == "__main__":
    # 设置OpenAI API密钥 (应该从Doppler获取)
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        print("警告: OPENAI_API_KEY 未设置，请先在Doppler中配置")
        exit(1)
    
    update_articles_with_embeddings()