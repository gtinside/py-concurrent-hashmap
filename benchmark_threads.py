import time
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread
from concurrent_collections.core import ConcurrentHashMap

def benchmark_map(map_instance, num_threads, num_operations):
    write_latencies = []
    read_latencies = []

    def worker(thread_id, num_ops):
        local_write_latencies = []
        local_read_latencies = []
        for i in range(num_ops):
            key = f'key{thread_id}_{i}'
            
            start_time = time.perf_counter()
            map_instance.put(key, f'value{i}')
            end_time = time.perf_counter()
            local_write_latencies.append(end_time - start_time)

            start_time = time.perf_counter()
            map_instance.get(key)
            end_time = time.perf_counter()
            local_read_latencies.append(end_time - start_time)
        
        write_latencies.extend(local_write_latencies)
        read_latencies.extend(local_read_latencies)

    threads = []
    ops_per_thread = num_operations // num_threads

    start_time = time.perf_counter()
    for i in range(num_threads):
        t = Thread(target=worker, args=(i, ops_per_thread))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_write_latency = np.mean(write_latencies)
    avg_read_latency = np.mean(read_latencies)

    print(f"Threads: {num_threads}, Total time: {total_time:.6f} s, "
          f"Avg write: {avg_write_latency:.9f} s, Avg read: {avg_read_latency:.9f} s")

    return avg_write_latency, avg_read_latency, total_time

def run_benchmarks():
    thread_counts = [1, 5, 10, 15, 20, 25, 30]
    num_operations = 100000
    
    write_latencies = []
    read_latencies = []
    total_times = []

    for num_threads in thread_counts:
        map_instance = ConcurrentHashMap(capacity=500)
        write_latency, read_latency, total_time = benchmark_map(map_instance, num_threads, num_operations)
        write_latencies.append(write_latency)
        read_latencies.append(read_latency)
        total_times.append(total_time)

    return thread_counts, write_latencies, read_latencies, total_times

def plot_results(thread_counts, write_latencies, read_latencies, total_times):
    plt.figure(figsize=(12, 8))

    # Convert latencies to microseconds for better readability
    write_latencies_us = [l * 1e6 for l in write_latencies]
    read_latencies_us = [l * 1e6 for l in read_latencies]

    plt.subplot(2, 1, 1)
    plt.plot(thread_counts, write_latencies_us, 'bo-', label='Write Latency')
    plt.plot(thread_counts, read_latencies_us, 'ro-', label='Read Latency')
    plt.ylabel('Average Latency (microseconds)')
    plt.title('ConcurrentHashMap Read and Write Latencies')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(thread_counts, total_times, 'go-', label='Total Time')
    plt.xlabel('Number of Threads')
    plt.ylabel('Total Time (seconds)')
    plt.title('Total Execution Time')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    thread_counts, write_latencies, read_latencies, total_times = run_benchmarks()
    plot_results(thread_counts, write_latencies, read_latencies, total_times)