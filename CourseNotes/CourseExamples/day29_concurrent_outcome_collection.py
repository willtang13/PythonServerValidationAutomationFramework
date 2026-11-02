from concurrent.futures import ThreadPoolExecutor, as_completed

def collect(jobs, run):
    outcomes = {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending = {pool.submit(run, value): job_id for job_id, value in jobs}
        for future in as_completed(pending):
            job_id = pending[future]
            try:
                outcomes[job_id] = ('completed', future.result())
            except ValueError as exc:
                outcomes[job_id] = ('failed', type(exc).__name__)
    return outcomes

def test_outcomes():
    def square(value):
        if value < 0:
            raise ValueError('negative input')
        return value * value
    results = collect([('a', 2), ('b', -1), ('c', 3)], square)
    assert results == {'a': ('completed', 4), 'b': ('failed', 'ValueError'),
                       'c': ('completed', 9)}

if __name__ == '__main__':
    test_outcomes()
    print('per-job outcomes retained; input IDs must be unique')
