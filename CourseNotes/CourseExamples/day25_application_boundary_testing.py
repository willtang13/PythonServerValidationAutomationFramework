from io import StringIO

def application(config, run, output):
    if config.get('attempts', 0) < 1:
        raise ValueError('invalid attempts')
    for attempt in range(config['attempts']):
        try:
            code = run()
            print(f'code={code}', file=output)
            return 0 if code == 0 else 1
        except ConnectionRefusedError:
            if attempt + 1 == config['attempts']:
                raise

def test_boundary():
    values = iter([ConnectionRefusedError(), 7])
    def run():
        value = next(values)
        if isinstance(value, Exception):
            raise value
        return value
    output = StringIO()
    assert application({'attempts': 2}, run, output) == 1
    assert output.getvalue() == 'code=7\n'

if __name__ == '__main__':
    test_boundary()
    print('application boundary verified with a safe pre-request failure')
