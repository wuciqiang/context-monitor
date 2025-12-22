#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SessionEnd Hook
会话结束时清理临时文件并生成最终报告
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Warning: Invalid JSON input: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error: Failed to read hook input: {e}\n")
        sys.exit(2)

    # 读取会话信息和使用数据
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
    session_file = Path(temp_dir) / "claude-session-info.json"
    usage_file = Path(temp_dir) / "claude-current-usage.json"

    session_info = {}
    usage_data = {}

    try:
        if session_file.exists():
            with open(session_file) as f:
                session_info = json.load(f)
    except Exception as e:
        sys.stderr.write(f"Warning: Failed to read session info: {e}\n")

    try:
        if usage_file.exists():
            with open(usage_file) as f:
                usage_data = json.load(f)
    except Exception as e:
        sys.stderr.write(f"Warning: Failed to read usage data: {e}\n")

    # 生成最终报告
    cwd = session_info.get("cwd", ".")
    state_dir = Path(cwd) / ".claude" / "state"

    try:
        state_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        sys.stderr.write(f"Warning: Failed to create state directory: {e}\n")

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    session_id = session_info.get("session_id", "unknown")
    report_file = state_dir / f"session-end-{session_id}-{timestamp}.json"

    report_data = {
        "event": "session_end",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "session_id": session_id,
        "final_usage_percent": usage_data.get("usage_percent", 0),
        "final_context_tokens": usage_data.get("context_tokens", 0),
        "transcript_path": session_info.get("transcript_path", ""),
        "cwd": cwd
    }

    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
    except IOError as e:
        sys.stderr.write(f"Warning: Failed to write report file: {e}\n")

    # 清理临时文件（可选）
    # 注释掉以保留临时文件用于调试
    # try:
    #     if session_file.exists():
    #         session_file.unlink()
    #     if usage_file.exists():
    #         usage_file.unlink()
    # except Exception as e:
    #     sys.stderr.write(f"Warning: Failed to cleanup temp files: {e}\n")

if __name__ == "__main__":
    main()
