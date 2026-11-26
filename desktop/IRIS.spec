# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

datas = [
    ("assets/models/face_landmarker.task", "assets/models"),
]
datas += collect_data_files("mediapipe")
binaries = collect_dynamic_libs("mediapipe")
hiddenimports = [
    "mediapipe.tasks",
    "mediapipe.tasks.python",
    "mediapipe.tasks.python.vision",
    "mediapipe.tasks.python.vision.face_landmarker",
    "mediapipe.tasks.python.core.base_options",
    "mediapipe.tasks.python.vision.core.vision_task_running_mode",
    "mediapipe.python._framework_bindings",
]

a = Analysis(
    ["iris/__main__.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "mediapipe.tasks.python.test",
        "scipy",
        "matplotlib",
        "pytest",
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="IRIS",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="IRIS",
)
