#!/usr/bin/env python3
"""
Context Monitor MCP Server
监控 Claude Code 会话的上下文使用率
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 模型上下文限制配置
# max_tokens: 理论最大值
# usable_tokens: 80% 阈值 (Claude auto-compact 触发点)
MODEL_CONTEXT_LIMITS = {
    'claude-sonnet-4-5': {'max': 200000, 'usable': 160000},
    'claude-sonnet-4-5[1m]': {'max': 1000000, 'usable': 800000},
    'claude-opus-4-5': {'max': 200000, 'usable': 160000},
    'claude-haiku-4-5': {'max': 200000, 'usable': 160000},
    'default': {'max': 200000, 'usable': 160000},
}

def get_context_limits(model_id: str = None) -> dict:
    """根据模型 ID 获取上下文限制"""
    if not model_id:
        return MODEL_CONTEXT_LIMITS['default']

    model_id_lower = model_id.lower()

    # 检测长上下文版本 [1m]
    if '[1m]' in model_id_lower:
        return MODEL_CONTEXT_LIMITS['claude-sonnet-4-5[1m]']

    # 匹配已知模型
    for key in MODEL_CONTEXT_LIMITS:
        if key != 'default' and key in model_id_lower:
            return MODEL_CONTEXT_LIMITS[key]

    return MODEL_CONTEXT_LIMITS['default']

def read_session_info():
    """读取 hook 捕获的会话信息"""
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
    session_file = Path(temp_dir) / "claude-session-info.json"
    if not session_file.exists():
        return None

    try:
        with open(session_file) as f:
            return json.load(f)
    except Exception as e:
        return None

def check_context_usage():
    """检查当前上下文使用率"""
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
    usage_file = Path(temp_dir) / "claude-current-usage.json"

    if not usage_file.exists():
        return {
            "error": "No usage data available. PostToolUse hook may not be configured or no tools have been used yet."
        }

    try:
        with open(usage_file) as f:
            data = json.load(f)
            context_tokens = data.get('context_tokens', 0)
            model_id = data.get('model_id', None)

        # 获取模型特定的上下文限制
        limits = get_context_limits(model_id)
        max_tokens = limits['max']
        usable_tokens = limits['usable']

        # 计算双指标
        usage_percent = (context_tokens / max_tokens) * 100 if max_tokens > 0 else 0
        usable_percent = (context_tokens / usable_tokens) * 100 if usable_tokens > 0 else 0

        # 基于 usable_percent 确定状态 (更接近真实危险阈值)
        if usable_percent < 50:
            status = "SAFE"
            recommendation = "Context usage is healthy. Continue working normally."
        elif usable_percent < 70:
            status = "WARNING"
            recommendation = "Context usage is moderate. Consider completing current task soon."
        elif usable_percent < 85:
            status = "HIGH"
            recommendation = "Context usage is high! Complete current task and save state immediately."
        else:
            status = "CRITICAL"
            recommendation = "Context usage is critical! Save state NOW and prompt user to execute /clear"

        return {
            "context_tokens": context_tokens,
            "max_tokens": max_tokens,
            "usable_tokens": usable_tokens,
            "usage_percent": round(usage_percent, 1),
            "usable_percent": round(usable_percent, 1),
            "model_id": model_id,
            "status": status,
            "recommendation": recommendation,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "error": f"Failed to read usage data: {str(e)}"
        }

def save_session_state(state_data):
    """保存会话状态到文件（带超时和降级方案）"""
    session_info = read_session_info()
    if not session_info:
        return {"error": "No active session"}

    session_id = session_info.get('session_id', 'default')
    cwd = session_info.get("cwd", ".")
    state_dir = Path(cwd) / ".claude" / "state"

    try:
        state_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create state directory: {str(e)}"
        }

    # 使用 session_id 避免并发冲突
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    state_file = state_dir / f"session-{session_id}-{timestamp}.md"

    # 同时保存到 current-session.md 作为快速访问点
    current_file = state_dir / "current-session.md"

    # 生成状态文件内容
    content = f"""# Session State
**Session ID**: {session_id}
**Timestamp**: {datetime.utcnow().isoformat()}Z
**Context Usage**: {state_data.get('usage_percent', 0)}%

## State Data
{state_data.get('content', 'No content provided')}

## Next Steps
{state_data.get('next_steps', 'Continue with next task')}
"""

    try:
        # 主保存：带 session_id 的唯一文件
        with open(state_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # 降级保存：覆盖 current-session.md
        try:
            with open(current_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            # current-session.md 失败不影响主保存
            pass

        return {
            "success": True,
            "state_file": str(state_file),
            "current_file": str(current_file),
            "message": "Session state saved successfully"
        }

    except Exception as e:
        # 降级方案：尝试保存到临时目录
        try:
            temp_dir = os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
            fallback_file = Path(temp_dir) / f"claude-state-{session_id}-{timestamp}.md"
            with open(fallback_file, 'w', encoding='utf-8') as f:
                f.write(content)

            return {
                "success": True,
                "state_file": str(fallback_file),
                "warning": f"Primary save failed: {str(e)}, used fallback location",
                "message": "Session state saved to fallback location"
            }
        except Exception as fallback_error:
            return {
                "success": False,
                "error": f"Both primary and fallback save failed. Primary: {str(e)}, Fallback: {str(fallback_error)}"
            }

# MCP Server Protocol
def handle_request(request):
    """处理 MCP 请求"""
    method = request.get("method")

    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "context-monitor",
                "version": "1.0.0"
            }
        }

    elif method == "tools/list":
        return {
            "tools": [
                {
                    "name": "check_context_usage",
                    "description": "Check current Claude Code session context usage. Returns usage percentage and recommendations. Call this periodically (every 5-10 messages) to monitor context.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "save_session_state",
                    "description": "Save current session state to .claude/state/current-session.md for recovery after /clear",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "State content to save"
                            },
                            "next_steps": {
                                "type": "string",
                                "description": "Next steps after clearing context"
                            }
                        },
                        "required": ["content"]
                    }
                }
            ]
        }

    elif method == "tools/call":
        tool_name = request.get("params", {}).get("name")
        arguments = request.get("params", {}).get("arguments", {})

        if tool_name == "check_context_usage":
            result = check_context_usage()
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2)
                    }
                ]
            }

        elif tool_name == "save_session_state":
            result = save_session_state(arguments)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2)
                    }
                ]
            }

    return {"error": "Unknown method"}

# Main loop
if __name__ == "__main__":
    for line in sys.stdin:
        try:
            request = json.loads(line)
            request_id = request.get("id")
            result = handle_request(request)

            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            request_id = None
            try:
                request_id = json.loads(line).get("id")
            except:
                pass

            error_response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()
