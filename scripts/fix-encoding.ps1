# Windows UTF-8 编码修复脚本
# 以管理员权限运行此脚本

Write-Host "正在配置 Windows UTF-8 支持..." -ForegroundColor Green

# 方法 1：设置系统环境变量
[System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
[System.Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")

Write-Host "✓ 已设置 Python UTF-8 环境变量" -ForegroundColor Green

# 方法 2：修改注册表启用 UTF-8（需要管理员权限）
try {
    $registryPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Nls\CodePage"
    Set-ItemProperty -Path $registryPath -Name "ACP" -Value "65001" -ErrorAction Stop
    Set-ItemProperty -Path $registryPath -Name "OEMCP" -Value "65001" -ErrorAction Stop
    Write-Host "✓ 已修改注册表启用 UTF-8" -ForegroundColor Green
    Write-Host "⚠ 需要重启计算机才能生效" -ForegroundColor Yellow
} catch {
    Write-Host "⚠ 无法修改注册表（需要管理员权限）" -ForegroundColor Yellow
    Write-Host "  可以手动在 控制面板 > 区域 > 管理 > 更改系统区域设置 中启用 UTF-8" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "配置完成！请重启 Claude Code 使环境变量生效。" -ForegroundColor Cyan
