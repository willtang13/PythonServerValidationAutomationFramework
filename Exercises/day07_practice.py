from dataclasses import dataclass

@dataclass(frozen=True)
class RawResult:
    stdout: bytes
    stderr: bytes
    exit_code: int

@dataclass(frozen=True)
class DecodedResult:
    stdout: str
    stderr: str
    exit_code: int

def decoder(result: RawResult) -> DecodedResult:

    stdout = result.stdout.decode('utf-8')
    stderr = result.stderr.decode('utf-8')
    exit_code = result.exit_code

    decoded_result = DecodedResult(
        stdout=stdout,
        stderr=stderr,
        exit_code=exit_code
    )
    return decoded_result


def test_decode_empty_result() -> None:

    raw_result = RawResult(
        stdout=b'',
        stderr=b'',
        exit_code=0
    )

    decoded_result = decoder(raw_result)

    assert decoded_result.stdout == ""
    assert decoded_result.stderr == ""
    assert decoded_result.exit_code == 0


def test_decode_dianostic_result() -> None:

    raw_result = RawResult(
        stdout="  節點 A  \n".encode("utf-8"),
        stderr="  診斷：略過一筆  \n".encode("utf-8"),
        exit_code=9
    )

    decoded_result = decoder(raw_result)

    assert decoded_result.stdout == "  節點 A  \n"
    assert decoded_result.stderr == "  診斷：略過一筆  \n"
    assert decoded_result.exit_code == 9


def test_decode_with_raising_unicode_decode_error() -> None:

    raw_result = RawResult(
        stdout=b'\xff',
        stderr=b'',
        exit_code=0
    )

    try:
        decoder(raw_result)

    except UnicodeDecodeError as exc:
        # print(str(exc))
        assert str(exc) == "'utf-8' codec can't decode byte 0xff" \
                            " in position 0: invalid start byte"

    else:
        AssertionError("Expected UnicodeDecodeError, but decoder returned")

if __name__ == "__main__":
    test_decode_empty_result()
    test_decode_dianostic_result()
    test_decode_with_raising_unicode_decode_error()
    print("decode result verified")