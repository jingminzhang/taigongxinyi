// MongoDB Atlas Vector Search Index Creation Script
// 为swarm辩论系统创建向量索引

// 连接到数据库
use('taigong');

// 创建向量索引用于语义搜索和内容聚类
// 这个索引将支持swarm辩论系统的语义相似性匹配
db.articles.createSearchIndex(
  "vector_search_index",
  {
    "fields": [
      {
        "type": "vector",
        "path": "embedding",
        "numDimensions": 1536, // OpenAI text-embedding-ada-002 维度
        "similarity": "cosine"
      },
      {
        "type": "filter",
        "path": "published_time"
      },
      {
        "type": "filter", 
        "path": "title"
      }
    ]
  }
);

print("向量索引创建完成！");
print("索引名称: vector_search_index");
print("向量维度: 1536 (OpenAI embedding)");
print("相似性算法: cosine");
print("支持过滤字段: published_time, title");