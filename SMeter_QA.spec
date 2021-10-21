# -*- mode: python -*-

block_cipher = None


a = Analysis(['SMeter_QA.py'],
             pathex=['E:\\Anaconda3\\envs\\py35\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'E:\\Workspaces\\Python3\\SMeter_QA'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='SMeter_QA',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SMeter_QA')
