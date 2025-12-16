# 原子任务规范模板
# Atomic Task Specification Template

## 任务信息

**任务 ID**: `{task_id}`
**任务名称**: `{task_name}`
**所属模块**: `{module_name}`
**优先级**: `{priority}` (P0/P1/P2)
**预估时长**: `{duration}` 分钟
**负责代理**: `{agent}` (claude/codex/gemini)

---

## 📋 任务描述

### 单句描述
{one_sentence_description}

### 详细说明
{detailed_description}

### 为什么需要这个任务？
{rationale}

---

## 📁 涉及文件

### 需要修改的文件
- `{file_path_1}` - {modification_type} - {reason}
- `{file_path_2}` - {modification_type} - {reason}
- `{file_path_3}` - {modification_type} - {reason}

### 需要创建的文件
- `{new_file_path_1}` - {file_type} - {purpose}

### 需要删除的文件
- `{delete_file_path}` - {reason}

**文件数量限制**: ≤ 3 个文件（符合原子任务标准）

---

## 🔗 依赖关系

### 前置任务（必须先完成）
- [ ] `{prerequisite_task_id}` - {prerequisite_task_name}
- [ ] `{prerequisite_task_id}` - {prerequisite_task_name}

### 后续任务（依赖本任务）
- `{dependent_task_id}` - {dependent_task_name}
- `{dependent_task_id}` - {dependent_task_name}

### 并行任务（可同时进行）
- `{parallel_task_id}` - {parallel_task_name}

**依赖状态**:
- ✅ 可立即开始（无前置依赖）
- ⏳ 等待前置任务完成
- 🔄 部分依赖（可并行开始）

---

## 🎯 验收标准

### 功能验收
- [ ] {acceptance_criterion_1}
- [ ] {acceptance_criterion_2}
- [ ] {acceptance_criterion_3}

### 代码质量
- [ ] 代码通过 ESLint/Prettier 检查
- [ ] 无 TypeScript 类型错误
- [ ] 遵循项目代码规范

### 测试验收
- [ ] 单元测试通过（如适用）
- [ ] 集成测试通过（如适用）
- [ ] 手动测试通过

### 文档验收
- [ ] 代码注释完整（仅在必要时）
- [ ] README 更新（如需要）
- [ ] API 文档更新（如需要）

---

## 🛠️ 技术实现

### 技术栈
- **语言**: {language}
- **框架**: {framework}
- **库**: {libraries}

### 关键技术点
1. {key_technical_point_1}
2. {key_technical_point_2}
3. {key_technical_point_3}

### 潜在风险
- ⚠️ {risk_1} - 缓解措施: {mitigation_1}
- ⚠️ {risk_2} - 缓解措施: {mitigation_2}

### 性能考虑
- {performance_consideration_1}
- {performance_consideration_2}

---

## 📝 实施步骤

### Step 1: 准备工作
1. 阅读相关文档
2. 检查依赖任务完成状态
3. 准备测试数据

### Step 2: 获取代码原型（如需要）
```bash
# 向 codex/gemini 请求原型
skill(codeagent) --task-id={task_id} --mode=prototype
```

### Step 3: 实施开发
1. {implementation_step_1}
2. {implementation_step_2}
3. {implementation_step_3}

### Step 4: 自我测试
1. 运行单元测试
2. 手动测试关键路径
3. 检查边界情况

### Step 5: 代码审查
```bash
# 提交 codex 审查
skill(codeagent) --task-id={task_id} --mode=review
```

### Step 6: 修复问题
1. 根据审查意见修复
2. 重新测试
3. 再次审查（如需要）

### Step 7: 提交代码
```bash
git add {files}
git commit -m "feat: {task_name} (Task {task_id})"
```

---

## 🧪 测试计划

### 单元测试
```typescript
// 测试文件: {test_file_path}
describe('{feature_name}', () => {
  it('should {test_case_1}', () => {
    // Test implementation
  });

  it('should {test_case_2}', () => {
    // Test implementation
  });
});
```

### 集成测试
- {integration_test_scenario_1}
- {integration_test_scenario_2}

### 手动测试清单
- [ ] {manual_test_1}
- [ ] {manual_test_2}
- [ ] {manual_test_3}

---

## 📊 进度追踪

### 状态
- [ ] 未开始 (Not Started)
- [ ] 进行中 (In Progress)
- [ ] 代码审查中 (In Review)
- [ ] 修复问题中 (Fixing Issues)
- [ ] 已完成 (Completed)
- [ ] 已验收 (Accepted)

### 时间记录
- **开始时间**: {start_time}
- **完成时间**: {end_time}
- **实际耗时**: {actual_duration} 分钟
- **预估耗时**: {estimated_duration} 分钟
- **偏差**: {deviation}%

### 问题记录
| 问题 | 严重程度 | 状态 | 解决方案 |
|------|----------|------|----------|
| {issue_1} | {severity} | {status} | {solution} |

---

## 🔍 代码审查记录

### Codex 审查意见
```markdown
{codex_review_comments}
```

### 修复记录
- [ ] {fix_1} - 已修复
- [ ] {fix_2} - 已修复

### 最终审查结果
- ✅ 通过审查
- ❌ 需要修改
- ⏳ 等待审查

---

## 📚 参考资料

### 相关文档
- [{doc_title_1}]({doc_url_1})
- [{doc_title_2}]({doc_url_2})

### 相关代码
- `{related_file_1}` - {description}
- `{related_file_2}` - {description}

### 外部资源
- [{resource_title_1}]({resource_url_1})
- [{resource_title_2}]({resource_url_2})

---

## 💬 备注

### 开发笔记
{developer_notes}

### 已知限制
- {limitation_1}
- {limitation_2}

### 未来优化
- {future_optimization_1}
- {future_optimization_2}

---

## ✅ 完成检查清单

在标记任务为"已完成"前，请确认：

- [ ] 所有验收标准已满足
- [ ] 代码已通过审查
- [ ] 测试已全部通过
- [ ] 文档已更新
- [ ] 代码已提交到 Git
- [ ] 进度已更新到 `.claude/progress.md`
- [ ] 后续任务已通知（如有）

---

**任务创建时间**: {created_at}
**最后更新时间**: {updated_at}
**创建者**: {creator}
**审查者**: {reviewer}
