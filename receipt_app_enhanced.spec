# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['receipt_app_enhanced.py'],
    pathex=[],
    binaries=[],
    datas=[('enhanced_receipt_database.db', '.'), ('logo.png', '.'), ('admin_management.py', '.'), ('receipt_app_gui.py', '.'), ('view_receipts.py', '.'), ('view_receipts_gui.py', '.')],
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
    name='receipt_app_enhanced',
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
)
