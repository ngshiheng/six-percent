# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\ngshi\\Documents\\Personal\\six-percent'],
             binaries=[('bin\\driver\\chromedriver.exe', 'bin\\driver\\')],
             datas=[('config.ini', '.'), ('users.json', '.')],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SixPercent',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='bin\\favicon.ico')

import shutil
shutil.copyfile('config.ini', '{0}/config.ini'.format(DISTPATH))
shutil.copyfile('users.json', '{0}/users.json'.format(DISTPATH))