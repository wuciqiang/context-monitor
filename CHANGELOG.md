# Changelog

## [1.1.2] - 2025-12-20

### 🐛 修复
- **终端渲染问题** - 移除所有 Emoji 表情符号,解决终端大片空白渲染问题
  - `server.py`: 状态标识从 Emoji 改为纯文本 (SAFE/WARNING/HIGH/CRITICAL)
  - `statusline.py`: 状态图标从 Emoji 改为文本标签 ([OK]/[WARN]/[HIGH]/[CRIT])
  - 提升跨平台兼容性 (Windows/macOS/Linux)

### ✨ 新增
- **自动状态栏配置** - 插件安装后自动配置状态栏显示
  - 在 `plugin.json` 中添加 `statusLine` 配置
  - 无需手动修改 `.claude/settings.json`
  - 重启 Claude Code 即可看到上下文使用率

### 📝 文档
- 更新 README.md,说明状态栏自动配置
- 移除手动配置状态栏的说明

---

## [1.1.1] - 2025-12-19

### 🐛 修复
- 修复 `save_session_state` 工具的 AbortError 问题
- 修复多会话并发时的文件冲突
- 改进 Windows 编码支持

### ✨ 新增
- 添加 `/cm:auto` 快捷命令
- 实现并行多模型调用 (性能提升 40-50%)
- 增强的状态保存机制

---

## [1.1.0] - 2025-12-18

### ✨ 新增
- 快捷命令 `/cm:auto` - 一键完成所有工作流阶段
- 并行多模型调用 - Phase 2 和 Phase 5 支持并行执行
- 增强的状态保存 - 使用 session_id 避免并发冲突

### 🐛 修复
- 修复 `save_session_state` 工具的 AbortError 问题
- 修复多会话并发时的文件冲突
- 改进错误处理和用户反馈

### 📈 性能优化
- 多模型调用并行化：节省 40-50% 时间
- 状态保存优化：添加超时和降级机制
- 文件操作优化：使用唯一文件名避免冲突

---

## [1.0.0] - 2025-12-17

### ✨ 初始版本
- 6 阶段结构化工作流
- 上下文监控和状态保存
- 多模型协作 (Codex + Gemini)
- 双模型审计系统
- MCP 服务器集成
- Claude Code 插件支持
