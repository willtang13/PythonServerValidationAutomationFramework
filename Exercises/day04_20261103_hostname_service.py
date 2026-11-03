import pytest

work_calls = {
    "create": 0,
    "read": 0,
    "close": 0,
}

class FakeClient:
    def __init__(
            self,
            is_read_success=True, 
            is_create_success=True,
            ) -> None:

        work_calls["create"] += 1
        if not is_create_success:
            raise TypeError("Fail to factory client")
        
        self._is_closed = False
        self._is_read_success = is_read_success

    def read_hostname(self) -> str:
        work_calls["read"] += 1
        if self._is_read_success:
            return "my_host"
        else:
            raise ValueError("Fail to read hostname")

    def close(self) -> None:
        work_calls["close"] += 1
        self._is_closed = True


class HostnameService:
    def __init__(self, client_factory) -> None:
        self._client_factory = client_factory

    def read(self) -> str:
        client = self._client_factory()

        try:
            return client.read_hostname()

        finally:
            client.close()


def test_read_service_hostname_success() -> None:
    client = FakeClient()
    service = HostnameService(lambda: client)
    assert not client._is_closed
    assert service.read() == "my_host"
    assert client._is_closed

def test_read_service_hostname_fail() -> None:
    client = FakeClient(is_read_success=False)
    service = HostnameService(lambda: client)
    assert not client._is_closed
    with pytest.raises(ValueError, match="Fail to read hostname"):
         service.read()
    assert client._is_closed

def test_factory_client_fail() -> None:
    service = HostnameService(
        lambda: FakeClient(is_create_success=False)
        )
    with pytest.raises(TypeError, match="Fail to factory client"):
        service.read()


if __name__ == "__main__":
    test_read_service_hostname_success()
    test_read_service_hostname_fail()
    test_factory_client_fail()

    print(work_calls)
