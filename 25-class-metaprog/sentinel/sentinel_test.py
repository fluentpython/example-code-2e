import pickle

import pytest

from sentinel import Sentinel


class PlainSentinel(Sentinel):
    pass


class SentinelCustomRepr(Sentinel):
    repr = '***SentinelRepr***'


def test_repr():
    assert repr(PlainSentinel) == 'PlainSentinel'


def test_cannot_instantiate():
    with pytest.raises(TypeError) as e:
        PlainSentinel()
    msg = "'PlainSentinel' is a sentinel and cannot be instantiated"
    assert msg in str(e.value)


def test_custom_repr():
    assert repr(SentinelCustomRepr) == '***SentinelRepr***'


def test_pickle():
    s = pickle.dumps(SentinelCustomRepr)
    ps = pickle.loads(s)
    assert ps is SentinelCustomRepr


def test_sentinel_comes_ready_to_use():
    assert repr(Sentinel) == 'Sentinel'
    s = pickle.dumps(Sentinel)
    ps = pickle.loads(s)
    assert ps is Sentinel
