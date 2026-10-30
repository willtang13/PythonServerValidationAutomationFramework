from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CommandResult:
    stdout: str
    stderr: str
    exit_code: int


class DemoConnection:
    def connect(self) -> None:
        print("建立連線")

    def run(self) -> CommandResult:
        print("執行指令")
        return CommandResult(
            stdout="serverlab-ubuntu\n",
            stderr="",
            exit_code=0,
        )

    def close(self) -> None:
        print("關閉連線")


def execute_command() -> CommandResult:
    connection = DemoConnection()

    try:
        connection.connect()
        return connection.run()
    finally:
        connection.close()


def main() -> None:
    result = execute_command()
    print("Caller 收到結果")
    assert result.exit_code == 0


if __name__ == "__main__":
    main()