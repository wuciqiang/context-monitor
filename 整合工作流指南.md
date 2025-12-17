# 整合工作流快速指南
# Integrated Workflow Quick Guide

> Context Monitor + Code Index MCP + Multi-Model Collaboration

---

## 🎯 系统概述

本系统整合了三大核心能力：

1. **Context Monitor** - 上下文资源管理
2. **Code Index MCP** - 智能代码检索
3. **Multi-Model Skills** - 多模型协作（Codex + Gemini）

---

## 🚀 快速开始

### 1. 启动 Claude Code

```bash
cd /path/to/your/project
claude
```

系统会自动激活，你会看到：
```
📊 Context monitoring active. Use check_context_usage tool to monitor usage.
```

### 2. 初始化代码索引（首次使用）

```
请初始化代码索引：
1. 设置项目路径为当前目录
2. 构建深度索引
3. 启用文件监控
```

### 3. 开始工作

```
我需要实现用户认证功能，包括登录、注册和密码重置
```

系统会自动执行整合工作流。

---

## 📋 完整工作流

### Phase 0: 初始化与上下文检查

**自动执行**：
- ✅ SessionStart hook 捕获会话信息
- ✅ Context Monitor 自动加载
- ✅ 显示监控激活提示

**手动执行**（复杂任务前）：
```
请检查当前上下文使用率
```

**预期输出**：
```json
{
  "usage_percent": 15.3,
  "status": "✅ SAFE",
  "recommendation": "Context usage is healthy. Continue working normally."
}
```

---

### Phase 1: 上下文检索

**自动执行**：Claude 会自动使用 Code Index 搜索相关代码

**手动触发**：
```
请搜索与用户认证相关的代码
```

**工具调用**：
- `search_code_advanced("user authentication")`
- `get_file_summary("path/to/auth.py")`

**预期输出**：
- 相关文件列表
- 完整的类、函数定义
- 依赖关系

---

### Phase 2: 多模型分析

**自动执行**：Claude 会调用 Codex 和 Gemini 进行分析

**工具调用**：
- Codex: 后端逻辑分析
- Gemini: 前端UI分析（如需要）

**预期输出**：
- 经过交叉验证的实施计划
- Step-by-step 步骤
- 伪代码示例

**上下文检查点**：
- 若使用率 > 70%，简化分析范围

---

### Phase 3: 原型获取

**自动执行**：根据任务类型路由到 Codex 或 Gemini

**前端任务** → Gemini:
```
请 Gemini 提供登录页面的 React 组件原型
```

**后端任务** → Codex:
```
请 Codex 提供用户认证的后端逻辑原型
```

**预期输出**：
- Unified Diff Patch
- 原型代码（仅供参考）

**上下文检查点**：
- 若使用率 > 70%，先保存状态

---

### Phase 4: 编码实施

**自动执行**：Claude 基于原型重构为生产代码

**自动监控**：
- 每 5-10 个工具调用后自动检查使用率
- 根据使用率自动提醒

**预期输出**：
- 企业级生产代码
- 精简高效，无冗余
- 非必要不添加注释

---

### Phase 4.5: 上下文管理

**自动触发**：当使用率达到阈值时

**使用率分级**：
- **< 50% (SAFE)**: 继续工作 ✅
- **50-70% (WARNING)**: 注意使用率 ⚠️
- **70-85% (HIGH)**: 准备保存状态 🔴
- **> 85% (CRITICAL)**: 立即保存并建议 `/clear` 🚨

**保存状态示例**：
```
⚠️ 上下文使用率已达 87.3%

已保存会话状态到 .claude/state/current-session.md

建议立即执行 `/clear` 清除上下文，然后使用以下提示词恢复：
"请阅读 .claude/state/current-session.md 了解之前的进度，继续 Phase 5 审计交付"
```

---

### Phase 5: 审计与交付

**手动触发**（在 `/clear` 后）：
```
请阅读 .claude/state/current-session.md 了解之前的进度，继续 Phase 5 审计交付
```

**自动执行**：
- Codex 和 Gemini 同时进行 Code Review
- 综合反馈并修正
- 最终上下文检查

**预期输出**：
- 审计报告
- 修正后的最终代码
- 使用率确认

---

## 🛠️ 常用命令

### 上下文管理

```bash
# 检查使用率
请检查当前上下文使用率

# 保存状态
请保存当前会话状态

# 恢复状态（在 /clear 后）
请阅读 .claude/state/current-session.md 了解之前的进度，然后继续工作
```

### 代码检索

```bash
# 自然语言搜索
请搜索处理支付的代码

# 获取文件详情
请分析 src/auth/login.py 的完整结构

# 查找文件
请找到所有的测试文件
```

### 多模型协作

