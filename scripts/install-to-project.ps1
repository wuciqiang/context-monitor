# Context Monitor Project Installation Script (PowerShell)

param(
    [string]$TargetDir
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Context Monitor Project Installation ===" -ForegroundColor Cyan
Write-Host ""

if (-not $TargetDir) {
    $TargetDir = Read-Host "Enter target project path"
}

if (-not (Test-Path $TargetDir)) {
    Write-Host "ERROR: Directory not found: $TargetDir" -ForegroundColor Red
    exit 1
}

$TargetDir = Resolve-Path $TargetDir
Write-Host "Target project: $TargetDir"
Write-Host ""

Write-Host "[1/5] Creating directory structure..."
New-Item -ItemType Directory -Force -Path "$TargetDir\.claude\hooks" | Out-Null
New-Item -ItemType Directory -Force -Path "$TargetDir\.claude\mcp-servers\context-monitor" | Out-Null
New-Item -ItemType Directory -Force -Path "$TargetDir\.claude\state" | Out-Null

Write-Host "[2/5] Copying files..."
Copy-Item "$ScriptDir\.claude\hooks\capture-session-info.py" "$TargetDir\.claude\hooks\" -Force
Copy-Item "$ScriptDir\.claude\mcp-servers\context-monitor\server.py" "$TargetDir\.claude\mcp-servers\context-monitor\" -Force

Write-Host "[3/5] Configuring .mcp.json..."
$McpFile = "$TargetDir\.mcp.json"

if (Test-Path $McpFile) {
    Write-Host "Existing .mcp.json detected, backing up to .mcp.json.backup"
    Copy-Item $McpFile "$McpFile.backup" -Force
}

$McpContent = @'
{
  "mcpServers": {
    "context-monitor": {
      "type": "stdio",
      "command": "python",
      "args": [".claude/mcp-servers/context-monitor/server.py"],
      "env": {}
    }
  }
}
'@

$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False
$McpContentUnix = $McpContent -replace "`r`n", "`n"
[System.IO.File]::WriteAllText($McpFile, $McpContentUnix, $Utf8NoBomEncoding)

Write-Host "[4/5] Configuring .claude\settings.local.json..."
$SettingsFile = "$TargetDir\.claude\settings.local.json"

if (Test-Path $SettingsFile) {
    Write-Host "Existing config detected, backing up to settings.local.json.backup"
    Copy-Item $SettingsFile "$SettingsFile.backup" -Force
}

$SettingsContent = @'
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture-session-info.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
'@

$SettingsContentUnix = $SettingsContent -replace "`r`n", "`n"
[System.IO.File]::WriteAllText($SettingsFile, $SettingsContentUnix, $Utf8NoBomEncoding)

Write-Host "[5/5] Verifying installation..."
if ((Test-Path "$TargetDir\.claude\hooks\capture-session-info.py") -and `
    (Test-Path "$TargetDir\.claude\mcp-servers\context-monitor\server.py") -and `
    (Test-Path "$TargetDir\.claude\settings.local.json") -and `
    (Test-Path "$TargetDir\.mcp.json")) {
    Write-Host ""
    Write-Host "[SUCCESS] Context Monitor installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installation location: $TargetDir"
    Write-Host ""
    Write-Host "Files created:"
    Write-Host "  - .mcp.json (MCP server config)"
    Write-Host "  - .claude/settings.local.json (Hook config)"
    Write-Host "  - .claude/hooks/capture-session-info.py"
    Write-Host "  - .claude/mcp-servers/context-monitor/server.py"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "1. cd $TargetDir"
    Write-Host "2. claude"
    Write-Host "3. Approve context-monitor MCP server when prompted"
    Write-Host "4. In conversation: 请检查当前上下文使用率"
} else {
    Write-Host "[ERROR] Installation verification failed" -ForegroundColor Red
    exit 1
}
