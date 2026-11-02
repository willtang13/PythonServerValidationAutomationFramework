COMMANDS = [
    'python -m pip install -e .',
    'python -m pip install pytest',
    'python -m pytest -m "not integration" -q',
]

def test_ci_contract():
    text = '\n'.join(COMMANDS)
    assert 'not integration' in text
    assert 'passphrase' not in text

if __name__ == '__main__':
    test_ci_contract()
    print('Service-neutral steps, not a deployed CI workflow:')
    print('\n'.join(COMMANDS))
