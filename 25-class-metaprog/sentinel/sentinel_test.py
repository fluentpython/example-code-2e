from sentinel import Sentinel

class PlainSentinel(Sentinel): pass


class SentinelCustomRepr(Sentinel):
    repr = '***SentinelRepr***'


def test_repr():
    assert repr(PlainSentinel) == 'PlainSentinel'


def test_pickle():
    from pickle import dumps, loads
    s = dumps(PlainSentinel)
    ps = loads(s)
    assert ps is PlainSentinel

def test_custom_repr():
    assert repr(SentinelCustomRepr) == '***SentinelRepr***'
    