import time
from threading import Thread
import matplotlib.pyplot as plt
import numpy as np
from concurrent_collections.core import ConcurrentHashMap

# Assuming ConcurrentHashMap is imported

def benchmark_map(map_instance, num_threads, num_operations):
    """Benchmark throughput and latency for the concurrent map."""
    latencies = []
    throughput = 0

    def worker(start, end):
        nonlocal throughput
        for i in range(start, end):
            start_time = time.time()
            map_instance.put(f'key{i}', f'value{i}')
            end_time = time.time()

            # Record latency for each operation
            latencies.append(end_time - start_time)
            throughput += 1

    # Create and start threads
    threads = []
    operations_per_thread = num_operations // num_threads
    for i in range(num_threads):
        t = Thread(target=worker, args=(i * operations_per_thread, (i + 1) * operations_per_thread))
        threads.append(t)

    start_benchmark = time.time()

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    end_benchmark = time.time()

    # Calculate average latency and total throughput
    avg_latency = np.mean(latencies)
    total_throughput = throughput / (end_benchmark - start_benchmark)

    return avg_latency, total_throughput


def run_benchmark():
    thread_counts = [1, 2, 4, 8, 16, 32]
    num_operations = 10000

    latencies = []
    throughputs = []

    for num_threads in thread_counts:
        print(f"Running benchmark with {num_threads} threads...")
        map_instance = ConcurrentHashMap(capacity=500)
        avg_latency, total_throughput = benchmark_map(map_instance, num_threads, num_operations)
        latencies.append(avg_latency)
        throughputs.append(total_throughput)

    # Plot the results
    plot_results(thread_counts, latencies, throughputs)


def plot_results(thread_counts, latencies, throughputs):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Number of Threads')
    ax1.set_ylabel('Average Latency (seconds)', color=color)
    ax1.plot(thread_counts, latencies, color=color, marker='o', label='Latency')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second y-axis
    color = 'tab:blue'
    ax2.set_ylabel('Throughput (operations/sec)', color=color)  # we already handled the x-label with ax1
    ax2.plot(thread_counts, throughputs, color=color, marker='o', label='Throughput')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # to adjust layout to prevent overlap
    plt.title("Concurrent HashMap Benchmark")
    plt.show()


if __name__ == "__main__":
    run_benchmark()
