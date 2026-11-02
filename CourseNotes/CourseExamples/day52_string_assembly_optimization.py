from timeit import repeat

def before(parts):
    result = ''
    for part in parts:
        result += part
    return result

def after(parts):
    return ''.join(parts)

def test_equivalence():
    for parts in ([], [''], ['台', '灣', '\n'], ['x'] * 100):
        assert before(parts) == after(parts)

if __name__ == '__main__':
    test_equivalence()
    parts = ['sample'] * 1000
    for operation in (before, after):
        print(operation.__name__, repeat(lambda: operation(parts), number=100, repeat=3))
    print('measure, do not assume a speedup on every interpreter')
