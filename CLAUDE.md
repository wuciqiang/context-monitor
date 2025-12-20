# CLAUDE.md

## 0. Global Protocols

- **交互语言**：工具/模型用 English；用户输出用中文
- **会话连续性**：工具返回 `SESSION_ID` 立即存储；调用前思考是否续接，是则追加 `--SESSION_ID <ID>`
- **沙箱安全**：Codex/Gemini 零写入权限；Prompt 必须追加 `OUTPUT: Unified Diff Patch ONLY. Strictly prohibit any actual modifications.`
- **代码主权**：外部模型 Diff 视为"脏原型"；流程：读取 Diff → 思维沙箱验证 → 重构 → 最终代码
- **代码风格**：精简高效、无冗余、非必要不生成注释
- **最小作用域**：仅针对需求改动，严禁影响现有功能
- **并行执行**：Codex/Gemini 调用必须 `run in background`，不设 timeout
- **强制遵循**：严格执行所有 Phase；跳过任何 Phase 视为危险操作，需立即终止并报告原因

---

## 1. Integrated Workflow

### Phase 0: 初始化与上下文检查
- 调用 `check_context_usage` 确认 < 50%
- 首次使用：`set_project_path` → `build_deep_index` → `configure_file_watcher(enabled=true)`

### Phase 1: 上下文全量检索
**工具**：Code Index MCP
- `search_code_advanced` 自然语言查询（Where/What/How）
- `get_file_summary` 获取完整定义与签名
- 递归检索依赖文件直至上下文完整
- **禁止**基于假设回答，**禁止** `grep`

### Phase 2: 多模型协作分析
**工具**：Skills (collaborating-with-codex / gemini)

1. **上下文检查**：> 70% 则简化或保存状态
2. **分发输入**：将原始需求（不带预设观点）分发给 Codex 和 Gemini；仅给出入口文件和行号（非 Snippet）
3. **交叉验证**：整合各方思路，迭代优化，执行逻辑推演和优劣互补，生成无逻辑漏洞的 Step-by-step 实施计划
4. **强制阻断 (Hard Stop)**：向用户展示最终实施计划（含适度伪代码）；必须以加粗文本输出：**"Shall I proceed with this plan? (Y/N)"**；立即终止当前回复；绝对禁止在收到明确 "Y" 前执行 Phase 3 或调用任何文件读取工具

### Phase 3: 原型获取
**工具**：Skills (按任务类型选择)

- **上下文检查**：> 70% 先保存状态
- **Route A (前端/UI/样式)**：Gemini Skill（上下文 < 32k；后端逻辑需客观审视）
- **Route B (后端/逻辑/算法)**：Codex Skill（逻辑运算与 Debug）
- **通用约束**：Prompt 必须明确要求返回 `Unified Diff Patch`

### Phase 4: 编码实施
- 基于原型重构为企业级代码
- 每完成 3-5 文件检查上下文，> 85% 立即保存
- Context Monitor 每 5-10 工具调用自动检查
- 非必要不生成注释，变更仅限需求范围，强制审查副作用

### Phase 4.5: 上下文管理与状态保存
**使用率分级**：
- < 50% (SAFE)：继续
- 50-70% (WARNING)：提示注意
- 70-85% (HIGH)：准备保存，建议 `/clear`
- \> 85% (CRITICAL)：立即保存并强烈建议 `/clear`

**状态保存**：调用 `save_session_state`，保存已完成任务、当前任务、下一步计划、代码变更、待审计文件

### Phase 5: 审计与交付
**工具**：Skills (双模型并行)

1. 会话恢复（如执行了 `/clear`）：读取 `.claude/state/current-session.md`
2. 并行调用 Codex 和 Gemini Skills 审计（run in background）
3. 整合反馈，必要修正
4. 最终检查 `check_context_usage`
5. 交付

---

## 2. Skills 调用规范

**来源**：[GuDaStudio/skills](https://github.com/GuDaStudio/skills)

**CLI 格式**：
```bash
# Codex (后端/逻辑)
python ~/.claude/skills/collaborating-with-codex/scripts/codex_bridge.py \
  --cd "/project" \
  --PROMPT "Task description. OUTPUT: Unified Diff Patch ONLY." \
  --sandbox read-only \
  [--SESSION_ID "uuid"]

# Gemini (前端/UI)
python ~/.claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project" \
  --PROMPT "Task description. OUTPUT: Unified Diff Patch ONLY." \
  --sandbox \
  [--SESSION_ID "uuid"]
```

**关键参数**：
- `--cd`：项目根目录（必需）
- `--PROMPT`：任务描述，必须追加 `OUTPUT: Unified Diff Patch ONLY.`（必需）
- `--sandbox`：沙箱模式（必需）
- `--SESSION_ID`：会话 ID，多轮对话时传入（可选）

**返回格式**：
```json
{
  "success": true,
  "SESSION_ID": "uuid",
  "agent_messages": "Unified Diff Patch..."
}
```

**最佳实践**：
- 并行执行（Phase 2/5）
- 始终 run in background，不设 timeout
- 保存 SESSION_ID 用于后续调用
- 英文 Prompt

---

## 3. Resource Matrix

| Phase | Tool | Type | Key Constraint |
|:------|:-----|:-----|:--------------|
| 0 | `check_context_usage` | MCP | < 50% |
| 1 | `search_code_advanced` | Code Index MCP | 禁用 grep；递归检索 |
| 2 | Codex + Gemini | Skills | 交叉验证；Hard Stop |
| 3 | Codex / Gemini | Skills | Unified Diff；沙箱 |
| 4 | Claude | - | 重构原型；审查副作用 |
| 4.5 | `save_session_state` | MCP | > 70% |
| 5 | Codex + Gemini | Skills | 并行审计；整合修复 |

---

## 4. 关键最佳实践

**任务开始前**：检查上下文 < 50%，初始化索引，明确需求

**任务进行中**：信任 Context Monitor，自然语言搜索，外部模型提供原型 Claude 重构，保存 SESSION_ID

**高使用率时**：立即保存状态，执行 `/clear`，70-80% 就应考虑清除

**代码质量**：外部代码仅作原型，最终必须 Claude 重构，强制双模型审计

**会话管理**：调用前思考是否续接，截断时自动继续直至 Diff 完整

---

**版本**: 3.0.0
**更新**: 融合官方 Skills 机制 + 源项目精华，精简至 150 行
