const items = $input.all();
const processedItems = [];

// 获取当前最大流水号
async function getCurrentMaxId() {
    try {
        const result = await mongoClient.db('taigong').collection('articles')
            .findOne({}, { 
                sort: { sequence_id: -1 }, 
                projection: { sequence_id: 1 } 
            });
        
        return result ? result.sequence_id : 0;
    } catch (error) {
        console.log('获取最大流水号失败，从1开始:', error.message);
        return 0;
    }
}

// 获取已存在的文章标题集合（用于去重检查）
async function getExistingTitles() {
    try {
        const existing = await mongoClient.db('taigong').collection('articles')
            .find({}, { projection: { title: 1 } })
            .toArray();
        
        return new Set(existing.map(doc => doc.title));
    } catch (error) {
        console.log('获取已存在标题失败:', error.message);
        return new Set();
    }
}

// 生成内容哈希（用于内容变化检测）
function generateContentHash(content) {
    if (!content) return '';
    
    let hash = 0;
    const str = content.substring(0, 200); // 取前200字符
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash).toString(16);
}

console.log(`开始处理 ${items.length} 条RSS数据`);

// 1. 获取当前最大流水号
const currentMaxId = await getCurrentMaxId();
console.log(`当前数据库最大流水号: ${currentMaxId}`);

// 2. 获取已存在的文章标题
const existingTitles = await getExistingTitles();
console.log(`数据库中已有 ${existingTitles.size} 篇文章`);

// 3. 处理新数据，分配流水号
let nextSequenceId = currentMaxId + 1;
const seenTitlesInBatch = new Set(); // 本批次内去重

for (const item of items) {
    const data = item.json;
    
    // 跳过无效数据
    if (!data.title) {
        console.log('跳过无标题数据');
        continue;
    }
    
    // 检查是否已存在（数据库 + 本批次）
    if (existingTitles.has(data.title) || seenTitlesInBatch.has(data.title)) {
        console.log('⏭️  跳过重复文章:', data.title);
        continue;
    }
    
    // 分配新的流水号
    const sequenceId = nextSequenceId++;
    
    // 生成文章数据
    const articleData = {
        sequence_id: sequenceId,  // 主键：流水号
        article_id: `NEWS_${sequenceId.toString().padStart(8, '0')}`, // 格式化ID：NEWS_00000001
        title: data.title,
        content: data['content:encodedSnippet'] || data.contentSnippet || '',
        content_hash: generateContentHash(data['content:encodedSnippet'] || data.contentSnippet || ''),
        published_time: data.isoDate || data.pubDate || new Date().toISOString(),
        source_url: data.link || '',
        rss_source: data.meta?.title || 'unknown', // RSS源名称
        processed: false,
        created_at: new Date().toISOString(),
        batch_id: Date.now().toString() // 批次ID，用于追踪
    };
    
    processedItems.push({ json: articleData });
    seenTitlesInBatch.add(data.title);
    
    console.log(`✅ 分配流水号 ${sequenceId}: ${data.title}`);
}

console.log(`流水号分配完成:`);
console.log(`  原始数据: ${items.length} 条`);
console.log(`  跳过重复: ${items.length - processedItems.length} 条`);
console.log(`  新增数据: ${processedItems.length} 条`);
console.log(`  流水号范围: ${currentMaxId + 1} - ${nextSequenceId - 1}`);

// 如果没有新数据，返回空结果
if (processedItems.length === 0) {
    return [{
        json: {
            message: '没有新数据需要处理',
            current_max_id: currentMaxId,
            total_articles_in_db: existingTitles.size,
            status: 'no_new_data'
        }
    }];
}

return processedItems;