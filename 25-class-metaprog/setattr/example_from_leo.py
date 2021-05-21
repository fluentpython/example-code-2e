#!/usr/bin/env python3

class Foo:
    @property
    def bar(self):
        return self._bar

    @bar.setter
    def bar(self, value):
        self._bar = value

    def __setattr__(self, name, value):
        print(f'setting {name!r} to {value!r}')
        super().__setattr__(name, value)

o = Foo()
o.bar = 8
print(o.bar)
print(o._bar)
