# Context Monitor Plugin

> Claude Code 插件：智能化的开发工作流系统

## 🎯 功能

Context Monitor 插件为 Claude Code 提供完整的开发工作流支持：

- 📊 **上下文监控** - 实时跟踪 token 使用率
- 🔍 **代码检索** - 智能搜索和理解代码库
- 🤝 **多模型协作** - Codex + Gemini 交叉验证
- ✅ **任务管理** - 原子级任务拆分和跟踪
- 💾 **状态保存** - 长时间任务的中断恢复

## 📦 安装

### 方法 1：从本地安装（开发/测试）

1. 克隆仓库：
   ```bash
   git clone https://github.com/your-org/context-monitor.git
   cd context-monitor
   ```

2. 创建本地 marketplace：
   ```bash
   mkdir -p .test-marketplace
   cat > .test-marketplace/marketplace.json << 'EOF'
   {
     "name": "test-marketplace",
     "owner": { "name": "Test" },
     "plugins": [
       {
         "name": "context-monitor",
         "source": "./",
         "description": "Context Monitor Plugin"
       }
     ]
   }
   EOF
   ```

3. 在 Claude Code 中安装：
   ```
   /plugin marketplace add ./.test-marketplace
   /plugin install context-monitor@test-marketplace
   ```

### 方法 2：从 GitHub 安装（推荐）

```
/plugin marketplace add https://github.com/your-org/context-monitor
/plugin install context-monitor
```

## 🚀 使用

### 完整工作流

```
# 1. 启动工作流（Phase 0-1）
/context-monitor:start

# 2. 多模型协作分析（Phase 2）
/context-monitor:analyze 实现用户认证功能

# 3. 任务拆分与实施（Phase 3-4）
/context-monitor:implement

# 4. 代码审计（Phase 5）
/context-monitor:audit
```

### 快捷命令

```
# 快速检查上下文
/context-monitor:check

# 保存会话状态
/context-monitor:save-state
```

## 📋 命令详解

### `/context-monitor:start`
启动完整工作流，执行：
- 检查上下文使用率
- 初始化代码索引
- 搜索相关代码
- 总结代码上下文

### `/context-monitor:analyze [task]`
多模型协作分析，执行：
- 调用 Codex 进行后端分析
- 调用 Gemini 进行前端分析
- 交叉验证结果
- 生成实施计划

### `/context-monitor:implement`
任务拆分与实施，执行：
- 获取原型代码
- 拆分为原子任务
- 逐步实施
- 监控上下文使用率

### `/context-monitor:audit`
代码审计与交付，执行：
- Codex + Gemini 双模型审计
- 整合反馈
- 修复问题
- 生成审计报告

### `/context-monitor:check`
快速检查上下文使用率

### `/context-monitor:save-state`
保存当前会话状态

## 🔧 配置

插件需要以下组件：

1. **MCP Server**（必需）
   - 在项目根目录创建 `.mcp.json`
   - 配置 context-monitor MCP server

2. **Skills**（可选）
   - collaborating-with-codex
   - collaborating-with-gemini

3. **Code Index**（推荐）
   - code-index MCP server

详细配置请参考 [项目级安装指南](./项目级安装指南.md)

## 📚 工作流说明

### Phase 0: 初始化与上下文检查
- 检查上下文使用率
- 初始化代码索引

### Phase 1: 上下文全量检索
- 搜索相关代码
- 获取完整定义

### Phase 2: 多模型协作分析
- Codex 后端分析
- Gemini 前端分析
- 交叉验证

### Phase 3: 原型获取
- 选择合适的模型
- 获取原型代码

### Phase 4: 编码实施
- 任务原子化
- 逐步实施
- 上下文监控

### Phase 4.5: 上下文管理
- 保存会话状态
- 提示清除上下文

### Phase 5: 审计与交付
- 双模型审计
- 整合修复
- 最终交付

## 🐛 故障排查

### Q: 命令不可用

**A**: 确认插件已安装：
```
/plugin list
```

如果未安装，重新安装插件。

### Q: MCP server 工具不可用

**A**: 确认 `.mcp.json` 在项目根目录，并重启 Claude Code。

### Q: Skills 不可用

**A**: Skills 是可选的。如果不使用多模型协作，可以跳过 Phase 2。

## 📄 License

MIT License

## 🙏 致谢

- [Claude Code](https://claude.com/claude-code)
- [GuDaStudio/skills](https://github.com/GuDaStudio/skills)
