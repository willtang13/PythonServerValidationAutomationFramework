from dataclasses import dataclass, field
from math import isfinite

INVALID_STRING = ("", " ", 0, True, list(), dict())

@dataclass(frozen=True, slots=True, kw_only=True)
class ConnectConfig:
    host: str
    username: str
    port: int = 22
    timeout: float = 10.0
    source: str
    destination: str
    passphrase: str | None = field(
        default=None,
        repr=False,
        compare=False,
    )

    def __post_init__(self):
        if not isinstance(self.host, str) \
            or not self.host.strip():
            raise ValueError("host must be nonempty")

        if not isinstance(self.username, str) \
            or not self.username.strip():
            raise ValueError("username must be nonempty")

        if type(self.port) is not int \
            or not 1 <= self.port <= 65535:
            raise ValueError("port must be 1 ~ 65535")

        if type(self.timeout) not in (int, float) \
            or not isfinite(self.timeout) \
            or self.timeout <= 0:
            raise ValueError("timeout must be finite and positive")

        if not isinstance(self.source, str) \
            or not self.source.strip():
            raise ValueError("source must be nonempty")

        if not isinstance(self.destination, str) \
            or not self.destination.strip():
            raise ValueError("destination must be nonempty")

        if (self.passphrase is not None 
            and (
                not isinstance(self.passphrase, str)
                or not self.passphrase.strip()
                )
            ):
            raise ValueError("passphrase must be nonempty")


def test_connect_config_model():
    config=ConnectConfig(
                    host="lab",
                    username="user",
                    source="source_path",
                    destination="dest_path",
                    )
    assert config.port == 22
    assert config.timeout == 10.0
    assert config.passphrase is None
    
    for valid_port in (1, 65535):
        for valid_timeout in (0.5, 10_000_000):
            config=ConnectConfig(
                host="lab",
                username="user",
                port=valid_port,
                timeout=valid_timeout,
                source="source_path",
                destination="dest_path",
                passphrase="DEMO_SECRET",
                )

            assert "DEMO_SECRET" not in repr(config)
            assert config.port == valid_port
            assert config.timeout == valid_timeout
            assert config.source == "source_path"
            assert config.destination == "dest_path"

    for invalid_string in INVALID_STRING:
        try:
            ConnectConfig(
                host=invalid_string,
                username='user',
                source="source_path",
                destination="dest_path",
                )
        
        except ValueError:
            continue

        else:
            raise AssertionError("Invalid host accepted")

    for invalid_string in INVALID_STRING:
        try:
            ConnectConfig(
                host="lab",
                username=invalid_string,
                source="source_path",
                destination="dest_path",
                )
        
        except ValueError:
            continue

        else:
            raise AssertionError("Invalid username accepted")

    for invalid_string in INVALID_STRING:
        try:
            ConnectConfig(
                host="lab",
                username="user",
                source=invalid_string,
                destination="dest_path",
                )
        
        except ValueError:
            continue

        else:
            raise AssertionError("Invalid source accepted")

    for invalid_string in INVALID_STRING:
        try:
            ConnectConfig(
                host="lab",
                username="user",
                source="source_path",
                destination=invalid_string,
                )
        
        except ValueError:
            continue

        else:
            raise AssertionError("Invalid destination accepted")

    for invalid_string in INVALID_STRING:
            try:
                ConnectConfig(
                    host="lab",
                    username="user",
                    source="source_path",
                    destination="dest_path",
                    passphrase=invalid_string,
                    )
            
            except ValueError:
                continue
    
            else:
                raise AssertionError("Invalid passphrase accepted")
        
    for invalid_port in (0, 65536, -1, float('inf'), float('nan'), True, ""):
        try:
            ConnectConfig(
                host="lab",
                username='user',
                port=invalid_port,
                source="source_path",
                destination="dest_path",
                )
        
        except ValueError:
            continue

        else:
            raise AssertionError("Invalid port accepted")

    for timeout in (0, -1, float('inf'), float('nan'), True, ""):
        try:
            ConnectConfig(
                host="lab",
                username='user',
                timeout=timeout,
                source="source_path",
                destination="dest_path",
                )
        
        except ValueError:
            continue

        else:
            raise AssertionError("Invalid timeout accepted")


@dataclass(frozen=True, slots=True, kw_only=True)
class TransferResult:
    bytes_transferred: int
    duration: float

    def __post_init__(self):
        if type(self.bytes_transferred) is not int \
            or self.bytes_transferred < 0:
            raise ValueError("bytes_transferred must be a nonnegative integer")

        if type(self.duration) not in (int, float) \
            or not isfinite(self.duration) \
            or self.duration < 0:
            raise ValueError("duration must be nonnegative")


def test_transfer_result_model():
    for valid_bytes in [0, 1, 10_000_000]:
        for valid_duration in [0, 0.1, 999.999]:
        
            result = TransferResult(bytes_transferred=valid_bytes, duration=valid_duration)
            assert result.bytes_transferred == valid_bytes
            assert result.duration == valid_duration

    for invalid_bytes in (-1, float('inf'), float('nan'), True, ""):
        try:
            TransferResult(bytes_transferred=invalid_bytes, duration=1)
        
        except ValueError:
            continue

        else:
            raise AssertionError("Invalid bytes_transferred accepted")

    for invalid_duration in (-1, float('inf'), float('nan'), True, ""):
        try:
            TransferResult(bytes_transferred=0, duration=invalid_duration)
        
        except ValueError:
            continue

        else:
            raise AssertionError("Invalid duration accepted")


if __name__ == "__main__":
    test_connect_config_model()
    test_transfer_result_model()
    print("models verified")