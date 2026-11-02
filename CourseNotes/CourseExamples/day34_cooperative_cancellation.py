from concurrent.futures import ThreadPoolExecutor
from threading import Event

def work(started, stop):
    started.set()
    while not stop.wait(0.01):
        pass
    return 'cancelled-cooperatively'

def test_cancellation():
    started, stop = Event(), Event()
    with ThreadPoolExecutor(max_workers=1) as pool:
        running = pool.submit(work, started, stop)
        try:
            assert started.wait(2)
            queued = pool.submit(lambda: 'not started')
            assert queued.cancel()
            assert not running.cancel()
        finally:
            stop.set()
        assert running.result(timeout=2) == 'cancelled-cooperatively'

if __name__ == '__main__':
    test_cancellation()
    print('queued cancellation differs from cooperative stopping')
