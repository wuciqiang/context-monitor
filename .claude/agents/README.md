# SubAgent 配置指南

## 概述

SubAgent (子代理) 是 Claude Code 的专业化 AI 助手,用于处理特定类型的任务。每个 SubAgent 有独立的上下文窗口、工具权限和系统提示词。

## 目录结构

```
.claude/agents/
├── README.md                    # 本文档
├── task-designer.md             # 任务设计专家 (Codex风格)
├── code-implementer.md          # 代码实施专家
├── code-reviewer.md             # 代码审查专家
├── doc-generator.md             # 文档生成专家 (Gemini风格)
└── test-runner.md               # 测试执行专家
```

## SubAgent 配置格式

每个 SubAgent 是一个 Markdown 文件,包含 YAML frontmatter 和系统提示词:

```markdown
---
name: subagent-name
description: 何时调用此 SubAgent 的描述
tools: Read, Write, Edit, Bash  # 可选,省略则继承所有工具
model: sonnet  # 可选: sonnet/opus/haiku/inherit
permissionMode: default  # 可选: default/acceptEdits/bypassPermissions
skills: skill1, skill2  # 可选: 自动加载的 Skills
---

系统提示词内容...
```

### 配置字段说明

| 字段 | 必需 | 说明 |
|:-----|:-----|:-----|
| `name` | 是 | 唯一标识符,使用小写字母和连字符 |
| `description` | 是 | 自然语言描述,用于自动委派 |
| `tools` | 否 | 逗号分隔的工具列表,省略则继承所有工具 |
| `model` | 否 | 模型选择: sonnet(推理)/opus(复杂)/haiku(快速) |
| `permissionMode` | 否 | 权限模式 |
| `skills` | 否 | 自动加载的 Skills |

## 内置 SubAgent 类型

### 1. general-purpose (通用型)
- **模型**: Sonnet
- **工具**: 所有工具
- **用途**: 复杂研究、多步骤操作、代码修改
- **适用场景**: 需要探索和修改的任务

### 2. Explore (探索型)
- **模型**: Haiku (快速)
- **模式**: 严格只读
- **工具**: Glob, Grep, Read, Bash (只读命令)
- **彻底度**: quick/medium/very thorough
- **适用场景**: 搜索/理解代码库,不做修改

### 3. Plan (规划型)
- **模型**: Sonnet
- **工具**: Read, Glob, Grep, Bash
- **用途**: 计划模式下的研究和信息收集
- **适用场景**: 规划阶段的代码库研究

## 工作流集成的 SubAgent

### task-designer (任务设计专家)
**用途**: Phase 3 - 为每个任务设计实现方案
- 分析任务需求
- 设计技术方案
- 识别风险点
- 提供实施建议

### code-implementer (代码实施专家)
**用途**: Phase 4 - 实施代码
- 基于设计方案实施代码
- 遵循项目规范
- 编写清晰代码
- 记录修改文件

### code-reviewer (代码审查专家)
**用途**: Phase 4 - 审查代码质量
- 5+类别评估
- 问题分级
- 提供修复建议
- 生成审查报告

### doc-generator (文档生成专家)
**用途**: Phase 5 - 生成文档
- 生成功能文档
- 编写 API 文档
- 创建使用指南
- 生成代码注释

### test-runner (测试执行专家)
**用途**: Phase 5 - 执行测试
- 运行测试套件
- 分析测试结果
- 修复失败测试
- 生成覆盖率报告

## 使用方式

### 1. 显式调用

```bash
# 在对话中明确指定
> 使用 task-designer 子代理设计用户认证方案
> 让 code-reviewer 子代理审查我的代码
```

### 2. 自动委派

Claude Code 会根据任务描述自动委派给合适的 SubAgent:

```bash
# 自动委派给 code-implementer
> 实现 JWT 认证功能

# 自动委派给 code-reviewer
> 审查最近的代码变更
```

