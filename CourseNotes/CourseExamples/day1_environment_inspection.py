import sys
from importlib.metadata import version

def describe():
    return {'python': sys.version.split()[0], 'executable': sys.executable,
            'pytest': version('pytest'), 'paramiko': version('paramiko')}

def test_environment():
    data = describe()
    assert data['executable']
    assert data['pytest']

if __name__ == '__main__':
    test_environment()
    print(describe())
