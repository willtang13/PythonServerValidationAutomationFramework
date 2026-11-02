from dataclasses import dataclass

@dataclass(frozen=True)
class Failure:
    temporary: bool
    request_sent: bool
    authentication: bool = False

def retry_allowed(failure, *, idempotent=False):
    return (failure.temporary and not failure.authentication
            and (not failure.request_sent or idempotent))

def test_decision():
    assert retry_allowed(Failure(True, False))
    assert not retry_allowed(Failure(True, True))
    assert not retry_allowed(Failure(True, False, True))
    assert retry_allowed(Failure(True, True), idempotent=True)

if __name__ == '__main__':
    test_decision()
    print('retry requires a safety decision, not just an error name')
