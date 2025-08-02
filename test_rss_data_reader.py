#!/usr/bin/env python3
"""
RSS数据读取测试器
测试从MongoDB读取RSS新闻数据，并分析索引需求
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
from src.mcp.swarm_mongodb_client import SwarmMongoDBClient

class RSSDataReader:
    """RSS数据读取器和分析器"""
    
    def __init__(self, mongodb_client: SwarmMongoDBClient, database_name: str = "news_debate_db"):
        self.mongodb_client = mongodb_client
        self.database_name = database_name
        self.collection_name = "news_articles"
        self.logger = logging.getLogger(__name__)
    
    async def connect_to_database(self) -> bool:
        """连接到数据库"""
        try:
            result = self.mongodb_client.connect(self.database_name)
            if result.get('success'):
                self.logger.info(f"成功连接到数据库: {self.database_name}")
                return True
            else:
                self.logger.error(f"数据库连接失败: {result}")
                return False
        except Exception as e:
            self.logger.error(f"数据库连接异常: {e}")
            return False
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """获取集合统计信息"""
        try:
            # 获取文档总数
            count_result = self.mongodb_client.count_documents(self.collection_name)
            total_count = count_result.get('count', 0) if count_result.get('success') else 0
            
            # 获取最新的几条记录来分析数据结构
            latest_docs = self.mongodb_client.find_documents(
                self.collection_name,
                query={},
                sort={'collected_at': -1},
                limit=5
            )
            
            # 获取最早的记录
            earliest_docs = self.mongodb_client.find_documents(
                self.collection_name,
                query={},
                sort={'collected_at': 1},
                limit=1
            )
            
            stats = {
                'total_documents': total_count,
                'latest_documents': latest_docs.get('documents', []) if latest_docs.get('success') else [],
                'earliest_document': earliest_docs.get('documents', []) if earliest_docs.get('success') else [],
                'collection_exists': total_count > 0
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"获取集合统计信息失败: {e}")
            return {'error': str(e)}
    
    async def analyze_data_structure(self, sample_size: int = 10) -> Dict[str, Any]:
        """分析数据结构"""
        try:
            # 获取样本数据
            sample_result = self.mongodb_client.find_documents(
                self.collection_name,
                query={},
                limit=sample_size
            )
            
            if not sample_result.get('success'):
                return {'error': '无法获取样本数据'}
            
            documents = sample_result.get('documents', [])
            if not documents:
                return {'error': '没有找到任何文档'}
            
            # 分析字段结构
            field_analysis = {}
            for doc in documents:
                for field, value in doc.items():
                    if field not in field_analysis:
                        field_analysis[field] = {
                            'type': type(value).__name__,
                            'sample_values': [],
                            'count': 0
                        }
                    
                    field_analysis[field]['count'] += 1
                    if len(field_analysis[field]['sample_values']) < 3:
                        field_analysis[field]['sample_values'].append(str(value)[:100])  # 限制长度
            
            # 分析常见查询字段
            query_fields = {
                'title': '标题搜索',
                'category': '分类筛选',
                'published': '时间范围查询',
                'collected_at': '收集时间排序',
                'tags': '标签搜索',
                'source_title': '来源筛选'
            }
            
            return {
                'sample_count': len(documents),
                'field_analysis': field_analysis,
                'recommended_query_fields': query_fields,
                'sample_document': documents[0] if documents else None
            }
            
        except Exception as e:
            self.logger.error(f"数据结构分析失败: {e}")
            return {'error': str(e)}
    
    async def test_query_performance(self) -> Dict[str, Any]:
        """测试查询性能"""
        performance_results = {}
        
        # 测试不同类型的查询
        test_queries = [
            {
                'name': '全表扫描',
                'query': {},
                'sort': None,
                'limit': 10
            },
            {
                'name': '按时间排序',
                'query': {},
                'sort': {'collected_at': -1},
                'limit': 10
            },
            {
                'name': '标题文本搜索',
                'query': {'title': {'$regex': '市场', '$options': 'i'}},
                'sort': None,
                'limit': 10
            },
            {
                'name': '分类筛选',
                'query': {'category': '财经新闻'},
                'sort': None,
                'limit': 10
            },
            {
                'name': '时间范围查询',
                'query': {
                    'collected_at': {
                        '$gte': datetime.now(timezone.utc) - timedelta(days=7)
                    }
                },
                'sort': {'collected_at': -1},
                'limit': 10
            }
        ]
        
        for test in test_queries:
            try:
                start_time = time.time()
                
                result = self.mongodb_client.find_documents(
                    self.collection_name,
                    query=test['query'],
                    sort=test.get('sort'),
                    limit=test['limit']
                )
                
                end_time = time.time()
                query_time = (end_time - start_time) * 1000  # 转换为毫秒
                
                performance_results[test['name']] = {
                    'query_time_ms': round(query_time, 2),
                    'success': result.get('success', False),
                    'document_count': len(result.get('documents', [])),
                    'query': test['query']
                }
                
            except Exception as e:
                performance_results[test['name']] = {
                    'error': str(e),
                    'query': test['query']
                }
        
        return performance_results
    
    async def check_existing_indexes(self) -> Dict[str, Any]:
        """检查现有索引"""
        try:
            # 注意：这里需要使用MongoDB的原生命令来获取索引信息
            # 由于SwarmMongoDBClient可能没有直接的索引查询方法，我们尝试其他方式
            
            # 尝试通过聚合管道获取索引信息
            pipeline = [
                {"$indexStats": {}}
            ]
            
            # 如果客户端支持聚合查询
            if hasattr(self.mongodb_client, 'aggregate_documents'):
                result = self.mongodb_client.aggregate_documents(
                    self.collection_name,
                    pipeline=pipeline
                )
                
                if result.get('success'):
                    return {
                        'indexes': result.get('documents', []),
                        'method': 'aggregation'
                    }
            
            # 如果无法直接获取索引信息，返回建议
            return {
                'message': '无法直接查询索引信息，建议手动检查',
                'method': 'manual_check_needed'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'message': '索引查询失败'
            }
    
    def generate_index_recommendations(self, performance_results: Dict[str, Any], 
                                     data_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成索引建议"""
        recommendations = {
            'basic_indexes': [],
            'compound_indexes': [],
            'text_indexes': [],
            'vector_indexes': [],
            'reasoning': []
        }
        
        # 基础索引建议
        slow_queries = [name for name, result in performance_results.items() 
                       if isinstance(result, dict) and result.get('query_time_ms', 0) > 100]
        
        if slow_queries:
            recommendations['reasoning'].append(f"发现慢查询: {', '.join(slow_queries)}")
        
        # 基于数据结构的索引建议
        field_analysis = data_analysis.get('field_analysis', {})
        
        # 时间字段索引（用于排序和范围查询）
        if 'collected_at' in field_analysis:
            recommendations['basic_indexes'].append({
                'field': 'collected_at',
                'type': 'descending',
                'reason': '用于时间排序和范围查询'
            })
        
        if 'published' in field_analysis:
            recommendations['basic_indexes'].append({
                'field': 'published',
                'type': 'descending', 
                'reason': '用于发布时间查询'
            })
        
        # 分类字段索引
        if 'category' in field_analysis:
            recommendations['basic_indexes'].append({
                'field': 'category',
                'type': 'ascending',
                'reason': '用于分类筛选'
            })
        
        # 唯一标识符索引
        if 'article_id' in field_analysis:
            recommendations['basic_indexes'].append({
                'field': 'article_id',
                'type': 'ascending',
                'unique': True,
                'reason': '唯一标识符，防止重复'
            })
        
        # 复合索引建议
        recommendations['compound_indexes'].append({
            'fields': ['category', 'collected_at'],
            'reason': '支持按分类筛选并按时间排序'
        })
        
        # 文本搜索索引
        text_fields = []
        for field in ['title', 'description', 'summary']:
            if field in field_analysis:
                text_fields.append(field)
        
        if text_fields:
            recommendations['text_indexes'].append({
                'fields': text_fields,
                'type': 'text',
                'reason': '支持全文搜索'
            })
        
        # 向量索引建议
        recommendations['vector_indexes'].append({
            'consideration': '如果需要语义搜索',
            'fields': ['title', 'description'],
            'method': 'embedding + vector_search',
            'reason': '用于基于内容相似性的智能搜索和推荐'
        })
        
        return recommendations
    
    async def test_sample_queries(self) -> Dict[str, Any]:
        """测试一些示例查询"""
        sample_queries = {}
        
        try:
            # 1. 获取最新10条新闻
            latest_news = self.mongodb_client.find_documents(
                self.collection_name,
                query={},
                sort={'collected_at': -1},
                limit=10
            )
            sample_queries['latest_news'] = {
                'success': latest_news.get('success'),
                'count': len(latest_news.get('documents', [])),
                'sample_titles': [doc.get('title', 'N/A')[:50] + '...' 
                                for doc in latest_news.get('documents', [])[:3]]
            }
            
            # 2. 按分类查询
            category_news = self.mongodb_client.find_documents(
                self.collection_name,
                query={'category': '财经新闻'},
                limit=5
            )
            sample_queries['category_news'] = {
                'success': category_news.get('success'),
                'count': len(category_news.get('documents', [])),
                'category': '财经新闻'
            }
            
            # 3. 关键词搜索
            keyword_search = self.mongodb_client.find_documents(
                self.collection_name,
                query={'title': {'$regex': '投资|股票|市场', '$options': 'i'}},
                limit=5
            )
            sample_queries['keyword_search'] = {
                'success': keyword_search.get('success'),
                'count': len(keyword_search.get('documents', [])),
                'keywords': '投资|股票|市场'
            }
            
        except Exception as e:
            sample_queries['error'] = str(e)
        
        return sample_queries
    
    async def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """运行完整的数据分析"""
        self.logger.info("开始RSS数据分析...")
        
        # 连接数据库
        if not await self.connect_to_database():
            return {'error': '无法连接到数据库'}
        
        analysis_results = {}
        
        # 1. 获取集合统计信息
        self.logger.info("获取集合统计信息...")
        analysis_results['collection_stats'] = await self.get_collection_stats()
        
        # 2. 分析数据结构
        self.logger.info("分析数据结构...")
        analysis_results['data_structure'] = await self.analyze_data_structure()
        
        # 3. 测试查询性能
        self.logger.info("测试查询性能...")
        analysis_results['query_performance'] = await self.test_query_performance()
        
        # 4. 检查现有索引
        self.logger.info("检查现有索引...")
        analysis_results['existing_indexes'] = await self.check_existing_indexes()
        
        # 5. 生成索引建议
        self.logger.info("生成索引建议...")
        analysis_results['index_recommendations'] = self.generate_index_recommendations(
            analysis_results['query_performance'],
            analysis_results['data_structure']
        )
        
        # 6. 测试示例查询
        self.logger.info("测试示例查询...")
        analysis_results['sample_queries'] = await self.test_sample_queries()
        
        return analysis_results

