#!/usr/bin/env python3
"""
RSS新闻收集器
收集RSS新闻并存储到MongoDB，为辩论系统提供数据源
"""

import asyncio
import feedparser
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
import hashlib
import requests
from src.mcp.swarm_mongodb_client import SwarmMongoDBClient

class RSSNewsCollector:
    """RSS新闻收集器"""
    
    def __init__(self, mongodb_client: SwarmMongoDBClient):
        self.mongodb_client = mongodb_client
        self.logger = logging.getLogger(__name__)
        
        # 默认RSS源配置
        self.rss_sources = {
            '财经新闻': [
                'https://feeds.finance.yahoo.com/rss/2.0/headline',
                'https://www.cnbc.com/id/100003114/device/rss/rss.html',
                'https://feeds.reuters.com/reuters/businessNews'
            ],
            '科技新闻': [
                'https://feeds.feedburner.com/TechCrunch',
                'https://www.wired.com/feed/rss',
                'https://feeds.arstechnica.com/arstechnica/index'
            ],
            '市场分析': [
                'https://feeds.marketwatch.com/marketwatch/marketpulse/',
                'https://feeds.bloomberg.com/markets/news.rss'
            ]
        }
    
    def generate_article_id(self, url: str, title: str) -> str:
        """生成文章唯一ID"""
        content = f"{url}_{title}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def parse_rss_feed(self, rss_url: str) -> List[Dict[str, Any]]:
        """解析RSS源"""
        try:
            feed = feedparser.parse(rss_url)
            articles = []
            
            for entry in feed.entries:
                # 提取文章信息
                article = {
                    'article_id': self.generate_article_id(entry.link, entry.title),
                    'title': entry.title,
                    'link': entry.link,
                    'description': getattr(entry, 'description', ''),
                    'summary': getattr(entry, 'summary', ''),
                    'published': self._parse_date(getattr(entry, 'published', '')),
                    'author': getattr(entry, 'author', ''),
                    'tags': [tag.term for tag in getattr(entry, 'tags', [])],
                    'source_url': rss_url,
                    'source_title': feed.feed.get('title', ''),
                    'collected_at': datetime.now(timezone.utc),
                    'content_hash': hashlib.md5(entry.title.encode()).hexdigest()
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            self.logger.error(f"解析RSS源失败 {rss_url}: {e}")
            return []
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """解析日期字符串"""
        if not date_str:
            return None
        
        try:
            # feedparser通常会解析时间
            import time
            parsed_time = feedparser._parse_date(date_str)
            if parsed_time:
                return datetime.fromtimestamp(time.mktime(parsed_time), tz=timezone.utc)
        except:
            pass
        
        return datetime.now(timezone.utc)
    
    async def collect_news_from_category(self, category: str) -> List[Dict[str, Any]]:
        """从指定类别收集新闻"""
        if category not in self.rss_sources:
            self.logger.warning(f"未知新闻类别: {category}")
            return []
        
        all_articles = []
        for rss_url in self.rss_sources[category]:
            self.logger.info(f"正在收集新闻: {rss_url}")
            articles = self.parse_rss_feed(rss_url)
            
            # 添加类别标签
            for article in articles:
                article['category'] = category
            
            all_articles.extend(articles)
        
        return all_articles
    
    async def collect_all_news(self) -> Dict[str, List[Dict[str, Any]]]:
        """收集所有类别的新闻"""
        all_news = {}
        
        for category in self.rss_sources.keys():
            news = await self.collect_news_from_category(category)
            all_news[category] = news
            self.logger.info(f"收集到 {len(news)} 条 {category} 新闻")
        
        return all_news
    
    async def store_news_to_mongodb(self, articles: List[Dict[str, Any]], collection_name: str = "news_articles") -> Dict[str, Any]:
        """将新闻存储到MongoDB"""
        if not articles:
            return {'success': True, 'inserted_count': 0, 'updated_count': 0}
        
        inserted_count = 0
        updated_count = 0
        
        for article in articles:
            # 检查文章是否已存在
            existing = self.mongodb_client.find_documents(
                collection_name,
                query={'article_id': article['article_id']},
                limit=1
            )
            
            if existing.get('success') and existing.get('documents'):
                # 更新现有文章
                update_result = self.mongodb_client.update_document(
                    collection_name,
                    query={'article_id': article['article_id']},
                    update={'$set': article}
                )
                if update_result.get('success'):
                    updated_count += 1
            else:
                # 插入新文章
                insert_result = self.mongodb_client.insert_document(
                    collection_name,
                    document=article
                )
                if insert_result.get('success'):
                    inserted_count += 1
        
        return {
            'success': True,
            'inserted_count': inserted_count,
            'updated_count': updated_count,
            'total_processed': len(articles)
        }
    
    async def get_latest_news(self, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最新新闻"""
        query = {}
        if category:
            query['category'] = category
        
        result = self.mongodb_client.find_documents(
            'news_articles',
            query=query,
            sort={'collected_at': -1},
            limit=limit
        )
        
        if result.get('success'):
            return result.get('documents', [])
        return []
    
    async def get_news_for_debate(self, topic_keywords: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """根据关键词获取相关新闻用于辩论"""
        # 构建搜索查询
        search_conditions = []
        for keyword in topic_keywords:
            search_conditions.extend([
                {'title': {'$regex': keyword, '$options': 'i'}},
                {'description': {'$regex': keyword, '$options': 'i'}},
                {'summary': {'$regex': keyword, '$options': 'i'}}
            ])
        
        query = {'$or': search_conditions} if search_conditions else {}
        
        result = self.mongodb_client.find_documents(
            'news_articles',
            query=query,
            sort={'published': -1},
            limit=limit
        )
        
        if result.get('success'):
            return result.get('documents', [])
        return []
    
    async def run_collection_cycle(self):
        """运行一次完整的新闻收集周期"""
        self.logger.info("开始新闻收集周期")
        
        # 收集所有新闻
        all_news = await self.collect_all_news()
        
        # 存储到数据库
        total_inserted = 0
        total_updated = 0
        
        for category, articles in all_news.items():
            if articles:
                result = await self.store_news_to_mongodb(articles)
                total_inserted += result.get('inserted_count', 0)
                total_updated += result.get('updated_count', 0)
                self.logger.info(f"{category}: 新增 {result.get('inserted_count', 0)}, 更新 {result.get('updated_count', 0)}")
        
        self.logger.info(f"新闻收集完成: 总新增 {total_inserted}, 总更新 {total_updated}")
        
        return {
            'success': True,
            'total_inserted': total_inserted,
            'total_updated': total_updated,
            'categories_processed': len(all_news)
        }

async def main():
    """主函数 - 演示RSS新闻收集"""
    # 初始化MongoDB客户端
    mongodb_client = SwarmMongoDBClient(
        mcp_server_url="http://localhost:8080",
        default_database="news_debate_db"
    )
    
    # 连接数据库
    connect_result = mongodb_client.connect("news_debate_db")
    if not connect_result.get('success'):
        print(f"数据库连接失败: {connect_result}")
        return
    
    # 创建新闻收集器
    collector = RSSNewsCollector(mongodb_client)
    
    # 运行收集周期
    result = await collector.run_collection_cycle()
    print(f"收集结果: {result}")
    
    # 获取最新新闻示例
    latest_news = await collector.get_latest_news(limit=5)
    print(f"\n最新新闻 ({len(latest_news)} 条):")
    for news in latest_news:
        print(f"- {news.get('title', 'N/A')} [{news.get('category', 'N/A')}]")
    
    # 根据关键词搜索新闻示例
    debate_news = await collector.get_news_for_debate(['投资', '市场', '经济'], limit=3)
    print(f"\n辩论相关新闻 ({len(debate_news)} 条):")
    for news in debate_news:
        print(f"- {news.get('title', 'N/A')} [{news.get('category', 'N/A')}]")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())