from PyInstaller.utils.hooks import copy_metadata
datas = []

modules = ['tqdm', 'regex', 'sacremoses', 'requests', 'packaging', 'filelock', 'torch', 'torchaudio', 'six', 'numpy', 'huggingface_hub', 'tokenizers', 'joblib',
 'pyparsing', 'torchvision', 'future',  'transformers', 'urllib3']

for module in modules:
    datas.append(copy_metadata(module)[0])

print("=============")
print(datas)
print("=============")
