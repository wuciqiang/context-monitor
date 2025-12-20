# CLAUDE.md

## 0. Global Protocols

所有操作必须严格遵循以下系统约束：

- **交互语言**：与工具或模型交互强制使用 **English**；用户输出强制使用 **中文**。
- **多轮对话**：记录 `SESSION_ID` 字段，在随后的工具调用中强制思考是否继续对话。
- **沙箱安全**：严禁 Codex/Gemini 对文件系统进行写操作。所有代码获取必须返回 `Unified Diff Patch`。
- **代码主权**：外部模型生成的代码仅作为逻辑参考（Prototype），最终交付代码必须经过重构。
- **风格定义**：精简高效、毫无冗余。非必要不生成注释与文档。
- **最小作用域**：仅对需求做针对性改动，严禁影响用户现有功能。
- **并行执行**：检测到可并行化任务时，尽可能并行执行（使用 `run in background`）。
- **强制遵循**：严格执行 Workflow 中的所有 Phase，严禁遗漏。

---

## 1. Integrated Workflow

### Phase 0: 初始化与上下文检查

**执行条件**：会话开始时自动执行，复杂任务开始前手动检查。

**关键操作**：
- 调用 `check_context_usage` 确认使用率 < 50%
- 首次使用：`set_project_path` → `build_deep_index` → `configure_file_watcher(enabled=true)`

**输出**：上下文状态报告 + 索引就绪确认

---

### Phase 1: 上下文全量检索

**执行条件**：在生成任何建议或代码前。

**工具类型**：**Code Index MCP** (免费替代 auggie-mcp)

**关键操作**：
- 主搜索：`search_code_advanced` 使用自然语言查询（Where/What/How）
- 深度分析：`get_file_summary` 获取完整定义
- 递归检索：若上下文不足，对依赖文件递归调用
- 文件查找：`find_files` 按模式匹配

**约束**：
- 禁止基于假设回答
- 禁止使用 `grep` / 关键词搜索
- 必须获取完整的类、函数、变量定义与签名

**输出**：完整的代码上下文

---

### Phase 2: 多模型协作分析

**执行条件**：上下文就绪后，编码开始前。

**工具类型**：**Skills** (collaborating-with-codex / collaborating-with-gemini)

**关键操作**：
1. 上下文检查：若使用率 > 70%，简化分析范围或保存状态
2. 分发输入：将原始需求分发给 Codex 和 Gemini（通过 Skills 调用）
3. 交叉验证：整合各方思路，生成无逻辑漏洞的实施计划
4. 用户确认：展示最终实施计划

**Skills 调用格式**：
```bash
# Codex
python ~/.claude/skills/collaborating-with-codex/scripts/codex_bridge.py \
  --cd "/project/path" \
  --PROMPT "Analyze the task..." \
  --sandbox read-only

# Gemini
python ~/.claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project/path" \
  --PROMPT "Analyze the task..." \
  --sandbox
```

**输出**：经过交叉验证的实施计划

---

### Phase 3: 原型获取

**执行条件**：实施计划确认后。

**工具类型**：**Skills** (根据任务类型选择)

**关键操作**：
- 上下文检查：若使用率 > 70%，先保存状态
- **Route A (前端/UI)**：Gemini Skill（上下文 < 32k，后端逻辑需客观审视）
- **Route B (后端/逻辑)**：Codex Skill（逻辑运算与 Debug）
- **通用约束**：必须在 Prompt 中明确要求返回 `Unified Diff Patch`

**Skills 调用示例**：
```bash
# 后端任务 - Codex
python ~/.claude/skills/collaborating-with-codex/scripts/codex_bridge.py \
  --cd "/project" \
  --PROMPT "Generate unified diff for authentication logic. OUTPUT: Unified Diff Patch ONLY." \
  --sandbox read-only

# 前端任务 - Gemini
python ~/.claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project" \
  --PROMPT "Generate unified diff for UI components. OUTPUT: Unified Diff Patch ONLY." \
  --sandbox
```

**输出**：Unified Diff Patch（原型代码）

---

### Phase 4: 编码实施

**执行条件**：原型获取完成后。

**关键操作**：
- 上下文检查：每完成 3-5 个文件修改后检查，若 > 85% 立即保存状态
- 逻辑重构：基于原型重写为企业级代码
- 自动监控：Context Monitor 每 5-10 个工具调用后自动检查

