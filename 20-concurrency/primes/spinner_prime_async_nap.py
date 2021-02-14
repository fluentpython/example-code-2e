# spinner_prime_async_nap.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/675659.html

import asyncio
import itertools
import math

# tag::PRIME_NAP[]
async def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
        if i % 100_000 == 1:  # <2>
            await asyncio.sleep(0)
    return True
# end::PRIME_NAP[]


async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

async def check(n: int) -> int:
    return await is_prime(n)  # <4>

async def supervisor(n: int) -> int:
    spinner = asyncio.create_task(spin('thinking!'))  # <1>
    print(f'spinner object: {spinner}')  # <2>
    result = await check(n)  # <3>
    spinner.cancel()  # <5>
    return result

def main() -> None:
    n = 5_000_111_000_222_021
    result = asyncio.run(supervisor(n))
    msg = 'is' if result else 'is not'
    print(f'{n:,} {msg} prime')

if __name__ == '__main__':
    main()
