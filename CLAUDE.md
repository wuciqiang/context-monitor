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

### Phase 0: 初始化与需求确认
**目标**: 检查环境、明确需求、创建Spec文档

1. **上下文检查** (必需)
   - 调用 `check_context_usage` 确认 < 50%
   - 首次使用: `set_project_path` → `build_deep_index` → `configure_file_watcher(enabled=true)`

2. **需求确认** (必需)
   - 使用 `AskUserQuestion` 询问用户偏好:
     * 问题1: "是否为此功能生成文档?"
       - 选项: "是 - 生成模块文档" / "否 - 仅代码"
     * 问题2: "是否执行测试?"
       - 选项: "是 - 运行测试套件" / "否 - 跳过测试"
   - 记录用户选择用于Phase 5

3. **创建Spec文档** (必需)
   - 创建 `.claude/specs/active/[feature-name]/spec.md`
   - 创建 `.claude/specs/active/[feature-name]/context.json`
   - 初始化任务清单结构

### Phase 1: 上下文全量检索
**工具**: Code Index MCP
- `search_code_advanced` 自然语言查询 (Where/What/How)
- `get_file_summary` 获取完整定义与签名
- 递归检索依赖文件直至上下文完整
- **禁止**基于假设回答, **禁止** `grep`

### Phase 2: 多模型协作分析与任务拆解
**工具**: Skills (collaborating-with-codex / gemini)

1. **上下文检查**: > 70% 则简化或保存状态

2. **并行分析** (必需)
   - 并行调用 Codex 和 Gemini (run in background)
   - 分发原始需求 (不带预设观点)
   - 仅给出入口文件和行号 (非 Snippet)

3. **交叉验证与任务拆解** (必需)
   - 整合各方思路, 执行逻辑推演
   - 生成任务拆解 (2-8个原子任务)
   - 分析任务依赖, 划分并行组和串行组
   - 格式:
     ```
     并行组1: T001, T002 (独立任务)
     串行组2: T003 (依赖并行组1)
     并行组3: T004, T005 (依赖串行组2)
     ```

4. **更新Spec文档** (必需)
   - 将任务清单写入 `spec.md`
   - 记录每个任务的: 描述、文件范围、SubAgent类型、依赖关系

5. **用户确认任务拆解** (必需)
   - 使用 `AskUserQuestion` 展示任务拆解
   - 选项: "确认并执行" / "需要调整"
   - 如需调整: 询问调整方式 → 更新Spec → 重新确认

6. **强制阻断 (Hard Stop)**
   - 向用户展示最终实施计划 (含适度伪代码)
   - 必须以加粗文本输出: **"Shall I proceed with this plan? (Y/N)"**
   - 立即终止当前回复
   - 绝对禁止在收到明确 "Y" 前执行 Phase 3

### Phase 3: 任务级设计
**工具**: SubAgent (task-designer) 或 Skills (Codex)

**对每个任务执行** (按并行/串行组顺序):

1. **任务设计** (必需)
   - **优先**: 使用 task-designer SubAgent
     ```typescript
     Task({
       subagent_type: "task-designer",
       description: "设计任务 T001",
       prompt: "任务 T001: [描述]\n设计实现方案..."
     })
     ```
   - **降级**: 如 SubAgent 不可用,调用 Codex Skill
   - 返回: 技术方案、文件修改、API设计、风险点
   - 保存设计要点到 `spec.md` 对应任务

2. **更新Spec状态** (必需)
   - 标记任务状态: `pending` → `in_progress`
   - 记录分配的 SubAgent ID

### Phase 4: 并行/串行实施
**执行策略**: 按组执行, 组内并行, 组间串行

**对每个任务执行**:

