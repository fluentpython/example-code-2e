from typing import List, Callable

import pytest  # type: ignore

import mymax as my

@pytest.fixture
def fruits():
    return 'banana kiwi mango apple'.split()

@pytest.mark.parametrize('args, expected', [
    ([1, 3], 3),
    ([3, 1], 3),
    ([30, 10, 20], 30),
])
def test_max_args(args, expected):
    result = my.max(*args)
    assert result == expected


@pytest.mark.parametrize('iterable, expected', [
    ([7], 7),
    ([1, 3], 3),
    ([3, 1], 3),
    ([30, 10, 20], 30),
])
def test_max_iterable(iterable, expected):
    result = my.max(iterable)
    assert result == expected


def test_max_single_arg_not_iterable():
    msg = "'int' object is not iterable"
    with pytest.raises(TypeError) as exc:
        my.max(1)
    assert exc.value.args[0] == msg


def test_max_empty_iterable_no_default():
    with pytest.raises(ValueError) as exc:
        my.max([])
    assert exc.value.args[0] == my.EMPTY_MSG


@pytest.mark.parametrize('iterable, default, expected', [
    ([7], -1, 7),
    ([], -1, -1),
    ([], None, None),
])
def test_max_empty_iterable_with_default(iterable, default, expected):
    result = my.max(iterable, default=default)
    assert result == expected


@pytest.mark.parametrize('key, expected', [
    (None, 'mango'),
    (lambda x: x, 'mango'),
    (len, 'banana'),
    (lambda s: -len(s), 'kiwi'),
    (lambda s: -ord(s[0]), 'apple'),
    (lambda s: ord(s[-1]), 'mango'),
])
def test_max_iterable_with_key(
    fruits: List[str],
    key: Callable[[str], str],
    expected: str
) -> None:
    result = my.max(fruits, key=key)
    assert result == expected
