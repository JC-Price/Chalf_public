# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['CHalf_v4_3.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'matplotlib.backends.backend_agg',
        'matplotlib.backends._backend_agg',
        'matplotlib.backends.backend_svg',
        'matplotlib.pyplot',
        'multiprocessing',
        'joblib',
        'pandas',
        'scipy.special.cython_special',
        'numpy.random.bit_generator',
        'dateutil',
        'dateutil.rrule'
    ],
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
    name='CHalf_v4_3_core',
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
    icon='CHalf Protein Logo.ico',
)