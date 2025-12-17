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
    session_file = Path("/tmp/claude-session-info.json")
    if not session_file.exists():
        return None

    try:
        with open(session_file) as f:
            return json.load(f)
    except Exception as e:
        return None

def get_transcript_size(transcript_path):
    """获取 transcript 文件大小（字节）"""
    try:
        return os.path.getsize(transcript_path)
    except:
        return 0

def estimate_token_usage(file_size_bytes):
    """估算 token 使用量（粗略估计：1 token ≈ 4 bytes）"""
    return file_size_bytes / 4

def calculate_usage_percent(estimated_tokens, max_tokens=200000):
    """计算使用率百分比"""
    return (estimated_tokens / max_tokens) * 100

def check_context_usage():
    """检查当前上下文使用率"""
    session_info = read_session_info()

    if not session_info:
        return {
            "error": "No active session found. SessionStart hook may not be configured."
        }

    transcript_path = session_info.get("transcript_path")
    if not transcript_path or not os.path.exists(transcript_path):
        return {
            "error": f"Transcript file not found: {transcript_path}"
        }

    file_size = get_transcript_size(transcript_path)
    estimated_tokens = estimate_token_usage(file_size)
    usage_percent = calculate_usage_percent(estimated_tokens)

    # 确定状态和建议
    if usage_percent < 50:
        status = "✅ SAFE"
        recommendation = "Context usage is healthy. Continue working normally."
    elif usage_percent < 70:
        status = "⚠️ WARNING"
        recommendation = "Context usage is moderate. Consider completing current task soon."
    elif usage_percent < 85:
        status = "🔴 HIGH"
        recommendation = "Context usage is high! Complete current task and save state immediately."
    else:
        status = "🚨 CRITICAL"
        recommendation = "Context usage is critical! Save state NOW and prompt user to execute /clear"

    return {
        "session_id": session_info.get("session_id"),
        "transcript_path": transcript_path,
        "file_size_mb": round(file_size / 1024 / 1024, 2),
        "estimated_tokens": int(estimated_tokens),
        "usage_percent": round(usage_percent, 1),
        "max_tokens": 200000,
        "status": status,
        "recommendation": recommendation,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def save_session_state(state_data):
    """保存会话状态到文件"""
    session_info = read_session_info()
    if not session_info:
        return {"error": "No active session"}

    cwd = session_info.get("cwd", ".")
    state_dir = Path(cwd) / ".claude" / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    state_file = state_dir / "current-session.md"

    # 生成状态文件内容
    content = f"""# Session State
**Session ID**: {session_info.get('session_id')}
**Timestamp**: {datetime.utcnow().isoformat()}Z
**Context Usage**: {state_data.get('usage_percent', 0)}%

## State Data
{state_data.get('content', 'No content provided')}

## Next Steps
{state_data.get('next_steps', 'Continue with next task')}
"""

    with open(state_file, 'w') as f:
        f.write(content)

    return {
        "success": True,
        "state_file": str(state_file),
        "message": "Session state saved successfully"
    }

# MCP Server Protocol
def handle_request(request):
    """处理 MCP 请求"""
    method = request.get("method")

    if method == "tools/list":
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
            response = handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            error_response = {"error": str(e)}
            print(json.dumps(error_response))
            sys.stdout.flush()
