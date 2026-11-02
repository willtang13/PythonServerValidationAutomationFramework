from dataclasses import dataclass, field, asdict

@dataclass
class Config:
    host: str
    passphrase: str = field(repr=False)

def public_summary(config):
    return {'host': config.host}

def test_allowlist():
    config = Config('lab', 'FAKE_SECRET_123')
    assert 'FAKE_SECRET_123' not in repr(config)
    assert asdict(config)['passphrase'] == 'FAKE_SECRET_123'
    assert 'FAKE_SECRET_123' not in repr(public_summary(config))

if __name__ == '__main__':
    test_allowlist()
    print('repr protection alone is not serialization protection')
