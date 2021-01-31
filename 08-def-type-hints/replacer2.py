"""
``zip_replace`` replaces multiple calls to ``str.replace``::

    >>> changes = [
    ...     ('(', ' ( '),
    ...     (')', ' ) '),
    ...     ('  ', ' '),
    ... ]
    >>> expr = '(+ 2 (* 3 7))'
    >>> zip_replace(expr, changes)
    ' ( + 2 ( * 3 7 ) ) '

"""

from typing import Iterable, NamedTuple


class FromTo(NamedTuple):
    from_: str
    to: str


def zip_replace(text: str, changes: Iterable[FromTo], count:int = -1) -> str:
    for from_, to in changes:
        text = text.replace(from_, to, count)
    return text


def demo() -> None:
    import doctest
    failed, count = doctest.testmod()
    print(f'{count-failed} of {count} doctests OK')
    l33t = [FromTo(*p) for p in 'a4 e3 i1 o0'.split()]
    text = 'mad skilled noob powned leet'
    print(zip_replace(text, l33t))


if __name__ == '__main__':
    demo()
