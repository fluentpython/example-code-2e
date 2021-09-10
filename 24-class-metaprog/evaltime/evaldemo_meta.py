#!/usr/bin/env python3

from builderlib import Builder, deco, Descriptor
from metalib import MetaKlass  # <1>

print('# evaldemo_meta module start')

@deco
class Klass(Builder, metaclass=MetaKlass):  # <2>
    print('# Klass body')

    attr = Descriptor()

    def __init__(self):
        super().__init__()
        print(f'# Klass.__init__({self!r})')

    def __repr__(self):
        return '<Klass instance>'


def main():
    obj = Klass()
    obj.method_a()
    obj.method_b()
    obj.method_c()  # <3>
    obj.attr = 999


if __name__ == '__main__':
    main()

print('# evaldemo_meta module end')