```bash
# 请求 Codex 分析
请 Codex 分析这个算法的时间复杂度

# 请求 Gemini 设计
请 Gemini 设计一个现代化的登录页面

# 双模型审计
请 Codex 和 Gemini 同时审查这段代码
```

---

## ⚠️ 最佳实践

### ✅ 推荐做法

1. **任务开始前检查上下文** - 确保有足够空间
2. **信任自动监控** - Context Monitor 会主动提醒
3. **及时保存状态** - 不要等到 100% 才清除
4. **使用自然语言搜索** - 比 grep 更智能
5. **让外部模型提供原型** - Claude 负责重构
6. **强制执行审计** - 代码变更后立即审查

### ❌ 避免做法

1. ❌ 忽略上下文警告 - 可能导致会话中断
2. ❌ 跳过代码检索 - 可能基于假设编码
3. ❌ 直接使用外部模型代码 - 必须重构
4. ❌ 过度添加注释 - 代码应自解释
5. ❌ 影响现有功能 - 仅针对性改动
6. ❌ 跳过审计阶段 - 质量无法保证

---

## 🐛 故障排查

### Context Monitor 未激活

**症状**：启动 Claude Code 后没有看到监控提示

**解决**：
```bash
# 检查配置
cat .claude/settings.local.json

# 测试 hook
echo '{"session_id":"test","transcript_path":"/tmp/test.jsonl","cwd":"."}' | \
  bash hooks/capture-session-info.sh

# 测试 MCP server
python3 mcp-servers/context-monitor/server.py
```

### Code Index 未工作

**症状**：搜索代码时报错

**解决**：
```bash
# 检查 uvx
uvx --version

# 重新初始化索引
请重新构建代码索引
```

### 使用率计算不准确

**说明**：使用文件大小估算，可能有 ±10% 误差

**建议**：在 60-70% 时就开始准备清除

---

## 📊 工作流可视化

```
用户需求
   ↓
[Phase 0] 上下文检查 ✅ < 50%
   ↓
[Phase 1] 代码检索 (Code Index)
   ↓
[Phase 2] 多模型分析 (Codex + Gemini)
   ↓ 上下文检查 ⚠️ 50-70%
[Phase 3] 原型获取 (Codex/Gemini)
   ↓ 上下文检查 🔴 70-85%
[Phase 4] Claude 重构实施
   ↓ 自动监控
[Phase 4.5] 🚨 > 85% → 保存状态
   ↓
用户执行 /clear
   ↓
恢复状态
   ↓
[Phase 5] 双模型审计 → 交付
```

---

## 📚 相关文档

- **CLAUDE.md** - 完整工作流定义和资源矩阵
- **CONTEXT_MONITORING.md** - Context Monitor 详细说明
- **README.md** - 项目概述和安装指南
- **STATELESS_WORKFLOW_GUIDE.md** - 无状态工作流指南

---

## 🎯 示例场景

### 场景 1: 实现新功能

```
用户: 我需要添加用户头像上传功能

Claude:
1. [Phase 0] 检查上下文使用率: 23% ✅
2. [Phase 1] 搜索现有的文件上传代码
3. [Phase 2] 请 Codex 和 Gemini 分析实施方案
4. [Phase 3] 获取原型代码
5. [Phase 4] 重构为生产代码
6. [自动监控] 使用率 45% ✅
7. [Phase 5] 双模型审计
8. 交付完成 ✅
```

### 场景 2: 长时间任务

```
用户: 重构整个认证系统

Claude:
1. [Phase 0] 检查上下文: 18% ✅
2. [Phase 1] 检索所有认证相关代码
3. [Phase 2] 多模型分析，制定计划
4. [Phase 3] 获取重构原型
5. [Phase 4] 开始实施...
6. [自动监控] 使用率 73% 🔴
7. [Phase 4.5] 保存状态到 .claude/state/current-session.md
8. 提示用户执行 /clear

用户: /clear

用户: 请阅读 .claude/state/current-session.md 继续工作

Claude:
1. 读取状态文件，了解进度
2. 继续 Phase 4 实施
3. [Phase 5] 双模型审计
4. 交付完成 ✅
```

---

## 🔧 系统要求

- **Claude Code** 2.0+
- **Python** 3.7+ (Context Monitor)
- **Python** 3.10+ (Code Index)
- **Node.js** 18+ (安装脚本)
- **uv/uvx** (Code Index 依赖)
- **Bash** (Hooks)

---

## 📞 获取帮助

如有问题：
1. 查看 CLAUDE.md 的故障排查部分
2. 运行 `bash test-integrated-setup.sh` 检查配置
3. 查看 `.claude/logs/` 中的日志
4. 在项目中创建 Issue

---

**版本**: 2.0.0 (Integrated)
**最后更新**: 2025-12-17
**维护者**: Project Team

🎉 **享受智能化的开发体验！**
