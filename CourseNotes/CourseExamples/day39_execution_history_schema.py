import sqlite3
from contextlib import closing

SCHEMA = """
CREATE TABLE batch(id TEXT PRIMARY KEY);
CREATE TABLE job(id TEXT PRIMARY KEY, batch_id TEXT NOT NULL REFERENCES batch(id));
CREATE TABLE attempt(job_id TEXT NOT NULL REFERENCES job(id), number INTEGER NOT NULL,
 state TEXT NOT NULL, exit_code INTEGER, PRIMARY KEY(job_id, number));
"""

def test_schema():
    with closing(sqlite3.connect(':memory:')) as db:
        db.execute('PRAGMA foreign_keys=ON')
        db.executescript(SCHEMA)
        with db:
            db.execute('INSERT INTO batch VALUES (?)', ('b1',))
            db.execute('INSERT INTO job VALUES (?, ?)', ('j1', 'b1'))
            db.execute('INSERT INTO attempt VALUES (?, ?, ?, ?)', ('j1', 1, 'failed', None))
            db.execute('INSERT INTO attempt VALUES (?, ?, ?, ?)', ('j1', 2, 'completed', 7))
        assert db.execute('SELECT COUNT(*) FROM attempt').fetchone()[0] == 2

if __name__ == '__main__':
    test_schema()
    print('attempt history retained without credentials')
