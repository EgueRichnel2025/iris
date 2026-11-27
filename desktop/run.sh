#!/usr/bin/env bash
set -euo pipefail
DESKTOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$DESKTOP_DIR/.venv/bin/python"
RUNTIME_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/iris/qt6-runtime"
SITE_PACKAGES="$("$VENV_PYTHON" -c 'import site; print(site.getsitepackages()[0])')"

if [[ ! -f "$RUNTIME_ROOT/usr/lib/x86_64-linux-gnu/libQt6Quick3D.so.6" ]]; then
  echo "Le moteur Qt Quick 3D n'est pas installé." >&2
  echo "Exécute d'abord : $DESKTOP_DIR/scripts/install_qt_quick3d_runtime.sh" >&2
  exit 1
fi

export LD_LIBRARY_PATH="$RUNTIME_ROOT/usr/lib/x86_64-linux-gnu:$SITE_PACKAGES/PySide6/Qt/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export QML2_IMPORT_PATH="$RUNTIME_ROOT/usr/lib/x86_64-linux-gnu/qt6/qml${QML2_IMPORT_PATH:+:$QML2_IMPORT_PATH}"
export QT_PLUGIN_PATH="$RUNTIME_ROOT/usr/lib/x86_64-linux-gnu/qt6/plugins${QT_PLUGIN_PATH:+:$QT_PLUGIN_PATH}"
exec "$VENV_PYTHON" -m iris "$@"
