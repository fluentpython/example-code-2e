from typing import TYPE_CHECKING, List, Optional

import mymax as my

def demo_args_list_float() -> None:
    args = [2.5, 3.5, 1.5]
    expected = 3.5
    result = my.max(*args)
    print(args, expected, result, sep='\n')
    assert result == expected
    if TYPE_CHECKING:
        reveal_type(args)
        reveal_type(expected)
        reveal_type(result)

def demo_args_iter_int() -> None:
    args = [30, 10, 20]
    expected = 30
    result = my.max(args)
    print(args, expected, result, sep='\n')
    assert result == expected
    if TYPE_CHECKING:
        reveal_type(args)
        reveal_type(expected)
        reveal_type(result)


def demo_args_iter_str() -> None:
    args = iter('banana kiwi mango apple'.split())
    expected = 'mango'
    result = my.max(args)
    print(args, expected, result, sep='\n')
    assert result == expected
    if TYPE_CHECKING:
        reveal_type(args)
        reveal_type(expected)
        reveal_type(result)


def demo_args_iter_not_comparable_with_key() -> None:
    args = [object(), object(), object()]
    key = id
    expected = max(args, key=id)
    result = my.max(args, key=key)
    print(args, key, expected, result, sep='\n')
    assert result == expected
    if TYPE_CHECKING:
        reveal_type(args)
        reveal_type(key)
        reveal_type(expected)
        reveal_type(result)


def demo_empty_iterable_with_default() -> None:
    args: List[float] = []
    default = None
    expected = None
    result = my.max(args, default=default)
    print(args, default, expected, result, sep='\n')
    assert result == expected
    if TYPE_CHECKING:
        reveal_type(args)
        reveal_type(default)
        reveal_type(expected)
        reveal_type(result)


def demo_different_key_return_type() -> None:
    args = iter('banana kiwi mango apple'.split())
    key = len
    expected = 'banana'
    result = my.max(args, key=key)
    print(args, key, expected, result, sep='\n')
    assert result == expected
    if TYPE_CHECKING:
        reveal_type(args)
        reveal_type(key)
        reveal_type(expected)
        reveal_type(result)


def demo_different_key_none() -> None:
    args = iter('banana kiwi mango apple'.split())
    key = None
    expected = 'mango'
    result = my.max(args, key=key)
    print(args, key, expected, result, sep='\n')
    assert result == expected
    if TYPE_CHECKING:
        reveal_type(args)
        reveal_type(key)
        reveal_type(expected)
        reveal_type(result)

###################################### intentional type errors

def error_reported_bug() -> None:
    # example from https://github.com/python/typeshed/issues/4051
    top: Optional[int] = None
    try:
        my.max(5, top)
    except TypeError as exc:
        print(exc)


def error_args_iter_not_comparable() -> None:
    try:
        my.max([None, None])
    except TypeError as exc:
        print(exc)


def error_single_arg_not_iterable() -> None:
    try:
        my.max(1)
    except TypeError as exc:
        print(exc)

###################################### run demo and error functions

def main():
    for name, val in globals().items():
        if name.startswith('demo') or name.startswith('error'):
            print('_' * 20, name)
            val()

if __name__ == '__main__':
    main()