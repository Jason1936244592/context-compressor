---
name: context-compressor
description: "压缩 Agent 对话历史，减少 token 消耗。智能摘要早期对话，保留关键信息，支持手动/自动触发，可节省 60-80% tokens。"
version: 1.0.0
author: Jason
created: 2026-03-29
tags:
  - optimization
  - token-management
  - context-management
  - cost-reduction
metadata:
  trigger: manual | auto | threshold
  threshold_tokens: 50000
  compression_ratio: 0.6-0.8
---

# Context Compressor - 对话上下文压缩技能

## 📋 概述

**Context Compressor** 是一个智能对话压缩工具，用于减少 Agent 对话历史的 token 消耗，同时保留关键信息和上下文连贯性。

### 核心价值

| 价值 | 说明 |
|------|------|
| 💰 **降低成本** | 减少 60-80% 的 token 消耗 |
| ⚡ **提升速度** | 更短的上下文 = 更快的响应 |
| 🎯 **避免超限** | 防止超出模型上下文窗口限制 |
| 📊 **智能保留** | 自动识别并保留关键信息 |

---

## 🎯 触发条件

### 手动触发
- 用户说："压缩对话"、"节省 token"、"上下文太长了"
- 用户说："总结之前的对话"、"清理历史记录"

### 自动触发
- 上下文超过 **50,000 tokens**（可配置）
- 接近模型上限的 **80%**
- 会话持续时间超过 **24 小时**

### 临界警告
- 上下文超过 **100,000 tokens** → 建议立即压缩
- 上下文超过 **150,000 tokens** → 警告，可能丢失信息

---

## 📝 执行步骤

### Step 1: 分析当前会话

```bash
# 1.1 统计基本信息
- 总 token 数
- 对话轮数
- 会话时长
- 模型类型及上下文限制

# 1.2 识别对话结构
- 识别关键决策点
- 提取代码块
- 提取配置变更
- 标记待办事项
- 识别用户偏好
```

### Step 2: 应用压缩策略

#### 分层压缩策略

| 层级 | 范围 | 策略 | 保留比例 |
|------|------|------|----------|
| **Level 1** | 最近 10 轮 | 完整保留 | 100% |
| **Level 2** | 10-50 轮 | 精简版 | 40-50% |
| **Level 3** | 50+ 轮 | 摘要版 | 10-20% |

#### 内容优先级

**必须保留（P0）**：
- [ ] 用户明确说"记住这个"、"很重要"的内容
- [ ] 已完成的代码文件和配置
- [ ] 关键决策和结论
- [ ] 待办事项和未完成的任务
- [ ] 用户偏好和约束条件

**可以压缩（P1）**：
- [ ] 详细的推理过程
- [ ] 工具调用的完整输出
- [ ] 长段解释性文字

**可以删除（P2）**：
- [ ] 寒暄和问候
- [ ] 试错和修正过程
- [ ] 重复的确认
- [ ] 已解决的错误详情

### Step 3: 生成摘要

使用 LLM 对早期对话生成结构化摘要：

```markdown
## 对话摘要 [时间范围]

### 核心需求
- 用户的主要目标...

### 已完成
- [x] 任务 1
- [x] 任务 2

### 进行中
- [ ] 任务 3

### 关键决策
- 决策 1：...
- 决策 2：...

### 重要配置
```配置内容```

### 待办事项
- [ ] 待办 1
- [ ] 待办 2
```

### Step 4: 生成压缩报告

```markdown
## 📊 压缩报告

| 指标 | 压缩前 | 压缩后 | 变化 |
|------|--------|--------|------|
| Tokens | 100,000 | 25,000 | -75% |
| 对话轮数 | 200 | 50 | -75% |
| 预计成本 | $0.15 | $0.04 | -73% |

### 保留内容
- ✅ 最近 20 轮完整对话
- ✅ 5 个代码块
- ✅ 3 个配置文件
- ✅ 8 个关键决策

### 压缩内容
- 📝 150 轮早期对话 → 摘要为 5 段
- 🗑️ 删除 30 条寒暄消息
- 🗑️ 删除 20 条重复确认
```

