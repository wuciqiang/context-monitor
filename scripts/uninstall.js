#!/usr/bin/env node
/**
 * Claude Context Monitor - 卸载脚本
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

async function confirm(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise(resolve => {
    rl.question(`${colors.yellow}${question} (y/N): ${colors.reset}`, answer => {
      rl.close();
      resolve(answer.toLowerCase() === 'y');
    });
  });
}

async function main() {
  log('\n🗑️  Claude Context Monitor - Uninstall', 'yellow');
  log('='.repeat(60), 'yellow');

  const shouldUninstall = await confirm('\nAre you sure you want to uninstall the context monitoring system?');

  if (!shouldUninstall) {
    log('\n❌ Uninstall cancelled', 'yellow');
    return;
  }

  log('\n🗑️  Removing files...', 'yellow');

  // 删除文件
  const filesToRemove = [
    '.claude/hooks/capture-session-info.sh',
    '.claude/mcp-servers/context-monitor/server.py',
    '.claude/CONTEXT_MONITORING.md',
    '.claude/test-context-monitor.sh'
  ];

  filesToRemove.forEach(file => {
    if (fs.existsSync(file)) {
      fs.unlinkSync(file);
      log(`✅ Removed ${file}`, 'green');
    }
  });

  // 清理空目录
  const dirsToRemove = [
    '.claude/mcp-servers/context-monitor',
    '.claude/scripts'
  ];

  dirsToRemove.forEach(dir => {
    if (fs.existsSync(dir) && fs.readdirSync(dir).length === 0) {
      fs.rmdirSync(dir);
      log(`✅ Removed empty directory ${dir}`, 'green');
    }
  });

  // 更新 settings.local.json
  const settingsPath = '.claude/settings.local.json';
  if (fs.existsSync(settingsPath)) {
    try {
      const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));

      // 移除 hook
      if (settings.hooks && settings.hooks.SessionStart) {
        delete settings.hooks.SessionStart;
      }

      // 移除 MCP server
      if (settings.mcpServers && settings.mcpServers['context-monitor']) {
        delete settings.mcpServers['context-monitor'];
      }

      fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
      log('✅ Updated settings.local.json', 'green');
    } catch (e) {
      log('⚠️  Failed to update settings.local.json', 'yellow');
    }
  }

  log('\n✅ Uninstall complete', 'green');
  log('\nNote: CLAUDE.md was not modified. Please manually remove context management instructions if needed.', 'yellow');
}

main();