### 3. 工作流集成

在工作流中使用 Task 工具调用:

```typescript
// Phase 3: 任务设计
Task({
  subagent_type: "task-designer",
  description: "设计任务 T001",
  prompt: "为任务 T001 设计实现方案..."
})

// Phase 4: 代码实施
Task({
  subagent_type: "code-implementer",
  description: "实施任务 T001",
  prompt: "基于设计方案实施代码..."
})

// Phase 4: 代码审查
Task({
  subagent_type: "code-reviewer",
  description: "审查任务 T001",
  prompt: "审查 SubAgent 实施的代码..."
})
```

### 4. 并行执行

单消息多个 Task 调用实现并行:

```typescript
// 并行组任务
[
  Task({ subagent_type: "code-implementer", prompt: "实施 T001..." }),
  Task({ subagent_type: "code-implementer", prompt: "实施 T002..." })
]
```

## 管理 SubAgent

### 查看所有 SubAgent

```bash
/agents
```

### 创建新 SubAgent

1. 使用 `/agents` 命令的交互式菜单
2. 或手动创建 `.claude/agents/your-agent.md`

### 编辑 SubAgent

```bash
# 编辑项目级 SubAgent
vim .claude/agents/task-designer.md

# 编辑用户级 SubAgent
vim ~/.claude/agents/your-agent.md
```

### 恢复 SubAgent 会话

每个 SubAgent 执行有唯一的 `agentId`:

```bash
> 恢复代理 abc123 并继续分析授权逻辑
```

会话记录保存在 `agent-{agentId}.jsonl`

## 最佳实践

### 1. 设计专注的 SubAgent
- 单一职责原则
- 明确的任务边界
- 清晰的输入输出

### 2. 编写详细的提示词
- 包含具体指令
- 提供示例
- 定义约束条件

### 3. 限制工具访问
- 只授予必要的工具
- 只读任务使用 Explore 类型
- 修改任务使用 general-purpose

### 4. 使用描述性 description
- 具体且面向行动
- 包含触发关键词
- 使用 "PROACTIVELY" 等强调词

### 5. 版本控制
- 将项目 SubAgent 纳入版本控制
- 团队共享配置
- 记录变更历史

### 6. 选择合适的模型
- Sonnet: 复杂推理、代码审查
- Opus: 最复杂的任务
- Haiku: 快速搜索、简单任务

## 工作流中的 SubAgent 流程

```
Phase 3: 任务设计
├─ task-designer (Sonnet)
│  ├─ 分析任务需求
│  ├─ 设计技术方案
│  └─ 输出设计文档

Phase 4: 代码实施
├─ 并行组
│  ├─ code-implementer #1 (Sonnet) - 任务 T001
│  └─ code-implementer #2 (Sonnet) - 任务 T002
├─ code-reviewer (Sonnet)
│  ├─ 5+类别评估
│  ├─ 问题分级
│  └─ 输出审查报告
└─ code-implementer (修复) - 如需要

Phase 5: 文档与测试
├─ doc-generator (Gemini风格) - 如启用
│  ├─ 生成功能文档
│  └─ 生成 API 文档
└─ test-runner (Sonnet) - 如启用
   ├─ 运行测试
   └─ 分析结果
```

## 故障排查

### SubAgent 未被调用
- 检查 `description` 是否足够具体
- 确认任务描述包含触发关键词
- 尝试显式调用

### SubAgent 权限不足
- 检查 `tools` 配置
- 确认 `permissionMode` 设置
- 考虑使用 `acceptEdits` 模式

### SubAgent 性能问题
- 考虑使用 Haiku 模型
- 限制工具访问范围
- 优化提示词长度

## 参考资源

- [Claude Code 官方文档](https://code.claude.com/docs/en/sub-agents.md)
- [SubAgent 最佳实践](https://code.claude.com/docs/en/best-practices.md)
- [工作流集成指南](../specs/README.md)
