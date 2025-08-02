const items = $input.all();
const results = [];

// 如果没有数据需要插入
if (items.length === 0 || (items.length === 1 && items[0].json.status === 'no_new_data')) {
    console.log('没有新数据需要插入');
    return items;
}

console.log(`准备插入 ${items.length} 条新文章`);

// 准备批量插入的数据
const documentsToInsert = items.map(item => item.json);

try {
    // 批量插入，因为已经确保了唯一性，所以直接插入
    const result = await mongoClient.db('taigong').collection('articles').insertMany(
        documentsToInsert,
        { ordered: false } // 即使某条失败也继续插入其他的
    );
    
    console.log(`✅ 成功插入 ${result.insertedCount} 条文章`);
    
    // 返回插入结果
    for (let i = 0; i < documentsToInsert.length; i++) {
        const doc = documentsToInsert[i];
        const insertedId = result.insertedIds[i];
        
        results.push({
            json: {
                action: 'inserted',
                sequence_id: doc.sequence_id,
                article_id: doc.article_id,
                title: doc.title,
                mongodb_id: insertedId,
                status: 'success'
            }
        });
    }
    
} catch (error) {
    console.error('❌ 批量插入失败:', error.message);
    
    // 如果批量插入失败，尝试逐条插入
    console.log('尝试逐条插入...');
    
    for (const doc of documentsToInsert) {
        try {
            const result = await mongoClient.db('taigong').collection('articles').insertOne(doc);
            
            console.log(`✅ 单条插入成功: ${doc.article_id}`);
            results.push({
                json: {
                    action: 'inserted',
                    sequence_id: doc.sequence_id,
                    article_id: doc.article_id,
                    title: doc.title,
                    mongodb_id: result.insertedId,
                    status: 'success'
                }
            });
            
        } catch (singleError) {
            console.error(`❌ 单条插入失败 ${doc.article_id}:`, singleError.message);
            results.push({
                json: {
                    action: 'error',
                    sequence_id: doc.sequence_id,
                    article_id: doc.article_id,
                    title: doc.title,
                    error: singleError.message,
                    status: 'failed'
                }
            });
        }
    }
}

// 统计结果
const successCount = results.filter(r => r.json.status === 'success').length;
const failCount = results.filter(r => r.json.status === 'failed').length;

console.log(`插入完成: 成功 ${successCount} 条, 失败 ${failCount} 条`);

return results;