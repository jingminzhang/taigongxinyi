# n8n MongoDB去重配置

## 方案1: JS函数 + MongoDB Upsert

### JS函数节点配置
使用 `scripts/n8n_minimal_news.js` 的代码，只做基本处理和本批次去重。

### MongoDB节点配置
1. **操作类型**: Update
2. **Collection**: articles  
3. **Update Key**: title (用标题作为唯一键)
4. **Upsert**: 启用 ✅
5. **Update Document**:
```json
{
  "$setOnInsert": {
    "id": "={{$json.id}}",
    "title": "={{$json.title}}",
    "published_time": "={{$json.published_time}}",
    "source_url": "={{$json.source_url}}",
    "created_at": "={{new Date().toISOString()}}"
  },
  "$set": {
    "last_seen": "={{new Date().toISOString()}}"
  }
}
```

## 方案2: 纯MongoDB节点去重

### MongoDB节点配置
1. **操作类型**: Update Many
2. **Collection**: articles
3. **Filter**: `{"title": "={{$json.title}}"}`
4. **Upsert**: 启用 ✅
5. **Update**:
```json
{
  "$setOnInsert": {
    "title": "={{$json.title}}",
    "published_time": "={{$json.published_time}}",
    "source_url": "={{$json.source_url}}",
    "created_at": "={{new Date().toISOString()}}"
  }
}
```

## 推荐方案

使用**方案1**，因为：
- JS函数生成连续的ID
- MongoDB只负责去重插入
- 逻辑清晰，易于调试

## 测试步骤

1. 第一次运行：应该插入所有新文章
2. 第二次运行：应该0条插入（全部跳过）
3. 检查数据库：确认没有重复标题