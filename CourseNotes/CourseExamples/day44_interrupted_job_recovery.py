import sqlite3
from contextlib import closing

def recover_single_process(db):
    # Precondition: exclusively owned database, no other live executor.
    with db:
        db.execute("UPDATE job SET state='unknown' WHERE state='running'")

def test_recovery():
    with closing(sqlite3.connect(':memory:')) as db:
        db.execute('CREATE TABLE job(id TEXT PRIMARY KEY, state TEXT)')
        with db:
            db.executemany('INSERT INTO job VALUES (?, ?)', [('a', 'running'), ('b', 'completed')])
        recover_single_process(db)
        assert db.execute('SELECT state FROM job ORDER BY id').fetchall() == [('unknown',), ('completed',)]

if __name__ == '__main__':
    test_recovery()
    print('unknown does not mean safe to rerun')
