#!/usr/bin/env python3
"""
Swarm辩论触发器
基于时间群聚效应和语义相似性触发蜂群辩论
"""

import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from typing import List, Dict, Optional
import numpy as np

class SwarmDebateTrigger:
    def __init__(self):
        self.mongodb_uri = os.getenv('MONGODB_URI')
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client.taigong
        self.collection = self.db.articles
        
        # 配置参数
        self.swarm_threshold = int(os.getenv('SWARM_THRESHOLD', 5))
        self.time_window_hours = int(os.getenv('SWARM_TIME_WINDOW_HOURS', 24))
    
    def detect_time_clustering(self) -> List[Dict]:
        """检测时间窗口内的文章群聚效应"""
        # 计算时间窗口
        now = datetime.utcnow()
        time_threshold = now - timedelta(hours=self.time_window_hours)
        
        # 使用published_time_index查询最近文章
        recent_articles = list(self.collection.find({
            "published_time": {"$gte": time_threshold}
        }).sort("published_time", -1))
        
        print(f"最近{self.time_window_hours}小时内发现 {len(recent_articles)} 篇文章")
        
        if len(recent_articles) >= self.swarm_threshold:
            print(f"✓ 触发群聚效应！文章数量({len(recent_articles)}) >= 阈值({self.swarm_threshold})")
            return recent_articles
        else:
            print(f"× 未达到群聚阈值，需要至少 {self.swarm_threshold} 篇文章")
            return []
    
    def find_semantic_clusters(self, articles: List[Dict], similarity_threshold: float = 0.8) -> List[List[Dict]]:
        """基于向量相似性找到语义聚类"""
        if not articles:
            return []
        
        # 过滤有embedding的文章
        articles_with_embeddings = [
            article for article in articles 
            if 'embedding' in article and article['embedding']
        ]
        
        if len(articles_with_embeddings) < 2:
            print("× 没有足够的embedding数据进行语义聚类")
            return [articles_with_embeddings] if articles_with_embeddings else []
        
        print(f"对 {len(articles_with_embeddings)} 篇文章进行语义聚类分析...")
        
        # 简单的相似性聚类算法
        clusters = []
        used_indices = set()
        
        for i, article1 in enumerate(articles_with_embeddings):
            if i in used_indices:
                continue
                
            cluster = [article1]
            used_indices.add(i)
            
            for j, article2 in enumerate(articles_with_embeddings):
                if j in used_indices or i == j:
                    continue
                
                # 计算余弦相似度
                similarity = self.cosine_similarity(
                    article1['embedding'], 
                    article2['embedding']
                )
                
                if similarity >= similarity_threshold:
                    cluster.append(article2)
                    used_indices.add(j)
            
            if len(cluster) >= 2:  # 至少2篇文章才算一个有效聚类
                clusters.append(cluster)
                print(f"✓ 发现语义聚类，包含 {len(cluster)} 篇相关文章")
        
        return clusters
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算两个向量的余弦相似度"""
        try:
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0
            
            return dot_product / (norm1 * norm2)
        except Exception as e:
            print(f"计算相似度失败: {e}")
            return 0
    
    def trigger_swarm_debate(self, clusters: List[List[Dict]]) -> bool:
        """触发swarm蜂群辩论"""
        if not clusters:
            print("× 没有发现有效的语义聚类，不触发辩论")
            return False
        
        print(f"\n🔥 触发Swarm蜂群辩论！")
        print(f"发现 {len(clusters)} 个语义聚类")
        
        for i, cluster in enumerate(clusters):
            print(f"\n聚类 {i+1}: {len(cluster)} 篇文章")
            for article in cluster:
                title = article.get('title', '无标题')[:50]
                time_str = article.get('published_time', '').strftime('%Y-%m-%d %H:%M') if article.get('published_time') else '未知时间'
                print(f"  - {title}... ({time_str})")
        
        # TODO: 在这里调用实际的辩论系统
        # 例如: jixia_swarm_debate(clusters)
        
        return True
    
    def run(self) -> bool:
        """运行swarm辩论触发检测"""
        print("🔍 开始检测swarm辩论触发条件...")
        
        # 1. 检测时间群聚效应
        recent_articles = self.detect_time_clustering()
        if not recent_articles:
            return False
        
        # 2. 进行语义聚类分析
        semantic_clusters = self.find_semantic_clusters(recent_articles)
        
        # 3. 触发辩论
        return self.trigger_swarm_debate(semantic_clusters)

if __name__ == "__main__":
    trigger = SwarmDebateTrigger()
    trigger.run()