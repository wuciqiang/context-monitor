#!/usr/bin/env node
/**
 * Claude Context Monitor - 初始化脚本
 * 自动设置上下文监控系统到当前项目
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function checkPrerequisites() {
  log('\n🔍 Checking prerequisites...', 'blue');

  // 检查 Python
  try {
    execSync('python3 --version', { stdio: 'ignore' });
    log('✅ Python 3 found', 'green');
  } catch {
    log('❌ Python 3 not found. Please install Python 3.', 'red');
    process.exit(1);
  }

  // 检查 bash (Windows 可能需要 Git Bash)
  try {
    execSync('bash --version', { stdio: 'ignore' });
    log('✅ Bash found', 'green');
  } catch {
    log('⚠️  Bash not found. Hooks may not work on Windows without Git Bash.', 'yellow');
  }
}

function createDirectories() {
  log('\n📁 Creating directories...', 'blue');

  const dirs = [
    '.claude',
    '.claude/hooks',
    '.claude/mcp-servers',
    '.claude/mcp-servers/context-monitor',
    '.claude/state',
    '.claude/scripts'
  ];

  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      log(`✅ Created ${dir}`, 'green');
    } else {
      log(`⏭️  ${dir} already exists`, 'yellow');
    }
  });
}

function copyFiles() {
  log('\n📄 Copying files...', 'blue');

  const sourceDir = path.join(__dirname, '..');
  const targetDir = process.cwd();

  const files = [
    { src: 'hooks/capture-session-info.sh', dest: '.claude/hooks/capture-session-info.sh' },
    { src: 'mcp-servers/context-monitor/server.py', dest: '.claude/mcp-servers/context-monitor/server.py' },
    { src: 'CONTEXT_MONITORING.md', dest: '.claude/CONTEXT_MONITORING.md' },
    { src: 'test-context-monitor.sh', dest: '.claude/test-context-monitor.sh' }
  ];

  files.forEach(({ src, dest }) => {
    const sourcePath = path.join(sourceDir, src);
    const destPath = path.join(targetDir, dest);

    if (fs.existsSync(sourcePath)) {
      fs.copyFileSync(sourcePath, destPath);

      // 设置执行权限 (Unix-like systems)
      if (process.platform !== 'win32' && (src.endsWith('.sh') || src.endsWith('.py'))) {
        fs.chmodSync(destPath, '755');
      }

      log(`✅ Copied ${dest}`, 'green');
    } else {
      log(`⚠️  Source file not found: ${src}`, 'yellow');
    }
  });
}

function updateSettings() {
  log('\n⚙️  Updating settings...', 'blue');

  const settingsPath = '.claude/settings.local.json';
  let settings = {};

  // 读取现有配置
  if (fs.existsSync(settingsPath)) {
    try {
      settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
      log('📖 Loaded existing settings', 'blue');
    } catch (e) {
      log('⚠️  Failed to parse existing settings, creating new', 'yellow');
    }
  }

  // 添加 hooks 配置
  if (!settings.hooks) {
    settings.hooks = {};
  }

  settings.hooks.SessionStart = [
    {
      hooks: [
        {
          type: 'command',
          command: 'bash .claude/hooks/capture-session-info.sh',
          timeout: 5
        }
      ]
    }
  ];

  // 添加 MCP server 配置
  if (!settings.mcpServers) {
    settings.mcpServers = {};
  }

  settings.mcpServers['context-monitor'] = {
    command: 'python3',
    args: ['.claude/mcp-servers/context-monitor/server.py'],
    env: {}
  };

  // 写入配置
  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
  log('✅ Updated settings.local.json', 'green');
}

function updateClaudeMd() {
  log('\n📝 Updating CLAUDE.md...', 'blue');

  const claudeMdPath = 'CLAUDE.md';
  const contextInstructions = `
## 🔄 上下文管理（Context Management）

**自动监控系统已启用**

本项目配置了上下文使用率监控系统。你必须遵守以下规则：

### 监控规则

1. **定期检查**：每完成 5-10 个工具调用后，使用 \`check_context_usage\` 工具检查上下文使用率
2. **响应警告**：
   - **< 50%**: 继续正常工作
   - **50-70%**: 注意使用率，考虑尽快完成当前任务
   - **70-85%**: 立即完成当前任务，准备保存状态
   - **> 85%**: 🚨 **紧急**：立即执行以下步骤

### 高使用率应急流程

当 \`check_context_usage\` 返回 > 70% 时，必须立即执行：

\`\`\`
1. 停止当前任务（如果接近完成则快速完成）
2. 使用 save_session_state 工具保存状态：
   - content: 当前进度、已完成内容、关键决策
   - next_steps: 下一步要做什么、如何继续
3. 向用户输出：
   "⚠️ 上下文使用率已达 XX%，已保存会话状态到 .claude/state/current-session.md

   请执行以下命令清除上下文：
   /clear

   清除后，使用以下提示词继续：
   请阅读 .claude/state/current-session.md 了解当前进度，然后继续 [具体任务]"
\`\`\`

---
`;

  if (fs.existsSync(claudeMdPath)) {
    let content = fs.readFileSync(claudeMdPath, 'utf8');

    // 检查是否已经包含上下文管理部分
    if (content.includes('上下文管理')) {
      log('⏭️  CLAUDE.md already contains context management instructions', 'yellow');
    } else {
      // 在文件开头添加（在第一个 ## 之前）
      const lines = content.split('\n');
      const firstHeaderIndex = lines.findIndex(line => line.startsWith('## '));

      if (firstHeaderIndex !== -1) {
        lines.splice(firstHeaderIndex, 0, contextInstructions);
        content = lines.join('\n');
      } else {
        content = contextInstructions + '\n' + content;
      }

      fs.writeFileSync(claudeMdPath, content);
      log('✅ Updated CLAUDE.md with context management instructions', 'green');
    }
  } else {
    // 创建新的 CLAUDE.md
    const newContent = `# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

---
${contextInstructions}
`;
    fs.writeFileSync(claudeMdPath, newContent);
    log('✅ Created CLAUDE.md with context management instructions', 'green');
  }
}

function printNextSteps() {
  log('\n' + '='.repeat(60), 'blue');
  log('✅ Context Monitoring System Installed Successfully!', 'green');
  log('='.repeat(60), 'blue');

  log('\n📚 Next Steps:', 'blue');
  log('1. Test the system:', 'yellow');
  log('   npm run test', 'reset');
  log('');
  log('2. Start a new Claude Code session:', 'yellow');
  log('   claude', 'reset');
  log('');
  log('3. Ask Claude to check context usage:', 'yellow');
  log('   "请检查当前上下文使用率"', 'reset');
  log('');
  log('4. Read the documentation:', 'yellow');
  log('   cat .claude/CONTEXT_MONITORING.md', 'reset');
  log('');
  log('📖 Documentation: .claude/CONTEXT_MONITORING.md', 'blue');
  log('');
}

// 主函数
function main() {
  log('\n🚀 Claude Context Monitor - Initialization', 'blue');
  log('='.repeat(60), 'blue');

  try {
    checkPrerequisites();
    createDirectories();
    copyFiles();
    updateSettings();
    updateClaudeMd();
    printNextSteps();
  } catch (error) {
    log(`\n❌ Installation failed: ${error.message}`, 'red');
    process.exit(1);
  }
}

main();
