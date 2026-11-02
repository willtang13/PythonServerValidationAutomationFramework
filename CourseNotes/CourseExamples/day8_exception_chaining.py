class ConfigReadError(Exception):
    pass

def read_config(loader):
    try:
        return loader()
    except OSError as exc:
        raise ConfigReadError('configuration unavailable') from exc

def test_cause():
    original = FileNotFoundError('demo.conf')
    def fail():
        raise original
    try:
        read_config(fail)
    except ConfigReadError as exc:
        assert exc.__cause__ is original
    else:
        raise AssertionError('expected domain error')

if __name__ == '__main__':
    test_cause()
    print('cause retained')
