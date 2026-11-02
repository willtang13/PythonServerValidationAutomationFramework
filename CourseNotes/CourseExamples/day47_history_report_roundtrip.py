import json
import sqlite3
from contextlib import closing

def test_roundtrip():
    outcomes = [('a', 'completed', 0), ('b', 'completed', 7), ('c', 'failed', None)]
    with closing(sqlite3.connect(':memory:')) as db:
        db.execute('CREATE TABLE result(id TEXT PRIMARY KEY, state TEXT, code INTEGER)')
        with db:
            db.executemany('INSERT INTO result VALUES (?, ?, ?)', outcomes)
        rows = db.execute('SELECT id, state, code FROM result ORDER BY id').fetchall()
        report = json.dumps([dict(zip(('job_id', 'state', 'exit_code'), row)) for row in rows])
        loaded = json.loads(report)
        assert [row['job_id'] for row in loaded] == ['a', 'b', 'c']
        assert loaded[1]['exit_code'] == 7 and loaded[2]['exit_code'] is None

if __name__ == '__main__':
    test_roundtrip()
    print('storage/report vertical slice verified without remote execution')
