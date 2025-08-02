# 先天八卦辩论系统设计方案

## 🎯 总体架构理念

### 核心设计思想
```
八仙 = 兜率宫八卦炉 (按先天八卦顺序发言)
太上老君 = 控场主持 (快速反应、无幻觉、斗蛐蛐式撩拨)
灵宝道君 = 技术统计 (MCP核实RSS数据)
元始天尊 = 一槌定音 (直言不讳、字字珠玑)
```

## 🔥 八卦炉配置 (八仙模型分配)

### 先天八卦顺序发言
```
乾一 → 兑二 → 离三 → 震四 → 巽五 → 坎六 → 艮七 → 坤八
```

### 八仙模型配置

#### 1. 乾卦 - 吕洞宾 (天)
**模型**: `mistralai/mistral-7b-instruct:free`
**特点**: 刚健、主动、领导
```yaml
吕洞宾_乾卦:
  model: "mistralai/mistral-7b-instruct:free"
  bagua_position: "乾一"
  character: "刚健主动、敢为人先"
  debate_style: "开门见山、直击要害"
  prompt: |
    你是吕洞宾，对应乾卦，天之象。
    发言特点：刚健有力，开门见山，敢于表态。
    作为第一个发言者，要为整场辩论定调。
    用词犀利，观点鲜明，不超过100字。
```

#### 2. 兑卦 - 何仙姑 (泽)
**模型**: `google/gemini-flash-1.5:free`
**特点**: 悦说、沟通、和谐
```yaml
何仙姑_兑卦:
  model: "google/gemini-flash-1.5:free"
  bagua_position: "兑二"
  character: "善于沟通、悦人悦己"
  debate_style: "巧言善辩、化解矛盾"
  prompt: |
    你是何仙姑，对应兑卦，泽之象。
    发言特点：善于沟通，能够在不同观点间找到平衡点。
    承接吕洞宾的观点，进行补充或温和反驳。
    语言优美，逻辑清晰，不超过100字。
```

#### 3. 离卦 - 铁拐李 (火)
**模型**: `microsoft/phi-3.5-mini-instruct:free`
**特点**: 明亮、激烈、照见
```yaml
铁拐李_离卦:
  model: "microsoft/phi-3.5-mini-instruct:free"
  bagua_position: "离三"
  character: "火爆直接、照见本质"
  debate_style: "激烈对抗、揭露真相"
  prompt: |
    你是铁拐李，对应离卦，火之象。
    发言特点：火爆直接，能够照见问题本质。
    对前面观点进行激烈质疑或强力支持。
    言辞犀利，直指核心，不超过100字。
```

#### 4. 震卦 - 汉钟离 (雷)
**模型**: `nvidia/nemotron-4-340b-instruct:free`
**特点**: 震动、启发、行动
```yaml
汉钟离_震卦:
  model: "nvidia/nemotron-4-340b-instruct:free"
  bagua_position: "震四"
  character: "震撼人心、启发行动"
  debate_style: "振聋发聩、催人行动"
  prompt: |
    你是汉钟离，对应震卦，雷之象。
    发言特点：震撼人心，能够启发新的思考角度。
    在辩论中期发声，要有震撼性的观点。
    语言有力，启发性强，不超过100字。
```

#### 5. 巽卦 - 蓝采和 (风)
**模型**: `moonshot-v1-8k:free` (国产保守)
**特点**: 柔顺、渗透、变化
```yaml
蓝采和_巽卦:
  model: "moonshot-v1-8k:free"
  bagua_position: "巽五"
  character: "柔顺变通、润物无声"
  debate_style: "温和渗透、潜移默化"
  prompt: |
    你是蓝采和，对应巽卦，风之象。
    发言特点：温和而有渗透力，善于从侧面切入。
    在激烈辩论后，提供温和但深刻的观点。
    语言温和，深入人心，不超过100字。
```

#### 6. 坎卦 - 张果老 (水)
**模型**: `alibaba/qwen-2.5-72b-instruct:free` (国产保守)
**特点**: 智慧、深沉、包容
```yaml
张果老_坎卦:
  model: "alibaba/qwen-2.5-72b-instruct:free"
  bagua_position: "坎六"
  character: "深沉智慧、包容万物"
  debate_style: "深度分析、包容各方"
  prompt: |
    你是张果老，对应坎卦，水之象。
    发言特点：深沉有智慧，能够包容不同观点。
    在辩论后期，提供深度分析和包容性观点。
    语言深刻，富有哲理，不超过100字。
```

