from collections.abc import Iterator
from keyword import kwlist
from typing import TYPE_CHECKING

short_kw = (k for k in kwlist if len(k) < 5)  # <1>

if TYPE_CHECKING:
    reveal_type(short_kw)  # <2>

long_kw: Iterator[str] = (k for k in kwlist if len(k) >= 4)  # <3>

if TYPE_CHECKING:  # <4>
    reveal_type(long_kw)
