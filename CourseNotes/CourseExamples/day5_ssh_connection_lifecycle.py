"""Day 5 teaching sample: run with Python or pytest; no network is used.

The factory transfers ownership of its returned client to this call.
Success returns None; errors propagate after cleanup. Cleanup errors are
not handled separately in this lesson.
"""

from collections.abc import Callable
from pathlib import Path
from typing import Protocol

import paramiko


class ConnectionClient(Protocol):
    """The operations needed by this connection probe."""

    def load_host_keys(self, filename: str) -> None: ...

    def set_missing_host_key_policy(
        self, policy: paramiko.MissingHostKeyPolicy
    ) -> None: ...

    def connect(
        self,
        *,
        hostname: str,
        username: str,
        key_filename: str,
        passphrase: str | None,
        look_for_keys: bool,
        allow_agent: bool,
        timeout: float,
        banner_timeout: float,
        auth_timeout: float,
    ) -> None: ...

    def close(self) -> None: ...


def probe_ssh_connection(
    client_factory: Callable[[], ConnectionClient],
    *,
    host: str,
    user: str,
    key: Path,
    known_hosts: Path,
    passphrase: str | None = None,
) -> None:
    client = client_factory()
    try:
        client.load_host_keys(str(known_hosts))
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(
            hostname=host,
            username=user,
            key_filename=str(key),
            passphrase=passphrase,
            look_for_keys=False,
            allow_agent=False,
            timeout=5,
            banner_timeout=5,
            auth_timeout=5,
        )
    finally:
        client.close()


class FakeClient:
    def __init__(self) -> None:
        self.known_hosts: str | None = None
        self.policy: paramiko.MissingHostKeyPolicy | None = None
        self.parameters: dict[str, object] = {}
        self.close_calls = 0

    def load_host_keys(self, filename: str) -> None:
        self.known_hosts = filename

    def set_missing_host_key_policy(
        self, policy: paramiko.MissingHostKeyPolicy
    ) -> None:
        self.policy = policy

    def connect(self, **kwargs: object) -> None:
        self.parameters = kwargs

    def close(self) -> None:
        self.close_calls += 1


class FailingConnectClient(FakeClient):
    def connect(self, **kwargs: object) -> None:
        self.parameters = kwargs
        raise RuntimeError("connection failed")


def test_probe_ssh_connection_success() -> None:
    client = FakeClient()
    result = probe_ssh_connection(
        lambda: client,
        host="lab",
        user="student",
        key=Path("fake.key"),
        known_hosts=Path("fake.hosts"),
    )
    assert result is None
    assert client.known_hosts == "fake.hosts"
    assert isinstance(client.policy, paramiko.RejectPolicy)
    assert client.parameters == {
        "hostname": "lab",
        "username": "student",
        "key_filename": "fake.key",
        "passphrase": None,
        "look_for_keys": False,
        "allow_agent": False,
        "timeout": 5,
        "banner_timeout": 5,
        "auth_timeout": 5,
    }
    assert client.close_calls == 1


def test_probe_ssh_connection_failure() -> None:
    client = FailingConnectClient()
    try:
        probe_ssh_connection(
            lambda: client,
            host="lab",
            user="student",
            key=Path("fake.key"),
            known_hosts=Path("fake.hosts"),
        )
    except RuntimeError as exc:
        assert str(exc) == "connection failed"
    else:
        raise AssertionError("Expected RuntimeError, but connection succeeded")
    assert client.close_calls == 1


if __name__ == "__main__":
    test_probe_ssh_connection_success()
    test_probe_ssh_connection_failure()
    print("success and failure paths verified; no network used")
