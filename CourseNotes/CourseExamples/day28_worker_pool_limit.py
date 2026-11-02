from concurrent.futures import ThreadPoolExecutor
from threading import Event, Lock

def test_worker_limit():
    gate, both_started, lock = Event(), Event(), Lock()
    active, peak = 0, 0
    def work():
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
            if active == 2:
                both_started.set()
        try:
            if not gate.wait(2):
                raise TimeoutError('test gate timed out')
            return 1
        finally:
            with lock:
                active -= 1
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(work) for _ in range(4)]
        try:
            assert both_started.wait(2)
            assert peak == 2
        finally:
            gate.set()
        assert sum(f.result(timeout=2) for f in futures) == 4
    assert peak <= 2 and active == 0

if __name__ == '__main__':
    test_worker_limit()
    print('worker limit observed with events')
