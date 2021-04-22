"""
A ``Checked`` subclass definition requires that keyword arguments are
used to create an instance, and provides a nice ``__repr__``::

# tag::MOVIE_DEFINITION[]

    >>> @checked
    ... class Movie:
    ...     title: str
    ...     year: int
    ...     megabucks: float
    ...
    >>> movie = Movie(title='The Godfather', year=1972, megabucks=137)  # <3>
    >>> movie.title
    'The Godfather'
    >>> movie  # <4>
    Movie(title='The Godfather', year=1972, megabucks=137.0)

# end::MOVIE_DEFINITION[]

The type of arguments is runtime checked when an attribute is set,
including during instantiation::

# tag::MOVIE_TYPE_VALIDATION[]

    >>> movie.year = 'MCMLXXII'  # <1>
    Traceback (most recent call last):
      ...
    TypeError: 'MCMLXXII' is not compatible with year:int
    >>> blockbuster = Movie(title='Avatar', year=2009, megabucks='billions')  # <2>
    Traceback (most recent call last):
      ...
    TypeError: 'billions' is not compatible with megabucks:float

# end::MOVIE_TYPE_VALIDATION[]

Attributes not passed as arguments to the constructor are initialized with
default values::

# tag::MOVIE_DEFAULTS[]

    >>> Movie(title='Life of Brian')
    Movie(title='Life of Brian', year=0, megabucks=0.0)

# end::MOVIE_DEFAULTS[]

Providing extra arguments to the constructor is not allowed::

    >>> blockbuster = Movie(title='Avatar', year=2009, megabucks=2000,
    ...                     director='James Cameron')
    Traceback (most recent call last):
      ...
    AttributeError: 'Movie' has no attribute 'director'

Creating new attributes at runtime is restricted as well::

    >>> movie.director = 'Francis Ford Coppola'
    Traceback (most recent call last):
      ...
    AttributeError: 'Movie' has no attribute 'director'

The `_as_dict` instance creates a `dict` from the attributes of a `Movie` object::

    >>> movie._asdict()
    {'title': 'The Godfather', 'year': 1972, 'megabucks': 137.0}

"""

from collections.abc import Callable  # <1>
from typing import Any, NoReturn, get_type_hints

MISSING = object()  # <2>


class Field:
    def __init__(self, name: str, constructor: Callable) -> None:  # <3>
        self.name = name
        self.constructor = constructor

    def __set__(self, instance: Any, value: Any) -> None:  # <4>
        if value is MISSING:  # <5>
            value = self.constructor()
        else:
            try:
                value = self.constructor(value)  # <6>
            except (TypeError, ValueError) as e:
                type_name = self.constructor.__name__
                msg = (
                    f'{value!r} is not compatible with {self.name}:{type_name}'
                )
                raise TypeError(msg) from e
        instance.__dict__[self.name] = value  # <7>


# tag::CHECKED_DECORATOR_TOP[]
_methods_to_inject: list[Callable] = []
_classmethods_to_inject: list[Callable] = []

def checked(cls: type) -> type:  # <2>
    for func in _methods_to_inject:
        name = func.__name__
        setattr(cls, name, func)  # <5>

    for func in _classmethods_to_inject:
        name = func.__name__
        setattr(cls, name, classmethod(func))  # <5>

    for name, constructor in _fields(cls).items():   # <4>
        setattr(cls, name, Field(name, constructor))  # <5>

    return cls


def _method(func: Callable) -> Callable:
    _methods_to_inject.append(func)
    return func


def _classmethod(func: Callable) -> Callable:
    _classmethods_to_inject.append(func)
    return func

# tag::CHECKED_METHODS_TOP[]
@_classmethod
def _fields(cls: type) -> dict[str, type]:  # <1>
    return get_type_hints(cls)

@_method
def __init__(self: Any, **kwargs: Any) -> None:
    for name in self._fields():             # <6>
        value = kwargs.pop(name, MISSING)   # <7>
        setattr(self, name, value)          # <8>
    if kwargs:                              # <9>
        self.__flag_unknown_attrs(*kwargs)  # <10>

@_method
def __setattr__(self: Any, name: str, value: Any) -> None:  # <11>
    if name in self._fields():              # <12>
        cls = self.__class__
        descriptor = getattr(cls, name)
        descriptor.__set__(self, value)     # <13>
    else:                                   # <14>
        self.__flag_unknown_attrs(name)
# end::CHECKED_METHODS_TOP[]

# tag::CHECKED_METHODS_BOTTOM[]
@_method
def __flag_unknown_attrs(self: Any, *names: str) -> NoReturn:  # <1>
    plural = 's' if len(names) > 1 else ''
    extra = ', '.join(f'{name!r}' for name in names)
    cls_name = repr(self.__class__.__name__)
    raise AttributeError(f'{cls_name} has no attribute{plural} {extra}')


@_method
def _asdict(self: Any) -> dict[str, Any]:  # <2>
    return {
        name: getattr(self, name)
        for name, attr in self.__class__.__dict__.items()
        if isinstance(attr, Field)
    }


@_method
def __repr__(self: Any) -> str:  # <3>
    kwargs = ', '.join(
        f'{key}={value!r}' for key, value in self._asdict().items()
    )
    return f'{self.__class__.__name__}({kwargs})'
# end::CHECKED_METHODS_BOTTOM[]
