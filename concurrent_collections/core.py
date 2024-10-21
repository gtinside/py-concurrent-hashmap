from threading import Lock

class ConcurrentHashMap:
    def __init__(self, capacity=20) -> None:
        # each bucket is a dictionary and has an associated readf write lock
        self.capacity = capacity
        self.buckets = [dict() for _ in range(capacity)]
        self.locks = [Lock() for _ in range(capacity)]
        self.elem_counter = [0]*capacity

    def put(self, key, value):
        bucket_num = self.hash(key) % self.capacity
        with self.locks[bucket_num]:
            self.buckets[bucket_num][key] = value
            self.elem_counter[bucket_num]+=1
            return value
        
    def get(self, key):
        bucket_num = self.hash(key) % self.capacity
        with self.locks[bucket_num]:
            if key in self.buckets[bucket_num]:
                return self.buckets[bucket_num]
            return None

    def contains_key(self, key) -> bool:
        bucket_num = self.hash(key) % self.capacity
        with self.locks[bucket_num]:
            if key in self.buckets[bucket_num]:
                return self.buckets[bucket_num]
            return None
    
    def remove(self, key):
        bucket_num = self.hash(key) % self.capacity
        with self.locks[bucket_num]:
            if key in self.buckets[bucket_num]:
                value = self.buckets[bucket_num].pop(key)
                self.elem_counter[bucket_num]-=1
                return value
            return None
    
    def clear(self, key):
        for bucket_num in range(len(self.buckets)):
            with self.locks[bucket_num]:
                self.buckets[bucket_num].clear()
                self.elem_counter[bucket_num] = 0
        return True
    
    def key_set(self):
        local_set = set()
        for bucket_num in range(len(self.buckets)):
            with self.locks[bucket_num]:
                local_set.update(self.buckets[bucket_num].keys())
        return local_set

    def values(self):
        local_values = list()
        for bucket_num in range(len(self.buckets)):
            with self.locks[bucket_num]:
                local_values.extend(self.buckets[bucket_num].values())
        return local_values

    def hash(self, key:str):
        return hash(key)
    
    def __len__(self):
        return sum(self.elem_counter)