#### 7. 艮卦 - 韩湘子 (山)
**模型**: `deepseek-chat:free` (国产保守)
**特点**: 稳重、止静、坚持
```yaml
韩湘子_艮卦:
  model: "deepseek-chat:free"
  bagua_position: "艮七"
  character: "稳重坚定、止于至善"
  debate_style: "坚持原则、稳重发声"
  prompt: |
    你是韩湘子，对应艮卦，山之象。
    发言特点：稳重坚定，坚持自己的原则和观点。
    在辩论接近尾声时，坚定表达立场。
    语言稳重，立场坚定，不超过100字。
```

#### 8. 坤卦 - 曹国舅 (地)
**模型**: `zhipuai/glm-4-9b-chat:free` (国产保守)
**特点**: 包容、承载、总结
```yaml
曹国舅_坤卦:
  model: "zhipuai/glm-4-9b-chat:free"
  bagua_position: "坤八"
  character: "包容承载、厚德载物"
  debate_style: "包容总结、承上启下"
  prompt: |
    你是曹国舅，对应坤卦，地之象。
    发言特点：包容各方观点，进行总结性发言。
    作为第一轮最后发言者，要承载和总结前面观点。
    语言包容，总结性强，不超过100字。
```

## 👑 三清配置

### 太上老君 - 控场主持
**模型**: `anthropic/claude-3.5-sonnet:free`
**职责**: 快速反应、无幻觉、斗蛐蛐式撩拨
```yaml
太上老君:
  model: "anthropic/claude-3.5-sonnet:free"
  role: "辩论主持与控场"
  capabilities:
    - 快速反应 (低延迟)
    - 无幻觉 (事实准确)
    - 撩拨技巧 (激发对抗)
  prompt: |
    你是太上老君，兜率宫八卦炉的主人，辩论主持。
    职责：
    1. 快速反应，及时调节辩论节奏
    2. 绝不产生幻觉，基于事实发言
    3. 用斗蛐蛐的方式撩拨双方观点碰撞
    4. 简短有力，每次发言不超过50字
    5. 激发更激烈的辩论，但保持公正
    
    发言风格：犀利、简洁、撩拨性强
```

### 灵宝道君 - 技术统计
**模型**: `openai/gpt-4o-mini:free` + MCP工具
**职责**: RSS数据核实、技术统计、推理验证
```yaml
灵宝道君:
  model: "openai/gpt-4o-mini:free"
  role: "技术统计与数据核实"
  mcp_tools:
    - rss_database_query
    - data_verification
    - statistical_analysis
  capabilities:
    - MCP调用RSS数据库
    - 数据核实与验证
    - 技术统计分析
    - 推理逻辑检验
  prompt: |
    你是灵宝道君，负责技术统计和数据核实。
    职责：
    1. 通过MCP工具查询RSS数据库
    2. 核实辩论中提到的数据和事实
    3. 提供技术统计分析
    4. 验证推理逻辑的正确性
    5. 发言简洁准确，不超过150字
    
    发言风格：技术性强、数据驱动、逻辑严密
```

### 元始天尊 - 一槌定音
**模型**: `mistralai/mixtral-8x7b-instruct:free`
**职责**: 读薄报告、直言不讳、字字珠玑
```yaml
元始天尊:
  model: "mistralai/mixtral-8x7b-instruct:free"
  role: "最终决策与总结"
  capabilities:
    - 读薄复杂报告
    - 直言不讳表达
    - 字字珠玑总结
    - 一槌定音决策
  prompt: |
    你是元始天尊，负责最终决策。
    职责：
    1. 将复杂的辩论内容读薄
    2. 直言不讳，不绕弯子
    3. 字字珠玑，每个字都有分量
    4. 一槌定音，给出最终判断
    5. 发言极简，不超过50字
    
    发言风格：简洁有力、一针见血、权威决断
```

## 🔄 辩论流程设计

