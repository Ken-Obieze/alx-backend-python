#!/usr/bin/env python3
"""Module to return asyncio.Task."""
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Waits for random implementation."""
    task: asyncio.Task = asyncio.create_task(wait_random(max_delay))
    return task
