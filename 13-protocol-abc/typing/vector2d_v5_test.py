from vector2d_v5 import Vector2d
from typing import SupportsComplex, SupportsAbs, TYPE_CHECKING

import pytest


def test_SupportsComplex_subclass() -> None:
    assert issubclass(Vector2d, SupportsComplex)

def test_SupportsComplex_isinstance() -> None:
    v = Vector2d(3, 4)
    assert isinstance(v, SupportsComplex)
    c = complex(v)
    assert c == 3 + 4j

def test_SupportsAbs_subclass() -> None:
    assert issubclass(Vector2d, SupportsAbs)

def test_SupportsAbs_isinstance() -> None:
    v = Vector2d(3, 4)
    assert isinstance(v, SupportsAbs)
    r = abs(v)
    assert r == 5.0
    if TYPE_CHECKING:
        reveal_type(r)  # Revealed type is 'builtins.float*'

def magnitude(v: SupportsAbs) -> float:
    return abs(v)

def test_SupportsAbs_Vector2d_argument() -> None:
    assert 5.0 == magnitude(Vector2d(3, 4))

def test_SupportsAbs_object_argument() -> None:
    with pytest.raises(TypeError):
        assert 5.0 == magnitude(object())
