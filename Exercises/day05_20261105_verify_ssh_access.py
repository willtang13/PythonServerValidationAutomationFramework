from collections.abc import Callable
from pathlib import Path
from typing import Protocol

import paramiko


class ConnectClient(Protocol):
    """描述連線驗證需要的 Client 介面，不提供網路實作。"""

    def load_host_keys(self, filename:str) -> None: ...

    def set_missing_host_key_policy(
            self, 
            policy: paramiko.MissingHostKeyPolicy,
    ) -> None: ...

    def connect(
            self,
            *,
            hostname: str,
            username: str,
            key_filename: str,
            port: int,
            passphrase: str | None,
            look_for_keys: bool,
            allow_agent: bool,
            timeout: float,
            banner_timeout: float,
            auth_timeout: float,
    ) -> None: ...

    def close(self) -> None: ...


def verify_ssh_access(
        client_factory: Callable[[], ConnectClient],
        *,
        host: str,
        user: str,
        port: int,
        passphrase: str | None = None,
        key: Path,
        known_hosts: Path,
) -> None:
    """以指定帳號與私鑰驗證 SSH 存取權限，不執行遠端指令。

    Args:
        client_factory: 無參數工廠，每次提供可用的 Client，並將其
            關閉責任交給本次呼叫；不得提供仍由其他工作使用的 Client。
        host: 目標主機名稱或 IP 位址。
        user: 遠端登入帳號。
        port: 遠端 SSH 服務連接埠。
        passphrase: 解開加密私鑰的密語；不需要時省略或傳入 None。
            本函式不互動詢問密語。
        key: 使用者私鑰路徑。
        known_hosts: 已信任主機公鑰檔案的路徑。

    正常完成時回傳 None。使用指定信任資料與 RejectPolicy，
    不自動信任未知主機，也不搜尋其他私鑰或使用 SSH agent。
    三個等待設定各為五秒，不代表整體連線的總期限。

    工廠失敗時直接傳出例外，不呼叫 close；工廠內部的部分資源
    由工廠清理。取得 Client 後，成功或失敗都嘗試 close 恰好一次。
    close 正常完成時，原本的工作例外直接傳給 Caller。
    本課假設 close 正常完成；若它也失敗，傳出的是清理例外，
    原先的工作例外保留在例外脈絡中，尚未制定額外處理政策。

    不預先驗證參數或檔案內容；真實連線行為取決於注入的 Client。
    """

    client = client_factory()

    try:
        client.load_host_keys(str(known_hosts))
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(
            hostname=host,
            username=user,
            port=port,
            passphrase=passphrase,
            key_filename=str(key),
            look_for_keys=False,
            allow_agent=False,
            timeout=5,
            banner_timeout=5,
            auth_timeout=5,
        )

    finally:
        client.close()


class FakeClient:
    """只記錄呼叫資料與關閉次數，不讀取檔案或建立網路連線。"""

    def __init__(self) -> None:
        self.parameters: dict[str,object] = {}
        self.close_calls: int = 0
        self.known_hosts: str | None = None
        self.policy: paramiko.MissingHostKeyPolicy | None = None

    def load_host_keys(self, filename: str) -> None:
            self.known_hosts = filename

    def set_missing_host_key_policy(
            self, 
            policy: paramiko.MissingHostKeyPolicy
    ) -> None:
        self.policy = policy

    def connect(
        self,
        **kwargs: object,      
    ) -> None:
        self.parameters = kwargs

    def close(self) -> None:
        self.close_calls += 1


class FakeClientConnectFail(FakeClient):
    def connect(
        self,
        **kwargs: object,      
    ) -> None:
        self.parameters = kwargs
        raise RuntimeError("Connect fail")


class FakeClientLoadHostKeyFail(FakeClient):
    def load_host_keys(self, filename: str) -> None:
        raise ValueError("Load host key fail")


class FakeClientCreateFail(FakeClient):
    """模擬工廠建立失敗，以類別計數器觀察 close 是否被呼叫。"""

    close_calls = 0

    def __init__(self) -> None:
        raise TypeError("Creates client fail")

    def close(self) -> None:
        FakeClientCreateFail.close_calls += 1


    
def test_ssh_access_success() -> None:
    client = FakeClient()

    result = verify_ssh_access(
        lambda: client,
        host="lab",
        user="me",
        port=22,
        passphrase="SECRET",
        key=Path("private.key"),
        known_hosts=Path("fake.hosts"),
    )

    assert result is None
    assert isinstance(client.policy, paramiko.RejectPolicy)
    assert client.known_hosts == "fake.hosts"
    assert client.close_calls == 1
    assert client.parameters == {
        "hostname": "lab",
        "username": "me",
        "port": 22,
        "passphrase": "SECRET",
        "key_filename": "private.key",
        "look_for_keys": False,
        "allow_agent": False,
        "timeout": 5,
        "banner_timeout": 5,
        "auth_timeout": 5,
    }


def test_ssh_access_connect_fail() -> None:
    client = FakeClientConnectFail()

    try:
        verify_ssh_access(
            lambda: client,
            host="lab",
            user="me",
            port=22,
            passphrase="SECRET",
            key=Path("private.key"),
            known_hosts=Path("fake.hosts"),
        )

    except RuntimeError as exc:
        assert str(exc) == "Connect fail"

    else:
        raise AssertionError("Expected RuntimeError, but connection succeeded")
    
    assert isinstance(client.policy, paramiko.RejectPolicy)
    assert client.close_calls == 1
    assert client.parameters == {
        "hostname": "lab",
        "username": "me",
        "port": 22,
        "passphrase": "SECRET",
        "key_filename": "private.key",
        "look_for_keys": False,
        "allow_agent": False,
        "timeout": 5,
        "banner_timeout": 5,
        "auth_timeout": 5,
    }


def test_ssh_access_load_host_key_fail() -> None:
    client = FakeClientLoadHostKeyFail()

    try:
        verify_ssh_access(
            lambda: client,
            host="lab",
            user="me",
            port=22,
            passphrase="SECRET",
            key=Path("private.key"),
            known_hosts=Path("fake.hosts"),
        )

    except ValueError as exc:
        assert str(exc) == "Load host key fail"

    else:
        raise AssertionError("Expected ValueError, but host key loaded")
    
    assert client.policy is None
    assert client.parameters == {}
    assert client.close_calls == 1


def test_ssh_access_factory_fail() -> None:
    FakeClientCreateFail.close_calls = 0

    try:
        verify_ssh_access(
            lambda: FakeClientCreateFail(),
            host="lab",
            user="me",
            port=22,
            passphrase="SECRET",
            key=Path("private.key"),
            known_hosts=Path("fake.hosts"),
        )

    except TypeError as exc:
        assert str(exc) == "Creates client fail"

    else:
        raise AssertionError("Expected TypeError, but client created")

    assert FakeClientCreateFail.close_calls == 0



if __name__ == "__main__":
    test_ssh_access_success()
    test_ssh_access_connect_fail()
    test_ssh_access_load_host_key_fail()
    test_ssh_access_factory_fail()
    print("SSH access verification: PASS")

