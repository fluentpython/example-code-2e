"""
A ``Persistent`` class definition::

    >>> class Movie(Persistent):
    ...     title: str
    ...     year: int
    ...     boxmega: float

Implemented behavior::

    >>> Movie._connect()  # doctest: +ELLIPSIS
    <sqlite3.Connection object at 0x...>
    >>> movie = Movie('The Godfather', 1972, 137)
    >>> movie.title
    'The Godfather'
    >>> movie.boxmega
    137.0

Instances always have a ``.pk`` attribute, but it is ``None`` until the
object is saved::

    >>> movie.pk is None
    True
    >>> movie._persist()
    >>> movie.pk
    1

Delete the in-memory ``movie``, and fetch the record from the database,
using ``Movie[pk]``—item access on the class itself::

    >>> del movie
    >>> film = Movie[1]
    >>> film
    Movie('The Godfather', 1972, 137.0, pk=1)

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

from typing import get_type_hints

import dblib as db


class Field:
    def __init__(self, name, py_type):
        self.name = name
        self.type = py_type

    def __set__(self, instance, value):
        try:
            value = self.type(value)
        except TypeError as e:
            msg = f'{value!r} is not compatible with {self.name}:{self.type}.'
            raise TypeError(msg) from e
        instance.__dict__[self.name] = value


class Persistent:
    def __init_subclass__(
        cls, *, db_path=db.DEFAULT_DB_PATH, table='', **kwargs
    ):
        super().__init_subclass__(**kwargs)
        cls._TABLE_NAME = table if table else cls.__name__.lower() + 's'
        cls._TABLE_READY = False
        for name, py_type in get_type_hints(cls).items():
            setattr(cls, name, Field(name, py_type))

    @staticmethod
    def _connect(db_path=db.DEFAULT_DB_PATH):
        return db.connect(db_path)

    @classmethod
    def _ensure_table(cls):
        if not cls._TABLE_READY:
            db.ensure_table(cls._TABLE_NAME, get_type_hints(cls))
            cls._TABLE_READY = True
        return cls._TABLE_NAME

    def _fields(self):
        return {
            name: getattr(self, name)
            for name, attr in self.__class__.__dict__.items()
            if isinstance(attr, Field)
        }

    def __init__(self, *args, pk=None):
        for name, arg in zip(self._fields(), args):
            setattr(self, name, arg)
        self.pk = pk

    def __class_getitem__(cls, pk):
        return cls(*db.fetch_record(cls._TABLE_NAME, pk)[1:], pk=pk)

    def __repr__(self):
        args = ', '.join(repr(value) for value in self._fields().values())
        pk = '' if self.pk is None else f', pk={self.pk}'
        return f'{self.__class__.__name__}({args}{pk})'

    def _persist(self):
        table = self.__class__._ensure_table()
        if self.pk is None:
            self.pk = db.insert_record(table, self._fields())
        else:
            db.update_record(table, self.pk, self._fields())
