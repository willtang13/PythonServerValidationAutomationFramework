from dataclasses import dataclass

@dataclass(frozen=True)
class Result:
    stdout: str
    stderr: str
    exit_code: int

def decode_result(out, err, code):
    return Result(out.decode('utf-8'), err.decode('utf-8'), code)

def test_preservation():
    result = decode_result(b'  partial\n', '診斷\n'.encode(), 7)
    assert result.stdout == '  partial\n'
    assert result.stderr == '診斷\n'
    assert result.exit_code == 7
    assert decode_result(b'', b'', 0).stdout == ''

if __name__ == '__main__':
    test_preservation()
    print('raw text preserved')
