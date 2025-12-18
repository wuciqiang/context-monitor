# Global Installation Script for Integrated Workflow (PowerShell)
# 整合工作流全局安装脚本 (PowerShell)

$ErrorActionPreference = "Stop"

# Colors
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Cyan "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-ColorOutput Cyan "  Integrated Workflow Global Installer"
Write-ColorOutput Cyan "  整合工作流全局安装器"
Write-ColorOutput Cyan "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Output ""

# Global Claude directory
$GLOBAL_CLAUDE_DIR = "$env:USERPROFILE\.claude"

Write-ColorOutput Cyan "📁 Global Claude directory: $GLOBAL_CLAUDE_DIR"
Write-Output ""

# Check if global directory exists
if (-not (Test-Path $GLOBAL_CLAUDE_DIR)) {
    Write-ColorOutput Red "❌ Global Claude directory not found: $GLOBAL_CLAUDE_DIR"
    Write-ColorOutput Yellow "   Please run Claude Code at least once to create the directory"
    exit 1
}

Write-ColorOutput Green "✅ Global Claude directory found"
Write-Output ""

# Backup existing CLAUDE.md if it exists
$CLAUDE_MD_PATH = Join-Path $GLOBAL_CLAUDE_DIR "CLAUDE.md"
if (Test-Path $CLAUDE_MD_PATH) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $BACKUP_FILE = "$CLAUDE_MD_PATH.backup.$timestamp"
    Write-ColorOutput Yellow "⚠️  Existing CLAUDE.md found, creating backup..."
    Copy-Item $CLAUDE_MD_PATH $BACKUP_FILE
    Write-ColorOutput Green "   ✓ Backup created: $BACKUP_FILE"
    Write-Output ""
}

# Copy CLAUDE.md to global directory
Write-ColorOutput Cyan "📄 Installing CLAUDE.md..."
if (Test-Path "CLAUDE.md") {
    Copy-Item "CLAUDE.md" $CLAUDE_MD_PATH -Force
    Write-ColorOutput Green "✅ CLAUDE.md installed"
} else {
    Write-ColorOutput Red "❌ CLAUDE.md not found in current directory"
    exit 1
}
Write-Output ""

# Update mcp.json to add Code Index MCP
Write-ColorOutput Cyan "🔌 Configuring Code Index MCP..."

$MCP_JSON = Join-Path $GLOBAL_CLAUDE_DIR "mcp.json"

if (Test-Path $MCP_JSON) {
    # Backup mcp.json
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $BACKUP_MCP = "$MCP_JSON.backup.$timestamp"
    Copy-Item $MCP_JSON $BACKUP_MCP
    Write-ColorOutput Green "   ✓ Backup created: $BACKUP_MCP"

    # Read and parse mcp.json
    $config = Get-Content $MCP_JSON -Raw | ConvertFrom-Json

    # Check if code-index already exists
    if ($config.mcpServers.PSObject.Properties.Name -contains "code-index") {
        Write-ColorOutput Yellow "   ⚠️  code-index already configured in mcp.json"
    } else {
        # Add code-index to mcp.json
        if (-not $config.mcpServers) {
            $config | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value @{}
        }

        $codeIndexConfig = @{
            type = "stdio"
            command = "uvx"
            args = @("code-index-mcp")
            env = @{}
        }

        $config.mcpServers | Add-Member -MemberType NoteProperty -Name "code-index" -Value $codeIndexConfig -Force

        # Save updated config
        $config | ConvertTo-Json -Depth 10 | Set-Content $MCP_JSON
        Write-ColorOutput Green "   ✓ code-index configured in mcp.json"
    }
} else {
    Write-ColorOutput Yellow "   ⚠️  mcp.json not found, creating new one..."
    $newConfig = @{
        mcpServers = @{
            "code-index" = @{
                type = "stdio"
                command = "uvx"
                args = @("code-index-mcp")
                env = @{}
            }
        }
    }
    $newConfig | ConvertTo-Json -Depth 10 | Set-Content $MCP_JSON
    Write-ColorOutput Green "   ✓ mcp.json created with code-index"
}
Write-Output ""

# Check if uvx is installed
Write-ColorOutput Cyan "📦 Checking dependencies..."
try {
    $uvxPath = Get-Command uvx -ErrorAction Stop
    Write-ColorOutput Green "✅ uvx is installed"
} catch {
    Write-ColorOutput Yellow "⚠️  uvx not found"
    Write-ColorOutput Yellow "   Install with: irm https://astral.sh/uv/install.ps1 | iex"
}
Write-Output ""

# Summary
Write-ColorOutput Cyan "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-ColorOutput Green "✅ Global installation completed!"
Write-ColorOutput Cyan "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Output ""
Write-ColorOutput Cyan "📋 Installed components:"
Write-Output "   ✅ CLAUDE.md → $CLAUDE_MD_PATH"
Write-Output "   ✅ Code Index MCP → $MCP_JSON"
Write-Output ""
Write-ColorOutput Cyan "🚀 Next steps:"
Write-Output ""
Write-ColorOutput Green "   1. Restart Claude Code"
Write-Output "      The integrated workflow will be active globally"
Write-Output ""
Write-ColorOutput Green "   2. For project-specific Context Monitor:"
Write-Output "      cd /path/to/your/project"
Write-Output "      npm install --save-dev @claude/context-monitor"
Write-Output "      npm run init"
Write-Output ""
Write-ColorOutput Green "   3. Initialize Code Index (in any project):"
Write-Output "      Start Claude Code and say:"
Write-Output '      "请初始化代码索引"'
Write-Output ""
Write-ColorOutput Cyan "📚 Documentation:"
Write-Output "   • CLAUDE.md - Complete workflow definition"
Write-Output "   • INTEGRATED_WORKFLOW_GUIDE.md - Quick reference"
Write-Output ""
Write-ColorOutput Cyan "⚠️  Note:"
Write-Output "   • CLAUDE.md is now global (applies to all projects)"
Write-Output "   • Code Index MCP is global (works in all projects)"
Write-Output "   • Context Monitor needs to be installed per-project"
Write-Output ""
Write-ColorOutput Green "[SUCCESS] Enjoy your intelligent development experience!"
Write-Output ""
