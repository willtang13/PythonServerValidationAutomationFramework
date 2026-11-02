from io import StringIO

def main(run, out, err):
    try:
        remote_code = run()
    except OSError:
        print('executor unavailable', file=err)
        return 2
    print(f'remote_exit_code={remote_code}', file=out)
    return 0 if remote_code == 0 else 1

def test_status():
    out, err = StringIO(), StringIO()
    assert main(lambda: 7, out, err) == 1
    assert '7' in out.getvalue() and err.getvalue() == ''
    def fail():
        raise OSError('internal detail')
    assert main(fail, out, err) == 2

if __name__ == '__main__':
    test_status()
    print('tool and remote statuses are distinct')
