#!/usr/bin/env python3

"""
threads.py: shows that Python threads are slower than
sequential code for CPU-intensive work.
"""

from time import perf_counter
from typing import NamedTuple
from threading import Thread
from queue import SimpleQueue
import sys
import os

from primes import is_prime, NUMBERS

class PrimeResult(NamedTuple):  # <3>
    n: int
    prime: bool
    elapsed: float

JobQueue = SimpleQueue[int]
ResultQueue = SimpleQueue[PrimeResult]

def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None:
    while n := jobs.get():
        results.put(check(n))

def main() -> None:
    if len(sys.argv) < 2:  # <1>
        workers = os.cpu_count() or 1  # make mypy happy
    else:
        workers = int(sys.argv[1])

    print(f'Checking {len(NUMBERS)} numbers with {workers} threads:')

    jobs: JobQueue = SimpleQueue() # <2>
    results: ResultQueue = SimpleQueue()
    t0 = perf_counter()

    for n in NUMBERS:  # <3>
        jobs.put(n)

    for _ in range(workers):
        proc = Thread(target=worker, args=(jobs, results))  # <4>
        proc.start()  # <5>
        jobs.put(0)  # <6>

    while True:
        n, prime, elapsed = results.get()  # <7>
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')
        if jobs.empty():  # <8>
            break

    time = perf_counter() - t0
    print('Total time:', f'{time:0.2f}s')

if __name__ == '__main__':
    main()
