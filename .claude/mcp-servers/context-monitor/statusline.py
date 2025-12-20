#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def read_session_info():
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
    session_file = Path(temp_dir) / "claude-session-info.json"
    if not session_file.exists():
        return None
    try:
        with open(session_file) as f:
            return json.load(f)
    except:
        return None

def estimate_usage_from_file(transcript_path):
    """基于文件大小估算,但限制最大值为100%"""
    try:
        size = os.path.getsize(transcript_path)
        # 假设平均每个token 4字节,200k tokens = 800KB
        estimated_tokens = size / 4
        usage = (estimated_tokens / 200000) * 100
        # 限制最大100%
        return min(usage, 100.0)
    except:
        return 0

def get_status_icon(usage_percent):
    if usage_percent < 50:
        return "[OK]"
    elif usage_percent < 70:
        return "[WARN]"
    elif usage_percent < 85:
        return "[HIGH]"
    else:
        return "[CRIT]"

def main():
    session_info = read_session_info()
    if not session_info:
        print("Context: N/A")
        return

    transcript_path = session_info.get("transcript_path")
    if not transcript_path or not os.path.exists(transcript_path):
        print("Context: N/A")
        return

    usage_percent = estimate_usage_from_file(transcript_path)
    icon = get_status_icon(usage_percent)
    print(f"{icon} Context: {usage_percent:.1f}%")

if __name__ == "__main__":
    main()
