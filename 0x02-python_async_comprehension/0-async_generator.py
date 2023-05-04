#!/usr/bin/env python3
"""async_generator coroutine module."""
import random
import asyncio
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None]:
    """Generate async element."""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
