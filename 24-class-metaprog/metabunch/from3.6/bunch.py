"""
The `MetaBunch` metaclass is a simplified version of the
last example in the _How a Metaclass Creates a Class_ section
of _Chapter 4: Object Oriented Python_ from
[_Python in a Nutshell, 3rd edition_](https://learning.oreilly.com/library/view/python-in-a/9781491913833)
by Alex Martelli, Anna Ravenscroft, and Steve Holden.

Here are a few tests. ``bunch_test.py`` has a few more.

# tag::BUNCH_POINT_DEMO_1[]
    >>> class Point(Bunch):
    ...     x = 0.0
    ...     y = 0.0
    ...     color = 'gray'
    ...
    >>> Point(x=1.2, y=3, color='green')
    Point(x=1.2, y=3, color='green')
    >>> p = Point()
    >>> p.x, p.y, p.color
    (0.0, 0.0, 'gray')
    >>> p
    Point()

# end::BUNCH_POINT_DEMO_1[]

# tag::BUNCH_POINT_DEMO_2[]

    >>> Point(x=1, y=2, z=3)
    Traceback (most recent call last):
      ...
    AttributeError: No slots left for: 'z'
    >>> p = Point(x=21)
    >>> p.y = 42
    >>> p
    Point(x=21, y=42)
    >>> p.flavor = 'banana'
    Traceback (most recent call last):
      ...
    AttributeError: 'Point' object has no attribute 'flavor'

# end::BUNCH_POINT_DEMO_2[]
"""

# tag::METABUNCH[]
class MetaBunch(type):  # <1>
    def __new__(meta_cls, cls_name, bases, cls_dict):  # <2>

        defaults = {}  # <3>

        def __init__(self, **kwargs):  # <4>
            for name, default in defaults.items():  # <5>
                setattr(self, name, kwargs.pop(name, default))
            if kwargs:  # <6>
                extra = ', '.join(kwargs)
                raise AttributeError(f'No slots left for: {extra!r}')

        def __repr__(self):  # <7>
            rep = ', '.join(f'{name}={value!r}'
                            for name, default in defaults.items()
                            if (value := getattr(self, name)) != default)
            return f'{cls_name}({rep})'

        new_dict = dict(__slots__=[], __init__=__init__, __repr__=__repr__)  # <8>

        for name, value in cls_dict.items():  # <9>
            if name.startswith('__') and name.endswith('__'):  # <10>
                if name in new_dict:
                    raise AttributeError(f"Can't set {name!r} in {cls_name!r}")
                new_dict[name] = value
            else:  # <11>
                new_dict['__slots__'].append(name)
                defaults[name] = value
        return super().__new__(meta_cls, cls_name, bases, new_dict)  # <12>


class Bunch(metaclass=MetaBunch):  # <13>
    pass
# end::METABUNCH[]
