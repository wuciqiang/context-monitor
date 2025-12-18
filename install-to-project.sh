#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Context Monitor 项目安装脚本 ==="
echo ""

if [ -z "$1" ]; then
    read -p "请输入目标项目路径: " TARGET_DIR
else
    TARGET_DIR="$1"
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "错误: 目录不存在: $TARGET_DIR"
    exit 1
fi

TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"
echo "目标项目: $TARGET_DIR"
echo ""

echo "[1/5] 创建目录结构..."
mkdir -p "$TARGET_DIR/.claude/hooks"
mkdir -p "$TARGET_DIR/.claude/mcp-servers/context-monitor"
mkdir -p "$TARGET_DIR/.claude/state"

echo "[2/5] 复制文件..."
cp "$SCRIPT_DIR/.claude/hooks/capture-session-info.py" "$TARGET_DIR/.claude/hooks/"
cp "$SCRIPT_DIR/.claude/mcp-servers/context-monitor/server.py" "$TARGET_DIR/.claude/mcp-servers/context-monitor/"
chmod +x "$TARGET_DIR/.claude/hooks/capture-session-info.py"
chmod +x "$TARGET_DIR/.claude/mcp-servers/context-monitor/server.py"

echo "[3/5] 配置 .mcp.json..."
MCP_FILE="$TARGET_DIR/.mcp.json"

if [ -f "$MCP_FILE" ]; then
    echo "检测到现有 .mcp.json，备份为 .mcp.json.backup"
    cp "$MCP_FILE" "$MCP_FILE.backup"
fi

cat > "$MCP_FILE" << 'EOF'
{
  "mcpServers": {
    "context-monitor": {
      "type": "stdio",
      "command": "python3",
      "args": [".claude/mcp-servers/context-monitor/server.py"],
      "env": {}
    }
  }
}
EOF

echo "[4/5] 配置 .claude/settings.local.json..."
SETTINGS_FILE="$TARGET_DIR/.claude/settings.local.json"

if [ -f "$SETTINGS_FILE" ]; then
    echo "检测到现有配置文件，备份为 settings.local.json.backup"
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"
fi

cat > "$SETTINGS_FILE" << 'EOF'
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture-session-info.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
EOF

echo "[5/5] 验证安装..."
if [ -f "$TARGET_DIR/.claude/hooks/capture-session-info.py" ] && \
   [ -f "$TARGET_DIR/.claude/mcp-servers/context-monitor/server.py" ] && \
   [ -f "$TARGET_DIR/.claude/settings.local.json" ] && \
   [ -f "$TARGET_DIR/.mcp.json" ]; then
    echo ""
    echo "✅ Context Monitor 安装成功！"
    echo ""
    echo "安装位置: $TARGET_DIR"
    echo ""
    echo "已创建文件:"
    echo "  - .mcp.json (MCP server 配置)"
    echo "  - .claude/settings.local.json (Hook 配置)"
    echo "  - .claude/hooks/capture-session-info.py"
    echo "  - .claude/mcp-servers/context-monitor/server.py"
    echo ""
    echo "下一步:"
    echo "1. cd $TARGET_DIR"
    echo "2. claude"
    echo "3. 批准 context-monitor MCP server"
    echo "4. 在对话中输入: 请检查当前上下文使用率"
else
    echo "❌ 安装验证失败"
    exit 1
fi