### Step 5: 用户确认

**压缩前必须展示**：
1. 压缩报告预览
2. 保留内容清单
3. 备份位置说明
4. 恢复方法说明

**用户确认后执行**：
- 执行压缩
- 保存备份
- 更新会话

---

## 💡 使用示例

### 示例 1：手动触发压缩

```
用户：现在的对话太长了，帮我压缩一下，节省点 token

AI: 好的，我来分析当前对话并生成压缩方案...

📊 当前会话分析
- 总 Tokens: 125,000
- 对话轮数：280 轮
- 会话时长：3 天

📋 压缩方案
- 保留最近 20 轮完整对话
- 将早期 260 轮压缩为 8 段摘要
- 预计节省：78% tokens (约 97,500 tokens)

是否执行压缩？确认后我将：
1. 保存完整备份到 ~/.openclaw/backups/
2. 应用压缩
3. 更新当前会话

用户：确认

AI: ✅ 压缩完成！
- 压缩前：125,000 tokens
- 压缩后：27,500 tokens
- 节省：97,500 tokens (78%)
- 备份位置：~/.openclaw/backups/session-20260329-125700.json
```

### 示例 2：自动触发警告

```
AI: ⚠️ 上下文长度警告

当前会话已达到 110,000 tokens，接近模型限制的 80%。
建议进行上下文压缩以避免信息丢失。

预计压缩效果：
- 可节省：60,000-80,000 tokens
- 保留：最近 30 轮完整对话 + 关键信息摘要

是否现在压缩？(是/否/稍后提醒)
```

### 示例 3：查看压缩历史

```
用户：查看之前的压缩记录

AI: 📋 压缩历史记录

| 日期 | 压缩前 | 压缩后 | 节省 |
|------|--------|--------|------|
| 2026-03-29 | 125K | 27.5K | 78% |
| 2026-03-25 | 80K | 20K | 75% |
| 2026-03-20 | 150K | 35K | 77% |

累计节省：约 272,500 tokens
累计节省成本：约 $0.41

需要恢复某个压缩前的版本吗？
```

---

## 🛠️ 技术实现

### 目录结构

```
context-compressor/
├── SKILL.md                  # 本文件
├── scripts/
│   ├── compress.py           # 压缩主脚本
│   ├── analyze.py            # 上下文分析
│   └── report.py             # 生成报告
├── references/
│   ├── compression-rules.md  # 压缩规则详情
│   └── examples.md           # 更多示例
└── assets/
    └── templates/
        └── summary-template.md  # 摘要模板
```

### 核心脚本：compress.py

