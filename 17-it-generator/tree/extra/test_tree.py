from tree import tree


def test_1_level():
    class One: pass
    expected = [('One', 0, True)]
    result = [(cls.__name__, level, last)
              for cls, level, last in tree(One)]
    assert expected == result


def test_2_levels_2_leaves():
    class Branch: pass
    class Leaf1(Branch): pass
    class Leaf2(Branch): pass
    expected = [
        ('Branch', 0, True),
            ('Leaf1', 1, False),
            ('Leaf2', 1, True),
    ]
    result = [(cls.__name__, level, last)
              for cls, level, last in tree(Branch)]
    assert expected == result


def test_3_levels_1_leaf():
    class X: pass
    class Y(X): pass
    class Z(Y): pass
    expected = [
        ('X', 0, True),
            ('Y', 1, True),
                ('Z', 2, True),
    ]
    result = [(cls.__name__, level, last)
              for cls, level, last in tree(X)]
    assert expected == result


def test_4_levels_1_leaf():
    class Level0: pass
    class Level1(Level0): pass
    class Level2(Level1): pass
    class Level3(Level2): pass
    expected = [
        ('Level0', 0, True),
            ('Level1', 1, True),
                ('Level2', 2, True),
                    ('Level3', 3, True),
    ]

    result = [(cls.__name__, level, last)
              for cls, level, last in tree(Level0)]
    assert expected == result


def test_4_levels_3_leaves():
    class A: pass
    class B1(A): pass
    class B2(A): pass
    class C1(B1): pass
    class C2(B2): pass
    class D1(C1): pass
    class D2(C1): pass
    expected = [
        ('A', 0, True),
            ('B1', 1, False),
                ('C1', 2, True),
                    ('D1', 3, False),
                    ('D2', 3, True),
            ('B2', 1, True),
                ('C2', 2, True),
    ]

    result = [(cls.__name__, level, last)
              for cls, level, last in tree(A)]
    assert expected == result


def test_many_levels_1_leaf():
    class Root: pass
    level_count = 100
    expected = [('Root', 0, True)]
    parent = Root
    for level in range(1, level_count):
        name = f'Sub{level}'
        cls = type(name, (parent,), {})
        expected.append((name, level, True))
        parent = cls

    result = [(cls.__name__, level, last)
              for cls, level, last in tree(Root)]
    assert len(result) == level_count
    assert result[0] == ('Root', 0, True)
    assert result[-1] == ('Sub99', 99, True)
    assert expected == result
