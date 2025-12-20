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
            usage_percent = data.get('usage_percent', 0)

        # 确定状态和建议
        if usage_percent < 50:
            status = "SAFE"
            recommendation = "Context usage is healthy. Continue working normally."
        elif usage_percent < 70:
            status = "WARNING"
            recommendation = "Context usage is moderate. Consider completing current task soon."
        elif usage_percent < 85:
            status = "HIGH"
            recommendation = "Context usage is high! Complete current task and save state immediately."
        else:
            status = "CRITICAL"
            recommendation = "Context usage is critical! Save state NOW and prompt user to execute /clear"

        return {
            "context_tokens": context_tokens,
            "usage_percent": round(usage_percent, 1),
            "max_tokens": 200000,
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
