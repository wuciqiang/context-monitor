#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        # 非阻塞错误：记录但不阻止执行
        sys.stderr.write(f"Warning: Invalid JSON input: {e}\n")
        sys.exit(1)
    except Exception as e:
        # 阻塞错误：阻止执行
        sys.stderr.write(f"Error: Failed to read hook input: {e}\n")
        sys.exit(2)

    usage = hook_input.get("usage", {})

    # 验证并获取 token 值
    try:
        cache_read = int(usage.get("cache_read_input_tokens", 0))
        input_tokens = int(usage.get("input_tokens", 0))
        cache_creation = int(usage.get("cache_creation_input_tokens", 0))
        output_tokens = int(usage.get("output_tokens", 0))

        # 验证值的合理性
        if cache_read < 0 or input_tokens < 0 or cache_creation < 0:
            sys.stderr.write("Warning: Negative token values detected\n")
            sys.exit(1)

    except (ValueError, TypeError) as e:
        sys.stderr.write(f"Warning: Invalid token values: {e}\n")
        sys.exit(1)

    context_tokens = cache_read + input_tokens + cache_creation
    max_tokens = 200000
    usage_percent = (context_tokens / max_tokens) * 100

    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
    usage_file = Path(temp_dir) / "claude-current-usage.json"

    usage_data = {
        "context_tokens": context_tokens,
        "usage_percent": usage_percent,
        "cache_read": cache_read,
        "input_tokens": input_tokens,
        "cache_creation": cache_creation,
        "output_tokens": output_tokens
    }

    try:
        with open(usage_file, 'w', encoding='utf-8') as f:
            json.dump(usage_data, f, indent=2)
    except IOError as e:
        sys.stderr.write(f"Error: Failed to write usage file: {e}\n")
        sys.exit(2)
    except Exception as e:
        sys.stderr.write(f"Error: Unexpected error: {e}\n")
        sys.exit(2)

if __name__ == "__main__":
    main()
