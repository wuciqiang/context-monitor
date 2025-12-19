# Context Monitor

> 智能化的 Claude Code 开发工作流系统：上下文监控 + 代码检索 + 多模型协作

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)

🚀 **[快速开始](#快速开始)** | 📋 **[工作流概览](#工作流概览)** | 🎉 **[最新更新](#最新更新v110)**

---

## 核心能力

### 🎯 解决的问题

- ❌ 上下文管理混乱 → ✅ 自动监控 + 状态保存
- ❌ 工作流不一致 → ✅ 强制执行标准流程
- ❌ 代码搜索低效 → ✅ 自然语言查询 + 深度索引
- ❌ 单一模型局限 → ✅ 多模型协作机制
- ❌ 缺乏质量保障 → ✅ 双模型审计系统

### 🔧 核心组件

- **Claude Code Plugin** - 6 个 slash commands 强制执行工作流
- **Context Monitor MCP** - 实时监控上下文使用率
- **Code Index MCP** - 语义搜索和符号索引
- **Multi-Model Skills** - Codex（后端）+ Gemini（前端）协作

---

## 快速开始

### 插件安装（推荐）

```bash
# 1. 添加 marketplace
/plugin marketplace add https://github.com/wuciqiang/context-monitor

# 2. 安装插件
/plugin install cm

# 3. 验证安装
/cm:check
```

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

- **Node.js** 18+
- **Python** 3.7+
- **Claude Code** 2.0+

### Windows 用户特别注意

必须配置 UTF-8 编码，否则 Codex/Gemini 会报错：

```powershell
[System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")
```

---

## 项目结构

```
context-monitor/
├── .claude-plugin/          # 插件配置
│   ├── plugin.json
│   └── marketplace.json
├── commands/                # Slash commands
│   ├── start.md
│   ├── analyze.md
│   ├── implement.md
│   ├── audit.md
│   ├── auto.md             # 新增：自动化工作流
│   ├── check.md
│   └── save-state.md
├── scripts/                 # 安装和测试脚本
│   ├── install-to-project.ps1
│   ├── install-to-project.sh
│   ├── install-global.ps1
│   ├── install-global.sh
│   └── fix-encoding.ps1
├── templates/               # 配置模板
├── workflows/               # 工作流定义
├── CLAUDE.md               # 工作流定义
├── PLUGIN.md               # 插件说明
└── README.md               # 本文件
```

---

## 常见问题

### Q: 插件命令不可用？

A: 检查插件是否正确安装：
```bash
/plugin list
```

### Q: Codex/Gemini 编码错误？

A: 配置 UTF-8 编码环境变量（见上方"Windows 用户特别注意"）

### Q: 上下文检查失败？

A: 确保 MCP 服务器正确配置，重启 Claude Code

### Q: 如何获取详细文档？

A: 详细文档请参考项目中的 `CLAUDE.md` 和 `PLUGIN.md` 文件

---

## 🎉 最新更新（v1.1.0）

### ✨ 新功能

1. **`/cm:auto` 快捷命令** 🚀
   - 一键完成所有工作流阶段
   - 在关键决策点自动暂停确认
   - 降低学习成本，新手友好

2. **并行多模型调用** ⚡
   - Phase 2 分析和 Phase 5 审计支持并行执行
   - 性能提升 40-50%
   - Codex 和 Gemini 同时工作

3. **增强的状态保存** 🛡️
   - 使用 session_id 避免并发冲突
   - 添加降级方案（临时目录备份）
   - 详细的错误处理和日志

### 🐛 修复

- 修复 `save_session_state` 工具的 AbortError 问题
- 修复多会话并发时的文件冲突
- 改进错误处理和用户反馈

### 📈 性能优化

- 多模型调用并行化：节省 40-50% 时间
- 状态保存优化：添加超时和降级机制
- 文件操作优化：使用唯一文件名避免冲突

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

**版本**: 1.1.0
**最后更新**: 2025-12-19
**项目地址**: https://github.com/wuciqiang/context-monitor
