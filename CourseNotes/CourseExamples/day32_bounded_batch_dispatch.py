from concurrent.futures import ThreadPoolExecutor
from itertools import islice

def bounded_batches(source, run, workers=2):
    if type(workers) is not int or workers < 1:
        raise ValueError('workers must be positive')
    iterator = iter(source)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        while chunk := list(islice(iterator, workers)):
            futures = [pool.submit(run, item) for item in chunk]
            for future in futures:
                yield future.result()

def test_window():
    produced = []
    def source():
        for n in range(7):
            produced.append(n)
            yield n
    results = bounded_batches(source(), lambda n: n * 2, workers=2)
    assert next(results) == 0
    assert len(produced) == 2
    assert [0, *results] == [n * 2 for n in range(7)]

if __name__ == '__main__':
    test_window()
    print('bounded batch window; slower than a sliding window for uneven jobs')
