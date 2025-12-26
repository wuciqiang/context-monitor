# Context Monitor

> 智能化的 Claude Code 开发工作流系统：上下文监控 + 代码检索 + 多模型协作

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)

🚀 **[快速开始](#快速开始)** | 📋 **[工作流概览](#工作流概览)** | 🎉 **[最新更新](#最新更新v115)**

---

## 核心能力

### 🎯 解决的问题

- ❌ 上下文管理混乱 → ✅ 实时监控 + 自动捕获
- ❌ 工作流不一致 → ✅ 强制执行标准流程
- ❌ 代码搜索低效 → ✅ 自然语言查询 + 深度索引
- ❌ 单一模型局限 → ✅ 多模型协作机制
- ❌ 缺乏质量保障 → ✅ 双模型审计系统

### 🔧 核心组件

- **Claude Code Plugin** - 6 个 slash commands 强制执行工作流
- **Context Monitor MCP** - 通过 Hook 实时捕获上下文使用率
- **Code Index MCP** - 语义搜索和符号索引
- **Multi-Model Skills** - Codex（后端）+ Gemini（前端）协作

---

## 快速开始

### 前置依赖

#### 安装 Multi-Model Skills（可选）

用于 Phase 2 和 Phase 5 的多模型协作：

```bash
# 克隆 skills 仓库
git clone https://github.com/GuDaStudio/skills ~/.claude/skills

# 配置 Codex（后端/逻辑分析）
# 需要配置 Codex API key

# 配置 Gemini（前端/UI 分析）
# 需要配置 Gemini API key
```

**Skills 的作用**:
- ✅ Codex: 后端逻辑分析、代码设计、代码审查
- ✅ Gemini: 前端 UI 分析、文档生成
- ✅ 并行执行提升性能 40-50%

**注意**: Skills 是可选的，如果不安装，工作流会降级为 Claude 单独分析。

### 插件安装（必需）

```bash
# 1. 添加 marketplace
/plugin marketplace add wuciqiang/context-monitor

# 2. 安装插件
/plugin install cm

# 3. 配置状态栏（一键完成）
/cm:setup

# 4. 重启 Claude Code
# 状态栏会显示: ✅ Context: 25.3%
```

**就这么简单!** 插件会自动配置:
- ✅ SessionStart hook (捕获会话信息)
- ✅ PostToolUse hook (实时捕获上下文使用率)
- ✅ MCP 服务器 (提供上下文监控工具)
- ✅ 状态栏显示 (通过 /cm:setup 一键配置)

### ⚠️ 重要：全局配置

**插件安装后，还需要在全局 CLAUDE.md 中添加工作流提示词：**

```bash
# 1. 打开全局配置文件
# Windows: C:\Users\<用户名>\.claude\CLAUDE.md
# macOS/Linux: ~/.claude/CLAUDE.md

# 2. 将本项目的 CLAUDE.md 内容复制到全局文件中
# 或者直接复制文件：
cp ./CLAUDE.md ~/.claude/CLAUDE.md  # macOS/Linux
copy CLAUDE.md %USERPROFILE%\.claude\CLAUDE.md  # Windows
```

**为什么需要全局配置？**
- 插件提供的 slash commands 只是触发器
- 实际的工作流逻辑（Phase 0-5）定义在 CLAUDE.md 中
- 全局配置确保所有项目都能使用统一的工作流

**配置后的效果：**
- ✅ 所有项目自动应用工作流
- ✅ 强制执行 Phase 0-5 流程
- ✅ 自动触发多模型协作
- ✅ 统一的代码质量标准

### 基本使用

#### 🚀 快捷模式（推荐新手）

```bash
# 一键完成所有阶段（自动化工作流）
/cm:auto 实现用户认证功能

# 在关键决策点会暂停等待确认
# 性能提升：并行执行多模型调用，节省 40-50% 时间
```

#### 🎯 专业模式（精细控制）

```bash
# 启动工作流（Phase 0-1）
/cm:start

# 多模型分析（Phase 2）⚡ 并行执行
/cm:analyze 实现用户认证功能

# 任务实施（Phase 3-4）
/cm:implement

# 代码审计（Phase 5）⚡ 并行执行
/cm:audit

# 快速检查上下文
/cm:check

# 保存会话状态
/cm:save-state
```

---

## 工作流概览

```
Phase 0: 初始化检查 → Phase 1: 代码检索 → Phase 2: 多模型分析
    ↓
Phase 3: 原型获取 → Phase 4: 编码实施 → Phase 4.5: 状态保存
    ↓
Phase 5: 双模型审计 → 最终交付
```

### 工作流说明

- **Phase 0-1**: 初始化上下文检查和代码检索
- **Phase 2**: 多模型协作分析（Codex + Gemini 并行）
- **Phase 3-4**: 原型获取和编码实施
- **Phase 4.5**: 自动状态保存
- **Phase 5**: 双模型审计（Codex + Gemini 并行）

### 配置文件

- [CLAUDE.md](./CLAUDE.md) - 工作流定义和使用指南
- [PLUGIN.md](./PLUGIN.md) - 插件说明

---

## 系统要求

- **Python** 3.7+
- **Claude Code** 2.0+

### Windows 用户特别注意

必须配置 UTF-8 编码，否则 Codex/Gemini 会报错：

```powershell
[System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")
```

---

## 上下文监控机制

### 🎯 核心原理

通过 **PostToolUse Hook** 拦截每次工具调用后的 usage 数据，实现**实时监控运行时上下文**。

### 🔧 工作流程

1. **SessionStart Hook**: 捕获会话信息（session_id, transcript_path, cwd）
2. **PostToolUse Hook**: 每次工具调用后自动触发
   - 读取 stdin 的 usage 数据
   - 计算 context_tokens = cache_read + input + cache_creation
   - 保存到临时文件 `claude-current-usage.json`
3. **StatusLine**: 实时读取临时文件显示使用率
4. **MCP Tool**: `/cm:check` 命令读取相同数据

### ✅ 优势

- **准确性**: 使用 Claude API 的实际 usage 数据
- **实时性**: 每次工具调用后自动更新
- **通用性**: 适用于新会话和恢复会话
- **一致性**: 与官方 `/context` 使用相同数据源

### 📊 显示格式

状态栏会根据使用率显示不同图标:
- ✅ < 50%: 安全
- ⚠️ 50-70%: 警告
- 🔶 70-85%: 高使用率
- 🚨 > 85%: 危险

---

## 常见问题

### Q: 插件安装失败？

A: 使用正确的命令格式：
```bash
# 正确格式（简化）
/plugin marketplace add wuciqiang/context-monitor

# 错误格式（不要使用完整 URL）
/plugin marketplace add https://github.com/wuciqiang/context-monitor
```

### Q: PostToolUse Hook 报错找不到文件？

A: 这是因为插件从旧路径安装，需要重新安装：
```bash
# 1. 卸载旧插件
/plugin uninstall cm@context-monitor-marketplace

# 2. 重新安装
/plugin install cm

# 3. 重启 Claude Code
```

**原因**: 插件使用 `${CLAUDE_PLUGIN_ROOT}` 变量动态解析路径，但如果从本地路径安装，路径会被固定。重新从 marketplace 安装可解决此问题。

### Q: 状态栏显示 0% 或 --？

A:
- **显示 --**: PostToolUse Hook 还未触发（会话刚启动）
- **显示 0%**: 使用了旧版本的 statusline.py
- **解决方法**:
  1. 调用任意工具（Read/Write/Bash等）触发 Hook
  2. 确保 settings.json 中 statusLine 路径正确
  3. 重启 Claude Code

### Q: hooks 和 MCP 服务器需要手动配置吗？

A: 不需要！插件安装后会自动配置：
- SessionStart hook 自动捕获会话信息
- PostToolUse hook 自动捕获 usage 数据
- MCP 服务器自动启动提供工具
- 只有 statusline（状态栏显示）需要通过 `/cm:setup` 配置

### Q: Codex/Gemini 编码错误？

A: 配置 UTF-8 编码环境变量（见上方"Windows 用户特别注意"）

### Q: 如何获取详细文档？

A: 详细文档请参考项目中的 `CLAUDE.md` 和 `PLUGIN.md` 文件

---

## 🎉 最新更新（v1.2.0）

### ✨ 核心突破

1. **安全性和可靠性改进** 🎯
   - 修复 PostToolUse Hook 硬编码路径问题
   - 添加所有 Hook 的 timeout 配置
   - 改进错误处理和输入验证
   - 添加 PreCompact 和 SessionEnd Hook

2. **完整依赖说明** 📦
   - Multi-Model Skills 配置说明
   - 系统要求清单

---

## 🎉 历史更新（v1.1.5）

### ✨ 核心突破

1. **Hook 注入机制** 🎯
   - 通过 PostToolUse Hook 实时捕获运行时 usage 数据
   - 完美解决恢复会话无法获取上下文的问题
   - 与官方 `/context` 使用相同数据源，100% 准确

2. **实时上下文监控** ⚡
   - 每次工具调用后自动更新
   - 状态栏实时显示准确使用率
   - 支持所有会话类型（新会话/恢复会话）

3. **自动化配置** 📦
   - SessionStart + PostToolUse 双 Hook 自动配置
   - 无需手动编辑配置文件
   - 一键安装即可使用

### 🐛 修复

- 修复恢复会话显示 0% 的问题
- 修复状态栏路径配置错误
- 移除失效的估算方案

### 📈 技术改进

- 采用 Hook 注入获取运行时数据
- 简化代码逻辑，移除冗余计算
- 提升准确性和可靠性

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

## 致谢

- [Claude Code](https://claude.com/claude-code) - Anthropic 官方 CLI 工具
- [GuDaStudio/skills](https://github.com/GuDaStudio/skills) - 多模型协作技能
- [MCP Servers](https://github.com/modelcontextprotocol/servers) - Code Index MCP

---

**版本**: 1.2.0
**最后更新**: 2025-12-26
**项目地址**: https://github.com/wuciqiang/context-monitor
