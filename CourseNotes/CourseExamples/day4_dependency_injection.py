class VersionService:
    def __init__(self, client_factory):
        self._factory = client_factory

    def read(self):
        client = self._factory()
        try:
            return client.read_version()
        finally:
            client.close()

class FakeClient:
    closed = False
    def read_version(self):
        return '1.0'
    def close(self):
        self.closed = True

def test_injection():
    client = FakeClient()
    service = VersionService(lambda: client)
    assert not client.closed
    assert service.read() == '1.0'
    assert client.closed

if __name__ == '__main__':
    test_injection()
    print('injection verified')
