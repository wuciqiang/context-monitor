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
