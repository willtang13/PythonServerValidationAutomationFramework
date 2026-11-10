class ConfigReadError(Exception):
    pass


def read_config(loader) -> str:

    try:
        return loader()
    
    except OSError as exc:
        raise ConfigReadError("fail to load configuration") from exc


def test_read_config_success() -> None:

    def fake_loader_success() -> str:
        return "host=lab01\n"
    
    result = read_config(fake_loader_success)
    assert result == "host=lab01\n"


def test_read_config_file_not_found() -> None:
    original_error = FileNotFoundError("fake_file.ini")
    def fake_loader_fail() -> str:
        raise original_error

    try:
        read_config(fake_loader_fail)

    except ConfigReadError as exc:
        assert exc.__cause__ is original_error

    else:
        raise AssertionError("assert raise FileNotFoundError failed")


def test_read_config_permissin_denied() -> None:
    fake_secret = "fake_secret_passphrase_should_not_show"
    original_error = PermissionError(
        f"denied_file.ini, "
        f"passphrase={fake_secret}"
    )
    def fake_loader_fail() -> str:
        raise original_error

    try:
        read_config(fake_loader_fail)

    except ConfigReadError as exc:
        assert exc.__cause__ is original_error
        assert fake_secret not in str(exc)
        # print(f"exc ={exc.__cause__}")
        # print(f"check causeexc info= {str(exc)}")

    else:
        raise AssertionError("assert raise PermissionError failed")


def test_read_config_type_error() -> None:
    original_error = TypeError("unknown type")
    def fake_loader_fail() -> str:
        raise original_error

    try:
        read_config(fake_loader_fail)

    except TypeError as exc:
        assert exc is original_error

    else:
        # print(f"xxx = {Exception}")
        raise AssertionError("assert raise PermissionError failed")
    

if __name__ == "__main__":

    test_read_config_success()
    test_read_config_file_not_found()
    test_read_config_permissin_denied()
    test_read_config_type_error()

    print("read config verified")