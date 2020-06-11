import typing
from typing import Optional


def f(a: str, *b: int, **c: float) -> None:
    if typing.TYPE_CHECKING:
        # reveal_type(b)
        reveal_type(c)
    print(a, b, c)


def g(__a: int) -> None:
    print(__a)


def h(a: int, /) -> None:
    print(a)


def tag(
    name: str,
    /,
    *content: str,
    class_: Optional[str] = None,
    foo: Optional[str] = None,
    **attrs: str,
) -> str:
    return repr((name, content, class_, attrs))


f(a='1')
f('1', 2, 3, x=4, y=5)
g(__a=1)
# h(a=1)
print(tag('li', 'first', 'second', id='#123'))
print(tag('li', 'first', 'second', class_='menu', id='#123'))
