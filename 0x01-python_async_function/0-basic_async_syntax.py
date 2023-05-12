#!/usr/bin/env python3
"""Basic async module."""
import asyncio
import random


async def wait_random(max_delay=10) -> float:
    """Delay asyncronous implementation."""
    delay: float = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
