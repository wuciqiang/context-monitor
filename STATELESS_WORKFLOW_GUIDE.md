# 无状态工作流使用指南
# Stateless Workflow Guide

> 原子任务 + 状态文件 + 独立会话
> Version: 2.0.0

---

## 🎯 **核心概念**

### 什么是无状态工作流？

传统工作流依赖对话历史来维护上下文，导致：
- ❌ 上下文快速增长
- ❌ Token 使用量大
- ❌ 容易超过上下文限制

**无状态工作流**通过以下机制解决这些问题：
- ✅ 每个任务使用独立会话
- ✅ 通过文件传递状态
- ✅ 任务完成后清除上下文
- ✅ 单个任务上下文使用率 < 80%

---

## 🚀 **快速开始**

### 1. 初始化工作流

```bash
# 方式 1: 使用初始化脚本
cd /path/to/your-project
bash .claude/init-workflow.sh

# 方式 2: 手动创建目录
mkdir -p .claude/{workflows,templates,state,specs,progress}
cp .claude/templates/* .claude/
```

### 2. 配置项目信息

编辑 `CLAUDE.md`:
```markdown
# CLAUDE.md

## 项目信息
**项目名称**: My Awesome Project
**项目类型**: web-app
**项目描述**: A knowledge payment platform

## 技术栈
- **语言**: TypeScript
- **前端**: Next.js 14
- **后端**: Node.js
- **数据库**: PostgreSQL
```

### 3. 启动工作流

在 Claude Code 中执行：
```
/workflow run stateless-dev
```

或者直接开始：
```
请使用无状态工作流帮我开发 {项目描述}
```

---

## 📋 **工作流程详解**

### 完整流程图

```
用户需求
  ↓
需求澄清 (Step 1)
  ↓
技术分析 (Step 2)
  ↓
生成计划 (Step 3)
  ↓
任务原子化 (Step 4)
  ↓
┌─────────────────────────────────────┐
│ 任务执行循环 (无状态模式)            │
│                                     │
│  Task 1.1:                          │
│  ┌─────────────────────────────┐   │
│  │ 1. 加载状态文件              │   │
│  │ 2. 加载任务规范              │   │
│  │ 3. 执行任务                  │   │
│  │ 4. 保存输出到状态文件        │   │
│  │ 5. 提示用户执行 /clear       │   │
│  └─────────────────────────────┘   │
│           ↓                         │
│      用户执行 /clear                │
│           ↓                         │
│  Task 1.2:                          │
│  ┌─────────────────────────────┐   │
│  │ 1. 加载状态文件 (含 1.1 输出)│   │
│  │ 2. 加载任务规范              │   │
│  │ 3. 执行任务                  │   │
│  │ 4. 保存输出到状态文件        │   │
│  │ 5. 提示用户执行 /clear       │   │
│  └─────────────────────────────┘   │
│           ↓                         │
│      ... 重复 ...                   │
└─────────────────────────────────────┘
  ↓
所有任务完成
  ↓
集成测试 & 用户验收
```

### 单个任务的执行流程

```
┌─────────────────────────────────────────┐
│ Task N 开始                              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 1. 加载状态文件                          │
│    - .claude/state/current-session.md   │
│    - ./CLAUDE.md                        │
│    - .claude/specs/atomic-tasks.md      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 2. 加载任务规范                          │
│    - .claude/specs/task-N.md            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 3. 执行任务                              │
│    - 获取代码原型 (Codex/Gemini)        │
│    - 实施开发                            │
│    - 代码审查 (Codex)                   │
│    - 修复问题                            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 4. 保存任务输出                          │
│    - 更新 current-session.md            │
│    - 更新 CLAUDE.md                     │
│    - 更新 progress.md                   │
│    - 备份状态文件                        │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 5. 提示用户                              │
│    "请执行 /clear 清除上下文"            │
│    "然后继续执行 Task N+1"               │
└─────────────────────────────────────────┘
              ↓
        用户执行 /clear
              ↓
┌─────────────────────────────────────────┐
│ Task N+1 开始                            │
└─────────────────────────────────────────┘
```

---

## 📁 **文件结构说明**

### 核心文件

