# Doppler密钥管理迁移指南

## 🎯 为什么用Doppler管理Claude Actions

### **当前状态**
你有GitHub学生套餐 + Doppler Team Plan (到明年7月)，这是完美的组合！

### **优势**
- 🔐 **统一密钥管理**：所有API密钥在一个地方
- 🌍 **多环境支持**：开发/测试/生产环境隔离
- 📊 **安全审计**：密钥访问日志
- 🔄 **自动同步**：密钥更新自动推送到所有环境

## 🔧 迁移步骤

### **1. 在Doppler中组织密钥**

#### **项目结构建议**
```
doppler://cauldron/
├── development/
│   ├── ANTHROPIC_AUTH_TOKEN
│   ├── ANTHROPIC_BASE_URL  
│   ├── OPENROUTER_API_KEY_1
│   └── DATABASE_URL (开发库)
├── staging/
│   ├── ANTHROPIC_AUTH_TOKEN
│   ├── ANTHROPIC_BASE_URL
│   └── DATABASE_URL (测试库)
└── production/
    ├── ANTHROPIC_AUTH_TOKEN
    ├── ANTHROPIC_BASE_URL
    └── DATABASE_URL (生产库)
```

### **2. GitHub Actions配置**

#### **环境变量设置**
```yaml
# 在GitHub Secrets中只需要这几个Doppler配置
DOPPLER_TOKEN: dp.st.xxxx (你的Doppler服务令牌)
DOPPLER_PROJECT: cauldron
DOPPLER_CONFIG: production  # 或 development/staging
```

#### **Workflow中的使用**
```yaml
- name: Load from Doppler
  run: doppler secrets download --no-file --format env >> $GITHUB_ENV
  env:
    DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
```

### **3. 本地开发配置**

#### **安装Doppler CLI**
```bash
# macOS
brew install dopplerhq/cli/doppler

# 登录
doppler login

# 设置项目
doppler setup --project cauldron --config development
```

#### **本地使用**
```bash
# 运行应用时自动加载密钥
doppler run -- python app.py

# 或者导出到.env文件
doppler secrets download --no-file --format env > .env
```

## 🚀 高级功能

### **1. 密钥轮换**
```bash
# 更新API密钥
doppler secrets set ANTHROPIC_AUTH_TOKEN=new-token

# 自动同步到所有环境
```

### **2. 团队协作**
```bash
# 邀请团队成员
doppler team invite user@example.com

# 设置权限
doppler team update user@example.com --role developer
```

### **3. 审计日志**
- 📊 **访问记录**：谁在什么时候访问了哪个密钥
- 🔄 **变更历史**：密钥的修改历史
- 🚨 **异常告警**：异常访问模式检测

## 💰 成本优化

### **学生套餐期间 (到明年7月)**
- ✅ **免费使用所有功能**
- ✅ **团队协作功能**
- ✅ **无限密钥存储**

### **毕业后的选择**
1. **个人版** ($5/月)：个人项目足够
2. **开源项目**：申请免费额度
3. **迁移到其他方案**：GitHub Secrets + 自建方案

## 🎯 推荐配置

### **当前阶段**
```yaml
环境配置:
  - development: 本地开发
  - staging: GitHub Actions测试
  - production: 生产部署

密钥分类:
  - AI服务: ANTHROPIC_*, OPENROUTER_*
  - 数据库: DATABASE_URL, ZILLIZ_*
  - 社交媒体: MASTODON_*
  - 监控: DOPPLER_*
```

### **最佳实践**
- 🔐 **最小权限原则**：每个环境只访问必要的密钥
- 🔄 **定期轮换**：重要密钥定期更新
- 📊 **监控使用**：定期检查访问日志
- 🚨 **异常告警**：设置异常访问告警

---

**总结：充分利用你的学生福利，用Doppler构建企业级的密钥管理体系！** 🎓✨