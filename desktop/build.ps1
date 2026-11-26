$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

uv run --no-sync python -m PyInstaller --noconfirm --clean IRIS.spec

Write-Host ""
Write-Host "Windows executable: $PSScriptRoot\dist\IRIS\IRIS.exe"
