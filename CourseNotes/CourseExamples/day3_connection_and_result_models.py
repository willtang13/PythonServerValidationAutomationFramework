from dataclasses import dataclass, field
from math import isfinite

@dataclass(frozen=True, slots=True, kw_only=True)
class ConnectionConfig:
    host: str
    username: str
    port: int = 22
    timeout: float = 10.0
    passphrase: str | None = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        if not isinstance(self.host, str) or not self.host.strip():
            raise ValueError('host must be nonempty')
        if not isinstance(self.username, str) or not self.username.strip():
            raise ValueError('username must be nonempty')
        if type(self.port) is not int or not 1 <= self.port <= 65535:
            raise ValueError('invalid port')
        if type(self.timeout) not in (int, float) or not isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError('timeout must be finite and positive')

def test_model():
    config = ConnectionConfig(host='lab', username='student', passphrase='DEMO_SECRET')
    assert 'DEMO_SECRET' not in repr(config)
    for timeout in (0, -1, float('inf'), float('nan'), True):
        try:
            ConnectionConfig(host='lab', username='student', timeout=timeout)
        except ValueError:
            continue
        raise AssertionError('invalid timeout accepted')


@dataclass(frozen=True, slots=True, kw_only=True)
class CommandResult:
    stdout: str
    stderr: str
    exit_code: int
    duration: float

    def __post_init__(self):
        if not isinstance(self.stdout, str) or not isinstance(self.stderr, str):
            raise ValueError('outputs must be text')
        if type(self.exit_code) is not int or self.exit_code < 0:
            raise ValueError('complete result requires an exit code')
        if type(self.duration) not in (int, float) or not isfinite(self.duration) or self.duration < 0:
            raise ValueError('duration must be finite and nonnegative')

def test_result_model():
    result = CommandResult(stdout=' data\n', stderr='diagnostic\n', exit_code=7, duration=0)
    assert result.stdout == ' data\n' and result.exit_code == 7
    try:
        CommandResult(stdout='', stderr='', exit_code=-1, duration=0)
    except ValueError:
        pass
    else:
        raise AssertionError('missing status must not be a complete result')

if __name__ == '__main__':
    test_model()
    test_result_model()
    print('model verified')
