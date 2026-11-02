from pathlib import Path
from tempfile import TemporaryDirectory
import py_compile

def test_portable_files():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        report = root / 'report.txt'
        report.write_text('台灣\n', encoding='utf-8')
        assert report.read_text(encoding='utf-8') == '台灣\n'
        module = root / 'module.py'
        module.write_text('def value():\n    return 7\n', encoding='utf-8')
        py_compile.compile(str(module), doraise=True)

if __name__ == '__main__':
    test_portable_files()
    print('portable local file and syntax check; other platforms remain unverified')
