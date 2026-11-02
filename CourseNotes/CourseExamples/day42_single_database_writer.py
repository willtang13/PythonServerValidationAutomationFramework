import sqlite3
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from queue import Queue

def writer(queue):
    # Database ownership remains entirely in this thread.
    with closing(sqlite3.connect(':memory:')) as db:
        db.execute('CREATE TABLE result(value INTEGER)')
        with db:
            while True:
                item = queue.get(timeout=2)
                try:
                    if item is None:
                        break
                    db.execute('INSERT INTO result VALUES (?)', (item,))
                finally:
                    queue.task_done()
        return db.execute('SELECT value FROM result ORDER BY value').fetchall()

def test_writer():
    queue = Queue(maxsize=2)
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(writer, queue)
        for value in range(4):
            queue.put(value, timeout=2)
        queue.put(None, timeout=2)
        assert future.result(timeout=3) == [(0,), (1,), (2,), (3,)]
    assert queue.unfinished_tasks == 0

if __name__ == '__main__':
    test_writer()
    print('single-owner writer verified; production failure signalling is a separate integration step')
