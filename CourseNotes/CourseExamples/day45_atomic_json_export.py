import json
import os
import tempfile
from pathlib import Path

def export(path, records):
    path = Path(path)
    handle, temporary = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    try:
        with os.fdopen(handle, 'w', encoding='utf-8') as stream:
            json.dump(records, stream, ensure_ascii=False)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)

def test_export():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'report.json'
        records = [{'job_id': '一', 'state': 'completed', 'output': '中文\n'}]
        export(path, records)
        assert json.loads(path.read_text(encoding='utf-8')) == records

if __name__ == '__main__':
    test_export()
    print('atomic replacement demo; records must be allowlisted by caller')
