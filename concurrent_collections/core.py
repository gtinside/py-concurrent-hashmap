import hashlib
import loguru
from threading import RLock

class ConcurrentHashMap:
    def __init__(self, capacity=20) -> None:
        # each bucket is a dictionary and has an associated lock
        self.capacity = capacity
        self.buckets = [dict() for _ in range(capacity)]
        self.locks = [RLock() for _ in range(capacity)]

    def put(self, key, value):
        bucket_num = self.hash(key) % self.capacity
        with self.locks[bucket_num]:
            self.buckets[bucket_num][key] = value
            return value
        
    def get(self, key):
        bucket_num = self.hash(key) % self.capacity
        with self.locks[bucket_num]:
            return self.buckets[bucket_num][key]

    def containsKey(self, key) -> bool:
        bucket_num = self.hash(key) % self.capacity
        return key in self.buckets[bucket_num]

    def hash(self, key:str):
        """ Function to generate an md5 hash
        
        Parameters:
        key (str): Key that needs to be hashed

        Returns:
        str: Hex digest
        
        """
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), base=16)
    
    def __len__(self):
        return sum(len(bucket.keys()) for bucket in self.buckets)

