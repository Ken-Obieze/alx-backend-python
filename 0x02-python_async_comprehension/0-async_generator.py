import random
import asyncio

async def async_generator():
    """generate async element."""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random(0, 10)
