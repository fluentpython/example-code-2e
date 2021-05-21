from tree import tree


def test_1_level():
    class One: pass
    expected = [('One', 0)]
    result = list(tree(One))
    assert expected == result


def test_2_levels_2_leaves():
    class Branch: pass
    class Leaf1(Branch): pass
    class Leaf2(Branch): pass
    expected = [
        ('Branch', 0),
            ('Leaf1', 1),
            ('Leaf2', 1),
    ]
    result = list(tree(Branch))
    assert expected == result


def test_3_levels_1_leaf():
    class X: pass
    class Y(X): pass
    class Z(Y): pass
    expected = [
        ('X', 0),
            ('Y', 1),
                ('Z', 2),
    ]
    result = list(tree(X))
    assert expected == result


def test_4_levels_1_leaf():
    class Level0: pass
    class Level1(Level0): pass
    class Level2(Level1): pass
    class Level3(Level2): pass
    expected = [
        ('Level0', 0),
            ('Level1', 1),
                ('Level2', 2),
                    ('Level3', 3),
    ]

    result = list(tree(Level0))
    assert expected == result


def test_4_levels_3_leaves():
    class A: pass
    class B1(A): pass
    class C1(B1): pass
    class D1(C1): pass
    class B2(A): pass
    class D2(C1): pass
    class C2(B2): pass
    expected = [
        ('A', 0),
            ('B1', 1),
                ('C1', 2),
                    ('D1', 3),
                    ('D2', 3),
            ('B2', 1),
                ('C2', 2),
    ]

    result = list(tree(A))
    assert expected == result

