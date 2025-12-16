# 安装指南
# Installation Guide

> 如何将 Claude Context Monitor 安装到你的项目

---

## 📦 方式 1：使用 npm（推荐）

### 步骤 1：进入项目目录

```bash
cd /path/to/your-project
```

### 步骤 2：确保有 package.json

```bash
# 如果项目还没有 package.json
npm init -y
```

### 步骤 3：安装系统

```bash
# 从本地安装（开发阶段）
npm install --save-dev /path/to/claude-context-monitor/.claude

# 或从 npm 安装（发布后）
npm install --save-dev @claude/context-monitor
```

### 步骤 4：初始化

```bash
npm run init
```

你会看到：

```
🚀 Claude Context Monitor - Initialization
============================================================

🔍 Checking prerequisites...
✅ Python 3 found
✅ Bash found

📁 Creating directories...
✅ Created .claude
✅ Created .claude/hooks
✅ Created .claude/mcp-servers
✅ Created .claude/state

📄 Copying files...
✅ Copied .claude/hooks/capture-session-info.sh
✅ Copied .claude/mcp-servers/context-monitor/server.py
✅ Copied .claude/CONTEXT_MONITORING.md

⚙️  Updating settings...
✅ Updated settings.local.json

📝 Updating CLAUDE.md...
✅ Updated CLAUDE.md with context management instructions

============================================================
✅ Context Monitoring System Installed Successfully!
============================================================
```

### 步骤 5：测试

```bash
npm run test
```

---

## 📋 方式 2：手动安装

### 步骤 1：复制文件

```bash
# 复制整个 .claude 目录
cp -r /path/to/claude-context-monitor/.claude /path/to/your-project/

# 进入项目目录
cd /path/to/your-project
```

### 步骤 2：运行初始化脚本

```bash
node .claude/scripts/init.js
```

### 步骤 3：设置执行权限（Unix-like 系统）

```bash
chmod +x .claude/hooks/capture-session-info.sh
chmod +x .claude/mcp-servers/context-monitor/server.py
chmod +x .claude/test-context-monitor.sh
```

### 步骤 4：测试

```bash
bash .claude/test-context-monitor.sh
```

---

## 🔧 方式 3：Git Submodule（团队协作）

### 步骤 1：添加 submodule

```bash
cd /path/to/your-project
git submodule add https://github.com/your-org/claude-context-monitor.git .claude-monitor
```

### 步骤 2：创建符号链接

```bash
ln -s .claude-monitor/.claude .claude
```

### 步骤 3：初始化

```bash
node .claude/scripts/init.js
```

### 团队成员克隆项目

```bash
git clone --recursive https://github.com/your-org/your-project.git
cd your-project
node .claude/scripts/init.js
```

---

## ✅ 验证安装

### 1. 检查文件结构

```bash
ls -la .claude/
```

应该看到：

```
.claude/
├── hooks/
│   └── capture-session-info.sh
├── mcp-servers/
│   └── context-monitor/
│       └── server.py
├── state/
├── settings.local.json
├── CONTEXT_MONITORING.md
└── test-context-monitor.sh
```

### 2. 运行测试

```bash
npm run test
# 或
bash .claude/test-context-monitor.sh
```

### 3. 检查配置

```bash
cat .claude/settings.local.json
```

应该包含：

```json
{
  "hooks": {
    "SessionStart": [...]
  },
  "mcpServers": {
    "context-monitor": {...}
  }
}
```

### 4. 检查 CLAUDE.md

```bash
grep "上下文管理" CLAUDE.md
```

应该找到上下文管理部分。

---

## 🚀 开始使用

### 1. 启动 Claude Code

```bash
claude
```

### 2. 验证系统激活

你应该看到：

```
📊 Context monitoring active. Use check_context_usage tool to monitor usage.
```

### 3. 测试监控

在对话中输入：

```
请检查当前上下文使用率
```

Claude 会调用 `check_context_usage` 工具并返回结果。

---

## 🗑️ 卸载

如果需要卸载系统：

```bash
npm run uninstall
```

或手动删除：

```bash
rm -rf .claude/hooks/capture-session-info.sh
rm -rf .claude/mcp-servers/context-monitor/
rm -rf .claude/CONTEXT_MONITORING.md
rm -rf .claude/test-context-monitor.sh
```

然后手动编辑 `.claude/settings.local.json` 移除相关配置。

---

## 🐛 常见问题

### Q: Windows 上 bash 命令不可用

**A**: 安装 Git for Windows，它包含 Git Bash：
https://git-scm.com/download/win

### Q: Python 3 找不到

**A**: 安装 Python 3：
- macOS: `brew install python3`
- Ubuntu: `sudo apt install python3`
- Windows: https://www.python.org/downloads/

### Q: npm run init 失败

**A**: 检查：
1. Node.js 版本 >= 18
2. Python 3 已安装
3. 有写入权限

### Q: Hook 没有运行

**A**: 检查执行权限：
```bash
chmod +x .claude/hooks/capture-session-info.sh
```

---

## 📚 下一步

- 阅读 [使用文档](.claude/CONTEXT_MONITORING.md)
- 查看 [工作流指南](./STATELESS_WORKFLOW_GUIDE.md)
- 了解 [快速开始](./QUICK_START.md)

---

**需要帮助？** 查看 [故障排查](.claude/CONTEXT_MONITORING.md#故障排查) 或提交 Issue。
