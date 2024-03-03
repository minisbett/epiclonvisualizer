# -*- mode: python ; coding: utf-8 -*-


from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE


a = Analysis(
    ["../main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("../version.txt", "."),
        ("../templates/*", "templates"),
        ("../static/js/*", "static/js"),
        ("../static/css/*", "static/css"),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="epiclonvisualizer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icon.ico",
)
