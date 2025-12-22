#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Capture Session Hook
在会话开始时捕获会话信息并保存到临时文件
"""

import json
import os
import sys
from pathlib import Path

def main():
    # 从 stdin 读取 hook 输入
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Warning: Invalid JSON input: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error: Failed to read hook input: {e}\n")
        sys.exit(2)

    # 提取会话信息
    session_id = hook_input.get("sessionId", "unknown")
    transcript_path = hook_input.get("transcriptPath", "")
    cwd = hook_input.get("cwd", ".")

    # 如果 transcript_path 为空，尝试从环境变量或默认位置获取
    if not transcript_path:
        # 尝试从 cwd 推断 transcript 路径
        claude_dir = Path.home() / ".claude" / "projects"
        if claude_dir.exists():
            # 查找最新的 .jsonl 文件
            try:
                jsonl_files = list(claude_dir.rglob("*.jsonl"))
                if jsonl_files:
                    # 按修改时间排序，取最新的
                    transcript_path = str(max(jsonl_files, key=lambda p: p.stat().st_mtime))
            except Exception as e:
                sys.stderr.write(f"Warning: Failed to find transcript files: {e}\n")

    # 如果 session_id 是 unknown，尝试从 transcript_path 文件名提取
    if session_id == "unknown" and transcript_path:
        # transcript_path 格式: .../e58f2582-21dd-4ae9-bcfb-92a53c376293.jsonl
        filename = Path(transcript_path).stem
        if len(filename) == 36 and filename.count('-') == 4:  # UUID 格式
            session_id = filename

    # 保存到临时文件
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
    session_file = Path(temp_dir) / "claude-session-info.json"

    session_info = {
        "session_id": session_id,
        "transcript_path": transcript_path,
        "cwd": cwd
    }

    try:
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_info, f, indent=2)
    except IOError as e:
        sys.stderr.write(f"Error: Failed to write session file: {e}\n")
        sys.exit(2)
    except Exception as e:
        sys.stderr.write(f"Error: Unexpected error: {e}\n")
        sys.exit(2)

if __name__ == "__main__":
    main()