1. **代码实施** (必需)
   - **优先**: 使用 code-implementer SubAgent
     ```typescript
     // 并行组: 单消息多个 Task 调用
     [
       Task({
         subagent_type: "code-implementer",
         description: "实施任务 T001",
         prompt: "基于设计方案实施 T001...\n设计方案: [task-designer输出]"
       }),
       Task({
         subagent_type: "code-implementer",
         description: "实施任务 T002",
         prompt: "基于设计方案实施 T002...\n设计方案: [task-designer输出]"
       })
     ]

     // 串行组: 逐个执行
     Task({
       subagent_type: "code-implementer",
       description: "实施任务 T003",
       prompt: "基于设计方案实施 T003..."
     })
     ```
   - **降级**: 如 SubAgent 不可用,使用 general-purpose 或 Codex Skill
   - 传递 task-designer 的设计方案
   - 收集修改的文件列表

2. **代码审查** (必需)
   - **优先**: 使用 code-reviewer SubAgent
     ```typescript
     Task({
       subagent_type: "code-reviewer",
       description: "审查任务 T001",
       prompt: "审查 T001 的代码实施...\n修改文件: [列表]\n设计方案: [原始设计]"
     })
     ```
   - **降级**: 如 SubAgent 不可用,调用 Codex Skill
   - 5+类别评估:
     * 可维护性
     * 性能
     * 安全性 (SQL注入/XSS/命令注入)
     * 风格一致性
     * 文档完整性
   - 问题分级: Critical/High/Medium/Low
   - 评分: 0-100

3. **修复循环** (如需要)
   - Critical/High问题: 立即修复
   - Medium/Low问题: 询问用户是否修复
   - 使用 code-implementer SubAgent 修复
   - 最多2轮 "修复 → 审查" 循环
   - 评分 ≥ 90% 且无 Critical/High 问题才通过

4. **更新Spec状态** (必需)
   - 标记任务: `in_progress` → `completed`
   - 记录: 修改文件、完成时间、审查结果
   - 更新 checkbox: `- [ ]` → `- [x]`

5. **上下文管理** (自动)
   - 每完成1个任务检查上下文
   - > 70%: 保存状态 → 建议 `/clear`
   - Context Monitor 每 5-10 工具调用自动检查

### Phase 4.5: 上下文管理与状态保存
**使用率分级**:
- < 50% (SAFE): 继续
- 50-70% (WARNING): 提示注意
- 70-85% (HIGH): 准备保存, 建议 `/clear`
- \> 85% (CRITICAL): 立即保存并强烈建议 `/clear`

**状态保存**: 调用 `save_session_state`, 保存已完成任务、当前任务、下一步计划、代码变更、待审计文件

### Phase 5: 审计、文档与归档
**工具**: Skills (双模型并行)

1. **会话恢复** (如执行了 `/clear`)
   - 读取 `.claude/state/current-session.md`

2. **双模型审计** (必需)
   - 并行调用 Codex 和 Gemini 审计 (run in background)
   - 整合反馈, 必要修正
   - 记录审查结果到 `spec.md`

3. **可选: 文档生成** (基于Phase 0选择)
   - 如用户启用文档生成:
     * 调用 Gemini 生成文档
     * 创建 `docs/[feature-name]/` 目录
     * 生成: overview.md, api.md, usage.md
     * 记录文档路径到 `spec.md`

4. **可选: 测试执行** (基于Phase 0选择)
   - 如用户启用测试:
     * 运行测试套件
     * 记录测试结果和覆盖率
     * 测试失败: 修复 → 重新测试

5. **归档Spec** (必需)
   - 更新 `spec.md` 元数据:
     * status: completed
     * completed_at: [时间戳]
     * 总任务数、成功数
     * 文档生成状态
     * 测试通过状态
   - 移动到 `.claude/specs/completed/[feature-name]/`

6. **最终检查**
   - `check_context_usage`
   - 生成完成摘要

