$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

uv run --no-sync pyinstaller --noconfirm --clean IRIS.spec

Write-Host ""
Write-Host "Windows executable: $PSScriptRoot\dist\IRIS\IRIS.exe"
