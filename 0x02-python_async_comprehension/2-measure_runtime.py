#!/usr/bin/env python3
"""measure_runtime coroutine module."""
import random
import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """Measure runtime of coroutine.""" 
    start_time = time.time()
    await asyncio.gather(async_comprehension(), async_comprehension(), async_comprehension(), async_comprehension())
    end_time = time.time()
    return (end_time - start_time)
