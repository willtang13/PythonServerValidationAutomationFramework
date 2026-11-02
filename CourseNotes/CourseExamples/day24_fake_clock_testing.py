class FakeClock:
    def __init__(self):
        self.now = 0.0
        self.waits = []
    def __call__(self):
        return self.now
    def sleep(self, seconds):
        if seconds < 0:
            raise ValueError('negative wait')
        self.waits.append(seconds)
        self.now += seconds

def wait_until_ready(clock, ready, timeout):
    end = clock() + timeout
    while clock() < end:
        if ready():
            return True
        clock.sleep(min(0.25, end - clock()))
    return False

def test_fake_clock():
    clock = FakeClock()
    assert wait_until_ready(clock, lambda: clock() >= 0.5, 1)
    assert clock() == 0.5
    assert not wait_until_ready(clock, lambda: False, 0.5)

if __name__ == '__main__':
    test_fake_clock()
    print('deterministic waits without wall-clock delay')
