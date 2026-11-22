$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

uv run pyinstaller `
  --noconfirm `
  --clean `
  --windowed `
  --name IRIS `
  --collect-all cv2 `
  iris/__main__.py

Write-Host ""
Write-Host "Windows executable: $PSScriptRoot\dist\IRIS\IRIS.exe"
