from concurrent.futures import ThreadPoolExecutor
from time import perf_counter, sleep
from statistics import median

def wait_job(item):
    sleep(0.005)
    return item

def measure(workers):
    times = []
    for _ in range(3):
        start = perf_counter()
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(wait_job, range(8)))
        times.append(perf_counter() - start)
        assert results == list(range(8))
    return {'workers': workers, 'samples': times, 'median': median(times), 'failures': 0}

def test_results():
    assert measure(1)['failures'] == 0

if __name__ == '__main__':
    for workers in (1, 2, 4):
        print(measure(workers))
