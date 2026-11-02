def use_resource(resource, action):
    try:
        result = action(resource)
    except BaseException as primary:
        try:
            resource.close()
        except BaseException as cleanup:
            raise BaseExceptionGroup('operation and cleanup failed', [primary, cleanup]) from None
        raise
    else:
        resource.close()
        return result

def test_double_failure():
    class Resource:
        def close(self):
            raise OSError('close failed')
    def action(resource):
        raise ValueError('operation failed')
    try:
        use_resource(Resource(), action)
    except ExceptionGroup as exc:
        assert [type(e) for e in exc.exceptions] == [ValueError, OSError]
    else:
        raise AssertionError('both failures must be observable')

if __name__ == '__main__':
    test_double_failure()
    print('double failure retained, including an explicit interruption cleanup policy')
