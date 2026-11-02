from math import isfinite

class Deadline:
    def __init__(self, seconds, clock):
        if not isfinite(seconds) or seconds <= 0:
            raise ValueError('positive finite budget required')
        self.clock = clock
        self.end = clock() + seconds
    def remaining(self):
        return max(0.0, self.end - self.clock())
    def check(self):
        if self.remaining() == 0:
            raise TimeoutError('budget exhausted')

def test_boundary():
    now = [100.0]
    deadline = Deadline(3, lambda: now[0])
    assert deadline.remaining() == 3
    now[0] = 103
    try:
        deadline.check()
    except TimeoutError:
        pass
    else:
        raise AssertionError('exact deadline must expire')
    now[0] = 104
    assert deadline.remaining() == 0

if __name__ == '__main__':
    test_boundary()
    print('deadline boundary verified')
