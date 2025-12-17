#!/bin/bash
# SessionStart hook: 捕获会话信息供 MCP server 使用

# 读取 hook 输入
input=$(cat)

# 提取 transcript_path 和 session_id
transcript_path=$(echo "$input" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('transcript_path', ''))")
session_id=$(echo "$input" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('session_id', ''))")
cwd=$(echo "$input" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('cwd', ''))")

# 写入共享文件供 MCP server 读取
session_info_file="/tmp/claude-session-info.json"
cat > "$session_info_file" <<EOF
{
  "session_id": "$session_id",
  "transcript_path": "$transcript_path",
  "cwd": "$cwd",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

# 输出提示信息（会被添加到 Claude 的上下文）
echo "📊 Context monitoring active. Use check_context_usage tool to monitor usage."
