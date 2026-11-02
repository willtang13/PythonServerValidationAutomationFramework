from concurrent.futures import ThreadPoolExecutor

class Resource:
    def __init__(self, job_id):
        self.job_id, self.closed = job_id, False
    def close(self):
        self.closed = True

def work(job_id, factory):
    resource = factory(job_id)
    try:
        return resource, job_id * 2
    finally:
        resource.close()

def test_ownership():
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda n: work(n, Resource), range(4)))
    resources = [row[0] for row in results]
    assert len({id(r) for r in resources}) == 4
    assert all(r.closed for r in resources)

if __name__ == '__main__':
    test_ownership()
    print('one owned resource per job')
