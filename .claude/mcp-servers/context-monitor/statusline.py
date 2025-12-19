#!/usr/bin/env python3
"""
Context Monitor Statusline
实时显示上下文使用率在 Claude Code 状态栏
"""

import json
import os
from pathlib import Path

def read_session_info():
    """读取会话信息"""
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
    session_file = Path(temp_dir) / "claude-session-info.json"
    if not session_file.exists():
        return None
    try:
        with open(session_file) as f:
            return json.load(f)
    except:
        return None

def get_transcript_size(transcript_path):
    """获取 transcript 文件大小"""
    try:
        return os.path.getsize(transcript_path)
    except:
        return 0

def estimate_token_usage(file_size_bytes):
    """估算 token 使用量"""
    return file_size_bytes / 4

def calculate_usage_percent(estimated_tokens, max_tokens=200000):
    """计算使用率"""
    return (estimated_tokens / max_tokens) * 100

def get_status_icon(usage_percent):
    """根据使用率返回状态图标"""
    if usage_percent < 50:
        return "✅"
    elif usage_percent < 70:
        return "⚠️"
    elif usage_percent < 85:
        return "🔴"
    else:
        return "🚨"

def main():
    """主函数"""
    session_info = read_session_info()

    if not session_info:
        print("Context: N/A")
        return

    transcript_path = session_info.get("transcript_path")
    if not transcript_path or not os.path.exists(transcript_path):
        print("Context: N/A")
        return

    file_size = get_transcript_size(transcript_path)
    estimated_tokens = estimate_token_usage(file_size)
    usage_percent = calculate_usage_percent(estimated_tokens)

    icon = get_status_icon(usage_percent)
    print(f"{icon} Context: {usage_percent:.1f}%")

if __name__ == "__main__":
    main()
