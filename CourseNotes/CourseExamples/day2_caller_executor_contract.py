from dataclasses import dataclass

@dataclass(frozen=True)
class Result:
    stdout: str
    stderr: str
    exit_code: int

def execute(command):
    if command == 'cannot-login':
        raise PermissionError('authentication failed')
    return Result('partial\n', 'diagnostic\n', 7)

def test_contract():
    result = execute('demo')
    assert result.exit_code == 7  # Caller expects 7.
    try:
        execute('cannot-login')
    except PermissionError:
        pass
    else:
        raise AssertionError('must not return a fabricated result')

if __name__ == '__main__':
    test_contract()
    print('contract verified with a fake executor')
