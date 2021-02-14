"""
Coroutine closing demonstration::

# tag::DEMO_CORO_EXC_1[]
    >>> exc_coro = demo_exc_handling()
    >>> next(exc_coro)
    -> coroutine started
    >>> exc_coro.send(11)
    -> coroutine received: 11
    >>> exc_coro.send(22)
    -> coroutine received: 22
    >>> exc_coro.close()
    >>> from inspect import getgeneratorstate
    >>> getgeneratorstate(exc_coro)
    'GEN_CLOSED'

# end::DEMO_CORO_EXC_1[]

Coroutine handling exception::

# tag::DEMO_CORO_EXC_2[]
    >>> exc_coro = demo_exc_handling()
    >>> next(exc_coro)
    -> coroutine started
    >>> exc_coro.send(11)
    -> coroutine received: 11
    >>> exc_coro.throw(DemoException)
    *** DemoException handled. Continuing...
    >>> getgeneratorstate(exc_coro)
    'GEN_SUSPENDED'

# end::DEMO_CORO_EXC_2[]

Coroutine not handling exception::

# tag::DEMO_CORO_EXC_3[]
    >>> exc_coro = demo_exc_handling()
    >>> next(exc_coro)
    -> coroutine started
    >>> exc_coro.send(11)
    -> coroutine received: 11
    >>> exc_coro.throw(ZeroDivisionError)
    Traceback (most recent call last):
      ...
    ZeroDivisionError
    >>> getgeneratorstate(exc_coro)
    'GEN_CLOSED'

# end::DEMO_CORO_EXC_3[]
"""

# tag::EX_CORO_EXC[]
class DemoException(Exception):
    """An exception type for the demonstration."""

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:  # <1>
            print('*** DemoException handled. Continuing...')
        else:  # <2>
            print(f'-> coroutine received: {x!r}')
    raise RuntimeError('This line should never run.')  # <3>
# end::EX_CORO_EXC[]
