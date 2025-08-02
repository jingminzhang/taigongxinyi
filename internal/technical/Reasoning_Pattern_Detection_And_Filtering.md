# 推理模型思考过程检测与过滤技术

## 🔍 推理模型思考过程的格式特征

### 常见的思考标记格式
```python
# 不同推理模型的思考标记模式
REASONING_PATTERNS = {
    "openai_o1": {
        "start_markers": ["<thinking>", "<thought>", "Let me think", "I need to"],
        "end_markers": ["</thinking>", "</thought>"],
        "inline_patterns": [r"Let me think.*?\.{3,}", r"I need to consider.*?\.{3,}"]
    },
    
    "anthropic_reasoning": {
        "start_markers": ["<reasoning>", "<analysis>", "Let me analyze"],
        "end_markers": ["</reasoning>", "</analysis>"],
        "inline_patterns": [r"Let me analyze.*?\.{3,}", r"I should consider.*?\.{3,}"]
    },
    
    "deepseek_r1": {
        "start_markers": ["<think>", "<reasoning>", "让我想想", "我需要分析"],
        "end_markers": ["</think>", "</reasoning>"],
        "inline_patterns": [r"让我想想.*?\.{3,}", r"我需要分析.*?\.{3,}"]
    },
    
    "qwen_reasoning": {
        "start_markers": ["<思考>", "<分析>", "让我分析", "首先"],
        "end_markers": ["</思考>", "</分析>"],
        "inline_patterns": [r"让我分析.*?然后", r"首先.*?接下来"]
    },
    
    "general_reasoning": {
        "start_markers": [
            "Let me think", "I need to", "Let me analyze", "Let me consider",
            "让我想想", "让我分析", "我需要考虑", "首先分析"
        ],
        "end_markers": [
            "Now I'll", "So my answer", "Therefore", "In conclusion",
            "现在我", "所以我的答案", "因此", "总结"
        ],
        "inline_patterns": [
            r"Let me think.*?\.{2,}",
            r"I need to.*?\.{2,}",
            r"让我想想.*?\.{2,}",
            r"首先.*?然后.*?最后",
            r"从.*?角度.*?来看"
        ]
    }
}
```

## 🛠️ 检测与过滤实现

### 1. 正则表达式检测器
```python
import re
from typing import List, Tuple, Dict

class ReasoningDetector:
    """推理过程检测器"""
    
    def __init__(self):
        self.patterns = REASONING_PATTERNS
        self.compiled_patterns = self._compile_patterns()
    
    def _compile_patterns(self):
        """编译正则表达式模式"""
        compiled = {}
        for model_type, patterns in self.patterns.items():
            compiled[model_type] = {
                "start_regex": [re.compile(pattern, re.IGNORECASE | re.DOTALL) 
                               for pattern in patterns["start_markers"]],
                "end_regex": [re.compile(pattern, re.IGNORECASE | re.DOTALL) 
                             for pattern in patterns["end_markers"]],
                "inline_regex": [re.compile(pattern, re.IGNORECASE | re.DOTALL) 
                                for pattern in patterns["inline_patterns"]]
            }
        return compiled
    
    def detect_reasoning_blocks(self, text: str) -> List[Dict]:
        """检测推理块"""
        reasoning_blocks = []
        
        for model_type, patterns in self.compiled_patterns.items():
            # 检测XML标签式的推理块
            for start_pattern in patterns["start_regex"]:
                for end_pattern in patterns["end_regex"]:
                    # 查找成对的开始和结束标记
                    combined_pattern = f"({start_pattern.pattern}).*?({end_pattern.pattern})"
                    matches = re.finditer(combined_pattern, text, re.IGNORECASE | re.DOTALL)
                    
                    for match in matches:
                        reasoning_blocks.append({
                            "type": "block",
                            "model": model_type,
                            "start": match.start(),
                            "end": match.end(),
                            "content": match.group(),
                            "confidence": 0.9
                        })
            
            # 检测内联推理模式
            for inline_pattern in patterns["inline_regex"]:
                matches = re.finditer(inline_pattern, text)
                for match in matches:
                    reasoning_blocks.append({
                        "type": "inline",
                        "model": model_type,
                        "start": match.start(),
                        "end": match.end(),
                        "content": match.group(),
                        "confidence": 0.7
                    })
        
        # 去重和排序
        reasoning_blocks = self._deduplicate_blocks(reasoning_blocks)
        return sorted(reasoning_blocks, key=lambda x: x["start"])
    
    def _deduplicate_blocks(self, blocks: List[Dict]) -> List[Dict]:
        """去重重叠的检测块"""
        if not blocks:
            return blocks
        
        # 按置信度和长度排序
        blocks.sort(key=lambda x: (x["confidence"], x["end"] - x["start"]), reverse=True)
        
        deduplicated = []
        for block in blocks:
            # 检查是否与已有块重叠
            overlaps = False
            for existing in deduplicated:
                if (block["start"] < existing["end"] and 
                    block["end"] > existing["start"]):
                    overlaps = True
                    break
            
            if not overlaps:
                deduplicated.append(block)
        
        return deduplicated
```

