from typing import SupportsComplex, SupportsAbs, Tuple
from typing import TYPE_CHECKING
import math
import pytest

from vector2d_v4 import Vector2d

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
        reveal_type(r)  # Revealed type is 'Any'

def magnitude(v: SupportsAbs) -> float:
    return abs(v)

def test_SupportsAbs_Vector2d_argument() -> None:
    assert magnitude(Vector2d(3, 4)) == 5.0

def test_SupportsAbs_object_argument() -> None:
    with pytest.raises(TypeError):
        magnitude(object())
        # mypy error:
        # Argument 1 to "magnitude" has incompatible type "object"; expected "SupportsAbs[Any]"

def polar(datum: SupportsComplex) -> Tuple[float, float]:
    c = complex(datum)
    return abs(c), math.atan2(c.imag, c.real)

def test_SupportsComplex_Vector2d_argument() -> None:
    assert polar(Vector2d(2, 0)) == (2, 0)
    expected = (2, math.pi / 2)
    result = polar(Vector2d(0, 2))
    assert math.isclose(result[0], expected[0])
    assert math.isclose(result[1], expected[1])

def test_SupportsComplex_complex_argument() -> None:
    assert polar(complex(2, 0)) == (2, 0)
    expected = (2, math.pi / 2)
    result = polar(complex(0, 2))
    assert math.isclose(result[0], expected[0])
    assert math.isclose(result[1], expected[1])
