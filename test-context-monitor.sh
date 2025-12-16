#!/bin/bash
# 测试上下文监控系统

echo "🧪 Testing Context Monitoring System"
echo "===================================="
echo ""

# 1. 测试 SessionStart Hook
echo "1️⃣ Testing SessionStart Hook..."
test_input='{"session_id":"test-123","transcript_path":"/tmp/test-transcript.jsonl","cwd":"'$(pwd)'"}'
echo "$test_input" | bash .claude/hooks/capture-session-info.sh
if [ -f "/tmp/claude-session-info.json" ]; then
    echo "✅ Hook executed successfully"
    echo "   Session info:"
    cat /tmp/claude-session-info.json | python3 -m json.tool
else
    echo "❌ Hook failed - session info file not created"
fi
echo ""

# 2. 创建测试 transcript 文件
echo "2️⃣ Creating test transcript file..."
# 创建一个 3MB 的测试文件（约 60% 使用率）
dd if=/dev/zero of=/tmp/test-transcript.jsonl bs=1M count=3 2>/dev/null
echo "✅ Created 3MB test transcript"
echo ""

# 3. 测试 MCP Server（简化测试）
echo "3️⃣ Testing MCP Server tools..."
echo "   Note: Full MCP testing requires Claude Code runtime"
echo "   Checking if server script is executable..."
if [ -x ".claude/mcp-servers/context-monitor/server.py" ]; then
    echo "✅ Server script is executable"
elif [ -f ".claude/mcp-servers/context-monitor/server.py" ]; then
    echo "⚠️  Server script exists but not executable"
    echo "   Run: chmod +x .claude/mcp-servers/context-monitor/server.py"
else
    echo "❌ Server script not found"
fi
echo ""

# 4. 验证配置文件
echo "4️⃣ Verifying configuration..."
if [ -f ".claude/settings.local.json" ]; then
    echo "✅ settings.local.json exists"
    if grep -q "SessionStart" .claude/settings.local.json; then
        echo "✅ SessionStart hook configured"
    else
        echo "❌ SessionStart hook not configured"
    fi
    if grep -q "context-monitor" .claude/settings.local.json; then
        echo "✅ context-monitor MCP server configured"
    else
        echo "❌ context-monitor MCP server not configured"
    fi
else
    echo "❌ settings.local.json not found"
fi
echo ""

# 5. 检查 CLAUDE.md
echo "5️⃣ Checking CLAUDE.md instructions..."
if grep -q "上下文管理" CLAUDE.md; then
    echo "✅ Context management instructions found in CLAUDE.md"
else
    echo "❌ Context management instructions not found in CLAUDE.md"
fi
echo ""

# 6. 清理
echo "6️⃣ Cleanup..."
rm -f /tmp/test-transcript.jsonl
echo "✅ Test files cleaned up"
echo ""

echo "===================================="
echo "✅ Context Monitoring System Test Complete"
echo ""
echo "Next steps:"
echo "1. Start a new Claude Code session"
echo "2. Ask Claude to check context usage"
echo "3. Verify the monitoring system works"
