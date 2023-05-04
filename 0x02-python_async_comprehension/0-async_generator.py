#!/usr/bin/env python3
"""async_generator coroutine module."""
import random
import asyncio


async def async_generator():
    """Generate async element."""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
