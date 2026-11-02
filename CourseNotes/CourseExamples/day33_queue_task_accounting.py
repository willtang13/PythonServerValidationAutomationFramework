from queue import Queue

def consume_available(queue, run):
    errors = []
    # Single consumer; caller has already finished producing this finite batch.
    while not queue.empty():
        item = queue.get_nowait()
        try:
            run(item)
        except ValueError as exc:
            errors.append(type(exc).__name__)
        finally:
            queue.task_done()
    return errors

def test_accounting():
    queue = Queue()
    for item in (1, -1, 2):
        queue.put(item)
    def run(item):
        if item < 0:
            raise ValueError('bad item')
    assert consume_available(queue, run) == ['ValueError']
    assert queue.unfinished_tasks == 0
    queue.join()

if __name__ == '__main__':
    test_accounting()
    print('every successful get acknowledged, even on failure')
