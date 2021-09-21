"""
A "mirroring" ``stdout`` context manager.

While active, the context manager reverses text output to
``stdout``::

# tag::MIRROR_GEN_DEMO_1[]

    >>> from mirror_gen import looking_glass
    >>> with looking_glass() as what:  # <1>
    ...      print('Alice, Kitty and Snowdrop')
    ...      print(what)
    ...
    pordwonS dna yttiK ,ecilA
    YKCOWREBBAJ
    >>> what
    'JABBERWOCKY'
    >>> print('back to normal')
    back to normal


# end::MIRROR_GEN_DEMO_1[]


This exposes the context manager operation::

# tag::MIRROR_GEN_DEMO_2[]

    >>> from mirror_gen import looking_glass
    >>> manager = looking_glass()  # <1>
    >>> manager  # doctest: +ELLIPSIS
    <contextlib._GeneratorContextManager object at 0x...>
    >>> monster = manager.__enter__()  # <2>
    >>> monster == 'JABBERWOCKY'  # <3>
    eurT
    >>> monster
    'YKCOWREBBAJ'
    >>> manager  # doctest: +ELLIPSIS
    >...x0 ta tcejbo reganaMtxetnoCrotareneG_.biltxetnoc<
    >>> manager.__exit__(None, None, None)  # <4>
    False
    >>> monster
    'JABBERWOCKY'

# end::MIRROR_GEN_DEMO_2[]

The decorated generator also works as a decorator:


# tag::MIRROR_GEN_DECO[]
    >>> @looking_glass()
    ... def verse():
    ...     print('The time has come')
    ...
    >>> verse()  # <1>
    emoc sah emit ehT
    >>> print('back to normal')  # <2>
    back to normal

# end::MIRROR_GEN_DECO[]

"""


# tag::MIRROR_GEN_EX[]
import contextlib
import sys

@contextlib.contextmanager  # <1>
def looking_glass():
    original_write = sys.stdout.write  # <2>

    def reverse_write(text):  # <3>
        original_write(text[::-1])

    sys.stdout.write = reverse_write  # <4>
    yield 'JABBERWOCKY'  # <5>
    sys.stdout.write = original_write  # <6>
# end::MIRROR_GEN_EX[]
