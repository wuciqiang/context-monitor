# Claude Context Monitor

> 半自动化的 Claude Code 上下文使用率监控系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)

---

## 🎯 功能特性

- ✅ **自动监控** - SessionStart hook 自动捕获会话信息
- ✅ **智能提醒** - Claude 根据使用率主动采取行动
- ✅ **状态保存** - 自动保存会话状态以便恢复
- ✅ **简单安装** - 一条命令完成安装
- ✅ **跨项目** - 可安装到任何 Claude Code 项目

---

## 🚀 快速开始

### 安装

在你的项目根目录运行：

```bash
# 方式 1: 使用 npm（推荐）
cd /path/to/your-project
npm init -y  # 如果项目还没有 package.json
npm install --save-dev @claude/context-monitor
npm run init

# 方式 2: 手动复制
cp -r /path/to/claude-context-monitor/.claude /path/to/your-project/
cd /path/to/your-project
node .claude/scripts/init.js
```

### 测试

```bash
npm run test
# 或
bash .claude/test-context-monitor.sh
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

安装后会创建以下文件：

```
your-project/
├── .claude/
│   ├── hooks/
│   │   └── capture-session-info.sh       # SessionStart hook
│   ├── mcp-servers/
│   │   └── context-monitor/
│   │       └── server.py                  # MCP server
│   ├── state/                             # 会话状态目录
│   ├── settings.local.json                # Hook 和 MCP 配置
│   ├── CONTEXT_MONITORING.md              # 详细文档
│   └── test-context-monitor.sh            # 测试脚本
└── CLAUDE.md                              # 包含上下文管理指令
```

---

## 🔧 可用命令

```bash
# 初始化系统
npm run init

# 测试系统
npm run test

# 卸载系统
npm run uninstall
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

- [完整文档](.claude/CONTEXT_MONITORING.md) - 详细使用说明
- [工作流指南](./STATELESS_WORKFLOW_GUIDE.md) - 无状态工作流
- [快速开始](./QUICK_START.md) - 5分钟上手

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
