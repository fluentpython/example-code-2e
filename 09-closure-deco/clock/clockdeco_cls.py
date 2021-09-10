# clockdeco_class.py

"""
>>> snooze(.1)  # doctest: +ELLIPSIS
[0.101...s] snooze(0.1) -> None
>>> clock('{name}: {elapsed}')(time.sleep)(.2)  # doctest: +ELLIPSIS
sleep: 0.20...
>>> clock('{name}({args}) dt={elapsed:0.3f}s')(time.sleep)(.2)
sleep(0.2) dt=0.201s
"""

# tag::CLOCKDECO_CLS[]
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

class clock:  # <1>

    def __init__(self, fmt=DEFAULT_FMT):  # <2>
        self.fmt = fmt

    def __call__(self, func):  # <3>
        def clocked(*_args):
            t0 = time.perf_counter()
            _result = func(*_args)  # <4>
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(self.fmt.format(**locals()))
            return _result
        return clocked
# end::CLOCKDECO_CLS[]

if __name__ == '__main__':

    @clock()
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)

