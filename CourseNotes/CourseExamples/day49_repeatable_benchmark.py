from statistics import median
from time import perf_counter

def benchmark(operation, repeats=5):
    operation()  # Warm-up excluded.
    samples = []
    for _ in range(repeats):
        start = perf_counter()
        operation()
        samples.append(perf_counter() - start)
    return {'samples': samples, 'median': median(samples), 'range': [min(samples), max(samples)]}

def test_measurement_shape():
    result = benchmark(lambda: sum(range(100)))
    assert len(result['samples']) == 5
    assert result['range'][0] <= result['median'] <= result['range'][1]

if __name__ == '__main__':
    test_measurement_shape()
    print(benchmark(lambda: sum(range(1000))))
