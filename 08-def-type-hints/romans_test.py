import pytest

from romans import to_roman


def test_to_roman_1():
    assert to_roman(1) == 'I'


@pytest.mark.parametrize('arabic, roman', [
    (3, 'III'),
    (4, 'IV'),
    (1009, 'MIX'),
    (1969, 'MCMLXIX'),
    (3999, 'MMMCMXCIX')
])
def test_to_roman(arabic, roman):
    assert to_roman(arabic) == roman
