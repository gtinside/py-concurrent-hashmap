import pyperf
from concurrent.futures import ThreadPoolExecutor
from concurrent_collections.core import ConcurrentHashMap

def worker(thread_id, map):
    map.put(str(thread_id), thread_id)

def run_benchmark(num_threads):
    map = ConcurrentHashMap()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(worker, range(num_threads), [map]*num_threads)
    return len(map)

def main(runner):
    runner.bench_func('concurrent_hashmap_threads-1', run_benchmark, 100)
    runner.bench_func('concurrent_hashmap_threads-2', run_benchmark, 500)
    runner.bench_func('concurrent_hashmap_threads-3', run_benchmark, 1000)

if __name__ == '__main__':
    runner = pyperf.Runner()
    main(runner)

