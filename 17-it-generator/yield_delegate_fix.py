""" Example adapted from ``yield_delegate_fail.py``

The following program performs a simple abstraction over the process of
yielding.

"""

# tag::YIELD_DELEGATE_FIX[]
def f():
    def do_yield(n):
        yield n
    x = 0
    while True:
        x += 1
        yield from do_yield(x)
# end::YIELD_DELEGATE_FIX[]

if __name__ == '__main__':
    print('Invoking f() now produces a generator')
    g = f()
    print(next(g))
    print(next(g))
    print(next(g))

