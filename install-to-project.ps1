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

Write-Host "[1/4] Creating directory structure..."
New-Item -ItemType Directory -Force -Path "$TargetDir\.claude\hooks" | Out-Null
New-Item -ItemType Directory -Force -Path "$TargetDir\.claude\mcp-servers\context-monitor" | Out-Null
New-Item -ItemType Directory -Force -Path "$TargetDir\.claude\state" | Out-Null

Write-Host "[2/4] Copying files..."
Copy-Item "$ScriptDir\.claude\hooks\capture-session-info.sh" "$TargetDir\.claude\hooks\" -Force
Copy-Item "$ScriptDir\.claude\mcp-servers\context-monitor\server.py" "$TargetDir\.claude\mcp-servers\context-monitor\" -Force

Write-Host "[3/4] Configuring .claude\settings.local.json..."
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
        "type": "command",
        "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture-session-info.sh\"",
        "timeout": 5
      }
    ]
  },
  "mcpServers": {
    "context-monitor": {
      "command": "python3",
      "args": [".claude/mcp-servers/context-monitor/server.py"],
      "env": {}
    }
  }
}
'@

Set-Content -Path $SettingsFile -Value $SettingsContent -Encoding UTF8

Write-Host "[4/4] Verifying installation..."
if ((Test-Path "$TargetDir\.claude\hooks\capture-session-info.sh") -and `
    (Test-Path "$TargetDir\.claude\mcp-servers\context-monitor\server.py") -and `
    (Test-Path "$TargetDir\.claude\settings.local.json")) {
    Write-Host ""
    Write-Host "[SUCCESS] Context Monitor installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installation location: $TargetDir"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "1. cd $TargetDir"
    Write-Host "2. claude"
    Write-Host "3. In conversation: check current context usage"
} else {
    Write-Host "[ERROR] Installation verification failed" -ForegroundColor Red
    exit 1
}
