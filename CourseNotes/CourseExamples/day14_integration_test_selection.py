def should_skip_integration(*, marked, enabled):
    return marked and not enabled

def test_selection():
    assert should_skip_integration(marked=True, enabled=False)
    assert not should_skip_integration(marked=True, enabled=True)
    assert not should_skip_integration(marked=False, enabled=False)

if __name__ == '__main__':
    test_selection()
    print('selection policy verified; see course for pytest hooks')
