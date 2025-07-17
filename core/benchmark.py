import time
import psutil
import numpy as np
import json
import datetime
import os
import subprocess
import tempfile
import hashlib
from multiprocessing import Pool, cpu_count


#cPU benchmark function
def _hash_job(size):
    data = os.urandom(size)
    hashlib.sha256(data).digest()

def cpu_benchmark(mode="quick"):
    rounds = 200 if mode == "quick" else 800
    data_size = 1024 * 1024  # 1MB block

    # Single-core
    start = time.time()
    for _ in range(rounds):
        _hash_job(data_size)
    single_time = time.time() - start
    single_score = round(rounds / single_time, 2)

    # Multi-core
    start = time.time()
    with Pool(cpu_count()) as pool:
        pool.map(_hash_job, [data_size] * rounds)
    multi_time = time.time() - start
    multi_score = round(rounds / multi_time, 2)

    return {
        "CPU Single-Core": single_score,
        "CPU Multi-Core": multi_score
    }

# RAM benchmark function
def ram_benchmark(mode="quick"):
    try:
        size = 1000 if mode == "quick" else 2000  # NxN matrix
        a = np.random.rand(size, size)
        b = np.random.rand(size, size)

        start = time.time()
        np.dot(a, b)
        duration = time.time() - start

        bytes_accessed = a.nbytes + b.nbytes + (size**2 * 8)
        mb_accessed = bytes_accessed / (1024**2)
        speed = round(mb_accessed / duration, 2)
        return speed

    except Exception as e:
        print(f"[RAM Benchmark Error] {e}")
        return 0

# Disk benchmark function

def disk_benchmark(mode="quick"):
    file_size_mb = 100 if mode == "quick" else 512
    block_size = 1024 * 1024
    file_path = os.path.join(tempfile.gettempdir(), "pulse_benchmark.tmp")
    data = os.urandom(block_size)

    try:
        # Write
        start = time.time()
        with open(file_path, 'wb') as f:
            for _ in range(file_size_mb):
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
        write_time = time.time() - start
        write_speed = round(file_size_mb / write_time, 2)

        # Read
        start = time.time()
        with open(file_path, 'rb') as f:
            while f.read(block_size):
                pass
        read_time = time.time() - start
        read_speed = round(file_size_mb / read_time, 2)

        return {
            "Disk Write": write_speed,
            "Disk Read": read_speed
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# Calculate final score based on benchmarks
def calculate_score(cpu_single, cpu_multi, ram, disk_read, disk_write):
    def norm(val, max_val):
        return min(val / max_val, 1.0)

    final_score = (
        0.25 * norm(cpu_single, 100) +
        0.25 * norm(cpu_multi, 500) +
        0.25 * norm(ram, 15000) +
        0.25 * norm((disk_read + disk_write) / 2, 3000)
    ) * 10

    return round(final_score, 2)

def run_benchmark(mode="quick"):
    cpu = cpu_benchmark(mode)
    ram = ram_benchmark(mode)
    disk = disk_benchmark(mode)

    return {
        "CPU Single": cpu["Single-Core Score"],
        "CPU Multi": cpu["Multi-Core Score"],
        "RAM Score": ram,
        "Disk Write": disk["Write Speed (MB/s)"],
        "Disk Read": disk["Read Speed (MB/s)"]
    }


def export_benchmark_report(results, format="json", directory="reports"):
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{directory}/pulse_benchmark_{timestamp}.{format}"

    if format == "json":
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
    elif format == "txt":
        with open(filename, 'w') as f:
            for key, value in results.items():
                f.write(f"{key}: {value}\n")
    return filename
