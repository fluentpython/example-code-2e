from coordinates_named import geohash, Coordinate, display

def test_geohash_max_precision() -> None:
    sao_paulo = -23.5505, -46.6339
    result = geohash(Coordinate(*sao_paulo))
    assert '6gyf4bf0r' == result

def test_display() -> None:
    sao_paulo = -23.5505, -46.6339
    assert display(sao_paulo) == '23.6°S, 46.6°W'
    shanghai = 31.2304, 121.4737
    assert display(shanghai) == '31.2°N, 121.5°E'
