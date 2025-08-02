const items = $input.all();
const processedItems = [];

// 改进的哈希函数 - 基于内容生成稳定的ID
function generateStableId(title, pubDate, content) {
    const normalizedTitle = title.trim().toLowerCase();
    const contentHash = content ? content.substring(0, 100) : '';
    const dateStr = pubDate || '';
    
    const combined = normalizedTitle + '|' + dateStr + '|' + contentHash;
    
    let hash = 0;
    for (let i = 0; i < combined.length; i++) {
        const char = combined.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash).toString(16);
}

// 1. 从数据库查询已存在的文章ID和标题
const existingArticles = new Set();
try {
    const existing = await mongoClient.db('taigong').collection('articles')
        .find({}, { projection: { article_id: 1, title: 1, content_hash: 1 } })
        .toArray();
    
    existing.forEach(article => {
        existingArticles.add(article.article_id);
        // 同时用标题做备用检查
        existingArticles.add(article.title);
    });
    
    console.log(`数据库中已有 ${existing.length} 篇文章`);
} catch (error) {
    console.log('查询现有文章失败:', error);
}

// 2. 处理新数据
for (const item of items) {
    const data = item.json;
    
    // 跳过无效数据
    if (!data.title) continue;
    
    // 生成稳定的文章ID
    const stableId = generateStableId(
        data.title, 
        data.isoDate || data.pubDate,
        data['content:encodedSnippet'] || data.contentSnippet || ''
    );
    
    // 检查是否已存在（用ID和标题双重检查）
    if (existingArticles.has(stableId) || existingArticles.has(data.title)) {
        console.log('跳过重复文章:', data.title);
        continue;
    }
    
    // 生成内容哈希用于后续去重检查
    const contentHash = generateStableId(
        data['content:encodedSnippet'] || data.contentSnippet || '', 
        '', 
        ''
    );
    
    const processedItem = {
        article_id: stableId,  // 使用稳定ID
        title: data.title,
        content: data['content:encodedSnippet'] || data.contentSnippet || '',
        content_hash: contentHash,  // 新增：内容哈希
        published_time: data.isoDate || data.pubDate || new Date().toISOString(),
        source_url: data.link || '',  // 新增：源链接
        processed: false,
        created_at: new Date().toISOString(),
        last_updated: new Date().toISOString()  // 新增：更新时间
    };
    
    processedItems.push({ json: processedItem });
    // 添加到已存在集合，避免本次执行内重复
    existingArticles.add(stableId);
    existingArticles.add(data.title);
}

console.log(`处理完成: 原始${items.length}条, 去重后${processedItems.length}条`);
return processedItems;