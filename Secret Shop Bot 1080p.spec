# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['1080_main.py'],
    pathex=[],
    binaries=[],
    datas=[('1080shop_cov.png', '.'), ('1080shop_myst.png', '.'), ('icon.png', '.'), ('icon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Secret Shop Bot 1080p',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info_1080p.txt',
    icon=['icon.ico'],
)
