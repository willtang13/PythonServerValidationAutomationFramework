import sqlite3
from contextlib import closing

class ResultRepository:
    def __init__(self, connection):
        self.db = connection  # Borrowed; caller owns close and transaction.
    def add(self, job_id, output):
        self.db.execute('INSERT INTO result VALUES (?, ?)', (job_id, output))
    def get(self, job_id):
        return self.db.execute('SELECT output FROM result WHERE id=?', (job_id,)).fetchone()

def test_repository():
    with closing(sqlite3.connect(':memory:')) as db:
        db.execute('CREATE TABLE result(id TEXT PRIMARY KEY, output TEXT)')
        repo = ResultRepository(db)
        with db:
            repo.add('job', "quote'\n中文")
        assert repo.get('job') == ("quote'\n中文",)

if __name__ == '__main__':
    test_repository()
    print('bound parameters preserve data')
