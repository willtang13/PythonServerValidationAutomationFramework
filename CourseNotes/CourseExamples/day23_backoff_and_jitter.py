def next_delay(attempt, *, base, cap, remaining, random_unit):
    if attempt < 1 or base < 0 or cap < 0 or remaining <= 0:
        raise TimeoutError('no retry budget or invalid schedule')
    ceiling = min(cap, base * 2 ** min(attempt - 1, 30))
    delay = ceiling * random_unit()
    if delay >= remaining:
        raise TimeoutError('backoff would exhaust budget')
    return delay

def test_backoff():
    kwargs = dict(base=1, cap=4, remaining=10, random_unit=lambda: 0.5)
    assert [next_delay(n, **kwargs) for n in (1, 2, 3, 4)] == [0.5, 1, 2, 2]
    try:
        next_delay(4, base=1, cap=4, remaining=1, random_unit=lambda: 0.5)
    except TimeoutError:
        pass
    else:
        raise AssertionError('must not wait past budget')

if __name__ == '__main__':
    test_backoff()
    print('capped jitter schedule verified; caller must recheck clock after sleeping')
