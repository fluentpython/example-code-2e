# tag::PRIMES_PROC_TOP[]
from time import perf_counter
from typing import Tuple, NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count  # <1>
from multiprocessing import queues  # <2>
import sys

from primes import is_prime, NUMBERS

class Result(NamedTuple):  # <3>
    flag: bool
    elapsed: float

JobQueue = queues.SimpleQueue[int]  # <4>
ResultQueue = queues.SimpleQueue[Tuple[int, Result]]  # <5>

def check(n: int) -> Result:  # <6>
    t0 = perf_counter()
    res = is_prime(n)
    return Result(res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None:  # <7>
    while n := jobs.get():  # <8>
        result = check(n)  # <9>
        results.put((n, result))  # <10>
# end::PRIMES_PROC_TOP[]

# tag::PRIMES_PROC_MAIN[]
def main() -> None:
    if len(sys.argv) < 2:  # <1>
        workers = cpu_count()
    else:
        workers = int(sys.argv[1])

    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue() # <2>
    results: ResultQueue = SimpleQueue()

    print(f'Checking {len(NUMBERS)} numbers with {workers} processes:')

    for n in NUMBERS:  # <3>
        jobs.put(n)

    for _ in range(workers):
        proc = Process(target=worker, args=(jobs, results))  # <4>
        proc.start()  # <5>
        jobs.put(0)  # <6>

    while True:
        n, (prime, elapsed) = results.get()  # <7>
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')  # <8>
        if jobs.empty():  # <9>
            break

    time = perf_counter() - t0
    print('Total time:', f'{time:0.2f}s')

if __name__ == '__main__':
    main()
# end::PRIMES_PROC_MAIN[]
