#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

def main():
    try:
        hook_input = json.load(sys.stdin)
    except:
        sys.exit(0)

    usage = hook_input.get("usage", {})
    cache_read = usage.get("cache_read_input_tokens", 0)
    input_tokens = usage.get("input_tokens", 0)
    cache_creation = usage.get("cache_creation_input_tokens", 0)
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
        "output_tokens": usage.get("output_tokens", 0)
    }

    try:
        with open(usage_file, 'w', encoding='utf-8') as f:
            json.dump(usage_data, f, indent=2)
    except:
        pass

if __name__ == "__main__":
    main()
