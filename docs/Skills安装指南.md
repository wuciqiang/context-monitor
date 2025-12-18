# Skills 安装指南
# Multi-Model Collaboration Skills Installation Guide

> 安装 Codex 和 Gemini 协作技能，实现多模型协作

---

## 📖 关于 Skills

本项目的多模型协作功能基于 [GuDaStudio/skills](https://github.com/GuDaStudio/skills) 开源项目，提供：

- **collaborating-with-codex** - 与 OpenAI Codex 协作（后端逻辑、算法分析）
- **collaborating-with-gemini** - 与 Google Gemini 协作（前端 UI、样式设计）

---

## 🎯 前置要求

### 1. Codex CLI

安装 OpenAI Codex CLI：
```bash
# 使用 npm 安装
npm install -g @openai/codex-cli

# 或使用 pip 安装
pip install openai-codex-cli
```

配置 API Key：
```bash
export OPENAI_API_KEY="your-api-key"
```

### 2. Gemini CLI

安装 Google Gemini CLI：
```bash
# 使用 npm 安装
npm install -g @google/gemini-cli

# 或使用 pip 安装
pip install google-gemini-cli
```

配置 API Key：
```bash
export GEMINI_API_KEY="your-api-key"
```

---

## 🚀 安装 Skills

### 方式 1: 从 GitHub 克隆（推荐）

```bash
# 克隆 GuDaStudio Skills 仓库
git clone https://github.com/GuDaStudio/skills.git /tmp/gudastudio-skills

# 复制到 Claude Code 全局 skills 目录
cp -r /tmp/gudastudio-skills/collaborating-with-codex ~/.claude/skills/
cp -r /tmp/gudastudio-skills/collaborating-with-gemini ~/.claude/skills/

# 清理临时文件
rm -rf /tmp/gudastudio-skills
```

### 方式 2: 手动下载

1. 访问 https://github.com/GuDaStudio/skills
2. 下载仓库 ZIP 文件
3. 解压后复制 `collaborating-with-codex` 和 `collaborating-with-gemini` 到：
   - Windows: `C:\Users\<username>\.claude\skills\`
   - macOS/Linux: `~/.claude/skills/`

---

## ✅ 验证安装

### 1. 检查目录结构

```bash
# Windows
dir C:\Users\admin\.claude\skills

# macOS/Linux
ls -la ~/.claude/skills/
```

应该看到：
```
.claude/skills/
├── collaborating-with-codex/
│   ├── scripts/
│   ├── SKILL.md
│   └── README.md
└── collaborating-with-gemini/
    ├── scripts/
    ├── SKILL.md
    └── README.md
```

### 2. 测试 Codex Skill

启动 Claude Code，在对话中输入：
```
请使用 Codex 分析以下代码的时间复杂度：
[粘贴代码]
```

### 3. 测试 Gemini Skill

在对话中输入：
```
请使用 Gemini 设计一个现代化的登录页面
```

---

## 🔧 配置说明

### Skill 配置文件

每个 Skill 包含 `SKILL.md` 文件，定义了：
- Skill 的触发条件
- 可用的工具和参数
- 使用示例

Claude Code 会自动加载这些配置。

### 环境变量

确保设置了必要的 API Keys：

**Windows (PowerShell)**:
```powershell
$env:OPENAI_API_KEY = "your-openai-key"
$env:GEMINI_API_KEY = "your-gemini-key"
```

**macOS/Linux (Bash)**:
```bash
export OPENAI_API_KEY="your-openai-key"
export GEMINI_API_KEY="your-gemini-key"
```

建议将这些环境变量添加到：
- Windows: 系统环境变量
- macOS/Linux: `~/.bashrc` 或 `~/.zshrc`

---

## 📋 工作流集成

安装 Skills 后，CLAUDE.md 中定义的整合工作流会自动使用这些 Skills：

### Phase 2: 多模型分析
Claude 会自动调用 Codex 和 Gemini 进行交叉验证分析

### Phase 3: 原型获取
- **前端/UI 任务** → 自动使用 Gemini
- **后端/逻辑任务** → 自动使用 Codex

### Phase 5: 审计与交付
自动并行调用 Codex 和 Gemini 进行代码审计

---

## 🐛 故障排查

### Q: Skills 没有被识别

**A**: 检查目录结构和文件权限：
```bash
ls -la ~/.claude/skills/collaborating-with-codex/
chmod -R 755 ~/.claude/skills/
```

### Q: API Key 错误

**A**: 验证环境变量：
```bash
echo $OPENAI_API_KEY
echo $GEMINI_API_KEY
```

### Q: Codex/Gemini CLI 找不到

**A**: 确认 CLI 已安装并在 PATH 中：
```bash
which codex
which gemini
```

### Q: 想只使用其中一个 Skill

**A**: 只安装需要的 Skill 即可。工作流会自动适应可用的 Skills。

---

## 📚 相关资源

- **GuDaStudio Skills 仓库**: https://github.com/GuDaStudio/skills
- **OpenAI Codex 文档**: https://platform.openai.com/docs/guides/codex
- **Google Gemini 文档**: https://ai.google.dev/docs

---

## 🔗 下一步

安装完 Skills 后：
1. 返回 [全局安装指南.md](./全局安装指南.md) 继续完成全局配置
2. 阅读 [整合工作流指南.md](./整合工作流指南.md) 了解如何使用
3. 查看 [CLAUDE.md](./CLAUDE.md) 了解完整的工作流定义

---

**注意**: Skills 是可选的。如果不安装 Skills，系统仍然可以工作，但会缺少多模型协作功能。
