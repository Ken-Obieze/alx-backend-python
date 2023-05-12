#!/usr/bin/env python3
"""Module to measure runtime."""
import asyncio
import time
from typing import List


wait_n = __import__('1-concurrent_coroutines').wait_n

def measure_time(n: int, max_delay: int) -> float:
    """Measure total time for coroutine execution."""
    start_time = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end_time = time.perf_counter()
    total_time = end_time - start_time
    return (total_time / n)
