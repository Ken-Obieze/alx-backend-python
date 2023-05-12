#!/usr/bin/env python3
"""Module for task_wait_n function."""
import asyncio
from typing import List, Any


task_wait_random = __import__('3-tasks').task_wait_random

async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Call tast_wait_random."""
    delays: List[float] = []
    for i in range(n):
        task: Any = task_wait_random(max_delay)
        await task
        delay: float = task.result()
        delays.append(delay)
    delays.sort()
    return delays
