# 快速开始指南
# Quick Start Guide

> 5 分钟上手 Claude 无状态工作流

---

## 🚀 **30 秒快速开始**

```bash
# 1. 初始化工作流
bash .claude/init-workflow.sh

# 2. 编辑项目信息
vim CLAUDE.md

# 3. 开始开发
# 在 Claude Code 中执行:
# "请使用无状态工作流帮我开发 {项目描述}"
```

---

## 📋 **完整步骤**

### Step 1: 初始化（1 分钟）

```bash
cd /path/to/your-project
bash .claude/init-workflow.sh
```

### Step 2: 配置（2 分钟）

编辑 `CLAUDE.md`:
```markdown
## 项目信息
**项目名称**: My Project
**项目类型**: web-app
**技术栈**: Next.js + PostgreSQL
```

### Step 3: 启动（2 分钟）

在 Claude Code 中：
```
我想开发一个 {项目描述}，
包含以下功能：
1. {功能 1}
2. {功能 2}
3. {功能 3}

请使用无状态工作流帮我开发。
```

---

## 🔄 **工作流程**

```
需求澄清 → 技术分析 → 生成计划 → 任务原子化
  ↓
Task 1 → 执行 → 保存状态 → /clear
  ↓
Task 2 → 执行 → 保存状态 → /clear
  ↓
Task 3 → 执行 → 保存状态 → /clear
  ↓
... 重复 ...
  ↓
完成 → 集成测试 → 交付
```

---

## 📁 **关键文件**

| 文件 | 作用 | 必须编辑 |
|------|------|----------|
| `CLAUDE.md` | 项目上下文 | ✅ 是 |
| `.claude/state/current-session.md` | 会话状态 | ❌ 自动 |
| `.claude/specs/atomic-tasks.md` | 任务列表 | ❌ 自动 |
| `.claude/config.yml` | 工作流配置 | ⚠️ 可选 |

---

## ⚡ **核心原则**

1. **每个任务独立会话** - 用 `/clear` 清除上下文
2. **通过文件传递状态** - 不依赖对话历史
3. **单任务 < 80% 上下文** - 监控 `/context`
4. **先保存再清除** - 避免丢失进度

---

## 🎯 **示例提示词**

### 开始新项目
```
我想开发一个知识付费平台，包含：
- 用户认证（JWT）
- 内容管理（CRUD）
- 支付集成（Stripe）
- 内容保护（防 F12）

技术栈：Next.js + PostgreSQL + Prisma

请使用无状态工作流帮我开发。
```

### 继续任务
```
请阅读 .claude/state/current-session.md 和 ./CLAUDE.md 了解当前进度，
然后执行 Task {N}: {任务名称}
```

### 恢复中断
```
我的会话中断了，请读取 .claude/state/current-session.md，
找到当前任务并继续执行。
```

---

## 📚 **详细文档**

- **完整指南**: `.claude/STATELESS_WORKFLOW_GUIDE.md`
- **工作流定义**: `.claude/workflows/stateless-dev.yml`
- **状态文件模板**: `.claude/templates/session-state.md`
- **迁移指南**: `.claude/MIGRATION_GUIDE.md`

---

## ⚠️ **重要提示**

### 必须做
- ✅ 每个任务后执行 `/clear`
- ✅ 清除前保存状态
- ✅ 监控上下文使用率
- ✅ 更新 CLAUDE.md

### 不要做
- ❌ 忘记执行 `/clear`
- ❌ 清除前不保存
- ❌ 任务过大（> 80% 上下文）
- ❌ 依赖对话历史

---

## 🆘 **遇到问题？**

### 常见问题

**Q: 上下文溢出了怎么办？**
A: 立即完成当前任务，保存状态，执行 `/clear`

**Q: 忘记保存状态就清除了？**
A: 从 `.claude/state/backups/` 恢复最近的备份

**Q: 任务太大无法完成？**
A: 拆分为更小的原子任务（15-30 分钟）

**Q: 如何并行执行任务？**
A: 开多个终端，每个执行一个独立任务

---

## 🎉 **开始使用**

```bash
# 运行快速启动脚本
bash .claude/quick-start.sh

# 或直接在 Claude Code 中开始
# "请使用无状态工作流帮我开发..."
```

---

**Happy Coding!** 🚀
