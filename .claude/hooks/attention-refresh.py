#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
注意力刷新提醒 Hook
每 N 次工具调用后提示重读 spec.md
"""

import json
import sys
import os
from pathlib import Path

# 配置
REFRESH_INTERVAL = 15  # 每15次工具调用提醒一次
STATE_FILE = ".claude/.attention-refresh-state.json"

def load_state():
    """加载状态"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"tool_call_count": 0, "last_refresh": 0}

def save_state(state):
    """保存状态"""
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f)
    except:
        pass  # 静默失败，不影响主流程

def check_active_spec():
    """检查是否有活跃的 spec"""
    active_dir = ".claude/specs/active"
    if not os.path.exists(active_dir):
        return None
    
    try:
        # 返回第一个活跃 spec 的路径
        for feature in os.listdir(active_dir):
            spec_path = os.path.join(active_dir, feature, "spec.md")
            if os.path.exists(spec_path):
                return spec_path
    except:
        pass
    return None

def main():
    # 静默失败策略：任何异常都不影响主工作流
    try:
        # 检查是否有活跃的 spec
        spec_path = check_active_spec()
        if not spec_path:
            sys.exit(0)  # 无活跃任务，静默退出
        
        # 加载状态
        state = load_state()
        state["tool_call_count"] = state.get("tool_call_count", 0) + 1
        
        # 判断是否需要提醒
        if state["tool_call_count"] - state.get("last_refresh", 0) >= REFRESH_INTERVAL:
            # 输出提示（通过 stderr 避免污染主输出）
            reminder_msg = (
                f"\\n⏰ [Manus 注意力刷新提醒]\\n"
                f"   已执行 {state['tool_call_count']} 次工具调用\\n"
                f"   建议重读 {spec_path} 的功能概述和当前任务状态\\n"
            )
            print(reminder_msg, file=sys.stderr)
            
            # 更新最后提醒时间
            state["last_refresh"] = state["tool_call_count"]
        
        # 保存状态
        save_state(state)
    except Exception:
        pass  # 完全静默，确保不影响主流程
    
    sys.exit(0)

if __name__ == "__main__":
    main()
