import sqlite3
from contextlib import closing

def test_transaction():
    with closing(sqlite3.connect(':memory:')) as db:
        db.execute('CREATE TABLE record(id INTEGER PRIMARY KEY)')
        try:
            with db:
                db.execute('INSERT INTO record VALUES (1)')
                db.execute('INSERT INTO record VALUES (1)')
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError('expected unique violation')
        assert db.execute('SELECT COUNT(*) FROM record').fetchone()[0] == 0
        with db:
            db.execute('INSERT INTO record VALUES (2)')
        assert db.execute('SELECT id FROM record').fetchall() == [(2,)]

if __name__ == '__main__':
    test_transaction()
    print('partial transaction rolled back')
