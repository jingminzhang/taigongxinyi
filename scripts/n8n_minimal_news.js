const items = $input.all();

console.log(`原始数据: ${items.length} 条`);

// 本批次内去重
const seenTitles = new Set();
const uniqueItems = [];

// 生成起始ID（基于时间戳，确保每次运行都不同）
let nextId = Math.floor(Date.now() / 1000);

for (const item of items) {
    const data = item.json;

    // 跳过无效数据
    if (!data.title) continue;

    // 本批次内去重
    if (seenTitles.has(data.title)) {
        console.log('⏭️  本批次重复，跳过:', data.title);
        continue;
    }

    const newsItem = {
        id: nextId,
        title: data.title,
        published_time: data.isoDate || data.pubDate || new Date().toISOString(),
        source_url: data.link || ''
    };

    uniqueItems.push({ json: newsItem });
    seenTitles.add(data.title);

    console.log(`✅ ID ${nextId}: ${data.title}`);
    nextId++;
}

console.log(`本批次去重后: ${uniqueItems.length} 条`);
return uniqueItems;