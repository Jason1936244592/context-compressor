# 对话摘要模板

## 📋 对话摘要

**压缩时间**: {{timestamp}}  
**原始轮数**: {{original_turns}} → **压缩后**: {{compressed_turns}}  
**Token 节省**: {{saved_tokens}} ({{saved_ratio}})

---

### 👤 用户信息

**用户偏好**:
{{#preferences}}
- {{.}}
{{/preferences}}

**约束条件**:
{{#constraints}}
- {{.}}
{{/constraints}}

---

### 🎯 核心目标

{{core_goals}}

---

### ✅ 已完成任务

{{#completed}}
- [x] {{.}}
{{/completed}}

---

### 🔄 进行中任务

{{#in_progress}}
- [ ] {{.}}
{{/in_progress}}

---

### 📋 待办事项

{{#todos}}
- [ ] {{.}}
{{/todos}}

---

### 💻 关键代码

{{#code_blocks}}
**文件**: {{filename}}
```{{language}}
{{code}}
```
{{/code_blocks}}

---

### ⚙️ 配置变更

{{#configs}}
- **{{name}}**: {{value}}
{{/configs}}

---

### 🎯 关键决策

{{#decisions}}
- **决策**: {{decision}}
  - 原因：{{reason}}
  - 影响：{{impact}}
{{/decisions}}

---

### 📌 重要信息

{{#important_notes}}
- {{.}}
{{/important_notes}}

---

### 🔗 相关资源

{{#resources}}
- [{{title}}]({{url}})
{{/resources}}

---

### 📝 备注

{{notes}}

---

*本摘要由 Context Compressor 自动生成 | 完整版本备份于：{{backup_location}}*
