# Global Installation Script for Integrated Workflow
# Simplified version without emoji

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Integrated Workflow Global Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$GLOBAL_CLAUDE_DIR = "$env:USERPROFILE\.claude"

Write-Host "Global Claude directory: $GLOBAL_CLAUDE_DIR" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $GLOBAL_CLAUDE_DIR)) {
    Write-Host "[ERROR] Global Claude directory not found" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Global Claude directory found" -ForegroundColor Green
Write-Host ""

# Backup existing CLAUDE.md
$CLAUDE_MD_PATH = Join-Path $GLOBAL_CLAUDE_DIR "CLAUDE.md"
if (Test-Path $CLAUDE_MD_PATH) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $BACKUP_FILE = "$CLAUDE_MD_PATH.backup.$timestamp"
    Write-Host "[BACKUP] Creating backup of existing CLAUDE.md..." -ForegroundColor Yellow
    Copy-Item $CLAUDE_MD_PATH $BACKUP_FILE
    Write-Host "[OK] Backup created: $BACKUP_FILE" -ForegroundColor Green
    Write-Host ""
}

# Copy CLAUDE.md
Write-Host "[INSTALL] Installing CLAUDE.md..." -ForegroundColor Cyan
if (Test-Path "CLAUDE.md") {
    Copy-Item "CLAUDE.md" $CLAUDE_MD_PATH -Force
    Write-Host "[OK] CLAUDE.md installed" -ForegroundColor Green
} else {
    Write-Host "[ERROR] CLAUDE.md not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Update mcp.json
Write-Host "[CONFIG] Configuring Code Index MCP..." -ForegroundColor Cyan
$MCP_JSON = Join-Path $GLOBAL_CLAUDE_DIR "mcp.json"

if (Test-Path $MCP_JSON) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $BACKUP_MCP = "$MCP_JSON.backup.$timestamp"
    Copy-Item $MCP_JSON $BACKUP_MCP
    Write-Host "[OK] Backup created: $BACKUP_MCP" -ForegroundColor Green

    $config = Get-Content $MCP_JSON -Raw | ConvertFrom-Json

    if ($config.mcpServers.PSObject.Properties.Name -contains "code-index") {
        Write-Host "[SKIP] code-index already configured" -ForegroundColor Yellow
    } else {
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
        $config | ConvertTo-Json -Depth 10 | Set-Content $MCP_JSON
        Write-Host "[OK] code-index configured" -ForegroundColor Green
    }
} else {
    Write-Host "[CREATE] Creating new mcp.json..." -ForegroundColor Yellow
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
    Write-Host "[OK] mcp.json created" -ForegroundColor Green
}
Write-Host ""

# Check uvx
Write-Host "[CHECK] Checking dependencies..." -ForegroundColor Cyan
try {
    $null = Get-Command uvx -ErrorAction Stop
    Write-Host "[OK] uvx is installed" -ForegroundColor Green
} catch {
    Write-Host "[WARN] uvx not found" -ForegroundColor Yellow
    Write-Host "       Install: irm https://astral.sh/uv/install.ps1 | iex" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[SUCCESS] Global installation completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installed components:" -ForegroundColor Cyan
Write-Host "  - CLAUDE.md -> $CLAUDE_MD_PATH"
Write-Host "  - Code Index MCP -> $MCP_JSON"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Restart Claude Code"
Write-Host "  2. The integrated workflow will be active globally"
Write-Host ""
Write-Host "[SUCCESS] Installation complete!" -ForegroundColor Green
