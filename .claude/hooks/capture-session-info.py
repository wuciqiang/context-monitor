#!/usr/bin/env python3
"""SessionStart hook: 捕获会话信息供 MCP server 使用"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path

def main():
    # 读取 hook 输入
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    # 提取信息
    session_id = input_data.get('session_id', '')
    transcript_path = input_data.get('transcript_path', '')
    cwd = input_data.get('cwd', '')

    # Windows 兼容的临时目录
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
    session_info_file = os.path.join(temp_dir, 'claude-session-info.json')

    # 写入共享文件供 MCP server 读取
    session_info = {
        'session_id': session_id,
        'transcript_path': transcript_path,
        'cwd': cwd,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

    try:
        with open(session_info_file, 'w', encoding='utf-8') as f:
            json.dump(session_info, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to write session info: {e}", file=sys.stderr)

    # 输出到 stderr（用户终端可见）
    print("Context monitoring active. Session started.", file=sys.stderr)

    # 输出到 stdout（添加到 Claude 的上下文）
    print("请立即调用 check_context_usage 工具检查当前上下文使用率。")

if __name__ == '__main__':
    main()
