from dataclasses import dataclass
import pytest

@dataclass(frozen=True, slots=True)
class CommandResult:
    stdout: str
    stderr: str
    exit_code: int


class AuthenticationError(Exception):
    """Raised when simulated SSH authentication fails."""

class DemoConnection:
    def __init__(
        self,
        connect_status: str,
        disk_usage: int,
        threshold: int,
        execute_time: int,
        command_timeout: int,
    ) -> None:
        self.connect_status = connect_status
        self.disk_usage = disk_usage
        self.threshold = threshold
        self.execute_time = execute_time
        self.command_timeout = command_timeout

    def connect(self) -> None:
        if self.connect_status == "OK":
            print("Connected")
        elif self.connect_status == "Fail":
            raise AuthenticationError()
        else:
            raise ValueError(f"Unknown value {self.connect_status}")
        
    def disconnect(self) -> None:
        self.connect_status = "Disconnected"
        print(self.connect_status)

    def check_disk_usage(self) -> CommandResult:
        if self.execute_time > self.command_timeout:
            raise TimeoutError
        
        print("Check Disk Usage")
        exit_code = 7 if self.disk_usage > self.threshold else 0

        return CommandResult(
            stdout=f"Disk usage = {self.disk_usage}%\n",
            stderr="",
            exit_code=exit_code,
        )
    

def execute_command(connection: DemoConnection) -> CommandResult:

    try:
        connection.connect()
        return connection.check_disk_usage()
    finally:
        connection.disconnect()
    

def test_check_disk_usage_under_80_percent():
    connection = DemoConnection(
        connect_status="OK",
        disk_usage=30,
        threshold=80,
        execute_time=5,
        command_timeout=100,
    )

    result = execute_command(connection)
    assert result.exit_code == 0
    assert connection.connect_status == "Disconnected"


def test_check_disk_usage_over_80_percent():
    connection = DemoConnection(
        connect_status="OK",
        disk_usage=90,
        threshold=80,
        execute_time=5,
        command_timeout=100,
    )

    result = execute_command(connection)
    assert result.exit_code == 7
    assert connection.connect_status == "Disconnected"


def test_check_disk_usage_connect_fail():
    connection = DemoConnection(
        connect_status="Fail",
        disk_usage=30,
        threshold=80,
        execute_time=0,
        command_timeout=100,
    )

    with pytest.raises(AuthenticationError):
        execute_command(connection)

    assert connection.connect_status == "Disconnected"


def test_check_disk_usage_command_timeout():
    connection = DemoConnection(
        connect_status="OK",
        disk_usage=30,
        threshold=80,
        execute_time=101,
        command_timeout=100,
    )

    with pytest.raises(TimeoutError):
        execute_command(connection)

    assert connection.connect_status == "Disconnected"


    
