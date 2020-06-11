from coordinates import geohash

def test_geohash_max_precision() -> None:
    sao_paulo = -23.5505, -46.6339
    result = geohash(sao_paulo)
    assert '6gyf4bf0r' == result
