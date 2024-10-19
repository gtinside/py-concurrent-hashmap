# Concurrent Hash Map

## Overview

The `ConcurrentHashMap` is a thread-safe implementation of a hash map in Python. It allows multiple threads to perform read and write operations on different buckets concurrently, ensuring efficient handling of data while avoiding race conditions. This project utilizes a fine-grained locking mechanism, where each bucket has its own lock, allowing for parallelism in operations.

## Features

- **Thread Safety**: Ensures safe concurrent access with the use of locks.
- **Scalable**: Uses fine-grained locks, meaning that only the bucket corresponding to a key is locked during operations, allowing for parallelism.
- **Basic Operations**: Supports typical hash map operations such as `put`, `get`, `contains_key`, `remove`, and checking the size with `__len__`.

## Usage

### Initialization
You can initialize the `ConcurrentHashMap` with a specific capacity (number of buckets). If no capacity is provided, the default value is 20.

```python
from concurrent_hash_map import ConcurrentHashMap

# Initialize the map with default capacity
concurrent_map = ConcurrentHashMap()

# Or initialize with a custom capacity
concurrent_map = ConcurrentHashMap(capacity=50) 
```

### Installation
To use this project, simply clone the repository:

```bash
git clone https://github.com/yourusername/concurrent-hash-map.git
cd concurrent-hash-map
```