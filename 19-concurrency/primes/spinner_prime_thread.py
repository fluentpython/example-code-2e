# spinner_prime_thread.py

# credits: Adapted from Michele Simionato's
# multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/675659.html

import itertools
from threading import Thread, Event

from primes import is_prime

def spin(msg: str, done: Event) -> None:  # <1>
    for char in itertools.cycle(r'\|/-'):  # <2>
        status = f'\r{char} {msg}'  # <3>
        print(status, end='', flush=True)
        if done.wait(.1):  # <4>
            break  # <5>
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')  # <6>

def check(n: int) -> int:
    return is_prime(n)

def supervisor(n: int) -> int:  # <1>
    done = Event()  # <2>
    spinner = Thread(target=spin,
                     args=('thinking!', done))  # <3>
    print(f'spinner object: {spinner}')  # <4>
    spinner.start()  # <5>
    result = check(n)  # <6>
    done.set()  # <7>
    spinner.join()  # <8>
    return result

def main() -> None:
    n = 5_000_111_000_222_021
    result = supervisor(n)  # <9>
    msg = 'is' if result else 'is not'
    print(f'{n:,} {msg} prime')

if __name__ == '__main__':
    main()
