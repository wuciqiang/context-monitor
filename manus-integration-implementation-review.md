# Manus 最终规范落地评审报告（Codex）

**评审对象**：当前项目修改
**基准规范**：`manus-integration-final-spec.md`
**评审时间**：2026-01-08

---

## 1. 结论概览

整体已完成 **P0/P1** 要求的大部分落地；**P2** 项（`context.json` schema 升级与 Hook 级注意力刷新）尚未实现。另有若干“规范一致性与可执行性”细节需要补充。

---

## 2. 已完成的对齐项（符合规范）

- **Global Protocols 中加入 Manus 协议**（注意力刷新 / 外部记忆 / 错误沉淀 / 追加式上下文）。
- **Phase 4 SubAgent 继承协议**已写入（禁止裸启动 + 传递 spec 摘要）。
- **Phase 4 超大只读文件切片读取规则**已补充（Phase 1 仍禁 grep）。
- **Spec 目录结构调整**：`notes.md` 替代 `task-log.md`。
- **Spec 模板新增章节**：边界与假设 / Errors & Issues。
- **Phase 0 创建 notes.md**，归档时随 spec 一并归档。
- **auto.md** 已加入 Phase 2/3/4 注意力刷新步骤，并删除 Phase 1 的 grep 描述。
- **atomic-task-spec.md 问题记录表增强**（上下文占用/学习点）。

---

## 3. 未完成 / 不符合规范项

### 3.1 P2 未落地
- **`context.json` schema 升级**（`schema_version` + `errors` 字段）尚未实现。
- **Hook 级注意力刷新提醒**（例如 `.claude/hooks/attention-refresh.py`）未新增。

### 3.2 规范执行细节
- **SubAgent 继承字段映射未明确**：Spec 模板中没有 “Status” 独立章节，需明确映射为“任务清单中当前任务状态”。
  - 建议在 `.claude/specs/README.md` 中追加说明。

### 3.3 无关变更疑似噪音
- `.spec-workflow/templates/*.md` 被标记为修改，但不在规范清单中；疑似换行/编码变更导致。
  - 建议确认是否真实需求，否则回退。

---

## 4. 关键文件对照（摘录）

- `CLAUDE.md`：新增 Manus 协议 + SubAgent 继承协议 + Phase 4 切片规则。
- `commands/auto.md`：Phase 2/3/4 注意力刷新、Phase 1 禁 grep、创建 notes.md。
- `.claude/specs/README.md`：notes.md 目录替换 + 新增章节。
- `templates/atomic-task-spec.md`：问题记录表增强。

---

## 5. 建议（供 Claude 后续完善）

1. **补齐 P2 项**
   - `context.json` 增加 `schema_version` 与 `errors` 字段，并明确默认兼容逻辑。
   - 新增 Hook 级注意力刷新提醒（可选，带节流）。

2. **明确 SubAgent 摘要字段来源**
   - 在 `.claude/specs/README.md` 明确 “Goal/Status/Out-of-scope” 对应章节：
     - Goal → 功能概述
     - Status → 任务清单当前任务状态
     - Out-of-scope → 边界与假设

3. **清理无关变更**
   - 若 `.spec-workflow/templates/*.md` 未被明确修改，建议回退以减少噪音 diff。

---

## 6. 结论

当前修改**整体符合** `manus-integration-final-spec.md` 的 P0/P1 要求；若要达成“严格按照最终规范修改”的标准，还需补齐 P2 项与细节映射，并清理无关改动。
