from time import perf_counter
from typing import Tuple, NamedTuple
from threading import Thread
from queue import SimpleQueue
import sys
import os

from primes import is_prime, NUMBERS

class Result(NamedTuple):
    flag: bool
    elapsed: float

JobQueue = SimpleQueue[int]
ResultQueue = SimpleQueue[Tuple[int, Result]]

def check(n: int) -> Result:
    t0 = perf_counter()
    res = is_prime(n)
    return Result(res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None:
    while n := jobs.get():
        result = check(n)
        results.put((n, result))

def main() -> None:
    if len(sys.argv) < 2:  # <1>
        workers = os.cpu_count() or 1  # make mypy happy
    else:
        workers = int(sys.argv[1])

    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue() # <2>
    results: ResultQueue = SimpleQueue()

    print(f'Checking {len(NUMBERS)} numbers with {workers} threads:')

    for n in NUMBERS:  # <3>
        jobs.put(n)

    for _ in range(workers):
        proc = Thread(target=worker, args=(jobs, results))  # <4>
        proc.start()  # <5>
        jobs.put(0)  # <6>

    while True:
        n, (prime, elapsed) = results.get()  # <7>
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')
        if jobs.empty():  # <8>
            break

    time = perf_counter() - t0
    print('Total time:', f'{time:0.2f}s')

if __name__ == '__main__':
    main()