7. **交付**

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
| 0 | `check_context_usage` + `AskUserQuestion` + Write | MCP + Built-in | < 50%; 创建Spec |
| 1 | `search_code_advanced` | Code Index MCP | 禁用 grep; 递归检索 |
| 2 | Codex + Gemini + `AskUserQuestion` + Edit | Skills + Built-in | 并行分析; 任务拆解; 用户确认; Hard Stop |
| 3 | **task-designer SubAgent** (降级: Codex) + Edit | SubAgent + Built-in | 任务级设计; 更新Spec状态 |
| 4 | **code-implementer SubAgent** (降级: general-purpose) + **code-reviewer SubAgent** (降级: Codex) + Edit | SubAgent + Built-in | 并行/串行执行; 5+类别审查; 实时更新Spec |
| 4.5 | `save_session_state` | MCP | > 70% |
| 5 | Codex + Gemini + Gemini(文档) + Bash(测试) + Edit | Skills + Built-in | 双模型审计; 可选文档; 可选测试; 归档Spec |

## 4. SubAgent 配置

### 工作流专用 SubAgent

| SubAgent | 用途 | Phase | 模型 | 工具 |
|:---------|:-----|:------|:-----|:-----|
| **task-designer** | 任务设计 | Phase 3 | Sonnet | Read, Grep, Glob, Bash |
| **code-implementer** | 代码实施 | Phase 4 | Sonnet | Read, Write, Edit, Bash, Grep, Glob |
| **code-reviewer** | 代码审查 | Phase 4 | Sonnet | Read, Grep, Glob, Bash |

### SubAgent 配置位置

- 项目级: `.claude/agents/` (优先级高)
- 用户级: `~/.claude/agents/` (优先级低)

### SubAgent 调用方式

**优先使用 SubAgent**:
```typescript
Task({
  subagent_type: "task-designer",
  description: "设计任务 T001",
  prompt: "任务描述和上下文..."
})
```

**降级方案**:
- SubAgent 不可用时,使用 Skills (Codex/Gemini)
- 或使用内置 SubAgent (general-purpose/Explore)

### SubAgent 管理

```bash
# 查看所有 SubAgent
/agents

# 恢复 SubAgent 会话
> 恢复代理 abc123 并继续工作
```

详细配置参见: `.claude/agents/README.md`

---

## 5. 关键最佳实践

### 任务开始前
- 检查上下文 < 50%, 初始化索引
- 询问用户文档和测试偏好
- 创建Spec文档, 明确需求

### 任务进行中
- 信任 Context Monitor, 自然语言搜索
- **优先使用 SubAgent**: task-designer → code-implementer → code-reviewer
- **降级方案**: SubAgent 不可用时使用 Skills (Codex/Gemini)
- 保存 SESSION_ID, 维持会话连续性
- 实时更新Spec状态, 记录每个任务进展
- 并行组任务单消息多Task调用
- 每个任务完成后立即审查

### SubAgent 使用
- Phase 3: 使用 task-designer 设计方案
- Phase 4: 使用 code-implementer 实施代码
- Phase 4: 使用 code-reviewer 审查代码
- 并行执行: 单消息多个 Task 调用
- 恢复会话: 使用 agentId 恢复

### 高使用率时
- 立即保存状态, 执行 `/clear`
- 70-80% 就应考虑清除

### 代码质量
- SubAgent 或外部模型设计方案, Claude 协调
- 强制5+类别审查: 可维护性、性能、安全性、风格、文档
- 问题分级: Critical/High/Medium/Low
- 评分 ≥ 90% 且无 Critical/High 问题才通过
- 最多2轮修复循环

### 任务拆解
- 2-8个原子任务
- 分析依赖, 划分并行组和串行组
- 用户确认任务拆解, 支持调整
- 记录到Spec文档

### Spec文档管理
- 实时更新任务状态: pending → in_progress → completed
- 记录设计要点和审查结果
- 记录修改文件和完成时间
- 完成后归档到 `.claude/specs/completed/`

### 会话管理
- 调用前思考是否续接
- 截断时自动继续直至 Diff 完整
- SubAgent 会话可恢复

---

**版本**: 4.1.0
**更新**: 集成 SubAgent 机制 - task-designer、code-implementer、code-reviewer
