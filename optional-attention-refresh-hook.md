# Hook级注意力刷新提醒 (可选增强)

**状态**: P2 可选项 - 供未来实现参考
**目的**: 自动化注意力刷新机制，避免依赖人工记忆

---

## 实现方案

### 1. Hook 脚本位置
`.claude/hooks/attention-refresh.py`

### 2. Hook 配置
在 `.claude-plugin/plugin.json` 中配置 PostToolUse Hook:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "attention-refresh",
        "script": "${CLAUDE_PLUGIN_ROOT}/../../.claude/hooks/attention-refresh.py",
        "timeout": 1000
      }
    ]
  }
}
```

### 3. 脚本逻辑

```python
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
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"tool_call_count": 0, "last_refresh": 0}

def save_state(state):
    """保存状态"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f)

def check_active_spec():
    """检查是否有活跃的 spec"""
    active_dir = ".claude/specs/active"
    if not os.path.exists(active_dir):
        return None
    
    # 返回第一个活跃 spec 的路径
    for feature in os.listdir(active_dir):
        spec_path = os.path.join(active_dir, feature, "spec.md")
        if os.path.exists(spec_path):
            return spec_path
    return None

def main():
    # 读取 Hook 输入
    try:
        hook_data = json.load(sys.stdin)
    except:
        sys.exit(0)  # 静默失败
    
    # 检查是否有活跃的 spec
    spec_path = check_active_spec()
    if not spec_path:
        sys.exit(0)  # 无活跃任务，不提醒
    
    # 加载状态
    state = load_state()
    state["tool_call_count"] += 1
    
    # 判断是否需要提醒
    if state["tool_call_count"] - state["last_refresh"] >= REFRESH_INTERVAL:
        # 输出提示到 stdout
        reminder = {
            "type": "attention_refresh_reminder",
            "message": f"⏰ 注意力刷新提醒：已执行 {state['tool_call_count']} 次工具调用，建议重读 {spec_path} 的功能概述和当前任务状态",
            "spec_path": spec_path,
            "tool_call_count": state["tool_call_count"]
        }
        print(json.dumps(reminder, ensure_ascii=False))
        
        # 更新最后提醒时间
        state["last_refresh"] = state["tool_call_count"]
    
    # 保存状态
    save_state(state)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 4. 节流机制

- **间隔**: 每 15 次工具调用提醒一次（可配置）
- **状态持久化**: 保存在 `.claude/.attention-refresh-state.json`
- **作用域**: 仅在存在活跃 spec 时生效

### 5. 使用方式

1. 将上述脚本保存到 `.claude/hooks/attention-refresh.py`
2. 添加可执行权限：`chmod +x .claude/hooks/attention-refresh.py`
3. 配置 Hook（如上）
4. 重启 Claude Code

---

## 注意事项

1. **可选性**: 此 Hook 是可选的，不影响核心工作流
2. **节流**: 通过间隔控制避免过度打扰
3. **轻量级**: Hook 执行时间 < 100ms
4. **向后兼容**: 如果脚本失败，不影响主工作流

---

**实施优先级**: P2 (可选)
**维护者**: 根据实际使用效果决定是否启用
