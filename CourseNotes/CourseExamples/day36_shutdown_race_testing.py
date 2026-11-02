from threading import Event, Lock, Thread

def test_close_before_submission():
    lock, closed, allow, done = Lock(), False, Event(), Event()
    accepted, rejected = [], []
    def submitter():
        if not allow.wait(2):
            return
        with lock:
            if closed:
                rejected.append('job')
            else:
                accepted.append('job')
        done.set()
    thread = Thread(target=submitter)
    thread.start()
    try:
        with lock:
            closed = True
        allow.set()
        assert done.wait(2)
    finally:
        allow.set()
        thread.join(timeout=2)
    assert not thread.is_alive()
    assert accepted == [] and rejected == ['job']

if __name__ == '__main__':
    test_close_before_submission()
    print('specific interleaving reproduced without timing guesses')