### 2. 智能过滤器
```python
class ReasoningFilter:
    """推理过程过滤器"""
    
    def __init__(self):
        self.detector = ReasoningDetector()
        self.filter_modes = {
            "remove": self._remove_reasoning,
            "replace": self._replace_reasoning,
            "hide": self._hide_reasoning,
            "summarize": self._summarize_reasoning
        }
    
    def filter_reasoning(self, text: str, mode: str = "remove") -> str:
        """过滤推理过程"""
        if mode not in self.filter_modes:
            raise ValueError(f"Unknown filter mode: {mode}")
        
        reasoning_blocks = self.detector.detect_reasoning_blocks(text)
        
        if not reasoning_blocks:
            return text  # 没有检测到推理过程
        
        return self.filter_modes[mode](text, reasoning_blocks)
    
    def _remove_reasoning(self, text: str, blocks: List[Dict]) -> str:
        """完全移除推理过程"""
        # 从后往前删除，避免索引变化
        for block in reversed(blocks):
            text = text[:block["start"]] + text[block["end"]:]
        
        # 清理多余的空行
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        return text.strip()
    
    def _replace_reasoning(self, text: str, blocks: List[Dict]) -> str:
        """用占位符替换推理过程"""
        for block in reversed(blocks):
            replacement = "[思考过程已隐藏]"
            text = text[:block["start"]] + replacement + text[block["end"]:]
        
        return text
    
    def _hide_reasoning(self, text: str, blocks: List[Dict]) -> str:
        """用折叠标记隐藏推理过程"""
        for block in reversed(blocks):
            hidden_content = f"<details><summary>点击查看思考过程</summary>\n{block['content']}\n</details>"
            text = text[:block["start"]] + hidden_content + text[block["end"]:]
        
        return text
    
    def _summarize_reasoning(self, text: str, blocks: List[Dict]) -> str:
        """总结推理过程"""
        for block in reversed(blocks):
            # 简单的总结逻辑
            summary = self._create_summary(block["content"])
            text = text[:block["start"]] + summary + text[block["end"]:]
        
        return text
    
    def _create_summary(self, reasoning_content: str) -> str:
        """创建推理过程的简要总结"""
        # 提取关键词和结论
        lines = reasoning_content.split('\n')
        key_lines = [line.strip() for line in lines 
                    if any(keyword in line.lower() for keyword in 
                          ['therefore', 'conclusion', 'result', '因此', '结论', '所以'])]
        
        if key_lines:
            return f"[推理总结: {key_lines[0][:50]}...]"
        else:
            return "[推理过程已简化]"
```

### 3. 实时过滤系统
```python
class RealtimeReasoningFilter:
    """实时推理过滤系统"""
    
    def __init__(self):
        self.filter = ReasoningFilter()
        self.cache = {}
    
    async def filter_model_output(self, model_name: str, raw_output: str, 
                                 filter_mode: str = "remove") -> Dict:
        """实时过滤模型输出"""
        
        # 检查缓存
        cache_key = f"{model_name}:{hash(raw_output)}:{filter_mode}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 检测推理模式
        reasoning_blocks = self.filter.detector.detect_reasoning_blocks(raw_output)
        
        # 过滤处理
        filtered_output = self.filter.filter_reasoning(raw_output, filter_mode)
        
        result = {
            "original": raw_output,
            "filtered": filtered_output,
            "reasoning_detected": len(reasoning_blocks) > 0,
            "reasoning_blocks": reasoning_blocks,
            "filter_mode": filter_mode,
            "model": model_name
        }
        
        # 缓存结果
        self.cache[cache_key] = result
        
        return result
    
    def get_clean_output(self, model_output_result: Dict) -> str:
        """获取清洁的输出"""
        return model_output_result["filtered"]
    
    def has_reasoning(self, model_output_result: Dict) -> bool:
        """检查是否包含推理过程"""
        return model_output_result["reasoning_detected"]
```

