from dataclasses import dataclass
from time import monotonic

@dataclass(frozen=True)
class Result:
    stdout: str
    stderr: str
    exit_code: int
    duration: float

def execute_small(client, command):
    # Small-output teaching slice only. Replaced by bounded polling in Days 11-13.
    start = monotonic()
    stdin, stdout, stderr = client.exec_command(command, timeout=2)
    stdin.close()
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    return Result(out, err, stdout.channel.recv_exit_status(), monotonic() - start)

def test_small():
    from io import BytesIO
    class Output(BytesIO):
        @property
        def channel(self):
            return self
        def recv_exit_status(self):
            return 0
    class Client:
        def exec_command(self, command, **kwargs):
            assert command == 'hostname'
            return BytesIO(), Output(b'serverlab-ubuntu\n'), Output(b'')
    result = execute_small(Client(), 'hostname')
    assert result.stdout == 'serverlab-ubuntu\n' and result.exit_code == 0

if __name__ == '__main__':
    test_small()
    print('small-output fake command verified')
