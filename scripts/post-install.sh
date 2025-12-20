#!/bin/bash
# PostInstall hook - 自动配置 statusLine

SETTINGS_FILE=".claude/settings.json"

# 创建 .claude 目录
mkdir -p .claude

# 获取插件路径
PLUGIN_PATH=$(echo ~/.claude/plugins/cm@*)
STATUSLINE_SCRIPT="$PLUGIN_PATH/.claude/mcp-servers/context-monitor/statusline.py"

# 读取或创建 settings.json
if [ -f "$SETTINGS_FILE" ]; then
    # 已存在,合并配置
    python3 << PYTHON
import json
with open('$SETTINGS_FILE', 'r') as f:
    settings = json.load(f)
settings['statusLine'] = {
    'type': 'command',
    'command': 'python $STATUSLINE_SCRIPT',
    'padding': 0
}
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(settings, f, indent=2)
PYTHON
else
    # 新建配置
    cat > "$SETTINGS_FILE" << JSON
{
  "statusLine": {
    "type": "command",
    "command": "python $STATUSLINE_SCRIPT",
    "padding": 0
  }
}
JSON
fi

echo "✅ statusLine 已自动配置"
echo "🔄 请重启 Claude Code 让配置生效"