**约束**：
- 非必要不生成注释与文档
- 变更仅限需求范围
- 强制审查是否引入副作用

**输出**：企业级生产代码

---

### Phase 4.5: 上下文管理与状态保存

**执行条件**：Context Monitor 检测到高使用率时自动触发。

**使用率分级响应**：
- **< 50% (SAFE)**：继续工作
- **50-70% (WARNING)**：提示用户注意使用率
- **70-85% (HIGH)**：准备保存状态，建议即将执行 `/clear`
- **> 85% (CRITICAL)**：立即保存状态并强烈建议执行 `/clear`

**状态保存**：
- 调用 `save_session_state` 工具
- 保存内容：已完成任务、当前任务、下一步计划、代码变更摘要、待审计文件

**用户提示**：
```
⚠️ 上下文使用率已达 {usage_percent}%
已保存会话状态到 .claude/state/current-session.md
建议立即执行 `/clear` 清除上下文，然后使用以下提示词恢复：
"请阅读 .claude/state/current-session.md 了解之前的进度，继续 Phase 5 审计交付"
```

---

### Phase 5: 审计与交付

**执行条件**：代码实施完成后（可能在 `/clear` 后恢复）。

**工具类型**：**Skills** (双模型并行审计)

**关键操作**：
1. 会话恢复（如果执行了 `/clear`）：读取 `.claude/state/current-session.md`
2. 自动审计：强制立即调用 Codex 与 Gemini Skills 同时进行 Code Review（并行执行）
3. 整合修复：综合两个模型的反馈，进行必要修正
4. 最终检查：调用 `check_context_usage` 确认使用率
5. 交付：审计通过后反馈给用户

**Skills 并行调用**：
```bash
# 同时启动两个审计（run in background）
python ~/.claude/skills/collaborating-with-codex/scripts/codex_bridge.py \
  --cd "/project" \
  --PROMPT "Review code changes for logic correctness, security, performance" \
  --sandbox read-only &

python ~/.claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project" \
  --PROMPT "Review code changes for UI/UX consistency, accessibility" \
  --sandbox &
```

**输出**：经过审计的最终代码 + 审计报告

---

## 2. Resource Matrix

| Phase | Tool / Model | Tool Type | Input | Output | Critical Constraints |
|:------|:------------|:----------|:------|:-------|:--------------------|
| **Phase 0** | `check_context_usage` | MCP | - | Usage % + Status | Ensure < 50% before starting |
| **Phase 0** | `set_project_path`, `build_deep_index` | MCP | Project path | Index status | Once per session |
| **Phase 1** | `search_code_advanced`, `get_file_summary`, `find_files` | **Code Index MCP** | Natural Language | Raw Code / Definitions | Forbidden: `grep`; Mandatory: Recursive retrieval |
| **Phase 2** | Codex AND Gemini | **Skills** | Raw Requirements | Step-by-Step Plan | Cross-validate outputs; Use Skills not MCP |
| **Phase 2** | `check_context_usage` | MCP | - | Usage status | If > 70%, simplify scope |
| **Phase 3** | Gemini (Frontend) | **Skills** | English (< 32k) | Unified Diff Patch | CSS/React/Vue authority |
| **Phase 3** | Codex (Backend) | **Skills** | English | Unified Diff Patch | Complex debugging |
| **Phase 3** | `check_context_usage` | MCP | - | Usage status | If > 70%, save state first |
| **Phase 4** | Claude (Self) | - | - | Production Code | Clean, efficient, minimal |
| **Phase 4** | Context Monitor | MCP | Auto every 5-10 calls | Usage status | Follow Phase 4.5 protocol |
| **Phase 4.5** | `save_session_state` | MCP | Session content | State file path | When usage > 70% |
| **Phase 5** | Codex AND Gemini | **Skills** | Unified Diff + File | Review Comments | Immediately after changes; Parallel execution |
| **Phase 5** | `check_context_usage` | MCP | - | Final usage status | Ensure healthy state |

---

## 3. 关键最佳实践

### 任务开始前
- ✅ 检查上下文使用率（确保 < 50%）
- ✅ 初始化代码索引（首次使用）
- ✅ 明确任务需求和范围

