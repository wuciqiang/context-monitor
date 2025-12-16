# 会话状态文件
# Session State File

> 此文件用于在独立会话间传递任务状态
> 每个任务完成后自动更新

---

## 会话元数据

- **会话 ID**: `{session_id}`
- **项目名称**: `{project_name}`
- **开始时间**: `{start_time}`
- **最后更新**: `{last_update}`
- **当前任务**: `{current_task_id}`

---

## 全局上下文

### 项目信息
- **项目名称**: {project_name}
- **项目类型**: {project_type}
- **项目描述**: {project_description}

### 技术栈
- **语言**: {language}
- **前端**: {frontend_stack}
- **后端**: {backend_stack}
- **数据库**: {database}
- **部署**: {deployment}

### 关键决策记录
1. **{decision_1_title}**: {decision_1_content}
2. **{decision_2_title}**: {decision_2_content}
3. **{decision_3_title}**: {decision_3_content}

---

## 任务执行状态

| 任务 ID | 任务名称 | 状态 | 完成时间 | 备注 |
|---------|----------|------|----------|------|
| 1.1 | {task_name} | ✅ 完成 | 2025-01-15 10:30 | - |
| 1.2 | {task_name} | ✅ 完成 | 2025-01-15 11:00 | - |
| 1.3 | {task_name} | 🔄 进行中 | - | - |
| 1.4 | {task_name} | ⏳ 待开始 | - | 依赖 1.3 |
| 1.5 | {task_name} | ⏳ 待开始 | - | 依赖 1.4 |

**进度**: {completed_count}/{total_count} ({percentage}%)

---

## 任务输出

### Task 1.1: {task_name}

**完成时间**: 2025-01-15 10:30

**输出文件**:
- `src/app/layout.tsx` - Next.js 根布局
- `src/app/page.tsx` - 首页
- `package.json` - 项目配置

**关键决策**:
- 使用 Next.js 14 App Router
- TypeScript 严格模式
- Tailwind CSS 用于样式

**传递给下一任务的数据**:
```typescript
// Next.js 项目结构
src/
  app/
    layout.tsx
    page.tsx
  components/
  lib/
```

---

### Task 1.2: {task_name}

**完成时间**: 2025-01-15 11:00

**输出文件**:
- `prisma/schema.prisma` - 数据库 schema
- `.env.example` - 环境变量模板
- `src/lib/prisma.ts` - Prisma 客户端

**关键决策**:
- 使用 PostgreSQL 数据库
- Prisma ORM
- 连接池配置

**传递给下一任务的数据**:
```prisma
// Prisma 配置
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}
```

---

### Task 1.3: {task_name} (当前任务)

**状态**: 🔄 进行中

**已完成**:
- ✅ 创建 User 模型基础结构
- ✅ 添加必要字段

**待完成**:
- ⏳ 添加索引
- ⏳ 添加关系
- ⏳ 运行 migration

**当前代码**:
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  password  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

---

## 任务间依赖数据

### 从 Task 1.1 传递的数据
```typescript
// Next.js 项目配置
export const appConfig = {
  name: "Knowledge Payment Platform",
  version: "1.0.0",
  framework: "Next.js 14"
};
```

### 从 Task 1.2 传递的数据
```typescript
// Prisma 客户端实例
import { PrismaClient } from '@prisma/client';

export const prisma = new PrismaClient();
```

### Task 1.3 将传递的数据
```typescript
// User 模型类型定义
export type User = {
  id: string;
  email: string;
  name: string | null;
  password: string;
  createdAt: Date;
  updatedAt: Date;
};
```

---

## 下一任务预览

### Task 1.4: 实现用户注册 API

**任务规范**: `.claude/specs/task-1.4.md`

**依赖**:
- ✅ Task 1.1 (Next.js 项目) - 已完成
- ✅ Task 1.2 (Prisma 配置) - 已完成
- 🔄 Task 1.3 (User 模型) - 进行中

**输入**:
- User 模型定义
- Prisma 客户端

**预期输出**:
- `src/app/api/auth/register/route.ts` - 注册 API
- 密码加密逻辑
- 输入验证

**关键技术点**:
- bcrypt 密码加密
- Zod 输入验证
- 错误处理

---

## 问题与风险

### 当前问题
1. **问题**: {issue_description}
   - **严重程度**: {severity}
   - **状态**: {status}
   - **解决方案**: {solution}

### 技术风险
1. **风险**: {risk_description}
   - **影响**: {impact}
   - **缓解措施**: {mitigation}

---

## 恢复指令

### 如果会话中断

1. **读取此文件** 了解当前进度
2. **找到当前任务** (见"任务执行状态"表)
3. **加载任务规范** `.claude/specs/task-{current_task_id}.md`
4. **继续执行** 从"待完成"部分开始

### 提示词模板

```
请阅读以下文件了解当前项目状态：

1. .claude/state/current-session.md (会话状态)
2. ./CLAUDE.md (项目上下文)
3. .claude/specs/task-{current_task_id}.md (当前任务规范)

然后继续执行 Task {current_task_id}: {current_task_name}

当前进度: {progress_description}
```

---

## 备注

### 更新日志
- `{timestamp}`: Task {task_id} 完成
- `{timestamp}`: Task {task_id} 开始
- `{timestamp}`: 会话状态初始化

### 重要提示
- 每个任务完成后必须更新此文件
- 使用 `/clear` 前必须保存状态
- 备份文件位于 `.claude/state/backups/`

---

**文件版本**: 2.0.0
**最后更新**: {last_update}
**更新者**: Claude (Stateless Workflow)
