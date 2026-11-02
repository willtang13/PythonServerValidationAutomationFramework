import cProfile
import pstats
from io import StringIO

def workload():
    return sum(len(str(n)) for n in range(1000))

def profile_work():
    profiler = cProfile.Profile()
    result = profiler.runcall(workload)
    stream = StringIO()
    pstats.Stats(profiler, stream=stream).sort_stats('cumulative').print_stats(5)
    return result, stream.getvalue()

def test_profile():
    result, report = profile_work()
    assert result == workload()
    assert 'function calls' in report

if __name__ == '__main__':
    test_profile()
    print(profile_work()[1])
