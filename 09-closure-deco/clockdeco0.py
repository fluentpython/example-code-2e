import time


def clock(func):
    def clocked(*args):  # <1>
        t0 = time.perf_counter()
        result = func(*args)  # <2>
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}')
        return result
    return clocked  # <3>
