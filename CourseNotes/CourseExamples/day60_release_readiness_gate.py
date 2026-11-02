REQUIRED = {'install', 'unit', 'integration', 'timeout', 'cancel',
            'storage', 'export', 'documentation'}

def release_ready(evidence):
    # Values must be actual reviewed results, not assumptions.
    return all(evidence.get(name) is True for name in REQUIRED)

def test_release_gate():
    evidence = dict.fromkeys(REQUIRED, True)
    evidence['integration'] = None
    assert not release_ready(evidence)
    evidence['integration'] = True
    assert release_ready(evidence)

if __name__ == '__main__':
    test_release_gate()
    print('release gate simulation only; no publication performed')
