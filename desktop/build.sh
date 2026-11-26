#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
uv run --no-sync pyinstaller --noconfirm --clean IRIS.spec

printf '\nLinux application bundle: %s\n' "$(pwd)/dist/IRIS"
