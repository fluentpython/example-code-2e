domainlib demonstration
=======================

Run Python's async console (requires Python ≥ 3.8)::

    $ python3 -m asyncio

I'll see ``asyncio`` imported automatically::

    >>> import asyncio

Now you can experiment with ``domainlib``.

At the `>>>` prompt, type these commands::

    >>> from domainlib import *
    >>> await probe('python.org')

Note the result.

Next::

    >>> names = 'python.org rust-lang.org golang.org n05uch1an9.org'.split()
    >>> async for result in multi_probe(names):
    ...     print(*result, sep='\t')

Note that if you run the last two lines again,
the results are likely to appear in a different order.
