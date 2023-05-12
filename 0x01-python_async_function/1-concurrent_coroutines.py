#!/usr/bin/env python3
"""Module for concorent coroutines."""
import asyncio
from typing import List


wait_random = __import__('0-basic_async_syntax').wait_random

async def wait_n(n: int, max_delay: int) -> List[float]:
    """Spawn wait_randon, n times."""
    delays = []
    tasks = []
    for i in range(n):
        task = asyncio.create_task(wait_random(max_delay))
        tasks.append(task)
    for task in tasks:
        delay = await task
        delays.append(delay)
    delays.sort()
    return delays
