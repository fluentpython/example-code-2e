from time import perf_counter
from typing import NamedTuple

from primes import is_prime, NUMBERS

class Result(NamedTuple):  # <1>
    flag: bool
    elapsed: float

def check(n: int) -> Result:  # <2>
    t0 = perf_counter()
    flag = is_prime(n)
    return Result(flag, perf_counter() - t0)

def main() -> None:
    t0 = perf_counter()
    for n in NUMBERS:  # <3>
        prime, elapsed = check(n)
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')

    elapsed = perf_counter() - t0  # <4>
    print('Total time:', f'{elapsed:0.2f}s')

if __name__ == '__main__':
    main()
