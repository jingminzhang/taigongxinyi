const items = $input.all();
const results = [];

// 通用MongoDB连接获取函数
function getMongoConnection() {
    // 尝试不同的MongoDB连接变量名
    if (typeof mongoClient !== 'undefined') return mongoClient;
    if (typeof mongo !== 'undefined') return mongo;
    if (typeof db !== 'undefined') return db;
    if (typeof $mongo !== 'undefined') return $mongo;
    if (typeof client !== 'undefined') return client;
    
    throw new Error('找不到MongoDB连接对象，请检查n8n MongoDB节点配置');
}

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

// 获取MongoDB连接
let mongoConnection;
try {
    mongoConnection = getMongoConnection();
    console.log('✅ MongoDB连接获取成功');
} catch (error) {
    console.error('❌ MongoDB连接失败:', error.message);
    return [{
        json: {
            error: 'MongoDB连接失败',
            message: error.message,
            status: 'connection_failed'
        }
    }];
}

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
    
    // 本次执行内去重检查
    if (processedInThisRun.has(data.title)) {
        console.log('⏭️  本次执行内重复，跳过:', data.title);
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
        rss_source: data.meta?.title || 'unknown',
        processed: false,
        created_at: new Date().toISOString(),
        last_updated: new Date().toISOString()
    };
    
    try {
        // 检查数据库中是否已存在
        const existing = await mongoConnection.db('taigong').collection('articles').findOne({
            $or: [
                { article_id: stableId },
                { title: data.title }
            ]
        });
        
        if (existing) {
            console.log('⏭️  数据库中已存在，跳过:', data.title);
            continue;
        }
        
        // 插入新文章
        const result = await mongoConnection.db('taigong').collection('articles').insertOne(articleData);
        
        console.log('✅ 新增文章:', data.title);
        results.push({
            json: {
                action: 'inserted',
                article_id: stableId,
                title: data.title,
                mongodb_id: result.insertedId,
                status: 'success'
            }
        });
        
        // 添加到本次执行的去重集合
        processedInThisRun.add(data.title);
        
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