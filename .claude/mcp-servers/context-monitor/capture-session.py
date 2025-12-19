#!/usr/bin/env python3
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
    except:
        sys.exit(0)

    # 提取会话信息
    session_id = hook_input.get("sessionId", "unknown")
    transcript_path = hook_input.get("transcriptPath", "")
    cwd = hook_input.get("cwd", ".")

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
    except:
        pass

if __name__ == "__main__":
    main()
