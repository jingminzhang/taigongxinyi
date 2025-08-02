const items = $input.all();

// 简单哈希函数
function simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash).toString(16);
}

console.log(`原始数据: ${items.length} 条`);

// 用标题去重
const seenTitles = new Set();
const uniqueItems = [];

for (const item of items) {
    const data = item.json;

    // 跳过无效数据
    if (!data.title) continue;

    // 本批次内去重
    if (seenTitles.has(data.title)) {
        console.log('跳过重复:', data.title);
        continue;
    }

    // 生成稳定ID
    const stableId = simpleHash(data.title + (data.isoDate || data.pubDate || ''));

    const processedItem = {
        article_id: stableId,
        title: data.title,
        content: data['content:encodedSnippet'] || data.contentSnippet || '',
        published_time: data.isoDate || data.pubDate || new Date().toISOString(),
        source_url: data.link || '',
        processed: false,
        created_at: new Date().toISOString()
    };

    uniqueItems.push({ json: processedItem });
    seenTitles.add(data.title);

    console.log(`✅ 处理: ${data.title}`);
}

console.log(`去重后: ${uniqueItems.length} 条`);
return uniqueItems;