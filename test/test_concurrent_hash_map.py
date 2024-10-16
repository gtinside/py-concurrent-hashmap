from concurrent_collections.core import ConcurrentHashMap
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger

map = ConcurrentHashMap()

def worker(thread_id):
    logger.info("Processing thread with {}", thread_id)
    map.put(thread_id, thread_id)



with ThreadPoolExecutor(max_workers=10) as executor:
    future_id = {executor.submit(worker, id): id for id in range(10)}
    for future in as_completed(future_id):
        thread_id = future_id[future]
        try:
            logger.info("{}: {}", thread_id, future.result())
        except Exception as e:
            logger.error("Some error")


    
