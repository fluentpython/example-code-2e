from typing import TYPE_CHECKING
import pytest
from double_protocol import double

def test_double_int() -> None:
    given = 2
    result = double(given)
    assert result == given * 2
    if TYPE_CHECKING:
        reveal_type(given)
        reveal_type(result)


def test_double_str() -> None:
    given = 'A'
    result = double(given)
    assert result == given * 2
    if TYPE_CHECKING:
        reveal_type(given)
        reveal_type(result)


def test_double_fraction() -> None:
    from fractions import Fraction
    given = Fraction(2, 5)
    result = double(given)
    assert result == given * 2
    if TYPE_CHECKING:
        reveal_type(given)
        reveal_type(result)


def test_double_array() -> None:
    from array import array
    given = array('d', [1.0, 2.0, 3.14])
    result = double(given)
    if TYPE_CHECKING:
        reveal_type(given)
        reveal_type(result)


def test_double_nparray() -> None:
    import numpy as np  # type: ignore
    given = np.array([[1, 2], [3, 4]])
    result = double(given)
    comparison = result == given * 2
    assert comparison.all()
    if TYPE_CHECKING:
        reveal_type(given)
        reveal_type(result)


def test_double_none() -> None:
    given = None
    with pytest.raises(TypeError):
        double(given)
