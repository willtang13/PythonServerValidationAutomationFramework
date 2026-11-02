import argparse

def positive(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError('must be positive')
    return number

def parse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    parser.add_argument('--timeout', type=positive, default=10)
    return parser.parse_args(argv)

def test_parse():
    assert parse(['--host', 'lab']).timeout == 10
    assert parse(['--host', 'lab', '--timeout', '3']).timeout == 3

if __name__ == '__main__':
    test_parse()
    print('parsing does not connect')