```
project-root/
├── CLAUDE.md                           # 项目上下文（必须）
│   ├── 项目信息
│   ├── 技术栈
│   ├── 开发规范
│   └── 当前进度（自动更新）
│
├── .claude/
│   ├── config.yml                      # 工作流配置
│   │
│   ├── workflows/
│   │   └── stateless-dev.yml           # 无状态工作流定义
│   │
│   ├── templates/
│   │   ├── session-state.md            # 状态文件模板
│   │   ├── atomic-task-spec.md         # 任务规范模板
│   │   └── completion-report.md        # 完成报告模板
│   │
│   ├── state/                          # 状态文件（核心！）
│   │   ├── current-session.md          # 当前会话状态
│   │   ├── backups/                    # 状态备份
│   │   │   ├── session-20250115-1000.md
│   │   │   └── session-20250115-1100.md
│   │   └── completed/                  # 已完成会话
│   │       └── session-project-final.md
│   │
│   ├── specs/                          # 任务规范
│   │   ├── atomic-tasks.md             # 所有任务列表
│   │   ├── task-1.1.md                 # 任务 1.1 规范
│   │   ├── task-1.2.md                 # 任务 1.2 规范
│   │   └── ...
│   │
│   ├── progress/                       # 进度追踪
│   │   ├── progress.md                 # 总体进度
│   │   ├── tasks/                      # 任务详情
│   │   └── reviews/                    # 审查记录
│   │
│   └── logs/                           # 日志
│       ├── workflow.log
│       └── errors.log
```

### 状态文件详解

**`.claude/state/current-session.md`** 是整个系统的核心，包含：

1. **会话元数据**
   - 会话 ID
   - 项目名称
   - 时间戳
   - 当前任务 ID

2. **全局上下文**
   - 项目信息
   - 技术栈
   - 关键决策

3. **任务执行状态**（表格）
   - 所有任务的状态
   - 完成时间
   - 备注

4. **任务输出**（每个任务）
   - 输出文件列表
   - 关键决策
   - 传递给下一任务的数据

5. **任务间依赖数据**
   - 代码片段
   - 配置信息
   - 类型定义

6. **下一任务预览**
   - 下一任务 ID
   - 任务名称
   - 依赖关系

---

## 🔄 **实际使用示例**

### 示例：开发知识付费平台

#### Step 1: 初始化

```bash
# 创建项目
mkdir knowledge-platform
cd knowledge-platform

# 初始化工作流
bash .claude/init-workflow.sh

# 编辑 CLAUDE.md
vim CLAUDE.md
```

#### Step 2: 启动工作流

在 Claude Code 中：
```
我想开发一个知识付费平台，包含：
1. 用户认证（JWT）
2. 内容管理（CRUD）
3. 支付集成（Stripe）
4. 内容保护（防 F12）

请使用无状态工作流帮我开发。
```

#### Step 3: 需求澄清

Claude 会询问：
- 技术栈选择？
- 数据库选择？
- 部署平台？
- ...

#### Step 4: 生成任务计划

Claude 生成 56 个原子任务，保存到：
- `.claude/specs/atomic-tasks.md`
- `.claude/specs/task-1.1.md`
- `.claude/specs/task-1.2.md`
- ...

#### Step 5: 执行 Task 1.1

```
Claude: 现在开始执行 Task 1.1: Next.js 项目初始化

[执行任务...]

Claude: ✅ Task 1.1 已完成

任务状态已保存到:
- .claude/state/current-session.md
- ./CLAUDE.md

下一步操作:
1. 请执行 /clear 清除当前上下文
2. 然后继续执行下一任务

下一任务: Task 1.2 - Prisma 数据库配置

提示词:
```
请阅读 .claude/state/current-session.md 和 ./CLAUDE.md 了解当前进度，
然后执行 Task 1.2: Prisma 数据库配置
```
```

#### Step 6: 清除上下文

```
/clear
```

#### Step 7: 继续 Task 1.2

复制提示词，开始新对话：
```
请阅读 .claude/state/current-session.md 和 ./CLAUDE.md 了解当前进度，
然后执行 Task 1.2: Prisma 数据库配置
```

Claude 会：
1. 读取状态文件
2. 了解 Task 1.1 的输出
3. 执行 Task 1.2
4. 保存状态
5. 提示清除上下文

#### Step 8: 重复直到完成

```
Task 1.1 → /clear → Task 1.2 → /clear → Task 1.3 → ... → Task 5.14 → 完成
```

---

## 🛠️ **高级用法**

### 1. 并行执行任务

如果任务没有依赖关系，可以并行执行：

