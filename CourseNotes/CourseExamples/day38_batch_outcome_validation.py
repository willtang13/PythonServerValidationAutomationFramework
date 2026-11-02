TERMINAL = {'completed', 'failed', 'cancelled', 'unknown'}

def validate_outcomes(submitted, outcomes):
    if len(submitted) != len(set(submitted)):
        raise ValueError('duplicate job id')
    if set(submitted) != set(outcomes):
        raise ValueError('lost or unexpected result')
    if any(state not in TERMINAL for state in outcomes.values()):
        raise ValueError('nonterminal result')

def test_completeness():
    validate_outcomes(['a', 'b'], {'a': 'completed', 'b': 'cancelled'})
    try:
        validate_outcomes(['a'], {})
    except ValueError:
        pass
    else:
        raise AssertionError('lost work not detected')

if __name__ == '__main__':
    test_completeness()
    print('outcome completeness verified')
