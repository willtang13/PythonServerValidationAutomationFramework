import gc
import tracemalloc

def observe():
    currents = []
    tracemalloc.start()
    try:
        for _ in range(5):
            data = [bytearray(128) for _ in range(200)]
            assert len(data) == 200
            del data
            gc.collect()
            current, peak = tracemalloc.get_traced_memory()
            currents.append(current)
        return currents, peak
    finally:
        tracemalloc.stop()

def test_finite_probe():
    currents, peak = observe()
    assert len(currents) == 5 and peak >= max(currents)

if __name__ == '__main__':
    test_finite_probe()
    print(observe())
