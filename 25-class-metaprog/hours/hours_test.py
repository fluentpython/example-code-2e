# content of test_expectation.py
from math import isclose

import pytest

from hours import normalize, H

HOURS_TO_HMS = [
    [1, (1, 0, 0.0)],
    [1.5, (1, 30, 0.0)],
    [1.1, (1, 6, 0.0)],
    [1.9, (1, 54, 0.0)],
    [1.01, (1, 0, 36.0)],
    [1.09, (1, 5, 24.0)],
    [2 + 1/60, (2, 1, 0.0)],
    [3 + 1/3600, (3, 0, 1.0)],
    [1.251, (1, 15, 3.6)],
]


@pytest.mark.parametrize('hours, expected', HOURS_TO_HMS)
def test_normalize(hours, expected):
    h, m, s = expected
    got_h, got_m, got_s = normalize(hours * 3600)
    assert (h, m) == (got_h, got_m)
    assert isclose(s, got_s, abs_tol=1e-12)
    got_hours = got_h + got_m / 60 + got_s / 3600
    assert isclose(hours, got_hours)


@pytest.mark.parametrize('h, expected', [
    (H[1], '1:00'),
    (H[1:0], '1:00'),
    (H[1:3], '1:03'),
    (H[1:59], '1:59'),
    (H[1:0:0], '1:00'),
    (H[1:2:3], '1:02:03'),
    (H[1:2:3.4], '1:02:03.4'),
    (H[1:2:0.1], '1:02:00.1'),
    (H[1:2:0.01], '1:02:00.01'),
    (H[1:2:0.001], '1:02:00.001'),
    (H[1:2:0.0001], '1:02'),
])
def test_repr(h, expected):
    assert expected == repr(h), f'seconds: {h.s}'


@pytest.mark.parametrize('expected, hms', HOURS_TO_HMS)
def test_float(expected, hms):
    got = float(H[slice(*hms)])
    assert isclose(expected, got)


@pytest.mark.parametrize('hms, units', [
    ((0, 60, 0), 'minutes'),
    ((0, 0, 60), 'seconds'),
    ((0, 60, 60), 'minutes'),
])
def test_class_getitem_errors(hms, units):
    with pytest.raises(ValueError) as excinfo:
        H[slice(*hms)]
    assert units in str(excinfo.value)


@pytest.mark.parametrize('hms1, hms2, expected', [
    (H[0:30], H[0:15], H[0:45]),
    (H[0:30], H[0:30], H[1:00]),
    (H[0:59:59], H[0:00:1], H[1:00]),
])
def test_add(hms1, hms2, expected):
    assert expected == hms1 + hms2
