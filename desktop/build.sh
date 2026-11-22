#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
uv run --no-sync pyinstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name IRIS \
  --collect-all cv2 \
  iris/__main__.py

printf '\nLinux application bundle: %s\n' "$(pwd)/dist/IRIS"
