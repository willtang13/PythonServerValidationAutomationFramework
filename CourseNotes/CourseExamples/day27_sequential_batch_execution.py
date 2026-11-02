def batch(jobs, run):
    results = []
    for job_id, command in jobs:
        try:
            results.append((job_id, 'completed', run(command)))
        except OSError as exc:
            results.append((job_id, 'failed', type(exc).__name__))
    return results

def test_batch():
    def run(command):
        if command == 'bad':
            raise OSError('unavailable')
        return 0
    result = batch([('a', 'ok'), ('b', 'bad'), ('c', 'ok')], run)
    assert [row[1] for row in result] == ['completed', 'failed', 'completed']
    assert batch([], run) == []

if __name__ == '__main__':
    test_batch()
    print('one failure does not end the batch')
