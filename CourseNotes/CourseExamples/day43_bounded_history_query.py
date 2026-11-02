import sqlite3
from contextlib import closing

def recent(db, state, limit):
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError('limit must be 1..100')
    return db.execute('SELECT id FROM result WHERE state=? ORDER BY created DESC, id DESC LIMIT ?',
                      (state, limit)).fetchall()

def test_query():
    with closing(sqlite3.connect(':memory:')) as db:
        db.execute('CREATE TABLE result(id INTEGER PRIMARY KEY, state TEXT, created INTEGER)')
        db.execute('CREATE INDEX by_state_time ON result(state, created, id)')
        with db:
            db.executemany('INSERT INTO result VALUES (?, ?, ?)', [(1, 'ok', 5), (2, 'ok', 5)])
        assert recent(db, 'ok', 1) == [(2,)]
        assert recent(db, 'failed', 1) == []

if __name__ == '__main__':
    test_query()
    print('bounded stable query verified')
