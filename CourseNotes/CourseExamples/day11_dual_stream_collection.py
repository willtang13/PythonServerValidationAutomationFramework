def collect_frames(frames):
    # Fake protocol: (stdout chunk, stderr chunk, input ended, exit status).
    out, err = bytearray(), bytearray()
    status = None
    for stdout, stderr, ended, code in frames:
        out.extend(stdout)
        err.extend(stderr)
        if code is not None:
            status = code
        if ended:
            if status is None:
                raise RuntimeError('missing exit status')
            return bytes(out), bytes(err), status
    raise RuntimeError('input did not finish')

def test_late_output():
    frames = [(b'a', b'e', False, 0), (b'b', b'f', True, None)]
    assert collect_frames(frames) == (b'ab', b'ef', 0)
    assert collect_frames([(b'', b'', True, 0)]) == (b'', b'', 0)

if __name__ == '__main__':
    test_late_output()
    print('exit status did not discard late output')
