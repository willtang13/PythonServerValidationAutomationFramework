class Resource:
        def __init__(
            self,
            get_fail=False,
            cleanup_fail=False
        ) -> None:
            self._close_call = 0
            self._get_fail = get_fail
            self._cleanup_fail = cleanup_fail
            
        def get_result(self) -> str:
            if self._get_fail:
                raise ValueError("get result fail")
            else:
                return "OK"
        
        def close(self) -> None:
            self._close_call += 1
            if self._cleanup_fail:
                raise OSError("cleanup fail")

                


def generate_abstract(resource: Resource) -> str:

    try:
        result = resource.get_result()

    except BaseException as primary:
        try:
            resource.close()
        
        except BaseException as cleanup:
            raise BaseExceptionGroup(
                "two operations fail", [primary, cleanup]
            ) from None
        raise

    else:
        resource.close()
        return result
        


def test_generate_abstract_success() -> None:
    try:
        resource = Resource(get_fail=False, cleanup_fail=False)
        result = generate_abstract(resource)

        assert result == "OK"
        assert resource._close_call == 1

    except Exception as e:
        raise AssertionError(f"unexpected exception: {str(e)}")



def test_generate_abstract_operation_fail() -> None:
    result = None
    try:
        resource = Resource(get_fail=True, cleanup_fail=False)
        result = generate_abstract(resource)

    except ValueError as exc:
        assert str(exc) == "get result fail"
        assert resource._close_call == 1
        assert result is None
        
    else:
        raise AssertionError("unexpected exception, expect ValueError")


def test_generate_abstract_cleanup_fail() -> None:
    try:
        resource = Resource(get_fail=False, cleanup_fail=True)
        generate_abstract(resource)
        
    except OSError as exc:
        assert str(exc) == "cleanup fail"
        assert resource._close_call == 1
        
    else:
        raise AssertionError("unexpected exception, expect OSError")


def test_generate_abstract_two_operations_fail() -> None:
    try:
        resource = Resource(get_fail=True, cleanup_fail=True)
        generate_abstract(resource)
        
    except ExceptionGroup as exc:
        assert exc.message == "two operations fail"
        assert [type(e) for e in exc.exceptions] == [ValueError, OSError]
        assert resource._close_call == 1
        
    else:
        raise AssertionError("both failures must be observable")


if __name__ == "__main__":
    test_generate_abstract_success()
    test_generate_abstract_operation_fail()
    test_generate_abstract_cleanup_fail()
    test_generate_abstract_two_operations_fail()
    print("operation and cleanup failures verified")