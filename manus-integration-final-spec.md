# Manus 模式集成最终规范（合并版）

**来源**：`planning-with-files-analysis.md`、`integration-strategy.md`、`review-manus-integration-*.md`
**目标**：在不破坏现有 6 阶段工作流的前提下，吸收 Manus 的“注意力刷新 + 外部记忆 + 错误沉淀”优势。
**最终决策摘要**：
- 术语统一：`task_plan` → `spec.md`
- 阈值统一：**>500 行**
- grep 例外：**Phase 1 禁止**，**Phase 4 仅限超大只读文件切片读取**
- notes 策略：**`notes.md` 替代 `task-log.md`**（单一真相源）
- SubAgent：**启动前必须传入 spec 摘要，禁止裸启动**
- context.json：新增 `schema_version` + `errors` 字段
- notes 生命周期：**归档，不删除**

---

## 1. 规范要求（执行性约束）

1. **注意力刷新**：在 Phase 2/3/4 进入时必须重读 `spec.md` 的“功能概述 + 当前任务状态”。
2. **外部记忆**：研究笔记、关键决策、错误日志必须写入 `notes.md` 或 `spec.md`，禁止堆在上下文。
3. **错误沉淀**：所有执行错误需记录在 `spec.md` 的 Errors/Issues 章节，并同步到 `context.json.errors`（结构化）。
4. **追加式上下文**：只追加，不修改历史；大内容写文件，Context 仅保留路径。
5. **SubAgent 继承协议**：启动 SubAgent 前必须传入 spec 摘要（功能概述 + 当前任务状态 + Out-of-scope）。

---

## 2. 具体修改清单（文件 → 段落 → 修改内容）

### A. `CLAUDE.md`

1. **`## 0. Global Protocols`**
   - 新增 **Manus Protocol** 段落：
     - 注意力刷新（Phase 2/3/4 入口重读 spec.md 目标）
     - 外部记忆（思考/中间状态写入 notes.md）
     - 错误沉淀（错误写 spec.md + context.json.errors）
     - 追加式上下文（不改历史，只追加）

2. **`Phase 1: 上下文全量检索`**
   - 明确 **禁止 grep**（保留现有规则）。
   - 取消任何 “Grep + Read” 描述。

3. **`Phase 4: 并行/串行实施`**
   - 增加 **SubAgent Context Inheritance Protocol**：
     - 启动前必须将 spec.md 的“功能概述 + 当前任务状态 + Out-of-scope”以摘要形式传入。
     - 禁止裸启动 SubAgent。
   - 增加 **超大文件只读切片规则**：
     - 仅在 Phase 4，对 >500 行只读文件允许切片读取（优先 Code Index）。

4. **`## 5. 关键最佳实践`**
   - 增加注意力刷新规则与 notes.md 位置说明。
   - 明确“>500 行阈值”作为唯一标准。

---

### B. `.claude/specs/README.md`

1. **目录结构说明**
   - 将 `task-log.md` 替换为 `notes.md`：
     ```
     .claude/specs/active/[feature]/
       ├── spec.md
       ├── notes.md
       └── context.json
     ```
   - 说明 notes.md 用途：研究/决策/错误日志的外部记忆。

2. **`spec.md` 结构模板**
   - 增加新章节：
     - `## 边界与假设`（Assumptions / Decisions / Out-of-scope）
     - `## Errors & Issues`（集中错误追踪表）
   - 明确“功能概述”即 SubAgent 继承协议的“目标摘要”。

3. **Phase 0 创建步骤**
   - 新增创建 `notes.md`。

4. **归档步骤**
   - 明确 `notes.md` 随 spec 一起归档到 `completed/`。

---

### C. `templates/atomic-task-spec.md`

1. **问题记录表增强**
   - 扩展字段：`上下文占用/解决方案/学习点`，避免再新增单独“错误日志表”。
   - 示例：
     ```
     | 问题 | 严重程度 | 上下文占用 | 状态 | 解决方案 | 学习点 |
     ```

---

### D. `commands/auto.md`

1. **Phase 0**
   - 创建 `notes.md`。

2. **Phase 1**
   - 删除 “Grep + Read” 描述，仅保留 `search_code_advanced`。

3. **Phase 2/3/4 入口**
   - 插入 “重读 spec.md 目标/任务状态” 步骤。

4. **Phase 4 SubAgent**
   - 明确将 spec 摘要（功能概述 + 当前任务状态 + Out-of-scope）写入 SubAgent Prompt。

---

### E. `context.json` Schema（新增规范）

1. **新增字段**
   - `schema_version: "1.1"`
   - `errors: []`（结构化错误列表）

2. **迁移规则**
   - 如果旧版缺少字段，读取时默认 `schema_version: "1.0"` 且 `errors: []`。

---

### F. 可选增强（P2）

1. **Hook 级注意力刷新提醒**
   - 新增 `.claude/hooks/attention-refresh.py`：
     - 每 N 次工具调用提示重读 spec 目标（默认 15）。
     - 节流避免打扰。

---

## 3. 实施优先级

**P0（立即）**
- CLAUDE.md：术语统一、grep 规则、阈值、注意力刷新
- commands/auto.md：Phase 1 规范化 + 重读步骤

**P1（本周）**
- `.claude/specs/README.md`：notes 替代 task-log + spec 结构扩展
- templates/atomic-task-spec.md：问题记录表增强
- SubAgent 继承协议落地

**P2（后续）**
- context.json schema 升级
- Hook 级注意力刷新提醒

---

## 4. 结论

以上为最终合并规范与可执行修改清单。先做 P0/P1 的文档和流程对齐，再进行 P2 的自动化增强，确保不引入双规范与执行空档。
