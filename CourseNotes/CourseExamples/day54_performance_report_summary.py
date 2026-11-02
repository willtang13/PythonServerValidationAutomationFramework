from statistics import median

def summarize(before, after):
    if not before or not after or min(before + after) <= 0:
        raise ValueError('positive measured samples required')
    old, new = median(before), median(after)
    return {'baseline_median': old, 'candidate_median': new,
            'reduction_percent': (old - new) / old * 100}

def test_calculation():
    report = summarize([10, 12, 11], [5, 6, 5.5])
    assert report['reduction_percent'] == 50

if __name__ == '__main__':
    test_calculation()
    print('synthetic arithmetic test only; use actual samples for project claims')
