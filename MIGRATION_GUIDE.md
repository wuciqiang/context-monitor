# 工作流迁移指南
# Workflow Migration Guide

> 如何将 Claude 工作流系统应用到新项目

---

## 🎯 **迁移步骤**

### Step 1: 复制工作流文件

```bash
# 方式 1: 直接复制
cp -r /path/to/template/.claude /path/to/new-project/

# 方式 2: 使用 Git 子模块
cd /path/to/new-project
git submodule add https://github.com/your-org/claude-workflow.git .claude

# 方式 3: 使用模板仓库
gh repo create my-new-project --template your-org/project-template
```

### Step 2: 配置项目信息

```bash
cd /path/to/new-project/.claude

# 复制配置模板
cp config.example.yml config.yml

# 编辑配置
vim config.yml  # 或使用你喜欢的编辑器
```

### Step 3: 更新项目特定配置

编辑 `config.yml`，修改以下关键字段：

```yaml
project:
  name: "Your Project Name"          # 修改项目名
  description: "..."                 # 修改描述
  type: "web-app"                    # 修改项目类型

  tech_stack:
    language: "typescript"           # 修改语言
    frontend:
      framework: "next.js"           # 修改前端框架
    backend:
      framework: "express"           # 修改后端框架
    database:
      type: "postgresql"             # 修改数据库
```

### Step 4: 初始化工作流

```bash
# 创建必要的目录
mkdir -p .claude/specs
mkdir -p .claude/progress/tasks
mkdir -p .claude/progress/reviews
mkdir -p .claude/logs

# 初始化 Git（如果还没有）
git init
git add .claude/
git commit -m "chore: add Claude workflow system"
```

### Step 5: 测试工作流

```bash
# 启动开发工作流
/dev

# 或者使用 skill
skill(dev-workflow)
```

---

## 📋 **迁移检查清单**

### 必须完成
- [ ] 复制 `.claude/` 目录到新项目
- [ ] 创建 `config.yml`（基于 `config.example.yml`）
- [ ] 更新项目名称和描述
- [ ] 更新技术栈配置
- [ ] 创建必要的目录结构
- [ ] 测试工作流是否正常运行

### 推荐完成
- [ ] 配置 Git hooks
- [ ] 配置代理（codex/gemini）
- [ ] 配置质量标准
- [ ] 配置通知渠道
- [ ] 添加项目特定的自定义规则

### 可选完成
- [ ] 创建自定义工作流
- [ ] 创建自定义 skills
- [ ] 配置 CI/CD 集成
- [ ] 配置性能监控

---

## 🔧 **项目类型特定配置**

### Web 应用 (Next.js / React)

```yaml
project:
  type: "web-app"
  tech_stack:
    language: "typescript"
    frontend:
      framework: "next.js"
      ui_library: "react"
      styling: "tailwind"
    backend:
      runtime: "node"
      framework: "next-api"
    database:
      type: "postgresql"
      orm: "prisma"

quality:
  performance:
    lighthouse_score: 90
    bundle_size_limit: 500
```

### API 服务 (Express / Fastify)

```yaml
project:
  type: "api"
  tech_stack:
    language: "typescript"
    backend:
      runtime: "node"
      framework: "express"
    database:
      type: "postgresql"
      orm: "typeorm"

quality:
  performance:
    response_time_p95: 100
  testing:
    coverage_threshold: 90
```

### 移动应用 (React Native)

```yaml
project:
  type: "mobile-app"
  tech_stack:
    language: "typescript"
    frontend:
      framework: "react-native"
      ui_library: "react-native-paper"
    backend:
      type: "api"
      url: "https://api.example.com"

quality:
  performance:
    startup_time: 2000  # ms
    memory_usage: 100   # MB
```

### 库/SDK (npm package)

```yaml
project:
  type: "library"
  tech_stack:
    language: "typescript"
    build_tool: "tsup"
    test_framework: "vitest"

quality:
  testing:
    coverage_threshold: 95
  code:
    bundle_size_limit: 50  # KB
```

---

## 🎨 **自定义工作流**

### 创建项目特定工作流

1. 复制模板:
```bash
cp .claude/workflows/dev.yml .claude/workflows/my-workflow.yml
```

2. 修改工作流:
```yaml
name: "My Custom Workflow"
description: "Project-specific workflow"

steps:
  - id: "custom-step"
    name: "Custom Step"
    agent: "claude"
    actions:
      - type: "custom_action"
        # ...
```

3. 注册工作流:
```yaml
# config.yml
workflows:
  my_workflow:
    enabled: true
    file: "workflows/my-workflow.yml"
```

4. 使用工作流:
```bash
/workflow run my-workflow
```

---

## 🔌 **集成现有工具**

### 集成 ESLint

