---
description: 保存会话状态（Phase 4.5）
---

# 保存会话状态

执行 Phase 4.5：上下文管理与状态保存

## 执行步骤

1. **检查上下文使用率**
   - 调用 `check_context_usage` 工具
   - 获取当前使用率

2. **评估状态**
   - < 50% (SAFE)：继续工作
   - 50-70% (WARNING)：提示用户注意使用率
   - **> 70% (HIGH)：立即保存状态并提示 `/clear`**
   - > 85% (CRITICAL)：强制保存并停止工作

3. **保存状态** (带降级方案)
   - **主方案**: 调用 `save_session_state` MCP 工具 (超时 5 秒)
   - **降级方案**: 如 MCP 失败，直接使用 Write 工具写入
   - 保存内容：
     * 已完成任务
     * 当前任务
     * 下一步计划
     * 代码变更摘要
     * 待审计文件
   - 保存路径: `.claude/state/current-session.md`

4. **用户提示与恢复流程**
   - 显示状态文件路径: `.claude/state/current-session.md`
   - **强烈建议执行 `/clear` 清除上下文**
   - 提供恢复提示词:
     ```
     请阅读 .claude/state/current-session.md 了解之前的进度，
     从 [当前阶段] 继续执行
     ```
   - **目标**: 保持纯净上下文，节省 Token，减少幻觉

**输出**：会话状态文件 + 恢复指令
