# GitHub 设置指南
# GitHub Setup Guide

> 如何将项目提交到 GitHub

---

## 🚀 快速开始

### Step 1: 初始化 Git 仓库

```bash
cd F:\LayaAir-GitHub\context-monitor
git init
git add .
git commit -m "Initial commit: Claude Context Monitor v1.0.0"
```

### Step 2: 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 填写信息：
   - **Repository name**: `context-monitor`
   - **Description**: `Semi-automated context usage monitoring system for Claude Code`
   - **Public** (推荐，npm 包通常是公开的)
   - **不要**勾选 "Initialize with README"（我们已经有了）

3. 点击 "Create repository"

### Step 3: 关联远程仓库

```bash
# 替换 YOUR-USERNAME 为你的 GitHub 用户名
git remote add origin https://github.com/YOUR-USERNAME/context-monitor.git

# 或使用 SSH
git remote add origin git@github.com:YOUR-USERNAME/context-monitor.git
```

### Step 4: 推送代码

```bash
git branch -M main
git push -u origin main
```

---

## 📋 推荐的仓库设置

### 1. 添加 Topics

在 GitHub 仓库页面，点击 "Add topics"，添加：
- `claude-code`
- `claude`
- `context-monitoring`
- `mcp-server`
- `hooks`
- `ai`
- `anthropic`
- `automation`
- `npm-package`

### 2. 设置 About

在仓库页面右侧，点击设置图标，填写：
- **Description**: `Semi-automated context usage monitoring system for Claude Code`
- **Website**: `https://www.npmjs.com/package/@claude/context-monitor`（发布后）

### 3. 启用 Issues

Settings → Features → Issues ✅

### 4. 创建 Branch Protection Rules（可选）

Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging

---

## 🏷️ 创建 Release

### 方式 1: 通过 GitHub 网页

1. 访问仓库页面
2. 点击 "Releases" → "Create a new release"
3. 填写：
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**:
     ```markdown
     ## 🎉 Initial Release

     ### Features
     - ✅ Automatic context usage monitoring
     - ✅ SessionStart hook for session tracking
     - ✅ MCP server with monitoring tools
     - ✅ Smart alerts based on usage thresholds
     - ✅ Session state saving and recovery
     - ✅ npm installation support

     ### Installation
     ```bash
     npm install @claude/context-monitor
     npm run init
     ```

     ### Documentation
     - [README](./README.md)
     - [Installation Guide](./INSTALL.md)
     - [Usage Guide](./CONTEXT_MONITORING.md)
     ```

4. 点击 "Publish release"

### 方式 2: 通过命令行

```bash
# 创建 tag
git tag -a v1.0.0 -m "Release v1.0.0"

# 推送 tag
git push origin v1.0.0

# 然后在 GitHub 网页上创建 Release
```

---

## 📝 README Badge

在 README.md 顶部添加 badges：

```markdown
[![npm version](https://badge.fury.io/js/@claude%2Fcontext-monitor.svg)](https://www.npmjs.com/package/@claude/context-monitor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/YOUR-USERNAME/context-monitor.svg?style=social)](https://github.com/YOUR-USERNAME/context-monitor)
```

---

## 🔄 后续更新流程

### 1. 开发新功能

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 开发...
git add .
git commit -m "feat: add new feature"

# 推送分支
git push origin feature/new-feature
```

### 2. 创建 Pull Request

在 GitHub 上创建 PR，合并到 main。

### 3. 发布新版本

```bash
# 切换到 main
git checkout main
git pull

# 更新版本
npm version patch  # 或 minor / major

# 推送
git push && git push --tags

# 发布到 npm
npm publish --access public

# 在 GitHub 创建 Release
```

---

## 📊 GitHub Actions（可选）

### 自动测试

创建 `.github/workflows/test.yml`：

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - run: npm install
      - run: npm test
```

### 自动发布

创建 `.github/workflows/publish.yml`：

```yaml
name: Publish

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm test
      - run: npm publish --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## 🎯 完整命令总结

```bash
# 1. 初始化 Git
cd F:\LayaAir-GitHub\context-monitor
git init
git add .
git commit -m "Initial commit: Claude Context Monitor v1.0.0"

# 2. 关联 GitHub（替换 YOUR-USERNAME）
git remote add origin https://github.com/YOUR-USERNAME/context-monitor.git

# 3. 推送代码
git branch -M main
git push -u origin main

# 4. 创建 tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 5. 在 GitHub 网页上创建 Release

# 6. 发布到 npm
npm login
npm publish --access public
```

---

## ✅ 检查清单

发布前确认：

- [ ] Git 仓库已初始化
- [ ] 代码已推送到 GitHub
- [ ] README.md 清晰完整
- [ ] LICENSE 文件存在
- [ ] package.json 中的 repository URL 正确
- [ ] 已创建 v1.0.0 tag
- [ ] 已在 GitHub 创建 Release
- [ ] 已发布到 npm
- [ ] npm 页面显示正常
- [ ] 测试安装成功

---

**准备好了吗？开始发布吧！** 🚀