```python
#!/usr/bin/env python3
"""
Context Compressor - 对话上下文压缩工具
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple

class ContextCompressor:
    def __init__(self, threshold_tokens: int = 50000):
        self.threshold = threshold_tokens
        self.compression_ratio = 0.7  # 目标压缩比例
        
    def analyze(self, history: List[Dict]) -> Dict:
        """分析对话历史"""
        return {
            "total_tokens": self.count_tokens(history),
            "turn_count": len(history) // 2,
            "key_moments": self.identify_key_moments(history),
            "code_blocks": self.extract_code_blocks(history),
            "configs": self.extract_configs(history),
            "todos": self.extract_todos(history)
        }
    
    def compress(self, history: List[Dict], strategy: str = "auto") -> Tuple[List[Dict], Dict]:
        """执行压缩"""
        # 分层压缩
        recent = history[-20:]  # 保留最近 20 轮
        middle = history[-50:-20]  # 中间 30 轮精简
        old = history[:-50]  # 早期对话摘要
        
        # 生成摘要
        summary = self.generate_summary(old)
        
        # 合并结果
        compressed = [summary] + middle + recent
        
        report = {
            "before_tokens": self.count_tokens(history),
            "after_tokens": self.count_tokens(compressed),
            "saved_ratio": 1 - self.count_tokens(compressed) / self.count_tokens(history)
        }
        
        return compressed, report
    
    def generate_summary(self, messages: List[Dict]) -> Dict:
        """生成对话摘要"""
        # 调用 LLM 生成结构化摘要
        summary_text = f"""
## 对话摘要 ({len(messages)} 轮压缩为 1 段)

### 核心需求
- [AI 识别的用户主要目标]

### 已完成
- [已完成的任务列表]

### 关键决策
- [重要决策点]

### 重要信息
- [代码/配置/偏好等]
"""
        return {
            "role": "system",
            "content": summary_text,
            "compressed_from": len(messages)
        }
    
    def count_tokens(self, messages: List[Dict]) -> int:
        """估算 token 数量"""
        # 简化估算：平均每字符 0.5 tokens
        total_chars = sum(len(m.get("content", "")) for m in messages)
        return int(total_chars * 0.5)
    
    def identify_key_moments(self, history: List[Dict]) -> List[int]:
        """识别关键时刻的索引"""
        key_indices = []
        keywords = ["记住", "重要", "决定", "结论", "完成", "配置"]
        
        for i, msg in enumerate(history):
            content = msg.get("content", "")
            if any(kw in content for kw in keywords):
                key_indices.append(i)
        
        return key_indices
    
    def extract_code_blocks(self, history: List[Dict]) -> List[str]:
        """提取代码块"""
        codes = []
        for msg in history:
            content = msg.get("content", "")
            if "```" in content:
                # 提取代码块
                codes.append(content)
        return codes
    
    def extract_configs(self, history: List[Dict]) -> List[str]:
        """提取配置变更"""
        configs = []
        config_keywords = ["config", "配置", "设置", "settings"]
        
        for msg in history:
            content = msg.get("content", "")
            if any(kw in content.lower() for kw in config_keywords):
                configs.append(content)
        
        return configs
    
    def extract_todos(self, history: List[Dict]) -> List[str]:
        """提取待办事项"""
        todos = []
        todo_keywords = ["待办", "todo", "需要", "稍后", "接下来"]
        
        for msg in history:
            content = msg.get("content", "")
            if any(kw in content.lower() for kw in todo_keywords):
                todos.append(content)
        
        return todos


def main():
    compressor = ContextCompressor(threshold_tokens=50000)
    
    # 从 stdin 读取对话历史
    history = json.load(sys.stdin)
    
    # 分析
    analysis = compressor.analyze(history)
    print(f"分析结果：{json.dumps(analysis, indent=2)}")
    
    # 压缩
    compressed, report = compressor.compress(history)
    print(f"压缩报告：{json.dumps(report, indent=2)}")
    
    # 输出压缩结果
    print(json.dumps(compressed, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

---

## ⚠️ 注意事项

### 安全机制

| 机制 | 说明 |
|------|------|
| **备份优先** | 压缩前必须保存完整备份 |
| **用户确认** | 必须用户明确确认后才执行 |
| **可恢复** | 提供解压/恢复功能 |
| **渐进压缩** | 首次压缩保守（50%），后续可调整 |

### 不适用场景

- ❌ 法律/医疗等需要完整记录的对话
- ❌ 调试中的问题排查（需要完整日志）
- ❌ 学习/教学场景（需要完整过程）

### 最佳实践

1. **定期压缩**：每 24-48 小时或达到阈值时
2. **保留关键**：代码、配置、决策必须保留
3. **备份习惯**：压缩前自动备份到安全位置
4. **预览确认**：始终预览压缩效果再确认

---

## 🔗 相关资源

- [OpenClaw Sessions API](https://docs.openclaw.ai/api/sessions)
- [Token 计费说明](https://docs.openclaw.ai/pricing)
- [上下文管理最佳实践](https://docs.openclaw.ai/best-practices/context-management)

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-29 | 初始版本 |

---

## 🙏 致谢

本 Skill 灵感来源于：
- OpenClaw 社区的最佳实践
- 对话管理系统的设计模式
- Token 优化需求
