from dataclasses import dataclass
from io import BytesIO
from time import monotonic


@dataclass(frozen=True)
class Result:
    """保存原始輸出、遠端結束代碼與本次執行耗時（秒）。"""
    stdout: str
    stderr: str
    exit_code: int
    duration: float


class Output(BytesIO):
    """以記憶體串流模擬小量輸出；子類別必須提供結束代碼。"""

    @property
    def channel(self):
        """回傳自己作為假通道，供 Executor 取得結束代碼。"""
        return self
    
    def recv_exit_status(self) -> int:
        """要求子類別覆寫；基底類別直接呼叫會明確失敗。"""
        raise NotImplementedError("子類別必須提供結束代碼")


class OutputSuccess(Output):
    """模擬指令正常完成且結束代碼為零的輸出。"""
    def recv_exit_status(self) -> int:
        return 0


class OutputFail(Output):
    """模擬指令正常完成但結束代碼為一的輸出。"""
    def recv_exit_status(self) -> int:
        return 1


class FakeClient:
    """提供預先安排的三個串流，不建立網路連線。

    僅接受 uname -s；close_call 記錄關閉次數。
    close 只記錄呼叫，不模擬真實連線與串流的資源釋放。
    """
    def __init__(
        self, 
        input:BytesIO,
        out: Output,
        err: Output
    ) -> None:
        """保存 Caller 提供的輸入、標準輸出與標準錯誤串流。"""
        self.stdin = input
        self.stdout = out
        self.stderr = err
        self.close_call = 0

    def exec_command(self, command, **kwargs) -> tuple:
        """檢查指令並回傳預設串流；其餘參數僅接收、不驗證。"""
        assert command == "uname -s"

        return (
            self.stdin,
            self.stdout,
            self.stderr
        )

    def close(self) -> None:
        """記錄一次關閉呼叫，供測試驗證 Caller 的清理流程。"""
        self.close_call += 1


class FakeClientRuntimeError(FakeClient):
    """模擬送出指令時發生例外的 Client。"""

    def exec_command(self, command, **kwargs) -> None:
        """直接拋出執行例外，不回傳串流。"""
        raise RuntimeError("execution failed")


def execute_uname_check(client: FakeClient, command: str) -> Result:
    """透過已連線的 Client 同步執行小輸出指令並回報事實。

    Args:
        client: 提供 exec_command 的 Client；由 Caller 擁有並負責關閉。
        command: 要送往遠端的指令；本函式不判斷 Linux 或測試預期。

    Returns:
        保留原始換行的 UTF-8 解碼輸出、結束代碼與耗時。
        耗時包含送出指令、讀取輸出與取得結束代碼，不含建立連線。
        非零結束代碼仍正常回傳 Result。

    Raises:
        Exception: 執行、串流操作或解碼的例外未經轉換直接傳出。

    本函式關閉 stdin，但不關閉 Client。僅適用本課小輸出情境；
    依序讀取兩個串流，未處理大量輸出、輸出上限或整體期限。
    timeout=2 不代表整個函式保證在兩秒內完成。
    """
    start = monotonic()

    stdin, stdout, stderr = client.exec_command(command, timeout=2)

    stdin.close()
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    exit_code = stdout.channel.recv_exit_status()
    duration = monotonic() - start

    return Result(
        out,
        err,
        exit_code,
        duration
    )
    

def test_uname_check_success() -> None:
    """驗證成功結果的四個欄位、原始換行及 Caller 關閉一次。"""
    client = FakeClient(
        input=BytesIO(),
        out=OutputSuccess(b'Linux\n'),
        err=OutputSuccess(b'')
    )
    try:
        result = execute_uname_check(client, "uname -s")

    finally:
        client.close()

    assert result.exit_code == 0
    assert result.stdout == "Linux\n"
    assert result.stderr == ""
    assert result.duration >= 0
    assert client.close_call == 1


def test_uname_check_permission_denied() -> None:
    """驗證非零代碼仍回傳原始結果，且 Caller 關閉一次。"""
    client = FakeClient(
        input=BytesIO(),
        out=OutputFail(b''),
        err=OutputFail(b'permission denied\n')
    )

    try:
        result = execute_uname_check(client, "uname -s")
    
    finally:
        client.close()

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == "permission denied\n"
    assert result.duration >= 0
    assert client.close_call == 1


def test_uname_check_runtime_error() -> None:
    """驗證執行例外的型別與訊息，以及 finally 仍關閉一次。"""
    client = FakeClientRuntimeError(
        input=BytesIO(),
        out=Output(),
        err=Output()
    )

    try:
        execute_uname_check(client, "uname -s")


    except RuntimeError as exc:
        assert str(exc) == "execution failed"

    else:
        raise AssertionError("Expected RuntimeError, but execute succeeded")

    finally:
        client.close()

    assert client.close_call == 1


if __name__ == "__main__":
    test_uname_check_success()
    test_uname_check_permission_denied()
    test_uname_check_runtime_error()
    print("uname check verified")


    

