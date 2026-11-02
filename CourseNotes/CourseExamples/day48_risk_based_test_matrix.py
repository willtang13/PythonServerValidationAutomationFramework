def uncovered(requirements, evidence):
    return {name for name in requirements if not evidence.get(name)}

def test_risk_matrix():
    requirements = {'cleanup': 'high', 'timeout': 'high', 'format': 'low'}
    evidence = {'format': ['test_format'], 'timeout': ['test_deadline']}
    assert uncovered(requirements, evidence) == {'cleanup'}

if __name__ == '__main__':
    test_risk_matrix()
    print('matrix demo; real evidence must refer to tests that can detect the defect')
