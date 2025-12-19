---
description: 多模型协作分析（Phase 2）
argument-hint: [task-description]
---

# 多模型协作分析

对任务 "$1" 执行 Phase 2：多模型协作分析

## 执行步骤

1. **上下文检查**
   - 调用 `check_context_usage` 检查使用率
   - 如果 > 70%，简化分析范围或保存状态

2. **并行调用多模型分析** ⚡ 性能优化
   - **Codex（后端/逻辑专家）** - 并行调用
     - 调用 `Skill` 工具，skill 参数为 "collaborating-with-codex"
     - 提供任务描述和相关代码上下文
     - 要求 Codex 分析技术方案和潜在问题

   - **Gemini（前端/UI 专家）** - 并行调用
     - 调用 `Skill` 工具，skill 参数为 "collaborating-with-gemini"
     - 提供任务描述和相关代码上下文
     - 要求 Gemini 分析 UI/UX 方案

   - **重要**：使用单个消息发送多个 Skill 工具调用以实现并行执行
   - **预期提升**：性能提升 40-50%

3. **交叉验证**
   - 整合 Codex 和 Gemini 的分析结果
   - 识别潜在冲突和问题
   - 生成统一的实施计划

4. **用户确认**
   - 展示最终实施计划
   - 等待用户确认后再进入实施阶段

**输出**：经过交叉验证的实施计划

**性能优化**：Codex 和 Gemini 并行调用，相比串行执行节省 40-50% 时间
