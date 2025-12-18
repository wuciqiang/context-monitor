# Context Monitor 文档中心

## 📚 文档导航

### 核心文档

- **[完整指南](./完整指南.md)** - 系统概述、安装配置、工作流详解、使用指南（推荐从这里开始）
- **[工作流介绍](./工作流介绍.md)** - 详细的工作流系统介绍，适合对外宣传
- **[编码问题解决方案](./编码问题解决方案.md)** - Windows 环境下的编码问题排查和修复

### 安装文档（已整合到完整指南）

以下文档已整合到《完整指南》中，保留作为参考：

- [全局安装指南](./全局安装指南.md) - 全局安装方式
- [项目级安装指南](./项目级安装指南.md) - 项目级安装方式
- [Skills安装指南](./Skills安装指南.md) - Codex/Gemini Skills 安装

### 技术文档（已整合到完整指南）

以下文档已整合到《完整指南》中，保留作为参考：

- [上下文监控详解](./上下文监控详解.md) - 上下文管理机制详解
- [整合工作流指南](./整合工作流指南.md) - 工作流整合说明

## 🚀 快速开始

```bash
# 1. 安装插件
/plugin marketplace add https://github.com/wuciqiang/context-monitor
/plugin install cm

# 2. 开始使用
/cm:start
```

详细说明请参阅 [完整指南](./完整指南.md)。

## 📖 推荐阅读顺序

1. **新用户**：完整指南 → 快速开始
2. **遇到问题**：完整指南 → 故障排除 → 编码问题解决方案
3. **深入了解**：工作流介绍 → 上下文监控详解
4. **对外介绍**：工作流介绍

## 🔧 脚本工具

所有安装和测试脚本位于 `../scripts/` 目录：

- `install-to-project.ps1` / `.sh` - 项目级安装脚本
- `install-global.ps1` / `.sh` - 全局安装脚本
- `fix-encoding.ps1` - Windows 编码修复脚本
- `test-*.sh` - 测试脚本

## 💡 获取帮助

- **GitHub Issues**: https://github.com/wuciqiang/context-monitor/issues
- **Claude Code 文档**: https://docs.anthropic.com/claude-code

---

**最后更新**: 2025-12-18
