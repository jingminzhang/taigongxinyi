# 炼妖壶Claude Code Action配置指南

## ✅ 已完成
- [x] 创建了 `.github/workflows/claude.yml`
- [x] 配置了炼妖壶专用的系统提示
- [x] 支持多种触发词：`@claude`、`@太公`、`@八仙`

## 🔧 需要完成的配置

### 1. 设置GitHub Secrets

在你的GitHub仓库中添加API密钥：

#### 方法A: 使用Anthropic API Key (推荐)
1. 访问：https://github.com/your-username/cauldron/settings/secrets/actions
2. 点击 "New repository secret"
3. 添加：
   - **Name**: `ANTHROPIC_API_KEY`
   - **Value**: 你的Anthropic API密钥

#### 方法B: 使用Claude Code OAuth Token (Pro/Max用户)
如果你有Claude Pro或Max账户：
```bash
# 在本地运行
claude setup-token
```
然后添加secret：
- **Name**: `CLAUDE_CODE_OAUTH_TOKEN`
- **Value**: 生成的OAuth token

### 2. 安装Claude GitHub App (如果还没安装)

1. 访问：https://github.com/apps/claude
2. 点击 "Install" 
3. 选择你的仓库或组织
4. 授权必要的权限

### 3. 测试配置

配置完成后，在任何Issue或PR中评论：

```
@claude 你好！请介绍一下炼妖壶项目的架构
```

或者：

```
@太公 请分析一下当前的心易系统设计
```

或者：

```
@八仙 帮我优化一下辩论系统的逻辑
```

## 🎯 使用场景

### 代码审查
在PR中评论：
```
@claude 请审查这个MCP管理器的实现，关注安全性和性能
```

### 功能实现
在Issue中评论：
```
@claude 帮我实现一个新的Yahoo Finance数据获取功能
```

### 架构讨论
```
@太公 如何优化当前的金融数据分析流程？
```

### 调试帮助
```
@claude 这个错误是什么原因：[粘贴错误信息]
```

## 🔍 高级配置

### 自定义触发词
如果你想添加更多触发词，编辑 `.github/workflows/claude.yml` 中的条件：

```yaml
if: contains(github.event.comment.body, '@claude') || 
    contains(github.event.comment.body, '@太公') || 
    contains(github.event.comment.body, '@八仙') ||
    contains(github.event.comment.body, '@炼妖')
```

### 模型配置
可以在workflow中调整：
- `model`: 选择不同的Claude模型
- `max-tokens`: 调整响应长度
- `system-prompt`: 自定义AI行为

## 🚨 注意事项

1. **API费用**: Claude Code Action会消耗你的Anthropic API配额
2. **权限**: 确保GitHub App有足够的权限操作仓库
3. **安全**: 不要在公开评论中包含敏感信息
4. **频率**: 避免过于频繁的调用

## 🎉 完成后的效果

配置成功后，你将拥有：
- 🤖 **智能代码助手**: 直接在GitHub中获得AI帮助
- 🔍 **自动代码审查**: PR中的智能建议
- 💡 **架构指导**: 针对炼妖壶项目的专业建议
- 🚀 **开发加速**: 减少查找文档和调试时间

---

配置完成后，在这个Issue中评论 `@claude 测试` 来验证是否工作正常！