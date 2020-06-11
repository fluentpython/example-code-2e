from pytest import mark  # type: ignore

from messages import show_count


@mark.parametrize('qty, expected', [
    (1, '1 part'),
    (2, '2 parts'),
    (0, 'no part'),
])
def test_show_count(qty, expected):
    got = show_count(qty, 'part')
    assert got == expected


# tag::TEST_IRREGULAR[]
@mark.parametrize('qty, expected', [
    (1, '1 child'),
    (2, '2 children'),
    (0, 'no child'),
])
def test_irregular(qty, expected) -> None:
    got = show_count(qty, 'child', 'children')
    assert got == expected
# end::TEST_IRREGULAR[]
