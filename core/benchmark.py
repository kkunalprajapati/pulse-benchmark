import time
import psutil

def cpu_benchmark(duration=3):
    start = time.time()
    count = 0
    while time.time() - start < duration:
        for i in range(1, 1000):
            _ = is_prime(i)
        count += 1
    return count

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def ram_benchmark():
    try:
        size = 100 * 1024 * 1024  # 100 MB
        start = time.time()
        block = bytearray(size)
        for i in range(0, size, 1024):
            block[i] = 1
        end = time.time()
        return round(1 / (end - start), 2)
    except Exception:
        return 0

def calculate_score(cpu_score, ram_score):
    norm_cpu = min(cpu_score / 150, 1.0)
    norm_ram = min(ram_score / 500, 1.0)
    return round((norm_cpu * 0.6 + norm_ram * 0.4) * 10, 1)

def run_benchmark():
    cpu = cpu_benchmark()
    ram = ram_benchmark()
    score = calculate_score(cpu, ram)
    return {
        "CPU Score": cpu,
        "RAM Score": ram,
        "Final Score": score
    }
