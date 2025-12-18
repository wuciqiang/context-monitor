#!/bin/bash

# Global Installation Script for Integrated Workflow
# 整合工作流全局安装脚本

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Integrated Workflow Global Installer${NC}"
echo -e "${BLUE}  整合工作流全局安装器${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Detect OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    GLOBAL_CLAUDE_DIR="$HOME/.claude"
else
    GLOBAL_CLAUDE_DIR="$HOME/.claude"
fi

echo -e "${BLUE}📁 Global Claude directory:${NC} $GLOBAL_CLAUDE_DIR"
echo ""

# Check if global directory exists
if [ ! -d "$GLOBAL_CLAUDE_DIR" ]; then
    echo -e "${RED}❌ Global Claude directory not found: $GLOBAL_CLAUDE_DIR${NC}"
    echo -e "${YELLOW}   Please run Claude Code at least once to create the directory${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Global Claude directory found${NC}"
echo ""

# Backup existing CLAUDE.md if it exists
if [ -f "$GLOBAL_CLAUDE_DIR/CLAUDE.md" ]; then
    BACKUP_FILE="$GLOBAL_CLAUDE_DIR/CLAUDE.md.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${YELLOW}⚠️  Existing CLAUDE.md found, creating backup...${NC}"
    cp "$GLOBAL_CLAUDE_DIR/CLAUDE.md" "$BACKUP_FILE"
    echo -e "${GREEN}   ✓ Backup created: $BACKUP_FILE${NC}"
    echo ""
fi

# Copy CLAUDE.md to global directory
echo -e "${BLUE}📄 Installing CLAUDE.md...${NC}"
if [ -f "CLAUDE.md" ]; then
    cp CLAUDE.md "$GLOBAL_CLAUDE_DIR/CLAUDE.md"
    echo -e "${GREEN}✅ CLAUDE.md installed${NC}"
else
    echo -e "${RED}❌ CLAUDE.md not found in current directory${NC}"
    exit 1
fi
echo ""

# Update mcp.json to add Code Index MCP
echo -e "${BLUE}🔌 Configuring Code Index MCP...${NC}"

MCP_JSON="$GLOBAL_CLAUDE_DIR/mcp.json"

if [ -f "$MCP_JSON" ]; then
    # Backup mcp.json
    BACKUP_MCP="$MCP_JSON.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$MCP_JSON" "$BACKUP_MCP"
    echo -e "${GREEN}   ✓ Backup created: $BACKUP_MCP${NC}"

    # Check if code-index already exists
    if grep -q '"code-index"' "$MCP_JSON"; then
        echo -e "${YELLOW}   ⚠️  code-index already configured in mcp.json${NC}"
    else
        # Add code-index to mcp.json using Python
        python3 << 'PYTHON_SCRIPT'
import json
import sys

mcp_file = sys.argv[1] if len(sys.argv) > 1 else None
if not mcp_file:
    print("Error: mcp.json path not provided")
    sys.exit(1)

try:
    with open(mcp_file, 'r') as f:
        config = json.load(f)

    if 'mcpServers' not in config:
        config['mcpServers'] = {}

    # Add code-index MCP server
    config['mcpServers']['code-index'] = {
        "type": "stdio",
        "command": "uvx",
        "args": ["code-index-mcp"],
        "env": {}
    }

    with open(mcp_file, 'w') as f:
        json.dump(config, f, indent=2)

    print("✓ code-index added to mcp.json")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
PYTHON_SCRIPT

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}   ✓ code-index configured in mcp.json${NC}"
        else
            echo -e "${RED}   ❌ Failed to configure code-index${NC}"
            echo -e "${YELLOW}   Please manually add the following to $MCP_JSON:${NC}"
            echo ""
            echo '    "code-index": {'
            echo '      "type": "stdio",'
            echo '      "command": "uvx",'
            echo '      "args": ["code-index-mcp"],'
            echo '      "env": {}'
            echo '    }'
            echo ""
        fi
    fi
else
    echo -e "${YELLOW}   ⚠️  mcp.json not found, creating new one...${NC}"
    cat > "$MCP_JSON" << 'EOF'
{
  "mcpServers": {
    "code-index": {
      "type": "stdio",
      "command": "uvx",
      "args": ["code-index-mcp"],
      "env": {}
    }
  }
}
EOF
    echo -e "${GREEN}   ✓ mcp.json created with code-index${NC}"
fi
echo ""

# Check if uvx is installed
echo -e "${BLUE}📦 Checking dependencies...${NC}"
if command -v uvx &> /dev/null; then
    echo -e "${GREEN}✅ uvx is installed${NC}"
else
    echo -e "${YELLOW}⚠️  uvx not found${NC}"
    echo -e "${YELLOW}   Install with: curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Global installation completed!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📋 Installed components:${NC}"
echo -e "   ✅ CLAUDE.md → $GLOBAL_CLAUDE_DIR/CLAUDE.md"
echo -e "   ✅ Code Index MCP → $MCP_JSON"
echo ""
echo -e "${BLUE}🚀 Next steps:${NC}"
echo ""
echo -e "   ${GREEN}1. Restart Claude Code${NC}"
echo -e "      The integrated workflow will be active globally"
echo ""
echo -e "   ${GREEN}2. For project-specific Context Monitor:${NC}"
echo -e "      cd /path/to/your/project"
echo -e "      npm install --save-dev @claude/context-monitor"
echo -e "      npm run init"
echo ""
echo -e "   ${GREEN}3. Initialize Code Index (in any project):${NC}"
echo -e "      Start Claude Code and say:"
echo -e "      \"请初始化代码索引\""
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo -e "   • CLAUDE.md - Complete workflow definition"
echo -e "   • INTEGRATED_WORKFLOW_GUIDE.md - Quick reference"
echo ""
echo -e "${BLUE}⚠️  Note:${NC}"
echo -e "   • CLAUDE.md is now global (applies to all projects)"
echo -e "   • Code Index MCP is global (works in all projects)"
echo -e "   • Context Monitor needs to be installed per-project"
echo ""
echo -e "${GREEN}🎉 Enjoy your intelligent development experience!${NC}"
echo ""
