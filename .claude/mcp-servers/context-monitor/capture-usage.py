#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    # 读取stdin的hook数据
    try:
        hook_data = json.loads(sys.stdin.read())
        usage = hook_data.get('usage', {})

        if not usage:
            sys.exit(0)

        # 计算当前上下文
        context_tokens = (
            usage.get('cache_read_input_tokens', 0) +
            usage.get('input_tokens', 0) +
            usage.get('cache_creation_input_tokens', 0)
        )

        # 保存到临时文件
        temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
        usage_file = Path(temp_dir) / "claude-current-usage.json"

        with open(usage_file, 'w') as f:
            json.dump({
                'context_tokens': context_tokens,
                'usage_percent': (context_tokens / 200000) * 100,
                'raw_usage': usage
            }, f)
    except:
        pass

if __name__ == "__main__":
    main()
