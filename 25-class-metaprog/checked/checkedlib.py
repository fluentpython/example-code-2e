"""
A ``Checked`` subclass definition requires that keyword arguments are
used to create an instance, and provides a nice ``__repr__``::

# tag::MOVIE_DEFINITION[]

    >>> class Movie(Checked):  # <1>
    ...     title: str  # <2>
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

# tag::CHECKED_FIELD[]
from collections.abc import Callable  # <1>
from typing import Any, NoReturn, get_type_hints

MISSING = object()  # <2>


class Field:
    def __init__(self, name: str, constructor: Callable) -> None:  # <3>
        self.name = name
        self.constructor = constructor

    def __set__(self, instance: 'Checked', value: Any) -> None:  # <4>
        if value is MISSING:  # <5>
            value = self.constructor()
        else:
            try:
                value = self.constructor(value)  # <6>
            except (TypeError, ValueError) as e:
                type_name = self.constructor.__name__
                msg = f'{value!r} is not compatible with {self.name}:{type_name}'
                raise TypeError(msg) from e
        instance.__dict__[self.name] = value  # <7>


# end::CHECKED_FIELD[]

# tag::CHECKED_TOP[]
class Checked:
    @classmethod
    def _fields(cls) -> dict[str, type]:  # <1>
        return get_type_hints(cls)

    def __init_subclass__(subclass) -> None:  # <2>
        super().__init_subclass__()           # <3>
        for name, constructor in subclass._fields().items():   # <4>
            setattr(subclass, name, Field(name, constructor))  # <5>

    def __init__(self, **kwargs: Any) -> None:
        for name in self._fields():             # <6>
            value = kwargs.pop(name, MISSING)   # <7>
            setattr(self, name, value)          # <8>
        if kwargs:                              # <9>
            self.__flag_unknown_attrs(*kwargs)  # <10>

    def __setattr__(self, name: str, value: Any) -> None:  # <11>
        if name in self._fields():              # <12>
            cls = self.__class__
            descriptor = getattr(cls, name)
            descriptor.__set__(self, value)     # <13>
        else:                                   # <14>
            self.__flag_unknown_attrs(name)

    # end::CHECKED_TOP[]

    # tag::CHECKED_BOTTOM[]
    def __flag_unknown_attrs(self, *names: str) -> NoReturn:  # <1>
        plural = 's' if len(names) > 1 else ''
        extra = ', '.join(f'{name!r}' for name in names)
        cls_name = repr(self.__class__.__name__)
        raise AttributeError(f'{cls_name} has no attribute{plural} {extra}')

    def _asdict(self) -> dict[str, Any]:  # <2>
        return {
            name: getattr(self, name)
            for name, attr in self.__class__.__dict__.items()
            if isinstance(attr, Field)
        }

    def __repr__(self) -> str:  # <3>
        kwargs = ', '.join(
            f'{key}={value!r}' for key, value in self._asdict().items()
        )
        return f'{self.__class__.__name__}({kwargs})'

# end::CHECKED_BOTTOM[]
