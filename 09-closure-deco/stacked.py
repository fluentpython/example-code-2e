def first(f):
    print(f'apply first({f.__name__})')

    def inner1st(n):
        result = f(n)
        print(f'inner1({n}): called {f.__name__}({n}) -> {result}')
        return result
    return inner1st


def second(f):
    print(f'apply second({f.__name__})')

    def inner2nd(n):
        result = f(n)
        print(f'inner2({n}): called {f.__name__}({n}) -> {result}')
        return result
    return inner2nd


@first
@second
def double(n):
    return n * 2


print(double(3))


def double_(n):
    return n * 2


double_ = first(second(double_))

print(double_(3))