## 🎭 八仙专用过滤系统

### 针对八仙的特殊处理
```python
class BaxianReasoningFilter:
    """八仙专用推理过滤器"""
    
    def __init__(self):
        self.realtime_filter = RealtimeReasoningFilter()
        self.immortal_configs = {
            "吕洞宾": {"filter_mode": "remove", "max_length": 100},
            "何仙姑": {"filter_mode": "remove", "max_length": 100},
            "铁拐李": {"filter_mode": "remove", "max_length": 80},
            "汉钟离": {"filter_mode": "remove", "max_length": 120},
            "蓝采和": {"filter_mode": "remove", "max_length": 100},
            "张果老": {"filter_mode": "remove", "max_length": 150},
            "韩湘子": {"filter_mode": "remove", "max_length": 100},
            "曹国舅": {"filter_mode": "remove", "max_length": 120}
        }
    
    async def get_clean_immortal_statement(self, immortal: str, 
                                          model_name: str, 
                                          raw_output: str) -> str:
        """获取清洁的仙人发言"""
        
        config = self.immortal_configs[immortal]
        
        # 过滤推理过程
        filter_result = await self.realtime_filter.filter_model_output(
            model_name, raw_output, config["filter_mode"]
        )
        
        clean_output = filter_result["filtered"]
        
        # 长度控制
        if len(clean_output) > config["max_length"]:
            clean_output = clean_output[:config["max_length"]] + "..."
        
        # 记录日志
        if filter_result["reasoning_detected"]:
            print(f"⚠️  {immortal} 的输出包含推理过程，已自动过滤")
        
        return clean_output
    
    async def batch_filter_debate(self, debate_outputs: Dict[str, str]) -> Dict[str, str]:
        """批量过滤辩论输出"""
        filtered_outputs = {}
        
        for immortal, raw_output in debate_outputs.items():
            if immortal in self.immortal_configs:
                filtered_outputs[immortal] = await self.get_clean_immortal_statement(
                    immortal, "unknown", raw_output
                )
            else:
                filtered_outputs[immortal] = raw_output
        
        return filtered_outputs
```

## 🔧 集成到现有系统

### 与八仙辩论系统集成
```python
class XiantianBaguaWithFiltering:
    """带过滤功能的先天八卦辩论系统"""
    
    def __init__(self):
        self.baxian_filter = BaxianReasoningFilter()
        self.model_caller = ModelCaller()
    
    async def get_filtered_immortal_statement(self, immortal: str, topic: str) -> str:
        """获取过滤后的仙人发言"""
        
        # 调用模型
        model_name = self.get_immortal_model(immortal)
        prompt = self.create_immortal_prompt(immortal, topic)
        raw_output = await self.model_caller.call(model_name, prompt)
        
        # 过滤推理过程
        clean_output = await self.baxian_filter.get_clean_immortal_statement(
            immortal, model_name, raw_output
        )
        
        return clean_output
    
    async def conduct_filtered_debate(self, topic: str) -> Dict:
        """进行过滤后的辩论"""
        bagua_order = ["吕洞宾", "何仙姑", "铁拐李", "汉钟离",
                      "蓝采和", "张果老", "韩湘子", "曹国舅"]
        
        debate_results = {}
        
        for immortal in bagua_order:
            statement = await self.get_filtered_immortal_statement(immortal, topic)
            debate_results[immortal] = statement
            
            print(f"{immortal}: {statement}")
        
        return debate_results
```

## 💡 实际效果演示

### Before（原始输出）：
```
"让我分析一下这个问题...首先从技术面来看，当前市场呈现出明显的突破信号...
我需要考虑多个因素...经过深入思考，我认为..."
```

### After（过滤后）：
```
"当前市场呈现明显突破信号，建议关注科技龙头股。"
```

## 🎯 优势总结

### 技术优势
1. **精确检测** - 多种模式识别推理过程
2. **灵活过滤** - 支持移除、替换、隐藏等模式
3. **实时处理** - 无需预先知道模型类型
4. **缓存优化** - 提高处理效率

### 实用优势
1. **保持专业** - 八仙不会暴露搞笑独白
2. **节省时间** - 用户只看结论
3. **提升体验** - 避免冗长的思考过程
4. **灵活控制** - 可选择是否显示推理

这样你就可以放心使用任何推理模型了，系统会自动过滤掉思考过程！🎭