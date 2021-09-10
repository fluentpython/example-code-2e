#!/usr/bin/env python3

"""
proc_pool.py: a version of the proc.py example from chapter 20,
but using `concurrent.futures.ProcessPoolExecutor`.
"""

# tag::PRIMES_POOL[]
import sys
from concurrent import futures  # <1>
from time import perf_counter
from typing import NamedTuple

from primes import is_prime, NUMBERS

class PrimeResult(NamedTuple):  # <2>
    n: int
    flag: bool
    elapsed: float

def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def main() -> None:
    if len(sys.argv) < 2:
        workers = None      # <3>
    else:
        workers = int(sys.argv[1])

    executor = futures.ProcessPoolExecutor(workers)  # <4>
    actual_workers = executor._max_workers  # type: ignore  # <5>

    print(f'Checking {len(NUMBERS)} numbers with {actual_workers} processes:')

    t0 = perf_counter()

    numbers = sorted(NUMBERS, reverse=True)  # <6>
    with executor:  # <7>
        for n, prime, elapsed in executor.map(check, numbers):  # <8>
            label = 'P' if prime else ' '
            print(f'{n:16}  {label} {elapsed:9.6f}s')

    time = perf_counter() - t0
    print(f'Total time: {time:.2f}s')

if __name__ == '__main__':
    main()
# end::PRIMES_POOL[]
