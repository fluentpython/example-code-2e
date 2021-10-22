from textwrap import dedent
from typing import SupportsBytes
from classtree import tree, render_lines, main, subclasses

from abc import ABCMeta


def test_subclasses():
    result = subclasses(UnicodeError)
    assert set(result) >= {UnicodeEncodeError, UnicodeDecodeError}


def test_subclasses_of_type():
    """
    The `type` class is a special case because `type.__subclasses__()`
    is an unbound method when called on it, so we must call it as
    `type.__subclasses__(type)` just for `type`.

    This test does not verify the full list of results, but just
    checks that `abc.ABCMeta` is included, because that's the only
    subclass of `type` (i.e. metaclass) I we get when I run
    `$ classtree.py type` at the command line.

    However, the Python console and `pytest` both load other modules,
    so `subclasses` may find more subclasses of `type`—for example,
    `enum.EnumMeta`.
    """
    result = subclasses(type)
    assert ABCMeta in result


def test_tree_1_level():
    result = list(tree(TabError))
    assert result == [(TabError, 0, True)]


def test_tree_2_levels():
    result = list(tree(IndentationError))
    assert result == [
        (IndentationError, 0, True),
        (TabError, 1, True),
    ]


def test_render_lines_1_level():
    result = list(render_lines(tree(TabError)))
    assert result == ['TabError']


def test_render_lines_2_levels_1_leaf():
    result = list(render_lines(tree(IndentationError)))
    expected = [
        'IndentationError',
        '└── TabError',
    ]
    assert expected == result


def test_render_lines_3_levels_1_leaf():
    class X: pass
    class Y(X): pass
    class Z(Y): pass
    result = list(render_lines(tree(X)))
    expected = [
        'X',
        '└── Y',
        '    └── Z',
    ]
    assert expected == result


def test_render_lines_4_levels_1_leaf():
    class Level0: pass
    class Level1(Level0): pass
    class Level2(Level1): pass
    class Level3(Level2): pass

    result = list(render_lines(tree(Level0)))
    expected = [
        'Level0',
        '└── Level1',
        '    └── Level2',
        '        └── Level3',
    ]
    assert expected == result


def test_render_lines_2_levels_2_leaves():
    class Branch: pass
    class Leaf1(Branch): pass
    class Leaf2(Branch): pass
    result = list(render_lines(tree(Branch)))
    expected = [
        'Branch',
        '├── Leaf1',
        '└── Leaf2',
    ]
    assert expected == result


def test_render_lines_3_levels_2_leaves_dedent():
    class A: pass
    class B(A): pass
    class C(B): pass
    class D(A): pass
    class E(D): pass

    result = list(render_lines(tree(A)))
    expected = [
        'A',
        '├── B',
        '│   └── C',
        '└── D',
        '    └── E',
    ]
    assert expected == result


def test_render_lines_4_levels_4_leaves_dedent():
    class A: pass
    class B1(A): pass
    class C1(B1): pass
    class D1(C1): pass
    class D2(C1): pass
    class C2(B1): pass
    class B2(A): pass
    expected = [
        'A',
        '├── B1',
        '│   ├── C1',
        '│   │   ├── D1',
        '│   │   └── D2',
        '│   └── C2',
        '└── B2',
    ]

    result = list(render_lines(tree(A)))
    assert expected == result


def test_main_simple(capsys):
    main('IndentationError')
    expected = dedent("""
        IndentationError
        └── TabError
    """).lstrip()
    captured = capsys.readouterr()
    assert captured.out == expected


def test_main_dotted(capsys):
    main('collections.abc.Sequence')
    expected = dedent("""
        Sequence
        ├── ByteString
        ├── MutableSequence
        │   └── UserList
    """).lstrip()
    captured = capsys.readouterr()
    assert captured.out.startswith(expected)


def test_main_class_not_found(capsys):
    main('NoSuchClass')
    expected = "*** 'NoSuchClass' not found in 'builtins'.\n"
    captured = capsys.readouterr()
    assert captured.out == expected


def test_main_module_not_found(capsys):
    main('nosuch.module')
    expected = "*** Could not import 'nosuch'.\n"
    captured = capsys.readouterr()
    assert captured.out == expected


def test_main_not_a_class(capsys):
    main('collections.abc')
    expected = "*** 'abc' is not a class.\n"
    captured = capsys.readouterr()
    assert captured.out == expected
