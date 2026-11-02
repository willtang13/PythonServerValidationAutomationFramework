from dataclasses import dataclass

@dataclass(frozen=True)
class Job:
    job_id: str
    target: str

def ordered(jobs, completed):
    by_id = dict(completed)
    return [(job.job_id, by_id[job.job_id]) for job in jobs]

def test_identity():
    jobs = [Job('a', 'lab'), Job('b', 'lab')]
    assert ordered(jobs, [('b', 2), ('a', 1)]) == [('a', 1), ('b', 2)]

if __name__ == '__main__':
    test_identity()
    print('identity is independent of completion order')