### 任务进行中
- ✅ 信任 Context Monitor 的自动提醒
- ✅ 使用自然语言进行代码搜索
- ✅ 让 Codex/Gemini 提供原型，Claude 负责重构
- ✅ 每完成一个阶段，检查上下文使用率

### 高使用率时
- ✅ 立即保存会话状态
- ✅ 执行 `/clear` 清除上下文
- ✅ 使用状态文件恢复并继续工作
- ✅ 不要等到 100% 才清除（70-80% 就应该考虑）

### 代码质量保证
- ✅ 外部模型的代码仅作为原型参考
- ✅ 最终代码必须由 Claude 重构
- ✅ 强制执行双模型审计
- ✅ 精简高效，非必要不添加注释

---

## 4. 多模型协作 Skills 说明

### 4.1 Skills 概述

**来源**: [GuDaStudio/skills](https://github.com/GuDaStudio/skills)

**核心 Skills**:
- `collaborating-with-codex`: 后端逻辑、算法、调试
- `collaborating-with-gemini`: 前端 UI、样式、用户体验

**关键特性**:
- 通过 Skills 调用（非 MCP）
- 沙箱模式确保安全
- 支持多轮对话（SESSION_ID）
- 返回 Unified Diff Patch

### 4.2 安装 Skills

```bash
# 克隆仓库
git clone --recurse-submodules https://github.com/GuDaStudio/skills
cd skills

# 用户级安装（推荐）
./install.sh --user --all  # Linux/macOS
.\install.ps1 -User -All   # Windows

# 验证安装
# Claude 应能识别 collaborating-with-codex 和 collaborating-with-gemini
```

### 4.3 调用格式

**Codex (后端/逻辑)**:
```bash
python ~/.claude/skills/collaborating-with-codex/scripts/codex_bridge.py \
  --cd "/project/path" \
  --PROMPT "Your task description" \
  --sandbox read-only \
  [--SESSION_ID "uuid"]  # 可选：多轮对话
```

**Gemini (前端/UI)**:
```bash
python ~/.claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project/path" \
  --PROMPT "Your task description" \
  --sandbox \
  [--SESSION_ID "uuid"]  # 可选：多轮对话
```

### 4.4 关键参数

| 参数 | 说明 | 必需 |
|------|------|------|
| `--cd` | 项目根目录 | ✅ |
| `--PROMPT` | 任务描述（英文） | ✅ |
| `--sandbox` | 沙箱模式 | ✅ |
| `--SESSION_ID` | 会话ID（多轮对话） | ❌ |
| `--return-all-messages` | 返回完整推理 | ❌ |

### 4.5 返回格式

```json
{
  "success": true,
  "SESSION_ID": "uuid",
  "agent_messages": "模型回复内容（Unified Diff Patch）"
}
```

### 4.6 最佳实践

1. **并行执行**: Phase 2 和 Phase 5 同时调用 Codex 和 Gemini（run in background）
2. **明确输出**: Prompt 中要求 "OUTPUT: Unified Diff Patch ONLY"
3. **沙箱安全**: 始终使用 `--sandbox` 或 `--sandbox read-only`
4. **多轮对话**: 保存 SESSION_ID 用于后续调用
5. **英文交互**: Prompt 必须使用英文

---

## 5. 快速参考

### Context Monitor
```
# 检查使用率
请检查当前上下文使用率

# 保存状态
请保存当前会话状态

# 恢复状态（在 /clear 后）
请阅读 .claude/state/current-session.md 了解之前的进度，然后继续工作
```

### Code Index (代码检索)
```
# 初始化（首次使用）
set_project_path /path/to/project
build_deep_index
configure_file_watcher enabled=true

# 搜索代码（Code Index MCP - 免费替代 auggie-mcp）
search_code_advanced "Where is the user authentication logic?"
get_file_summary path/to/file.py
find_files "*.ts"
```

### Skills (多模型协作)
```bash
# Codex - 后端/逻辑
python ~/.claude/skills/collaborating-with-codex/scripts/codex_bridge.py \
  --cd "/project" --PROMPT "Task..." --sandbox read-only

# Gemini - 前端/UI
python ~/.claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project" --PROMPT "Task..." --sandbox
```

---

**版本**: 2.1.0
**最后更新**: 2025-12-20
**更新内容**: 明确 Skills vs MCP，Code Index MCP 替代 auggie-mcp
