#!/usr/bin/env python3
"""
自动配置 statusLine 到项目的 .claude/settings.json
"""
import json
import os
from pathlib import Path

def setup_statusline(project_path=None):
    if not project_path:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    settings_file = project_path / ".claude" / "settings.json"
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取现有配置
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    else:
        settings = {}
    
    # 获取插件根目录
    plugin_root = Path.home() / ".claude" / "plugins"
    cm_plugin = None
    for p in plugin_root.glob("cm@*"):
        if p.is_dir():
            cm_plugin = p
            break
    
    if not cm_plugin:
        print("❌ 插件未安装,请先执行: /plugin install cm")
        return False
    
    statusline_script = cm_plugin / ".claude" / "mcp-servers" / "context-monitor" / "statusline.py"
    
    # 配置 statusLine
    settings["statusLine"] = {
        "type": "command",
        "command": f"python {statusline_script}",
        "padding": 0
    }
    
    # 保存配置
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    
    print(f"✅ statusLine 已配置到: {settings_file}")
    print(f"📍 脚本路径: {statusline_script}")
    print("\n🔄 请重启 Claude Code 让配置生效")
    return True

if __name__ == "__main__":
    import sys
    project = sys.argv[1] if len(sys.argv) > 1 else None
    setup_statusline(project)
