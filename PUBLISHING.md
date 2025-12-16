# 发布指南
# Publishing Guide

> 如何将 @claude/context-monitor 发布到 npm

---

## 📋 发布前检查清单

### 1. 更新版本号

编辑 `package.json`：

```json
{
  "version": "1.0.0"  // 更新版本号
}
```

或使用 npm 命令：

```bash
# 补丁版本 (1.0.0 -> 1.0.1)
npm version patch

# 次要版本 (1.0.0 -> 1.1.0)
npm version minor

# 主要版本 (1.0.0 -> 2.0.0)
npm version major
```

### 2. 更新 repository URL

编辑 `package.json`，替换为你的 GitHub 仓库：

```json
{
  "repository": {
    "type": "git",
    "url": "https://github.com/YOUR-USERNAME/context-monitor.git"
  },
  "bugs": {
    "url": "https://github.com/YOUR-USERNAME/context-monitor/issues"
  },
  "homepage": "https://github.com/YOUR-USERNAME/context-monitor#readme"
}
```

### 3. 测试包

```bash
# 本地测试
npm run test

# 测试打包
npm pack

# 查看将要发布的文件
npm publish --dry-run
```

---

## 🚀 首次发布

### Step 1: 创建 npm 账号

访问 https://www.npmjs.com/signup 注册账号。

### Step 2: 登录 npm

```bash
npm login
```

输入：
- Username
- Password
- Email
- One-time password (如果启用了 2FA)

### Step 3: 检查包名是否可用

```bash
npm search @claude/context-monitor
```

如果包名已被占用，需要修改 `package.json` 中的 `name` 字段。

### Step 4: 发布到 npm

```bash
# 发布公开包
npm publish --access public

# 如果是 scoped package (@claude/xxx)，必须加 --access public
```

---

## 🔄 更新发布

### Step 1: 提交所有更改

```bash
git add .
git commit -m "chore: release v1.0.1"
git push
```

### Step 2: 更新版本号

```bash
npm version patch  # 或 minor / major
```

这会自动：
- 更新 `package.json` 中的版本号
- 创建 git tag
- 提交更改

### Step 3: 推送 tag

```bash
git push --tags
```

### Step 4: 发布新版本

```bash
npm publish --access public
```

---

## 📦 发布流程自动化

### 使用 GitHub Actions

创建 `.github/workflows/publish.yml`：

```yaml
name: Publish to npm

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

### 配置 npm token

1. 在 npm 网站生成 token：https://www.npmjs.com/settings/YOUR-USERNAME/tokens
2. 在 GitHub 仓库设置中添加 secret：`NPM_TOKEN`

---

## 🏷️ 版本管理

### 语义化版本 (Semver)

格式：`MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的 API 更改
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

### 版本标签

```bash
# Beta 版本
npm version 1.1.0-beta.0
npm publish --tag beta

# Alpha 版本
npm version 1.1.0-alpha.0
npm publish --tag alpha

# 安装特定标签
npm install @claude/context-monitor@beta
```

---

## 📊 发布后验证

### 1. 检查 npm 页面

访问：https://www.npmjs.com/package/@claude/context-monitor

### 2. 测试安装

```bash
# 在新目录测试
mkdir test-install
cd test-install
npm init -y
npm install @claude/context-monitor
npm run init
```

### 3. 检查文档

确保 README.md 在 npm 页面正确显示。

---

## 🔧 常见问题

### Q: 发布失败 - 403 Forbidden

**A**: 检查：
1. 是否已登录：`npm whoami`
2. 包名是否已被占用
3. 是否有发布权限（scoped packages 需要 `--access public`）

### Q: 发布失败 - 包名不符合规范

**A**: 包名必须：
- 小写字母
- 可以包含 `-` 和 `_`
- scoped packages: `@scope/name`

### Q: 如何撤销已发布的版本？

**A**:
```bash
# 撤销特定版本（发布后 72 小时内）
npm unpublish @claude/context-monitor@1.0.0

# 撤销整个包（慎用！）
npm unpublish @claude/context-monitor --force
```

### Q: 如何废弃某个版本？

**A**:
```bash
npm deprecate @claude/context-monitor@1.0.0 "This version has a critical bug"
```

---

## 📝 发布检查清单

发布前确认：

- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] CHANGELOG.md 已更新
- [ ] 版本号已更新
- [ ] Git tag 已创建
- [ ] README.md 清晰易懂
- [ ] LICENSE 文件存在
- [ ] .npmignore 配置正确
- [ ] package.json 信息完整

---

## 🎯 快速发布命令

```bash
# 完整发布流程
npm test                          # 测试
npm version patch                 # 更新版本
git push && git push --tags       # 推送代码和标签
npm publish --access public       # 发布到 npm
```

---

## 📚 相关资源

- [npm 文档](https://docs.npmjs.com/)
- [语义化版本](https://semver.org/lang/zh-CN/)
- [npm 发布指南](https://docs.npmjs.com/cli/v8/commands/npm-publish)

---

**祝发布顺利！** 🚀
