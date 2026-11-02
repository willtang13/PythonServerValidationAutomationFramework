from threading import Lock

class Inbox:
    def __init__(self):
        self._lock = Lock()
        self._closed = False
        self._items = []
    def submit(self, item):
        with self._lock:
            if self._closed:
                raise RuntimeError('closed')
            self._items.append(item)
    def close(self):
        with self._lock:
            self._closed = True
            items, self._items = self._items, []
            return items

def test_close():
    inbox = Inbox()
    inbox.submit('a')
    assert inbox.close() == ['a']
    assert inbox.close() == []
    try:
        inbox.submit('b')
    except RuntimeError:
        pass
    else:
        raise AssertionError('submission after close')

if __name__ == '__main__':
    test_close()
    print('atomic close transition; worker shutdown remains a separate responsibility')
