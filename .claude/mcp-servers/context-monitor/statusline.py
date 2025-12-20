#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_status_icon(usage_percent):
    if usage_percent < 50:
        return "✅"
    elif usage_percent < 70:
        return "⚠️"
    elif usage_percent < 85:
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
            usage_percent = data.get('usage_percent', 0)
            icon = get_status_icon(usage_percent)
            print(f"{icon} Context: {usage_percent:.1f}%")
    except:
        print("Context: --")

if __name__ == "__main__":
    main()
