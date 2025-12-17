# Claude Context Monitor + Integrated Workflow

> 智能化的 Claude Code 开发系统：上下文监控 + 代码检索 + 多模型协作

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)

📖 **[文档导航](./文档导航.md)** - 快速找到你需要的文档

---

## 🎯 核心能力

### Context Monitor（上下文监控）
- ✅ **自动监控** - SessionStart hook 自动捕获会话信息
- ✅ **智能提醒** - 根据使用率主动采取行动
- ✅ **状态保存** - 自动保存会话状态以便恢复

### Code Index MCP（代码检索）
- ✅ **语义搜索** - 自然语言查询代码库
- ✅ **符号索引** - AST 解析，理解代码结构
- ✅ **实时监控** - 自动检测文件变化

### Multi-Model Collaboration（多模型协作）
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

参考 [全局安装指南.md](./全局安装指南.md) 安装 CLAUDE.md 和 Code Index MCP。

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

在对话中输入：
```
请检查当前上下文使用率
```

### 使用

1. 启动 Claude Code：
   ```bash
   claude
   ```

2. 系统自动激活，你会看到：
   ```
   📊 Context monitoring active. Use check_context_usage tool to monitor usage.
   ```

3. 在对话中要求 Claude 检查：
   ```
   请检查当前上下文使用率
   ```

4. Claude 会自动：
   - 每 5-10 个工具调用后检查使用率
   - 根据使用率采取相应行动
   - 在高使用率时保存状态并提示你执行 `/clear`

---

## 📋 系统要求

- **Node.js** 18+ (用于安装脚本)
- **Python** 3.7+ (用于 MCP server)
- **Bash** (用于 hooks，Windows 需要 Git Bash)
- **Claude Code** 2.0+

---

## 📁 文件结构

安装后会创建以下文件（所有文件都在 `.claude` 目录下，保持项目根目录整洁）：

```
your-project/
└── .claude/
    ├── hooks/
    │   └── capture-session-info.sh       # SessionStart hook
    ├── mcp-servers/
    │   └── context-monitor/
    │       └── server.py                  # MCP server
    ├── state/                             # 会话状态目录
    └── settings.local.json                # Hook 和 MCP 配置
```

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
SessionStart Hook 捕获 transcript_path
  ↓
写入 /tmp/claude-session-info.json
  ↓
Claude 定期调用 check_context_usage
  ↓
MCP Server 计算使用率
  ↓
返回状态和建议
  ↓
Claude 根据使用率采取行动：
  - < 50%: 继续工作
  - 50-70%: 注意使用率
  - 70-85%: 准备保存状态
  - > 85%: 立即保存并提示 /clear
```

---

## 🛠️ MCP 工具

### check_context_usage

检查当前会话的上下文使用率。

**输出示例：**
```json
{
  "usage_percent": 65.3,
  "status": "⚠️ WARNING",
  "recommendation": "Context usage is moderate. Consider completing current task soon."
}
```

### save_session_state

保存会话状态到 `.claude/state/current-session.md`。

**使用示例：**
```javascript
save_session_state({
  content: "已完成 Task 1-3，当前在实现用户认证",
  next_steps: "继续 Task 4: JWT token 刷新"
})
```

---

## ⚠️ 重要说明

### 限制

- **无法自动执行 /clear** - 这是 Claude Code 的架构限制，必须由用户手动执行
- **Token 估算不精确** - 使用文件大小估算，可能有 ±10% 的误差
- **需要 Python 3** - MCP server 需要 Python 3 环境

### 最佳实践

1. **信任 Claude 的判断** - 当 Claude 提示保存状态时，立即执行
2. **定期检查** - 在长时间会话中，主动要求 Claude 检查使用率
3. **及时清除** - 不要等到 100% 才清除，70-80% 就应该考虑

---

## 🐛 故障排查

### Hook 没有运行

```bash
# 检查执行权限
ls -l .claude/hooks/capture-session-info.sh

# 手动测试
echo '{"session_id":"test","transcript_path":"/tmp/test.jsonl","cwd":"."}' | \
  bash .claude/hooks/capture-session-info.sh
```

### MCP Server 无法启动

```bash
# 检查 Python
python3 --version

# 手动运行
python3 .claude/mcp-servers/context-monitor/server.py
```

### 更多问题

查看详细文档：`.claude/CONTEXT_MONITORING.md`

---

## 📚 文档

### 核心文档
- **[CLAUDE.md](./CLAUDE.md)** - 完整工作流定义和资源矩阵 ⭐
- **[整合工作流指南.md](./整合工作流指南.md)** - 整合工作流快速指南 ⭐

### 安装和使用
- **[全局安装指南.md](./全局安装指南.md)** - 安装 CLAUDE.md 和 Code Index MCP 到全局
- **[项目级安装指南.md](./项目级安装指南.md)** - 安装 Context Monitor 到项目（必需）

### 详细说明
- [上下文监控详解.md](./上下文监控详解.md) - Context Monitor 详细说明
- [CHANGELOG.md](./CHANGELOG.md) - 版本变更记录

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🙏 致谢

本项目基于 Claude Code 的 Hooks 和 MCP 系统构建。

---

**版本**: 1.0.0
**最后更新**: 2025-12-16
**维护者**: Project Team
