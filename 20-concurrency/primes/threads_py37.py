from queue import SimpleQueue
from time import perf_counter
from threading import Thread
from typing import List, NamedTuple

from primes import is_prime, NUMBERS

class Result(NamedTuple):  # <3>
    flag: bool
    elapsed: float

def check(n: int) -> Result:  # <5>
    t0 = perf_counter()
    res = is_prime(n)
    return Result(res, perf_counter() - t0)

def job(n: int, results: SimpleQueue) -> None:  # <6>
    results.put((n, check(n)))  # <7>

def main() -> None:
    t0 = perf_counter()
    results = SimpleQueue()  # type: ignore
    workers: List[Thread] = []  # <2>

    for n in NUMBERS:
        worker = Thread(target=job, args=(n, results))  # <3>
        worker.start()  # <4>
        workers.append(worker)  # <5>

    for _ in workers:  # <6>
        n, (prime, elapsed) = results.get()  # <7>
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')

    elapsed = perf_counter() - t0
    print(f'Total time: {elapsed:.2f}s')

if __name__ == '__main__':
    main()
