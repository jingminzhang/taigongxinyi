#!/usr/bin/env python3
"""
为现有文章添加流水号
"""

import os
from pymongo import MongoClient

def add_sequence_ids():
    """为现有文章添加流水号"""
    # 连接MongoDB
    mongo_uri = os.getenv('MONGODB_URI', 'mongodb+srv://ben:313131@cauldron.tx3qnoq.mongodb.net/')
    client = MongoClient(mongo_uri)
    db = client['taigong']
    collection = db['articles']
    
    print("开始为现有文章添加流水号...")
    
    # 查找所有没有sequence_id的文章
    articles_without_seq = list(collection.find(
        {"sequence_id": {"$exists": False}},
        {"_id": 1, "title": 1, "created_at": 1}
    ).sort("created_at", 1))  # 按创建时间排序
    
    print(f"找到 {len(articles_without_seq)} 篇文章需要添加流水号")
    
    if len(articles_without_seq) == 0:
        print("所有文章都已有流水号")
        return
    
    # 从1开始分配流水号
    for i, article in enumerate(articles_without_seq, 1):
        sequence_id = i
        article_id = f"NEWS_{sequence_id:08d}"  # NEWS_00000001 格式
        
        collection.update_one(
            {"_id": article["_id"]},
            {
                "$set": {
                    "sequence_id": sequence_id,
                    "article_id": article_id,
                    "batch_id": "migration_batch",
                    "last_updated": "2025-02-08T00:00:00Z"
                }
            }
        )
        
        print(f"  {sequence_id:3d}: {article['title'][:50]}...")
    
    print(f"流水号添加完成，共处理 {len(articles_without_seq)} 篇文章")
    
    # 验证结果
    total_with_seq = collection.count_documents({"sequence_id": {"$exists": True}})
    max_seq = collection.find_one({}, sort=[("sequence_id", -1)])
    
    print(f"验证结果:")
    print(f"  有流水号的文章: {total_with_seq} 篇")
    print(f"  最大流水号: {max_seq['sequence_id'] if max_seq else 0}")

if __name__ == "__main__":
    add_sequence_ids()