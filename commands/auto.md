---
description: 自动执行完整工作流(一键完成所有阶段,含Spec文档驱动)
---

# 自动化工作流

⚠️ **强制执行完整流程** - 此命令将自动执行 Phase 0 → Phase 5 所有阶段,确保工作流完整性。

## 🎯 工作流强制执行

此命令会:
1. ✅ 创建Spec文档追踪任务
2. ✅ 询问文档和测试偏好
3. ✅ 智能任务拆解(并行/串行分组)
4. ✅ 用户确认任务拆解
5. ✅ 强制执行所有 Phase(不可跳过)
6. ✅ 在 Phase 2 暂停等待确认
7. ✅ 实时更新Spec状态
8. ✅ 5+类别代码审查
9. ✅ 可选文档生成和测试执行
10. ✅ 归档Spec文档

## 执行流程

### 🔄 Phase 0: 初始化与需求确认(自动)

**状态更新**: 创建 `.claude/specs/active/[feature-name]/spec.md`

1. **检查上下文使用率** (必需)
   - 调用 `check_context_usage` 工具
   - 降级方案: 如 MCP 失败,手动计算
   - 如使用率 > 70%,先保存状态并建议 `/clear`

2. **询问用户偏好** (必需)
   - 使用 `AskUserQuestion` 询问:
     * 问题1: "是否为此功能生成文档?"
       - 选项: "是 - 生成模块文档" / "否 - 仅代码"
     * 问题2: "是否执行测试?"
       - 选项: "是 - 运行测试套件" / "否 - 跳过测试"
   - 记录用户选择

3. **创建Spec文档** (必需)
   - 创建 `.claude/specs/active/[feature-name]/spec.md`
   - 创建 `.claude/specs/active/[feature-name]/context.json`
   - 初始化任务清单结构

### 🔄 Phase 1: 上下文检索(自动)

4. **搜索相关代码** (必需)
   - 使用 `search_code_advanced` 或 Grep + Read
   - 获取完整代码上下文
   - 递归检索依赖文件

### ⏸️ Phase 2: 分析与任务拆解(暂停确认)

5. **多模型协作分析** (必需)
   - 并行调用 Codex 和 Gemini (run in background)
   - 降级方案: 如 Skills 不可用,Claude 单独分析
   - 交叉验证输出

6. **智能任务拆解** (必需)
   - 生成 2-8 个原子任务
   - 分析任务依赖关系
   - 划分并行组和串行组
   - 格式:
     ```
     并行组1: T001, T002 (独立任务)
     串行组2: T003 (依赖并行组1)
     并行组3: T004, T005 (依赖串行组2)
     ```

7. **更新Spec文档** (必需)
   - 将任务清单写入 `spec.md`
   - 记录每个任务的: 描述、文件范围、SubAgent类型、依赖关系

8. **用户确认任务拆解** (必需)
   - 使用 `AskUserQuestion` 展示任务拆解
   - 选项: "确认并执行" / "需要调整"
   - 如需调整: 询问调整方式 → 更新Spec → 重新确认

9. **展示实施方案并等待确认** (必需)
   - 显示技术方案、风险、步骤
   - ⏸️ **暂停**: 等待用户输入 "继续" / "修改" / "取消"

### 🔄 Phase 3: 任务级设计(自动)

**对每个任务执行** (按并行/串行组顺序):

10. **Codex设计方案** (必需)
    - 调用 Codex 为当前任务设计实现方案
    - 返回: 技术方案、文件修改、API设计、风险点
    - 保存设计要点到 `spec.md` 对应任务

11. **更新Spec状态** (必需)
    - 标记任务状态: `pending` → `in_progress`
    - 记录分配的 SubAgent ID

### 🔄 Phase 4: 并行/串行实施(自动)

**执行策略**: 按组执行,组内并行,组间串行

**对每个任务执行**:

12. **SubAgent实施代码** (必需)
    - 并行组: 单消息多个 Task 工具调用
    - 串行组: 逐个执行
    - 传递 Codex 设计方案给 SubAgent
    - 收集修改的文件列表

13. **Codex审查代码** (必需)
    - 调用 Codex 审查 SubAgent 的代码
    - 5+类别评估:
      * 可维护性
      * 性能
      * 安全性 (SQL注入/XSS/命令注入)
      * 风格一致性
      * 文档完整性
    - 问题分级: Critical/High/Medium/Low
    - 评分: 0-100

14. **修复循环** (如需要)
    - Critical/High问题: 立即修复
    - Medium/Low问题: 询问用户是否修复
    - 最多2轮 "修复 → 审查" 循环
    - 评分 ≥ 90% 且无 Critical/High 问题才通过