```bash
# 终端 1
claude
> 请执行 Task 2.1: Stripe 客户端初始化

# 终端 2
claude
> 请执行 Task 3.1: 文件上传功能

# 终端 3
claude
> 请执行 Task 5.1: Tailwind 配置
```

### 2. 恢复中断的任务

如果任务执行中断：

```
1. 读取 .claude/state/current-session.md
2. 找到当前任务 ID
3. 读取 .claude/specs/task-{id}.md
4. 继续执行该任务
```

### 3. 回滚到之前的状态

```bash
# 查看备份
ls .claude/state/backups/

# 恢复备份
cp .claude/state/backups/session-20250115-1000.md \
   .claude/state/current-session.md
```

### 4. 自定义任务规范

编辑 `.claude/specs/task-{id}.md`:
```markdown
# Task 1.3: 定义用户模型

## 任务描述
创建 Prisma User 模型，包含认证所需的所有字段。

## 验收标准
- [ ] User 模型包含 id, email, password 字段
- [ ] email 字段有唯一索引
- [ ] password 使用 bcrypt 加密
- [ ] 包含 createdAt 和 updatedAt 时间戳

## 技术要求
- 使用 Prisma schema 语法
- 遵循数据库命名规范
- 添加必要的索引

## 输出
- prisma/schema.prisma (更新)
- migration 文件
```

---

## 📊 **监控与调试**

### 查看当前进度

```bash
# 查看状态文件
cat .claude/state/current-session.md

# 查看进度
cat .claude/progress/progress.md

# 查看日志
tail -f .claude/logs/workflow.log
```

### 检查上下文使用率

在 Claude Code 中：
```
/context
```

如果接近 80%，立即完成当前任务并清除上下文。

### 调试任务失败

```bash
# 查看错误日志
cat .claude/logs/errors.log

# 查看错误状态
ls .claude/state/error-*.md
cat .claude/state/error-20250115-1200.md
```

---

## ⚠️ **注意事项**

### 必须遵守的规则

1. **每个任务完成后必须执行 `/clear`**
   - 不清除会导致上下文累积
   - 最终超过限制

2. **必须保存状态后再清除**
   - 先保存到 current-session.md
   - 再执行 /clear
   - 否则会丢失进度

3. **单个任务不超过 80% 上下文**
   - 如果任务过大，拆分为更小的任务
   - 监控 /context 输出

4. **状态文件是唯一真实来源**
   - 不依赖对话历史
   - 所有关键信息必须写入文件

### 常见错误

❌ **错误 1**: 忘记执行 /clear
```
结果: 上下文持续增长，最终溢出
解决: 严格遵守每个任务后清除
```

❌ **错误 2**: 清除前未保存状态
```
结果: 任务输出丢失，无法继续
解决: 先保存，再清除
```

❌ **错误 3**: 任务过大
```
结果: 单个任务超过 80% 上下文
解决: 拆分为更小的原子任务
```

❌ **错误 4**: 状态文件未更新
```
结果: 下一任务缺少必要信息
解决: 确保每个任务都更新状态文件
```

---

## 🎯 **最佳实践**

### 1. 任务设计

- ✅ 每个任务 15-30 分钟
- ✅ 涉及文件 ≤ 3 个
- ✅ 单一职责
- ✅ 可独立测试

### 2. 状态管理

- ✅ 及时更新状态文件
- ✅ 定期备份
- ✅ 清晰的任务输出描述
- ✅ 完整的依赖数据

### 3. 上下文控制

- ✅ 监控 /context
- ✅ 60% 时警惕
- ✅ 80% 时立即完成
- ✅ 完成后立即 /clear

### 4. 协作

- ✅ 状态文件提交到 Git
- ✅ 团队成员可以接手任何任务
- ✅ 清晰的任务规范
- ✅ 完整的文档

---

## 📞 **获取帮助**

### 文档
- **本指南**: `.claude/STATELESS_WORKFLOW_GUIDE.md`
- **工作流定义**: `.claude/workflows/stateless-dev.yml`
- **模板文件**: `.claude/templates/`

### 问题排查
1. 检查状态文件是否完整
2. 检查日志文件
3. 查看备份文件
4. 参考示例项目

### 社区
- GitHub Issues
- Discussions
- Wiki

---

**祝你开发顺利！** 🚀

如有问题，请参考文档或提交 Issue。
