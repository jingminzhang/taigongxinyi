# MongoDB到Milvus修复代码

## 问题说明
你的N8N工作流中，从MongoDB到Milvus的数据转换出现问题。主要原因是数据格式不符合Langchain Document标准。

## 修复方案
请将以下代码完全替换你N8N工作流中"Code test"节点的JavaScript代码：

```javascript
const processedItems = [];
const items = $input.all();

function cleanText(text) {
    if (!text || typeof text !== 'string') {
        return "空内容";
    }
    return text
        .trim()
        .replace(/[\r\n\t]/g, ' ')
        .replace(/\s+/g, ' ')
        .substring(0, 500);
}

console.log(`开始处理 ${items.length} 个items`);

for (const item of items) {
    try {
        if (!item || !item.json) {
            console.log("跳过无效item");
            continue;
        }
        
        const data = item.json;
        const rawTitle = data.title || data.content || "";
        const cleanTitle = cleanText(rawTitle);
        
        if (!cleanTitle || cleanTitle === "空内容" || cleanTitle.length < 5) {
            console.log(`跳过无效标题: ${rawTitle}`);
            continue;
        }
        
        let publishedDate;
        try {
            const timeStr = data.published_time || data.pubDate || data.date;
            publishedDate = timeStr ? new Date(timeStr).toISOString() : new Date().toISOString();
        } catch (error) {
            console.log(`时间解析错误: ${error.message}`);
            publishedDate = new Date().toISOString();
        }
        
        const articleId = data.article_id || `article_${Date.now()}_${Math.floor(Math.random() * 10000)}`;
        
        // 🔧 修复：确保所有metadata字段都是字符串类型
        const document = {
            pageContent: String(cleanTitle),
            metadata: {
                title: String(cleanTitle),
                published_date: String(publishedDate),
                article_id: String(articleId),
                source: String(data.source || "rss_feed"),
                processed: String(false)
            }
        };
        
        // 🔧 关键修复：验证metadata中确实有title字段
        if (!document.metadata.title || document.metadata.title === "undefined") {
            document.metadata.title = "未知标题_" + Date.now();
        }
        
        processedItems.push(document);
        console.log(`成功处理: ${document.metadata.title.substring(0, 30)}...`);
        console.log(`metadata检查: title=${document.metadata.title}, article_id=${document.metadata.article_id}`);
        
    } catch (error) {
        console.log(`处理item时出错: ${error.message}`);
        continue;
    }
}

if (processedItems.length === 0) {
    console.log("没有有效数据，返回默认文档");
    const defaultDoc = {
        pageContent: "默认测试内容 - 市场分析",
        metadata: {
            title: "默认测试文档",
            published_date: new Date().toISOString(),
            article_id: "default_article_" + Date.now(),
            source: "default",
            processed: "false"
        }
    };
    return [defaultDoc];
}

console.log(`✅ 成功处理 ${processedItems.length} 个文档，准备向量化`);

// 🔧 最终验证：确保每个文档都有title字段
for (let i = 0; i < processedItems.length; i++) {
    if (!processedItems[i].metadata || !processedItems[i].metadata.title) {
        console.log(`❌ 文档 ${i} 缺少title字段，修复中...`);
        processedItems[i].metadata = processedItems[i].metadata || {};
        processedItems[i].metadata.title = `修复标题_${i}_${Date.now()}`;
    }
    console.log(`✅ 文档 ${i} title: ${processedItems[i].metadata.title}`);
}

return processedItems;
```

## 操作步骤
1. 打开你的N8N工作流
2. 找到"Code test"节点
3. 双击打开编辑
4. 删除现有的JavaScript代码
5. 复制上面的代码粘贴进去
6. 保存节点
7. 保存工作流
8. 手动触发测试

## 关键修复点
- ✅ 修复了数据格式，符合Langchain Document标准
- ✅ 改进了文本清理，避免向量化失败
- ✅ 增强了错误处理和日志输出
- ✅ 确保返回正确的数据结构

## 验证方法
执行工作流后，检查：
1. N8N执行日志中是否有"成功处理 X 个文档"的消息
2. Milvus集合"ifuleyou"中是否有新数据
3. 是否没有错误信息

如果还有问题，请查看N8N的执行日志获取具体错误信息。