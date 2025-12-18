# Context Monitor

> 智能化的 Claude Code 开发工作流系统：上下文监控 + 代码检索 + 多模型协作

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)

📖 **[完整文档](./docs/)** | 🚀 **[快速开始](#快速开始)** | 🐛 **[故障排除](./docs/完整指南.md#故障排除)**

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

```bash
# 启动工作流（Phase 0-1）
/cm:start

# 多模型分析（Phase 2）
/cm:analyze 实现用户认证功能

# 任务实施（Phase 3-4）
/cm:implement

# 代码审计（Phase 5）
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

详细说明请参阅 [完整指南](./docs/完整指南.md#工作流详解)。

---

## 文档导航

### 核心文档

- **[完整指南](./docs/完整指南.md)** - 系统概述、安装配置、工作流详解、使用指南（推荐）
- **[工作流介绍](./docs/工作流介绍.md)** - 详细的系统介绍，适合对外宣传
- **[编码问题解决方案](./docs/编码问题解决方案.md)** - Windows 环境编码问题修复

### 参考文档

- [全局安装指南](./docs/全局安装指南.md)
- [项目级安装指南](./docs/项目级安装指南.md)
- [Skills安装指南](./docs/Skills安装指南.md)
- [上下文监控详解](./docs/上下文监控详解.md)
- [整合工作流指南](./docs/整合工作流指南.md)

### 配置文件

- [CLAUDE.md](./CLAUDE.md) - 工作流定义
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

详见 [编码问题解决方案](./docs/编码问题解决方案.md)。

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
│   ├── check.md
│   └── save-state.md
├── docs/                    # 文档
│   ├── README.md
│   ├── 完整指南.md
│   ├── 工作流介绍.md
│   └── 编码问题解决方案.md
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

A: 参见 [编码问题解决方案](./docs/编码问题解决方案.md)

### Q: 上下文检查失败？

A: 确保 MCP 服务器正确配置，重启 Claude Code

更多问题请参阅 [完整指南 - 故障排除](./docs/完整指南.md#故障排除)。

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

**版本**: 1.0.2
**最后更新**: 2025-12-18
**项目地址**: https://github.com/wuciqiang/context-monitor
