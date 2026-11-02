from queue import Queue, Full

def submit(queue, job):
    try:
        queue.put_nowait(job)
    except Full as exc:
        raise RuntimeError('input capacity exhausted') from exc

def test_backpressure():
    queue = Queue(maxsize=2)
    submit(queue, 'a')
    submit(queue, 'b')
    try:
        submit(queue, 'c')
    except RuntimeError:
        pass
    else:
        raise AssertionError('must reject full input')
    assert queue.get_nowait() == 'a'
    queue.task_done()
    submit(queue, 'c')

if __name__ == '__main__':
    test_backpressure()
    print('bounded input rejects excess submission')
