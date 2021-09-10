#!/usr/bin/env python3

"""
procs.py: shows that multiprocessing on a multicore machine
can be faster than sequential code for CPU-intensive work.
"""

# tag::PRIMES_PROC_TOP[]
import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count  # <1>
from multiprocessing import queues  # <2>

from primes import is_prime, NUMBERS

class PrimeResult(NamedTuple):  # <3>
    n: int
    prime: bool
    elapsed: float

JobQueue = queues.SimpleQueue  # <4>
ResultQueue = queues.SimpleQueue  # <5>

def check(n: int) -> PrimeResult:  # <6>
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None:  # <7>
    while True:
        n = jobs.get()  # <8>
        if n == 0:
            break
        results.put(check(n))  # <9>
# end::PRIMES_PROC_TOP[]

# tag::PRIMES_PROC_MAIN[]
def main() -> None:
    if len(sys.argv) < 2:  # <1>
        workers = cpu_count()
    else:
        workers = int(sys.argv[1])

    print(f'Checking {len(NUMBERS)} numbers with {workers} processes:')

    jobs: JobQueue = SimpleQueue() # <2>
    results: ResultQueue = SimpleQueue()
    t0 = perf_counter()

    for n in NUMBERS:  # <3>
        jobs.put(n)

    for _ in range(workers):
        proc = Process(target=worker, args=(jobs, results))  # <4>
        proc.start()  # <5>
        jobs.put(0)  # <6>

    while True:
        n, prime, elapsed = results.get()  # <7>
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')  # <8>
        if jobs.empty():  # <9>
            break

    elapsed = perf_counter() - t0
    print(f'Total time: {elapsed:.2f}s')

if __name__ == '__main__':
    main()
# end::PRIMES_PROC_MAIN[]