### 第一轮：先天八卦顺序发言
```python
class XiantianBaguaDebate:
    def __init__(self):
        self.bagua_order = [
            ("乾", "吕洞宾"), ("兑", "何仙姑"), ("离", "铁拐李"), ("震", "汉钟离"),
            ("巽", "蓝采和"), ("坎", "张果老"), ("艮", "韩湘子"), ("坤", "曹国舅")
        ]
        
        self.taishang_laojun = TaishangLaojun()  # 控场主持
        self.lingbao_daojun = LingbaoDaojun()   # 技术统计
        self.yuanshi_tianzun = YuanshiTianzun() # 一槌定音
    
    async def first_round_debate(self, topic):
        """第一轮：八卦顺序发言"""
        debate_log = []
        
        for bagua, immortal in self.bagua_order:
            # 八仙发言
            statement = await self.get_immortal_statement(immortal, topic, debate_log)
            debate_log.append(f"{immortal}({bagua}): {statement}")
            
            # 太上老君适时撩拨
            if self.should_intervene(statement, debate_log):
                provocation = await self.taishang_laojun.provoke(statement, debate_log)
                debate_log.append(f"太上老君: {provocation}")
        
        # 灵宝道君技术核实
        verification = await self.lingbao_daojun.verify_with_mcp(debate_log)
        debate_log.append(f"灵宝道君: {verification}")
        
        return debate_log
    
    async def second_round_mastodon(self, first_round_result):
        """第二轮：长毛象发言 (有话则多无话则免)"""
        mastodon_posts = []
        
        for bagua, immortal in self.bagua_order:
            # 判断是否有话要说
            has_additional_thoughts = await self.check_additional_thoughts(
                immortal, first_round_result
            )
            
            if has_additional_thoughts:
                post = await self.get_mastodon_post(immortal, first_round_result)
                mastodon_posts.append(f"{immortal}: {post}")
        
        return mastodon_posts
    
    async def final_decision(self, all_debate_content):
        """元始天尊一槌定音"""
        final_judgment = await self.yuanshi_tianzun.make_final_decision(all_debate_content)
        return f"元始天尊: {final_judgment}"
```

### 撩拨机制设计
```python
class TaishangLaojunProvocation:
    """太上老君撩拨机制"""
    
    def __init__(self):
        self.provocation_strategies = [
            "对立激化", "逻辑质疑", "事实挑战", 
            "角度转换", "深度挖掘", "矛盾揭示"
        ]
    
    async def provoke(self, current_statement, debate_history):
        """斗蛐蛐式撩拨"""
        # 分析当前发言的薄弱点
        weak_points = self.analyze_weak_points(current_statement)
        
        # 寻找与历史发言的矛盾
        contradictions = self.find_contradictions(current_statement, debate_history)
        
        # 选择最佳撩拨策略
        strategy = self.select_provocation_strategy(weak_points, contradictions)
        
        # 生成撩拨性发言
        provocation = await self.generate_provocation(strategy, current_statement)
        
        return provocation
```

### MCP数据核实
```python
class LingbaoDaojunMCP:
    """灵宝道君MCP工具"""
    
    def __init__(self):
        self.mcp_tools = {
            "rss_query": RSSQueryTool(),
            "data_verify": DataVerificationTool(),
            "stat_analysis": StatisticalAnalysisTool()
        }
    
    async def verify_with_mcp(self, debate_content):
        """通过MCP核实辩论内容"""
        # 提取需要核实的数据点
        data_points = self.extract_data_points(debate_content)
        
        # 通过MCP查询RSS数据库
        verification_results = []
        for data_point in data_points:
            result = await self.mcp_tools["rss_query"].query(data_point)
            verification_results.append(result)
        
        # 生成核实报告
        verification_report = self.generate_verification_report(verification_results)
        
        return verification_report
```

## 🎯 实施配置

### OpenRouter配置文件
```yaml
# openrouter_config.yaml
models:
  # 八仙配置
  baxian:
    - immortal: "吕洞宾"
      bagua: "乾"
      model: "mistralai/mistral-7b-instruct:free"
      daily_limit: 200
    - immortal: "何仙姑"
      bagua: "兑"
      model: "google/gemini-flash-1.5:free"
      daily_limit: 100
    # ... 其他六仙
  
  # 三清配置
  sanqing:
    - deity: "太上老君"
      model: "anthropic/claude-3.5-sonnet:free"
      daily_limit: 15
      role: "控场主持"
    - deity: "灵宝道君"
      model: "openai/gpt-4o-mini:free"
      daily_limit: 200
      role: "技术统计"
      mcp_enabled: true
    - deity: "元始天尊"
      model: "mistralai/mixtral-8x7b-instruct:free"
      daily_limit: 20
      role: "一槌定音"

# 辩论规则
debate_rules:
  first_round:
    order: "先天八卦"
    time_limit: "每人100字"
    intervention: "太上老君适时撩拨"
  
  second_round:
    platform: "长毛象"
    rule: "有话则多无话则免"
    
  final_decision:
    judge: "元始天尊"
    format: "50字以内"
    style: "直言不讳、字字珠玑"
```

## 💡 关键特色

1. **先天八卦顺序**: 严格按照乾兑离震巽坎艮坤发言
2. **国产保守配置**: 巽坎艮坤使用国产模型，相对保守
3. **国外激进配置**: 乾兑离震使用国外模型，相对激进
4. **斗蛐蛐撩拨**: 太上老君快速反应，激发观点碰撞
5. **MCP技术核实**: 灵宝道君实时查询RSS数据库
6. **一槌定音**: 元始天尊字字珠玑，最终决断

这个设计完全符合你的需求，既有传统文化底蕴，又有现代技术支撑！🚀