```yaml
# config.yml
quality:
  code:
    linter: "eslint"
    config_file: ".eslintrc.js"

hooks:
  pre_commit:
    - "eslint --fix"
```

### 集成 Prettier

```yaml
# config.yml
quality:
  code:
    formatter: "prettier"
    config_file: ".prettierrc"

hooks:
  pre_commit:
    - "prettier --write"
```

### 集成 Jest/Vitest

```yaml
# config.yml
quality:
  testing:
    framework: "vitest"
    config_file: "vitest.config.ts"
    coverage_threshold: 80

hooks:
  pre_commit:
    - "vitest run"
```

### 集成 GitHub Actions

```yaml
# .github/workflows/claude-workflow.yml
name: Claude Workflow

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Claude Review
        run: |
          claude workflow run review --pr ${{ github.event.pull_request.number }}
```

---

## 📚 **常见迁移场景**

### 场景 1: 从零开始的新项目

```bash
# 1. 创建项目目录
mkdir my-new-project
cd my-new-project

# 2. 初始化 Git
git init

# 3. 复制工作流
cp -r /path/to/template/.claude .

# 4. 配置项目
cp .claude/config.example.yml .claude/config.yml
vim .claude/config.yml

# 5. 启动工作流
/dev
```

### 场景 2: 迁移现有项目

```bash
# 1. 进入项目目录
cd existing-project

# 2. 备份现有配置
git checkout -b add-claude-workflow

# 3. 复制工作流
cp -r /path/to/template/.claude .

# 4. 配置项目（保留现有技术栈）
cp .claude/config.example.yml .claude/config.yml
# 根据现有项目配置修改 config.yml

# 5. 测试工作流
/dev

# 6. 提交更改
git add .claude/
git commit -m "chore: add Claude workflow system"
```

### 场景 3: 团队协作项目

```bash
# 1. 创建工作流模板仓库
gh repo create team-claude-workflow --public

# 2. 推送工作流文件
cd /path/to/template/.claude
git init
git add .
git commit -m "Initial workflow template"
git remote add origin https://github.com/your-org/team-claude-workflow.git
git push -u origin main

# 3. 在新项目中使用
cd /path/to/new-project
git submodule add https://github.com/your-org/team-claude-workflow.git .claude

# 4. 团队成员克隆项目
git clone --recurse-submodules https://github.com/your-org/new-project.git
```

---

## 🔄 **更新工作流**

### 更新到最新版本

```bash
# 如果使用 Git 子模块
cd .claude
git pull origin main
cd ..
git add .claude
git commit -m "chore: update Claude workflow to latest version"

# 如果直接复制
cp -r /path/to/template/.claude /path/to/project/
# 注意：会覆盖 config.yml，请先备份
```

### 查看更新日志

```bash
cd .claude
git log --oneline
```

---

## 🐛 **故障排除**

### 问题 1: 工作流无法启动

**症状**: 运行 `/dev` 没有响应

**解决方案**:
1. 检查 `config.yml` 是否存在
2. 检查配置文件语法是否正确
3. 检查代理配置是否正确

```bash
# 验证配置
claude config validate

# 查看日志
tail -f .claude/logs/workflow.log
```

### 问题 2: Codex/Gemini 无法调用

**症状**: 提示代理不可用

**解决方案**:
1. 检查 MCP 服务器是否运行
2. 检查代理配置

```yaml
# config.yml
agents:
  backend_expert:
    agent: "codex"
    enabled: true  # 确保启用
```

### 问题 3: 上下文溢出

**症状**: Token 使用超过限制

**解决方案**:
1. 启用 scout 代理
2. 减小任务粒度
3. 使用选择性文件读取

```yaml
# config.yml
context:
  max_tokens_per_step: 30000
  optimization:
    use_scout: true
    selective_read: true
```

---

## 📞 **获取帮助**

### 文档
- **主文档**: `.claude/README.md`
- **配置示例**: `.claude/config.example.yml`
- **迁移指南**: `.claude/MIGRATION_GUIDE.md` (本文件)

### 社区
- **GitHub Issues**: 报告问题和建议
- **Discussions**: 讨论最佳实践
- **Wiki**: 查看详细文档

### 联系方式
- **Email**: support@example.com
- **Slack**: #claude-workflow
- **Discord**: discord.gg/claude-workflow

---

## ✅ **迁移完成检查**

在完成迁移后，请确认：

- [ ] 工作流可以正常启动
- [ ] 需求澄清功能正常
- [ ] 技术分析功能正常
- [ ] 任务原子化功能正常
- [ ] 代码审查功能正常
- [ ] 进度追踪功能正常
- [ ] Git 集成正常
- [ ] 测试集成正常
- [ ] 团队成员可以使用

---

**祝你迁移顺利！** 🎉

如有问题，请参考文档或联系支持团队。
