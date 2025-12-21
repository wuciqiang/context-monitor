# Spec文档驱动开发

## 概述

Spec文档是任务追踪和知识沉淀的核心机制,记录从需求到交付的完整过程。

## 目录结构

```
.claude/specs/
├── README.md                    # 本文档
├── active/                      # 进行中的任务
│   └── [feature-name]/
│       ├── spec.md             # 主规格文档
│       ├── task-log.md         # 任务执行日志(可选)
│       └── context.json        # 上下文快照
└── completed/                   # 已完成的任务
    └── [feature-name]/
        └── ...
```

## Spec文档格式

### spec.md 结构

```markdown
---
status: pending|in_progress|completed
feature_name: [功能名称]
created_at: [ISO 8601时间戳]
updated_at: [ISO 8601时间戳]
completed_at: [ISO 8601时间戳]
documentation_enabled: true|false
testing_enabled: true|false
---

# [功能名称] 开发规格

## 功能概述
[从Phase 1获取的需求描述]

## 任务清单

### 并行组 1
- [ ] **T001**: [任务描述]
  - 文件范围: [涉及的文件]
  - SubAgent类型: general-purpose|Explore
  - 状态: pending|in_progress|completed
  - 分配的SubAgent: -
  - 修改的文件: -
  - 完成时间: -
  - Codex设计: [设计要点]
  - Codex审查: [审查结果]

### 串行组 2 (依赖并行组1)
- [ ] **T002**: [任务描述]
  - ...

## 技术约束
[从Phase 1获取的技术限制]

## 测试需求
[如果启用测试,记录测试要求]

## 文档需求
[如果启用文档,记录文档要求]

## 代码审查结果

### 审查轮次 1
- 审查时间: [时间戳]
- 审查模型: Codex + Gemini
- 总体评分: [0-100]

#### 可维护性 (评分: X/100)
- 问题: [具体问题]
- 严重级别: Critical|High|Medium|Low
- 位置: [file:line]
- 修复建议: [具体建议]

#### 性能 (评分: X/100)
...

#### 安全性 (评分: X/100)
...

#### 风格一致性 (评分: X/100)
...

#### 文档完整性 (评分: X/100)
...

## 修改文件汇总
- [file:line_start-line_end]: [变更摘要]

## 生成的文档
- docs/[feature-name]/overview.md
- docs/[feature-name]/api.md
- docs/[feature-name]/usage.md

## 测试结果
- 测试通过: [数量]
- 测试失败: [数量]
- 覆盖率: [百分比]

## 后续步骤
- [建议1]
- [建议2]
```

## 工作流集成

### Phase 0: 创建Spec
```typescript
// 询问用户偏好
AskUserQuestion({
  questions: [
    {
      question: "是否为此功能生成文档?",
      options: ["是 - 生成模块文档", "否 - 仅代码"]
    },
    {
      question: "是否执行测试?",
      options: ["是 - 运行测试套件", "否 - 跳过测试"]
    }
  ]
})

// 创建Spec目录和文件
Write(".claude/specs/active/[feature-name]/spec.md")
Write(".claude/specs/active/[feature-name]/context.json")
```

### Phase 2: 更新任务清单
```typescript
// 生成任务拆解后,更新spec.md
Edit(".claude/specs/active/[feature-name]/spec.md", {
  section: "任务清单",
  content: [并行组和串行组的任务列表]
})

// 用户确认任务拆解
AskUserQuestion({
  question: "确认此任务拆解和Spec?",
  options: ["确认并执行", "需要调整"]
})
```

### Phase 3-4: 实时更新状态
```typescript
// 任务开始前
Edit(spec, {
  task: "T001",
  status: "in_progress",
  assigned_agent: "SubAgent #1"
})

// 任务完成后
Edit(spec, {
  task: "T001",
  status: "completed",
  modified_files: ["src/auth.ts:10-50"],
  completed_at: new Date().toISOString()
})
```

### Phase 5: 记录审查结果
```typescript
// 添加审查结果到spec.md
Edit(spec, {
  section: "代码审查结果",
  content: {
    round: 1,
    models: ["Codex", "Gemini"],
    score: 92,
    categories: {
      maintainability: { score: 95, issues: [...] },
      performance: { score: 90, issues: [...] },
      security: { score: 95, issues: [...] },
      style: { score: 88, issues: [...] },
      documentation: { score: 92, issues: [...] }
    }
  }
})
```

### 完成后: 归档Spec
```typescript
// 更新元数据
Edit(spec, {
  metadata: {
    status: "completed",
    completed_at: new Date().toISOString()
  }
})

// 移动到completed目录
Bash("mv .claude/specs/active/[feature-name] .claude/specs/completed/")
```

## 最佳实践

1. **实时更新**: 每个任务状态变化立即更新Spec
2. **详细记录**: 记录Codex设计要点和审查结果
3. **问题追踪**: 所有审查问题都记录到Spec
4. **知识沉淀**: 完成的Spec是项目知识库的一部分
5. **可追溯性**: 通过Spec可追溯任何功能的开发过程

## 查询和分析

```bash
# 查看所有进行中的任务
ls .claude/specs/active/

# 查看某个功能的Spec
cat .claude/specs/active/user-auth/spec.md

# 搜索特定问题
grep -r "Critical" .claude/specs/active/

# 统计完成的功能
ls .claude/specs/completed/ | wc -l
```
