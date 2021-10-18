#!/usr/bin/env python3

import httpx  # make httpx classes available to .__subclasses__()


def tree(cls, level=0, last_sibling=True):
    yield cls, level, last_sibling
    subclasses = [c for c in cls.__subclasses__()
                  if c.__module__ == 'httpx' or c is RuntimeError]
    if subclasses:
        last = subclasses[-1]
    for sub_cls in subclasses:
        yield from tree(sub_cls, level+1, sub_cls is last)


def display(cls):
    for cls, level, _ in tree(cls):
        indent = ' ' * 4 * level
        module = 'builtins.' if cls.__module__ == 'builtins' else ''
        print(f'{indent}{module}{cls.__name__}')


if __name__ == '__main__':
    display(Exception)
