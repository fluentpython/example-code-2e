from pytest import mark

from messages import show_count


@mark.parametrize('qty, expected', [
    (1, '1 part'),
    (2, '2 parts'),
    (0, 'no parts'),
])
def test_show_count(qty: int, expected: str) -> None:
    got = show_count(qty, 'part')
    assert got == expected


# tag::TEST_IRREGULAR[]
@mark.parametrize('qty, expected', [
    (1, '1 child'),
    (2, '2 children'),
    (0, 'no children'),
])
def test_irregular(qty: int, expected: str) -> None:
    got = show_count(qty, 'child', 'children')
    assert got == expected
# end::TEST_IRREGULAR[]
