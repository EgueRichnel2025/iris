#!/usr/bin/env bash
set -euo pipefail
DESKTOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="$DESKTOP_DIR/.venv/bin/python"
RUNTIME_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/iris/qt6-runtime"

[[ -x "$VENV_PYTHON" ]] || { echo "Environnement Python introuvable : $VENV_PYTHON" >&2; exit 1; }
command -v apt >/dev/null && command -v dpkg-deb >/dev/null || { echo "Installation automatique disponible sur Ubuntu/Debian (apt + dpkg-deb)." >&2; exit 1; }

packages=(libassimp6 libqt6quick3d6 libqt6quick3dassetimport6 libqt6quick3dassetutils6 libqt6quick3druntimerender6 libqt6quick3dutils6 python3-pyside6.qtquick3d qml6-module-qtquick3d qml6-module-qtquick3d-assetutils qml6-module-qtquick-timeline qt6-quick3d-assetimporters-plugin)
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
(
  cd "$tmp_dir"
  echo "Téléchargement des composants Qt Quick 3D (sans privilèges administrateur)…"
  apt download "${packages[@]}"
)
mkdir -p "$RUNTIME_ROOT"
for package in "$tmp_dir"/*.deb; do dpkg-deb -x "$package" "$RUNTIME_ROOT"; done
site_packages="$("$VENV_PYTHON" -c 'import site; print(site.getsitepackages()[0])')"
mkdir -p "$site_packages/PySide6"
cp "$RUNTIME_ROOT/usr/lib/python3/dist-packages/PySide6/QtQuick3D.abi3.so" "$site_packages/PySide6/"
cp "$RUNTIME_ROOT/usr/lib/python3/dist-packages/PySide6/QtQuick3D.pyi" "$site_packages/PySide6/"
export LD_LIBRARY_PATH="$RUNTIME_ROOT/usr/lib/x86_64-linux-gnu:$site_packages/PySide6/Qt/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export QML2_IMPORT_PATH="$RUNTIME_ROOT/usr/lib/x86_64-linux-gnu/qt6/qml${QML2_IMPORT_PATH:+:$QML2_IMPORT_PATH}"
export QT_PLUGIN_PATH="$RUNTIME_ROOT/usr/lib/x86_64-linux-gnu/qt6/plugins${QT_PLUGIN_PATH:+:$QT_PLUGIN_PATH}"
"$VENV_PYTHON" -c 'from PySide6.QtQuick3D import QQuick3D; from PySide6.QtQuickWidgets import QQuickWidget; print("Qt Quick 3D Python runtime : OK")'
echo "Runtime Qt Quick 3D installé dans : $RUNTIME_ROOT"
echo "Lancement conseillé : $DESKTOP_DIR/run.sh"
