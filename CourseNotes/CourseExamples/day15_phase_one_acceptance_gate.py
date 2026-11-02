REQUIRED = {'success', 'nonzero', 'authentication', 'connection',
            'timeout', 'large_output', 'cleanup'}

def missing_evidence(evidence):
    return REQUIRED - {name for name, passed in evidence.items() if passed}

def test_gate():
    evidence = {name: True for name in REQUIRED}
    evidence['cleanup'] = False
    assert missing_evidence(evidence) == {'cleanup'}
    evidence['cleanup'] = True
    assert not missing_evidence(evidence)

if __name__ == '__main__':
    test_gate()
    print('gate logic verified; this is not remote acceptance evidence')
