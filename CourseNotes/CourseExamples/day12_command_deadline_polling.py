class CommandTimeout(TimeoutError):
    def __init__(self, partial):
        super().__init__('command deadline exceeded')
        self.partial = partial

def poll(read, clock, sleep, close, *, budget):
    end = clock() + budget
    data = bytearray()
    try:
        while True:
            if clock() >= end:
                raise CommandTimeout(bytes(data))
            chunk, done = read()
            data.extend(chunk)
            if clock() >= end:
                raise CommandTimeout(bytes(data))
            if done:
                return bytes(data)
            sleep(min(0.01, end - clock()))
    finally:
        close()

def test_timeout():
    now, closed = [0.0], []
    def sleep(seconds):
        now[0] += seconds
    for chunk in (b'', b'x'):
        now[0] = 0
        try:
            poll(lambda: (chunk, False), lambda: now[0], sleep,
                 lambda: closed.append(True), budget=0.03)
        except CommandTimeout as exc:
            assert not hasattr(exc, 'exit_code')
        else:
            raise AssertionError('must time out')
    assert len(closed) == 2

if __name__ == '__main__':
    test_timeout()
    print('silent and chatty fake commands expire')
