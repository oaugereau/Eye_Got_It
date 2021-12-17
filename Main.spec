# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['eye_got_it/Main.py'],
             pathex=['eye_got_it/eye_got_it'],
             binaries=[],
             datas=[('eye_got_it/docs','docs'),('eye_got_it/eyeTracker','eyeTracker'),('eye_got_it/eyeTrackerPro','eyeTrackerPro'),('eye_got_it/model','model'),('eye_got_it/opencv','opencv'),('eye_got_it/openFace','openFace'),('eye_got_it/Pictures','Pictures'),('eye_got_it/actionUnits.ini','.'),('eye_got_it/config.ini','.'),('eye_got_it/config.ini.bak','.'),('eye_got_it.ico','.'),('Changelog.txt','.'),('eye_got_it/README.txt','.')],
             hiddenimports=['sklearn.neighbors._typedefs','sklearn.utils._weight_vector','sklearn.neighbors._typedefs','sklearn.neighbors._quad_tree'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Eye Got It',
          icon = 'eye_got_it.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Eye Got It')