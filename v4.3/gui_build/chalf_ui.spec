# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['CHalf_v4_3_UI_production.py'],
    pathex=[],
    binaries=[],
    # Translates --add-data "images;images"
    # Format is (source_path, destination_folder)
    datas=[('images', 'images')], 
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CHalf_v4_3',  # The final name of your GUI exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,      # Translates --windowed (hides terminal)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='CHalf Protein Logo.ico', # Translates --icon
)