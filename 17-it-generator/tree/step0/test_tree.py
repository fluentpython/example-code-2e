from tree import tree


def test_1_level():
    class One: pass
    expected = ['One']
    result = list(tree(One))
    assert expected == result
