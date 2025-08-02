#!/usr/bin/env python3
"""
清理MongoDB中的重复文章数据
"""

import os
import sys
from pymongo import MongoClient
from collections import defaultdict
import hashlib

def generate_stable_id(title, pub_date, content):
    """生成稳定的文章ID"""
    normalized_title = title.strip().lower()
    content_hash = content[:100] if content else ''
    date_str = pub_date or ''
    
    combined = f"{normalized_title}|{date_str}|{content_hash}"
    return hashlib.md5(combined.encode()).hexdigest()[:16]

def cleanup_duplicates():
    """清理重复数据"""
    # 连接MongoDB
    mongo_uri = os.getenv('MONGODB_URI', 'mongodb+srv://ben:313131@cauldron.tx3qnoq.mongodb.net/')
    client = MongoClient(mongo_uri)
    db = client['taigong']
    collection = db['articles']
    
    print("开始清理重复数据...")
    
    # 1. 查找所有文章
    articles = list(collection.find({}))
    print(f"总共找到 {len(articles)} 篇文章")
    
    # 2. 按标题分组，找出重复项
    title_groups = defaultdict(list)
    for article in articles:
        title_groups[article['title']].append(article)
    
    # 3. 处理重复项
    duplicates_removed = 0
    articles_updated = 0
    
    for title, group in title_groups.items():
        if len(group) > 1:
            print(f"发现重复标题: {title} ({len(group)} 篇)")
            
            # 保留最早的一篇，删除其他
            group.sort(key=lambda x: x.get('created_at', ''))
            keep_article = group[0]
            
            # 更新保留文章的ID为稳定ID
            stable_id = generate_stable_id(
                keep_article['title'],
                keep_article.get('published_time', ''),
                keep_article.get('content', '')
            )
            
            collection.update_one(
                {'_id': keep_article['_id']},
                {
                    '$set': {
                        'article_id': stable_id,
                        'content_hash': generate_stable_id(keep_article.get('content', ''), '', ''),
                        'last_updated': '2025-02-08T00:00:00Z'
                    }
                }
            )
            articles_updated += 1
            
            # 删除重复项
            for duplicate in group[1:]:
                collection.delete_one({'_id': duplicate['_id']})
                duplicates_removed += 1
                print(f"  删除重复项: {duplicate.get('article_id', 'unknown')}")
    
    # 4. 为没有重复的文章更新ID
    single_articles = [group[0] for group in title_groups.values() if len(group) == 1]
    for article in single_articles:
        if not article.get('article_id') or len(article.get('article_id', '')) > 20:
            stable_id = generate_stable_id(
                article['title'],
                article.get('published_time', ''),
                article.get('content', '')
            )
            
            collection.update_one(
                {'_id': article['_id']},
                {
                    '$set': {
                        'article_id': stable_id,
                        'content_hash': generate_stable_id(article.get('content', ''), '', ''),
                        'last_updated': '2025-02-08T00:00:00Z'
                    }
                }
            )
            articles_updated += 1
    
    print(f"清理完成:")
    print(f"  删除重复文章: {duplicates_removed} 篇")
    print(f"  更新文章ID: {articles_updated} 篇")
    print(f"  最终文章数: {collection.count_documents({})} 篇")

if __name__ == "__main__":
    cleanup_duplicates()