15. **更新Spec状态** (必需)
    - 标记任务: `in_progress` → `completed`
    - 记录: 修改文件、完成时间、审查结果
    - 更新 checkbox: `- [ ]` → `- [x]`

16. **上下文管理** (自动)
    - 每完成1个任务检查上下文
    - > 70%: 保存状态 → 建议 `/clear`
    - Context Monitor 每 5-10 工具调用自动检查

### 🔄 Phase 5: 审计、文档与归档(自动)

17. **双模型审计** (必需)
    - 并行调用 Codex 和 Gemini 审计 (run in background)
    - 降级方案: Claude 单独审计
    - 生成审计报告
    - 记录审查结果到 `spec.md`

18. **可选: 文档生成** (基于Phase 0选择)
    - 如用户启用文档生成:
      * 调用 Gemini 生成文档
      * 创建 `docs/[feature-name]/` 目录
      * 生成: overview.md, api.md, usage.md
      * 记录文档路径到 `spec.md`

19. **可选: 测试执行** (基于Phase 0选择)
    - 如用户启用测试:
      * 运行测试套件
      * 记录测试结果和覆盖率
      * 测试失败: 修复 → 重新测试

20. **归档Spec** (必需)
    - 更新 `spec.md` 元数据:
      * status: completed
      * completed_at: [时间戳]
      * 总任务数、成功数
      * 文档生成状态
      * 测试通过状态
    - 移动到 `.claude/specs/completed/[feature-name]/`

21. **生成完成摘要** (必需)
    - 显示Spec文档路径
    - 列出完成的任务
    - 列出修改的文件
    - 显示代码审查结果
    - 显示生成的文档(如有)
    - 显示测试结果(如有)

## 优势

- ✅ **一个命令完成所有步骤** - 无需记忆多个阶段
- ✅ **Spec文档驱动** - 完整追踪任务进展
- ✅ **智能任务拆解** - 自动分析并行/串行依赖
- ✅ **用户确认机制** - 在关键点暂停确认
- ✅ **5+类别代码审查** - 结构化质量保证
- ✅ **实时状态更新** - Spec文档实时反映进度
- ✅ **可选功能模块化** - 文档和测试按需启用
- ✅ **自动化上下文管理** - 无需手动检查
- ✅ **并行执行提升性能** - 多模型调用并行化
- ✅ **知识沉淀** - 完成的Spec是项目知识库

## 使用方法

```bash
# 基本用法
/cm:auto 实现用户认证功能

# 带详细描述
/cm:auto 添加 JWT 认证,支持 token 刷新和权限验证
```

## 与手动模式对比

| 特性 | 手动模式 | 自动模式 |
|------|---------|---------|
| 命令数量 | 6 个 | 1 个 |
| 学习成本 | 高 | 低 |
| 控制粒度 | 细粒度 | 关键点 |
| 适用场景 | 复杂任务 | 常规任务 |
| 上下文管理 | 手动 | 自动 |
| Spec文档 | 可选 | 强制 |
| 任务拆解 | 手动 | 智能 |
| 代码审查 | 手动 | 强制5+类别 |

## Spec文档示例

完成后的Spec文档位于 `.claude/specs/completed/[feature-name]/spec.md`:

```markdown
---
status: completed
feature_name: user-authentication
created_at: 2025-12-21T08:00:00Z
updated_at: 2025-12-21T10:30:00Z
completed_at: 2025-12-21T10:30:00Z
documentation_enabled: true
testing_enabled: true
---

# 用户认证功能 开发规格

## 功能概述
实现基于JWT的用户认证系统...

## 任务清单

### 并行组 1
- [x] **T001**: 实现JWT生成和验证
  - 文件范围: src/auth/jwt.ts
  - SubAgent类型: general-purpose
  - 状态: completed
  - 分配的SubAgent: SubAgent #1
  - 修改的文件: src/auth/jwt.ts:1-150
  - 完成时间: 2025-12-21T09:00:00Z
  - Codex设计: 使用jsonwebtoken库,支持RS256算法
  - Codex审查: 评分95,无Critical问题

...

## 代码审查结果
- 总体评分: 92/100
- 可维护性: 95/100
- 性能: 90/100
- 安全性: 95/100
- 风格一致性: 88/100
- 文档完整性: 92/100

## 生成的文档
- docs/user-authentication/overview.md
- docs/user-authentication/api.md
- docs/user-authentication/usage.md

## 测试结果
- 测试通过: 25/25
- 覆盖率: 92%
```

## 注意事项

- 自动模式会在 Phase 2 暂停等待确认
- 如果任务特别复杂,建议使用手动模式以获得更多控制
- 上下文使用率会自动监控,无需手动检查
- Spec文档会实时更新,可随时查看进度
- 完成的Spec会归档到 `.claude/specs/completed/`

**ARGUMENTS**: $1
