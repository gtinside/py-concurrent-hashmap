from concurrent_collections.core import ConcurrentHashMap
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
import pyperf

map = ConcurrentHashMap()

def worker(thread_id):
    logger.info("Processing thread with {}", thread_id)
    map.put(str(thread_id), thread_id)

def run_benchmark():
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_id = {executor.submit(worker, id): id for id in range(10)}
        for future in as_completed(future_id):
            thread_id = future_id[future]
            try:
                logger.info("{}: {}", thread_id, future.result())
            except Exception as e:
                logger.error(e)
    return len(map)  # Return something measurable

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func('benchmark_concurrent_hash_map', run_benchmark)