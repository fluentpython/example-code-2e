"""
A ``Persistent`` class definition::

    >>> class Movie(Persistent):
    ...     title: str
    ...     year: int
    ...     box_office: float

Implemented behavior::

    >>> Movie._connect()  # doctest: +ELLIPSIS
    <sqlite3.Connection object at 0x...>
    >>> movie = Movie(title='The Godfather', year=1972, box_office=137)
    >>> movie.title
    'The Godfather'
    >>> movie.box_office
    137.0

Instances always have a ``._pk`` attribute, but it is ``None`` until the
object is saved::

    >>> movie._pk is None
    True
    >>> movie._save()
    1
    >>> movie._pk
    1

Delete the in-memory ``movie``, and fetch the record from the database,
using ``Movie[pk]``—item access on the class itself::

    >>> del movie
    >>> film = Movie[1]
    >>> film
    Movie(title='The Godfather', year=1972, box_office=137.0, _pk=1)

By default, the table name is the class name lowercased, with an appended
"s" for plural::

    >>> Movie._TABLE_NAME
    'movies'

If needed, a custom table name can be given as a keyword argument in the
class declaration::

    >>> class Aircraft(Persistent, table='aircraft'):
    ...     registration: str
    ...     model: str
    ...
    >>> Aircraft._TABLE_NAME
    'aircraft'

"""

from typing import Any, ClassVar, get_type_hints

import dblib as db


class Field:
    def __init__(self, name: str, py_type: type) -> None:
        self.name = name
        self.type = py_type

    def __set__(self, instance: 'Persistent', value: Any) -> None:
        try:
            value = self.type(value)
        except (TypeError, ValueError) as e:
            type_name = self.type.__name__
            msg = f'{value!r} is not compatible with {self.name}:{type_name}.'
            raise TypeError(msg) from e
        instance.__dict__[self.name] = value


class Persistent:
    _TABLE_NAME: ClassVar[str]
    _TABLE_READY: ClassVar[bool] = False

    @classmethod
    def _fields(cls) -> dict[str, type]:
        return {
            name: py_type
            for name, py_type in get_type_hints(cls).items()
            if not name.startswith('_')
        }

    def __init_subclass__(cls, *, table: str = '', **kwargs: Any):
        super().__init_subclass__(**kwargs)  # type:ignore
        cls._TABLE_NAME = table if table else cls.__name__.lower() + 's'
        for name, py_type in cls._fields().items():
            setattr(cls, name, Field(name, py_type))

    def __init__(self, *, _pk=None, **kwargs):
        field_names = self._asdict().keys()
        for name, arg in kwargs.items():
            if name not in field_names:
                msg = f'{self.__class__.__name__!r} has no attribute {name!r}'
                raise AttributeError(msg)
            setattr(self, name, arg)
        self._pk = _pk

    def __repr__(self) -> str:
        kwargs = ', '.join(
            f'{key}={value!r}' for key, value in self._asdict().items()
        )
        cls_name = self.__class__.__name__
        if self._pk is None:
            return f'{cls_name}({kwargs})'
        return f'{cls_name}({kwargs}, _pk={self._pk})'

    def _asdict(self) -> dict[str, Any]:
        return {
            name: getattr(self, name)
            for name, attr in self.__class__.__dict__.items()
            if isinstance(attr, Field)
        }


    # database methods

    @staticmethod
    def _connect(db_path: str = db.DEFAULT_DB_PATH):
        return db.connect(db_path)

    @classmethod
    def _ensure_table(cls) -> str:
        if not cls._TABLE_READY:
            db.ensure_table(cls._TABLE_NAME, cls._fields())
            cls._TABLE_READY = True
        return cls._TABLE_NAME

    def __class_getitem__(cls, pk: int) -> 'Persistent':
        field_names = ['_pk'] + list(cls._fields())
        values = db.fetch_record(cls._TABLE_NAME, pk)
        return cls(**dict(zip(field_names, values)))

    def _save(self) -> int:
        table = self.__class__._ensure_table()
        if self._pk is None:
            self._pk = db.insert_record(table, self._asdict())
        else:
            db.update_record(table, self._pk, self._asdict())
        return self._pk
