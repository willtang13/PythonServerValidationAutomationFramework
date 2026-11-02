class TemporaryFailure(Exception):
    pass

def retry(operation, *, max_attempts, sleep):
    if type(max_attempts) is not int or max_attempts < 1:
        raise ValueError('max_attempts includes the first call')
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except TemporaryFailure:
            if attempt == max_attempts:
                raise
            sleep(0.1)

def test_retry():
    calls, waits = [], []
    def operation():
        calls.append(1)
        if len(calls) < 3:
            raise TemporaryFailure('before request submission')
        return 7
    assert retry(operation, max_attempts=3, sleep=waits.append) == 7
    assert len(calls) == 3 and len(waits) == 2

if __name__ == '__main__':
    test_retry()
    print('three attempts, two waits')
