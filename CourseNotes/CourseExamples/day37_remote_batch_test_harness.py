from concurrent.futures import ThreadPoolExecutor, as_completed

def run_batch(run):
    jobs = [('host', 'hostname'), ('nonzero', "sh -c 'exit 7'"),
            ('timeout', 'sleep 2')]
    results = {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(run, command): job_id for job_id, command in jobs}
        for future in as_completed(futures):
            try:
                results[futures[future]] = future.result()
            except TimeoutError:
                results[futures[future]] = 'timeout'
    return results

def test_fake_batch():
    def run(command):
        if command == 'sleep 2':
            raise TimeoutError('fake deadline')
        return 7 if 'exit 7' in command else 0
    assert run_batch(run) == {'host': 0, 'nonzero': 7, 'timeout': 'timeout'}

if __name__ == '__main__':
    test_fake_batch()
    print('fake integration harness; replace run with owned real executor during class')
