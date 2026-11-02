import tomllib

def load(text, override=None):
    file_values = tomllib.loads(text)
    timeout = file_values.get('timeout', 10)
    if override is not None:
        timeout = override
    if type(timeout) is not int or timeout <= 0:
        raise ValueError('invalid timeout')
    return timeout

def test_priority():
    assert load('') == 10
    assert load('timeout = 8') == 8
    assert load('timeout = 8', 3) == 3
    try:
        load('timeout = 8', 0)
    except ValueError:
        pass
    else:
        raise AssertionError('invalid explicit override must fail')

if __name__ == '__main__':
    test_priority()
    print('explicit override validated')
