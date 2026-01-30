#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 模型上下文限制 (与 server.py 保持同步)
MODEL_CONTEXT_LIMITS = {
    'claude-sonnet-4-5': {'max': 200000, 'usable': 160000},
    'claude-sonnet-4-5[1m]': {'max': 1000000, 'usable': 800000},
    'claude-opus-4-5': {'max': 200000, 'usable': 160000},
    'claude-haiku-4-5': {'max': 200000, 'usable': 160000},
    'default': {'max': 200000, 'usable': 160000},
}

def get_context_limits(model_id: str = None) -> dict:
    if not model_id:
        return MODEL_CONTEXT_LIMITS['default']
    model_id_lower = model_id.lower()
    if '[1m]' in model_id_lower:
        return MODEL_CONTEXT_LIMITS['claude-sonnet-4-5[1m]']
    for key in MODEL_CONTEXT_LIMITS:
        if key != 'default' and key in model_id_lower:
            return MODEL_CONTEXT_LIMITS[key]
    return MODEL_CONTEXT_LIMITS['default']

def get_status_icon(usable_percent):
    """基于 usable_percent (可用上下文百分比) 返回状态图标"""
    if usable_percent < 50:
        return "✅"
    elif usable_percent < 70:
        return "⚠️"
    elif usable_percent < 85:
        return "🔶"
    else:
        return "🚨"

def main():
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
    usage_file = Path(temp_dir) / "claude-current-usage.json"

    if not usage_file.exists():
        print("Context: --")
        return

    try:
        with open(usage_file) as f:
            data = json.load(f)
            context_tokens = data.get('context_tokens', 0)
            model_id = data.get('model_id', None)

        limits = get_context_limits(model_id)
        usable_percent = (context_tokens / limits['usable']) * 100 if limits['usable'] > 0 else 0

        icon = get_status_icon(usable_percent)
        print(f"{icon} Context: {usable_percent:.1f}%")
    except:
        print("Context: --")

if __name__ == "__main__":
    main()
