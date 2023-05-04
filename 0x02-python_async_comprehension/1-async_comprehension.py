#!/usr/bin/env python3
"""async_generator coroutine module."""
import random
import asyncio
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """Collect 10 random numbers usig async_comprehension."""
    numbers = [number async for number in async_generator()]
    return numbers
