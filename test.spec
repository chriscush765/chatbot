# -*- mode: python ; coding: utf-8 -*-


from transformers import data


def extra_datas():
    from PyInstaller.utils.hooks import copy_metadata
    datas = []

    modules = ['tqdm', 'regex', 'sacremoses', 'requests', 'packaging', 'filelock', 'torch', 'torchaudio', 'six', 'numpy', 'huggingface_hub', 'tokenizers', 'joblib',
    'pyparsing', 'torchvision', 'future',  'transformers', 'urllib3']

    for module in modules:
        datas.append(copy_metadata(module)[0])
    return datas


block_cipher = None

a = Analysis(['test.py'],
             pathex=[],
             binaries=[],
             datas=extra_datas(),
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='test',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='test')
