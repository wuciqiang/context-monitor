# Claude Context Monitor + Integrated Workflow

> 智能化的 Claude Code 开发系统：上下文监控 + 代码检索 + 多模型协作

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)

📖 **[文档导航](./文档导航.md)** - 快速找到你需要的文档

---

## 🎯 核心能力

### Context Monitor（上下文监控）
- ✅ **实时监控** - MCP server 提供 `check_context_usage` 工具
- ✅ **智能提醒** - 根据使用率主动采取行动
- ✅ **状态保存** - 自动保存会话状态以便恢复
- ⚠️ **SessionStart Hook** - 在 macOS/Linux 上自动触发，Windows 上需手动调用

### Code Index MCP（代码检索）
- ✅ **语义搜索** - 自然语言查询代码库
- ✅ **符号索引** - AST 解析，理解代码结构
- ✅ **实时监控** - 自动检测文件变化

### Multi-Model Collaboration（多模型协作）
基于 [GuDaStudio/skills](https://github.com/GuDaStudio/skills) 实现：
- ✅ **Codex 集成** - 后端逻辑和算法分析
- ✅ **Gemini 集成** - 前端 UI 和样式设计
- ✅ **交叉验证** - 双模型审计确保质量

### Integrated Workflow（整合工作流）
- ✅ **资源感知** - 上下文检查点贯穿全流程
- ✅ **智能编排** - 自动协调多个工具和模型
- ✅ **状态恢复** - 支持长时间任务的中断恢复

---

## 🚀 快速开始

### 安装

**步骤 1: 全局安装（一次性）**

参考 [全局安装指南.md](./全局安装指南.md) 安装：
- CLAUDE.md（工作流定义）
- Code Index MCP（代码检索）
- Multi-Model Skills（Codex + Gemini，可选）

**步骤 2: 项目级安装（每个项目）**

```bash
# Windows (PowerShell)
cd F:\LayaAir-GitHub\context-monitor
.\install-to-project.ps1

# macOS / Linux / Git Bash
cd /path/to/context-monitor
./install-to-project.sh
```

详细说明请参考 [项目级安装指南.md](./项目级安装指南.md)

### 测试

```bash
cd /path/to/your-project
claude
```

首次启动会提示批准 `context-monitor` MCP server，点击"批准"继续。

在对话中输入：
```
请检查当前上下文使用率
```

预期输出：
```json
{
  "usage_percent": 15.3,
  "status": "✅ SAFE",
  "recommendation": "Context usage is healthy. Continue working normally."
}
```

---

## 📋 系统要求

- **Node.js** 18+ (用于安装脚本)
- **Python** 3.7+ (用于 MCP server)
- **Claude Code** 2.0+
- **Git Bash** (Windows 用户，用于运行 .sh 脚本)

---

## 📁 文件结构

安装后会创建以下文件：

```
your-project/
├── .mcp.json                        # MCP server 配置（项目根目录）
└── .claude/
    ├── hooks/
    │   └── capture-session-info.py  # SessionStart hook
    ├── mcp-servers/
    │   └── context-monitor/
    │       └── server.py            # MCP server
    ├── state/                       # 会话状态目录
    └── settings.local.json          # Hook 配置
```

**重要说明**：
- `.mcp.json` 必须放在项目根目录，不是 `.claude` 文件夹下
- 所有其他文件都在 `.claude` 目录下，保持项目根目录整洁

---

## 🔧 安装脚本

```bash
# 项目级安装（交互式）
./install-to-project.sh              # macOS/Linux/Git Bash
.\install-to-project.ps1             # Windows PowerShell

# 项目级安装（指定路径）
./install-to-project.sh /path/to/project
.\install-to-project.ps1 -TargetDir "D:\project"
```

---

## 📊 工作原理

```
会话开始
  ↓
SessionStart Hook 捕获 transcript_path (macOS/Linux)
  ↓
写入 /tmp/claude-session-info.json
  ↓
Claude 调用 check_context_usage 工具
  ↓
MCP Server 读取 session info 和 transcript
  ↓
计算使用率并返回建议
  ↓
Claude 根据建议采取行动
```

**Windows 用户注意**：
- SessionStart hook 在 Windows 上不工作（[已知 bug](https://github.com/anthropics/claude-code/issues/14219)）
- 需要在 CLAUDE.md 中添加强制指令，让 Claude 主动调用 `check_context_usage`
- 或者手动提醒 Claude 检查上下文使用率

---

## 🐛 故障排查

### Q: Windows 上 SessionStart hook 不执行

**A**: 这是 Claude Code 在 Windows 上的已知 bug ([Issue #14219](https://github.com/anthropics/claude-code/issues/14219))。

**Workaround**: 在 CLAUDE.md 中添加强制指令：
```markdown
- **会话启动强制检查**：每次会话开始（包括 /resume 后）必须立即调用 `check_context_usage` 检查上下文使用率，无需等待用户请求。这是强制性的第一步操作。
```

### Q: MCP server 工具不可用

**A**: 检查：
1. `.mcp.json` 是否在项目根目录（不是 `.claude` 文件夹下）
2. 重启 Claude Code
3. 首次使用时批准 MCP server

### Q: Python 找不到

**A**: 安装 Python 3：
- macOS: `brew install python3`
- Ubuntu: `sudo apt install python3`
- Windows: https://www.python.org/downloads/

Windows 用户确保 Python 在 PATH 中：
```powershell
python --version
```

### 更多问题

参考 [项目级安装指南.md](./项目级安装指南.md) 的故障排查部分。

---

## 📚 文档

- **[文档导航.md](./文档导航.md)** - 快速找到你需要的文档
- **[项目级安装指南.md](./项目级安装指南.md)** - 详细安装说明
- **[全局安装指南.md](./全局安装指南.md)** - 全局组件安装
- **[上下文监控详解.md](./上下文监控详解.md)** - 深入理解原理
- **[整合工作流指南.md](./整合工作流指南.md)** - 使用指南
- **[CLAUDE.md](./CLAUDE.md)** - 完整工作流定义
- **[CHANGELOG.md](./CHANGELOG.md)** - 版本变更记录

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 License

MIT License - 详见 [LICENSE](./LICENSE) 文件

---

## 🙏 致谢

- [Claude Code](https://claude.com/claude-code) - Anthropic 的官方 CLI 工具
- [GuDaStudio/skills](https://github.com/GuDaStudio/skills) - 多模型协作技能
- [code-index-mcp](https://github.com/modelcontextprotocol/servers/tree/main/src/code-index) - 代码检索 MCP server
