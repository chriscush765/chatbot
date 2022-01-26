import PyInstaller.__main__
import shutil

PyInstaller.__main__.run([
    'test.spec',
    '--noconfirm',
    '--clean',
    '--windowed'

], )

# shutil.copytree('model', 'dist/test/model')
# shutil.copytree('tokenizer', 'dist/test/tokenizer')