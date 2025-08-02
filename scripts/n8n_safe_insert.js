// n8n MongoDB插入节点代码
const items = $input.all();
const results = [];

for (const item of items) {
    const data = item.json;
    
    try {
        // 使用upsert操作，避免重复插入
        const result = await mongoClient.db('taigong').collection('articles').updateOne(
            { 
                $or: [
                    { article_id: data.article_id },
                    { title: data.title }
                ]
            },
            {
                $setOnInsert: {
                    article_id: data.article_id,
                    title: data.title,
                    content: data.content,
                    content_hash: data.content_hash,
                    published_time: data.published_time,
                    source_url: data.source_url,
                    processed: data.processed,
                    created_at: data.created_at
                },
                $set: {
                    last_updated: new Date().toISOString()
                }
            },
            { upsert: true }
        );
        
        if (result.upsertedCount > 0) {
            console.log('新增文章:', data.title);
            results.push({
                json: {
                    action: 'inserted',
                    article_id: data.article_id,
                    title: data.title
                }
            });
        } else {
            console.log('文章已存在，跳过:', data.title);
        }
        
    } catch (error) {
        console.error('插入文章失败:', data.title, error);
    }
}

console.log(`成功处理 ${results.length} 篇新文章`);
return results;