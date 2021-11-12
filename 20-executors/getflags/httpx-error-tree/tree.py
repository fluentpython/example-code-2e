#!/usr/bin/env python3

import httpx  # make httpx classes available to .__subclasses__()


def tree(cls, level=0, last_sibling=True):
    yield cls, level, last_sibling

    # get RuntimeError and exceptions defined in httpx
    subclasses = [sub for sub in cls.__subclasses__()
                  if sub is RuntimeError or sub.__module__ == 'httpx']
    if subclasses:
        last = subclasses[-1]
        for sub in subclasses:
            yield from tree(sub, level+1, sub is last)


def display(cls):
    for cls, level, _ in tree(cls):
        indent = ' ' * 4 * level
        module = 'builtins.' if cls.__module__ == 'builtins' else ''
        print(f'{indent}{module}{cls.__name__}')


if __name__ == '__main__':
    display(Exception)
