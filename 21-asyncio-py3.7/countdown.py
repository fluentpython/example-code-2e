#!/usr/bin/env python3

# Inspired by
# https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/

import asyncio
import time


async def countdown(label, delay):
    tabs = (ord(label) - ord('A')) * '\t'
    n = 3
    while n > 0:
        await asyncio.sleep(delay)  # <----
        dt = time.perf_counter() - t0
        print('━' * 50)
        print(f'{dt:7.4f}s \t{tabs}{label} = {n}')
        n -= 1

coros = [
    countdown('A', .7),
    countdown('B', 2),
    countdown('C', .3),
    countdown('D', 1),
]
t0 = time.perf_counter()
asyncio.run(asyncio.wait(coros))
print('━' * 50)
