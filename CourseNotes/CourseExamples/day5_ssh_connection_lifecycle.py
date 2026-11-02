def probe(factory, *, host, user, key, known_hosts, passphrase=None):
    client = factory()
    try:
        client.load_host_keys(str(known_hosts))
        import paramiko
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(hostname=host, username=user, key_filename=str(key),
                       passphrase=passphrase, look_for_keys=False, allow_agent=False,
                       timeout=5, banner_timeout=5, auth_timeout=5)
    finally:
        client.close()

class FakeClient:
    def __init__(self):
        self.closed = False
        self.parameters = None
    def load_host_keys(self, path):
        self.known_hosts = path
    def set_missing_host_key_policy(self, policy):
        self.policy = policy
    def connect(self, **kwargs):
        self.parameters = kwargs
    def close(self):
        self.closed = True

def test_probe():
    client = FakeClient()
    probe(lambda: client, host='lab', user='student', key='fake.key', known_hosts='fake.hosts')
    assert client.closed
    assert client.parameters['allow_agent'] is False

if __name__ == '__main__':
    test_probe()
    print('fake connection verified; no network used')
