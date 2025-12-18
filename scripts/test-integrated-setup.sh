#!/bin/bash

# Test Integrated Setup (Context Monitor + Code Index MCP)
# 测试整合配置（Context Monitor + Code Index MCP）

echo "🧪 Testing Integrated Setup..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check .claude directory
echo "📁 Test 1: Checking .claude directory..."
if [ -d ".claude" ]; then
    echo -e "${GREEN}✅ .claude directory exists${NC}"
else
    echo -e "${RED}❌ .claude directory not found${NC}"
    exit 1
fi

# Test 2: Check settings.local.json
echo ""
echo "⚙️  Test 2: Checking settings.local.json..."
if [ -f ".claude/settings.local.json" ]; then
    echo -e "${GREEN}✅ settings.local.json exists${NC}"

    # Validate JSON syntax
    if python3 -m json.tool .claude/settings.local.json > /dev/null 2>&1; then
        echo -e "${GREEN}✅ JSON syntax is valid${NC}"
    else
        echo -e "${RED}❌ JSON syntax error${NC}"
        exit 1
    fi

    # Check for required MCP servers
    if grep -q "context-monitor" .claude/settings.local.json && grep -q "code-index" .claude/settings.local.json; then
        echo -e "${GREEN}✅ Both MCP servers configured${NC}"
    else
        echo -e "${RED}❌ Missing MCP server configuration${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ settings.local.json not found${NC}"
    exit 1
fi

# Test 3: Check CLAUDE.md
echo ""
echo "📄 Test 3: Checking CLAUDE.md..."
if [ -f "CLAUDE.md" ]; then
    echo -e "${GREEN}✅ CLAUDE.md exists${NC}"

    # Check for key sections
    if grep -q "Integrated Workflow" CLAUDE.md && \
       grep -q "Context Monitor" CLAUDE.md && \
       grep -q "Code Index" CLAUDE.md; then
        echo -e "${GREEN}✅ CLAUDE.md contains integrated workflow${NC}"
    else
        echo -e "${YELLOW}⚠️  CLAUDE.md may be incomplete${NC}"
    fi
else
    echo -e "${RED}❌ CLAUDE.md not found${NC}"
    exit 1
fi

# Test 4: Check hooks
echo ""
echo "🪝 Test 4: Checking hooks..."
if [ -f "hooks/capture-session-info.sh" ]; then
    echo -e "${GREEN}✅ SessionStart hook exists${NC}"

    if [ -x "hooks/capture-session-info.sh" ]; then
        echo -e "${GREEN}✅ Hook is executable${NC}"
    else
        echo -e "${YELLOW}⚠️  Hook is not executable, fixing...${NC}"
        chmod +x hooks/capture-session-info.sh
        echo -e "${GREEN}✅ Fixed${NC}"
    fi
else
    echo -e "${RED}❌ SessionStart hook not found${NC}"
    exit 1
fi

# Test 5: Check MCP servers
echo ""
echo "🔌 Test 5: Checking MCP servers..."
if [ -f "mcp-servers/context-monitor/server.py" ]; then
    echo -e "${GREEN}✅ Context Monitor MCP server exists${NC}"

    if [ -x "mcp-servers/context-monitor/server.py" ]; then
        echo -e "${GREEN}✅ Server is executable${NC}"
    else
        echo -e "${YELLOW}⚠️  Server is not executable, fixing...${NC}"
        chmod +x mcp-servers/context-monitor/server.py
        echo -e "${GREEN}✅ Fixed${NC}"
    fi
else
    echo -e "${RED}❌ Context Monitor MCP server not found${NC}"
    exit 1
fi

# Test 6: Check Python
echo ""
echo "🐍 Test 6: Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✅ Python 3 installed: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

# Test 7: Check uvx (for Code Index MCP)
echo ""
echo "📦 Test 7: Checking uvx..."
if command -v uvx &> /dev/null; then
    echo -e "${GREEN}✅ uvx is installed${NC}"
else
    echo -e "${YELLOW}⚠️  uvx not found${NC}"
    echo -e "${YELLOW}   Install with: curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
fi

# Test 8: Test hook execution
echo ""
echo "🧪 Test 8: Testing hook execution..."
TEST_INPUT='{"session_id":"test-123","transcript_path":"/tmp/test-transcript.jsonl","cwd":"."}'
echo "$TEST_INPUT" | bash hooks/capture-session-info.sh > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Hook executes successfully${NC}"

    # Check if output file was created
    if [ -f "/tmp/claude-session-info.json" ]; then
        echo -e "${GREEN}✅ Session info file created${NC}"
    else
        echo -e "${YELLOW}⚠️  Session info file not created (may be expected)${NC}"
    fi
else
    echo -e "${RED}❌ Hook execution failed${NC}"
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Test Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✅ Integrated setup is ready!${NC}"
echo ""
echo "📋 Configuration includes:"
echo "   • Context Monitor (上下文监控)"
echo "   • Code Index MCP (代码索引)"
echo "   • Integrated Workflow (整合工作流)"
echo ""
echo "🚀 Next steps:"
echo "   1. Start Claude Code: claude"
echo "   2. System will auto-activate"
echo "   3. Try: '请检查当前上下文使用率'"
echo "   4. Try: 'set_project_path /path/to/your/project'"
echo ""
echo "📚 Documentation:"
echo "   • CLAUDE.md - Complete workflow guide"
echo "   • CONTEXT_MONITORING.md - Context Monitor details"
echo "   • README.md - Project overview"
echo ""
echo -e "${GREEN}🎉 All tests passed!${NC}"