async def main():
    """主函数"""
    # 初始化MongoDB客户端
    mongodb_client = SwarmMongoDBClient(
        mcp_server_url="http://localhost:8080",
        default_database="news_debate_db"
    )
    
    # 创建数据读取器
    reader = RSSDataReader(mongodb_client)
    
    # 运行分析
    results = await reader.run_comprehensive_analysis()
    
    # 输出结果
    print("\n" + "="*60)
    print("RSS数据分析报告")
    print("="*60)
    
    # 集合统计
    stats = results.get('collection_stats', {})
    print(f"\n📊 集合统计:")
    print(f"  总文档数: {stats.get('total_documents', 0)}")
    print(f"  集合存在: {stats.get('collection_exists', False)}")
    
    # 数据结构
    structure = results.get('data_structure', {})
    if 'field_analysis' in structure:
        print(f"\n🏗️  数据结构:")
        for field, info in structure['field_analysis'].items():
            print(f"  {field}: {info['type']} (出现{info['count']}次)")
    
    # 查询性能
    performance = results.get('query_performance', {})
    print(f"\n⚡ 查询性能:")
    for query_name, result in performance.items():
        if isinstance(result, dict) and 'query_time_ms' in result:
            print(f"  {query_name}: {result['query_time_ms']}ms ({result['document_count']}条结果)")
    
    # 索引建议
    recommendations = results.get('index_recommendations', {})
    print(f"\n💡 索引建议:")
    
    basic_indexes = recommendations.get('basic_indexes', [])
    if basic_indexes:
        print(f"  基础索引:")
        for idx in basic_indexes:
            print(f"    - {idx['field']} ({idx.get('type', 'ascending')}): {idx['reason']}")
    
    compound_indexes = recommendations.get('compound_indexes', [])
    if compound_indexes:
        print(f"  复合索引:")
        for idx in compound_indexes:
            print(f"    - {', '.join(idx['fields'])}: {idx['reason']}")
    
    text_indexes = recommendations.get('text_indexes', [])
    if text_indexes:
        print(f"  文本索引:")
        for idx in text_indexes:
            print(f"    - {', '.join(idx['fields'])}: {idx['reason']}")
    
    vector_indexes = recommendations.get('vector_indexes', [])
    if vector_indexes:
        print(f"  向量索引建议:")
        for idx in vector_indexes:
            print(f"    - {idx['consideration']}: {idx['reason']}")
    
    # 示例查询结果
    samples = results.get('sample_queries', {})
    print(f"\n🔍 示例查询:")
    for query_name, result in samples.items():
        if isinstance(result, dict) and 'count' in result:
            print(f"  {query_name}: {result['count']}条结果")
    
    print(f"\n" + "="*60)
    print("分析完成！")
    print("="*60)
    
    # 保存详细结果到文件
    with open('/home/ben/liurenchaxin/rss_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print("\n详细报告已保存到: rss_analysis_report.json")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(main())