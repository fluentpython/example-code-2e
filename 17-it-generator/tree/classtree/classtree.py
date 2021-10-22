#!/usr/bin/env python3

from importlib import import_module
import sys


SP    = '\N{SPACE}'
HLIN  = '\N{BOX DRAWINGS LIGHT HORIZONTAL}' * 2 + SP        # ──
VLIN  = '\N{BOX DRAWINGS LIGHT VERTICAL}' + SP * 3          # │
TEE   = '\N{BOX DRAWINGS LIGHT VERTICAL AND RIGHT}' + HLIN  # ├──
ELBOW = '\N{BOX DRAWINGS LIGHT UP AND RIGHT}' + HLIN        # └──


def subclasses(cls):
    try:
        return cls.__subclasses__()
    except TypeError:  # handle the `type` type
        return cls.__subclasses__(cls)


def tree(cls, level=0, last_sibling=True):
    yield cls, level, last_sibling
    chidren = subclasses(cls)
    if chidren:
        last = chidren[-1]
        for child in chidren:
            yield from tree(child, level + 1, child is last)


def render_lines(tree_generator):
    cls, _, _ = next(tree_generator)
    yield cls.__name__
    prefix = ''
    for cls, level, last in tree_generator:
        prefix = prefix[: 4 * (level - 1)]
        prefix = prefix.replace(TEE, VLIN).replace(ELBOW, SP * 4)
        prefix += ELBOW if last else TEE
        yield prefix + cls.__name__


def draw(cls):
    for line in render_lines(tree(cls)):
        print(line)


def parse(name):
    if '.' in name:
        return name.rsplit('.', 1)
    else:
        return 'builtins', name


def main(name):
    module_name, cls_name = parse(name)
    try:
        cls = getattr(import_module(module_name), cls_name)
    except ModuleNotFoundError:
        print(f'*** Could not import {module_name!r}.')
    except AttributeError:
        print(f'*** {cls_name!r} not found in {module_name!r}.')
    else:
        if isinstance(cls, type):
            draw(cls)
        else:
            print(f'*** {cls_name!r} is not a class.')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Usage:'
            f'\t{sys.argv[0]} Class          # for builtin classes\n'
            f'\t{sys.argv[0]} package.Class  # for other classes'
        )
