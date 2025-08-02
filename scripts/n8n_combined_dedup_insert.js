const items = $input.all();
const results = [];

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

console.log(`开始处理 ${items.length} 条RSS数据`);

// 用于本次执行内去重
const processedInThisRun = new Set();

// 处理每个RSS项目
for (const item of items) {
    const data = item.json;
    
    // 跳过无效数据
    if (!data.title) {
        console.log('跳过无标题数据');
        continue;
    }
    
    // 生成稳定的文章ID
    const stableId = generateStableId(
        data.title, 
        data.isoDate || data.pubDate,
        data['content:encodedSnippet'] || data.contentSnippet || ''
    );
    
    // 生成内容哈希
    const contentHash = generateStableId(
        data['content:encodedSnippet'] || data.contentSnippet || '', 
        '', 
        ''
    );
    
    // 准备文章数据
    const articleData = {
        article_id: stableId,
        title: data.title,
        content: data['content:encodedSnippet'] || data.contentSnippet || '',
        content_hash: contentHash,
        published_time: data.isoDate || data.pubDate || new Date().toISOString(),
        source_url: data.link || '',
        processed: false,
        created_at: new Date().toISOString(),
        last_updated: new Date().toISOString()
    };
    
    try {
        // 使用upsert操作，避免重复插入
        const result = await mongoClient.db('taigong').collection('articles').updateOne(
            { 
                $or: [
                    { article_id: stableId },
                    { title: data.title }
                ]
            },
            {
                $setOnInsert: {
                    article_id: stableId,
                    title: data.title,
                    content: articleData.content,
                    content_hash: contentHash,
                    published_time: articleData.published_time,
                    source_url: articleData.source_url,
                    processed: false,
                    created_at: articleData.created_at
                },
                $set: {
                    last_updated: new Date().toISOString()
                }
            },
            { upsert: true }
        );
        
        if (result.upsertedCount > 0) {
            console.log('✅ 新增文章:', data.title);
            results.push({
                json: {
                    action: 'inserted',
                    article_id: stableId,
                    title: data.title,
                    status: 'success'
                }
            });
        } else if (result.modifiedCount > 0) {
            console.log('🔄 更新文章:', data.title);
            results.push({
                json: {
                    action: 'updated',
                    article_id: stableId,
                    title: data.title,
                    status: 'success'
                }
            });
        } else {
            console.log('⏭️  文章已存在，跳过:', data.title);
        }
        
    } catch (error) {
        console.error('❌ 处理文章失败:', data.title, error.message);
        results.push({
            json: {
                action: 'error',
                title: data.title,
                error: error.message,
                status: 'failed'
            }
        });
    }
}

console.log(`处理完成: 原始${items.length}条, 成功处理${results.length}条`);

// 统计结果
const stats = results.reduce((acc, item) => {
    acc[item.json.action] = (acc[item.json.action] || 0) + 1;
    return acc;
}, {});

console.log('处理统计:', stats);

// 如果没有任何结果，返回一个空的成功状态
if (results.length === 0) {
    return [{
        json: {
            message: '没有新数据需要处理',
            total_processed: items.length,
            status: 'completed'
        }
    }];
}

return results;