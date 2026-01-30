#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 历史记录最大条数
MAX_HISTORY_ENTRIES = 1000

def get_temp_dir():
    return os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'

def read_previous_tokens(usage_file):
    """读取上一次的 context_tokens 用于计算 delta"""
    try:
        if usage_file.exists():
            with open(usage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('context_tokens', 0)
    except:
        pass
    return 0

def append_history(session_id, context_tokens, previous_tokens, tool_name):
    """追加历史记录到 jsonl 文件"""
    temp_dir = get_temp_dir()
    history_file = Path(temp_dir) / f"claude-usage-history-{session_id}.jsonl"

    entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'context_tokens': context_tokens,
        'delta': context_tokens - previous_tokens,
        'tool_name': tool_name
    }

    try:
        # 检查文件大小，超过限制则轮转
        if history_file.exists():
            line_count = sum(1 for _ in open(history_file, 'r', encoding='utf-8'))
            if line_count >= MAX_HISTORY_ENTRIES:
                # 保留最近一半的记录
                with open(history_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                with open(history_file, 'w', encoding='utf-8') as f:
                    f.writelines(lines[len(lines)//2:])

        with open(history_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        sys.stderr.write(f"Warning: Failed to write history: {e}\n")

def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Warning: Invalid JSON input: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error: Failed to read hook input: {e}\n")
        sys.exit(2)

    usage = hook_input.get("usage", {})
    session_id = hook_input.get("session_id", "default")
    tool_name = hook_input.get("tool_name", "unknown")
    model_id = hook_input.get("model", {}).get("id", None)

    # 验证并获取 token 值
    try:
        cache_read = int(usage.get("cache_read_input_tokens", 0))
        input_tokens = int(usage.get("input_tokens", 0))
        cache_creation = int(usage.get("cache_creation_input_tokens", 0))
        output_tokens = int(usage.get("output_tokens", 0))

        if cache_read < 0 or input_tokens < 0 or cache_creation < 0:
            sys.stderr.write("Warning: Negative token values detected\n")
            sys.exit(1)

    except (ValueError, TypeError) as e:
        sys.stderr.write(f"Warning: Invalid token values: {e}\n")
        sys.exit(1)

    context_tokens = cache_read + input_tokens + cache_creation

    temp_dir = get_temp_dir()

    # 会话隔离: 使用 session_id 区分文件
    usage_file = Path(temp_dir) / f"claude-usage-{session_id}.json"
    # 兼容旧版: 同时写入默认文件
    default_usage_file = Path(temp_dir) / "claude-current-usage.json"

    # 读取上一次的 tokens 用于计算 delta
    previous_tokens = read_previous_tokens(usage_file)

    usage_data = {
        "context_tokens": context_tokens,
        "session_id": session_id,
        "model_id": model_id,
        "cache_read": cache_read,
        "input_tokens": input_tokens,
        "cache_creation": cache_creation,
        "output_tokens": output_tokens,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }

    try:
        # 写入会话专属文件
        with open(usage_file, 'w', encoding='utf-8') as f:
            json.dump(usage_data, f, indent=2)

        # 兼容旧版: 同时写入默认文件
        with open(default_usage_file, 'w', encoding='utf-8') as f:
            json.dump(usage_data, f, indent=2)

        # 追加历史记录
        append_history(session_id, context_tokens, previous_tokens, tool_name)

    except IOError as e:
        sys.stderr.write(f"Error: Failed to write usage file: {e}\n")
        sys.exit(2)
    except Exception as e:
        sys.stderr.write(f"Error: Unexpected error: {e}\n")
        sys.exit(2)

if __name__ == "__main__":
    main()
