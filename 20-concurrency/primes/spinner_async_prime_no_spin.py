# spinner_async_experiment.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/675659.html

import asyncio
import itertools

import primes

async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    print('THIS WILL NEVER BE OUTPUT')

# tag::SPINNER_ASYNC_EXPERIMENT[]
async def slow() -> int:
    primes.is_prime(5_000_111_000_222_021)  # <4>
    return 42

async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!'))  # <1>
    print('spinner object:', spinner)  # <2>
    result = await slow()  # <3>
    spinner.cancel()  # <5>
    return result
# end::SPINNER_ASYNC_EXPERIMENT[]

def main() -> None:
    result = asyncio.run(supervisor())
    print('Answer:', result)

if __name__ == '__main__':
    main()
