# Concurrent Hash Map
A fast and ergonomic concurrent hash-map for read-heavy workloads.

## Implementation Details 
**Fine-grained Locking with Bucket-level Synchronization**

A simple way to achieve concurrency is by locking individual buckets instead of the entire map, ensuring that multiple threads can operate concurrently on different parts of the map.