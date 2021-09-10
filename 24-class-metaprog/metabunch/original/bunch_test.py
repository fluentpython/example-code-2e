import pytest

from bunch import MetaBunch

class Point(MetaBunch):
    """ A point has x and y coordinates, defaulting to 0.0,
        and a color, defaulting to 'gray'—and nothing more,
        except what Python and the metaclass conspire to add,
        such as __init__ and __repr__
    """
    x = 0.0
    y = 0.0
    color = 'gray'


def test_init_defaults():
    p = Point()
    assert repr(p) == 'Point()'


def test_init():
    p = Point(x=1.2, y=3.4, color='red')
    assert repr(p) == "Point(x=1.2, y=3.4, color='red')"


def test_init_wrong_argument():
    with pytest.raises(AttributeError) as exc:
        p = Point(x=1.2, y=3.4, flavor='coffee')
    assert "no attribute 'flavor'" in str(exc.value)


def test_slots():
    p = Point()
    with pytest.raises(AttributeError) as exc:
        p.z = 5.6
    assert "no attribute 'z'" in str(exc.value)


