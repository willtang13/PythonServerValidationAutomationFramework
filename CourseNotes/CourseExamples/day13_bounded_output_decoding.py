class OutputLimitError(Exception):
    pass

def decode_chunks(chunks, *, max_bytes):
    if type(max_bytes) is not int or max_bytes < 0:
        raise ValueError('nonnegative integer required')
    buffer = bytearray()
    for chunk in chunks:
        if len(buffer) + len(chunk) > max_bytes:
            raise OutputLimitError('combined output too large')
        buffer.extend(chunk)
    return buffer.decode('utf-8', errors='strict')

def test_split_character():
    raw = '台灣'.encode('utf-8')
    assert decode_chunks([raw[:1], raw[1:]], max_bytes=6) == '台灣'
    try:
        decode_chunks([raw], max_bytes=5)
    except OutputLimitError:
        pass
    else:
        raise AssertionError('limit not enforced')

if __name__ == '__main__':
    test_split_character()
    print('byte limit and split character verified')
