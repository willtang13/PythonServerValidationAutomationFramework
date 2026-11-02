from dataclasses import dataclass

@dataclass(frozen=True)
class Delivery:
    execution: str
    storage: str

def persist_result(result, save):
    try:
        save(result)
    except OSError:
        return Delivery('completed', 'failed')
    return Delivery('completed', 'stored')

def test_storage_failure():
    calls = []
    def save(result):
        calls.append(result)
        raise OSError('disk unavailable')
    assert persist_result(7, save) == Delivery('completed', 'failed')
    assert calls == [7]

if __name__ == '__main__':
    test_storage_failure()
    print('storage failure does not rerun the remote command')
