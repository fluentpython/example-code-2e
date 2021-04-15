# SQLite3 does not support parameterized table and field names,
# for CREATE TABLE and PRAGMA so we must use Python string formatting.
# Applying `check_identifier` to parameters prevents SQL injection.

import sqlite3
from typing import NamedTuple

DEFAULT_DB_PATH = ':memory:'
CONNECTION = None

SQL_TYPES = {
    int: 'INTEGER',
    str: 'TEXT',
    float: 'REAL',
    bytes: 'BLOB',
}


class NoConnection(Exception):
    """Call connect() to open connection."""


class SchemaMismatch(ValueError):
    """The table's schema doesn't match the class."""

    def __init__(self, table_name):
        self.table_name = table_name


class NoSuchRecord(LookupError):
    """The given primary key does not exist."""

    def __init__(self, pk):
        self.pk = pk


class UnexpectedMultipleResults(Exception):
    """Query returned more than 1 row."""


class ColumnSchema(NamedTuple):
    name: str
    sql_type: str


def check_identifier(name):
    if not name.isidentifier():
        raise ValueError(f'{name!r} is not an identifier')


def connect(db_path=DEFAULT_DB_PATH):
    global CONNECTION
    CONNECTION = sqlite3.connect(db_path)
    return CONNECTION


def get_connection():
    if CONNECTION is None:
        raise NoConnection()
    return CONNECTION


def gen_columns_sql(fields):
    for name, py_type in fields.items():
        check_identifier(name)
        try:
            sql_type = SQL_TYPES[py_type]
        except KeyError as e:
            raise ValueError(f'type {py_type!r} is not supported') from e
        yield ColumnSchema(name, sql_type)


def make_schema_sql(table_name, fields):
    check_identifier(table_name)
    pk = 'pk INTEGER PRIMARY KEY,'
    spcs = ' ' * 4
    columns = ',\n    '.join(
        f'{field_name} {sql_type}'
        for field_name, sql_type in gen_columns_sql(fields)
    )
    return f'CREATE TABLE {table_name} (\n{spcs}{pk}\n{spcs}{columns}\n)'


def create_table(table_name, fields):
    con = get_connection()
    con.execute(make_schema_sql(table_name, fields))


def read_columns_sql(table_name):
    con = get_connection()
    check_identifier(table_name)
    rows = con.execute(f'PRAGMA table_info({table_name!r})')
    # row fields: cid name type notnull dflt_value pk
    return [ColumnSchema(r[1], r[2]) for r in rows]


def valid_table(table_name, fields):
    table_columns = read_columns_sql(table_name)
    return set(gen_columns_sql(fields)) <= set(table_columns)


def ensure_table(table_name, fields):
    table_columns = read_columns_sql(table_name)
    if len(table_columns) == 0:
        create_table(table_name, fields)
    if not valid_table(table_name, fields):
        raise SchemaMismatch(table_name)


def insert_record(table_name, fields):
    con = get_connection()
    check_identifier(table_name)
    placeholders = ', '.join(['?'] * len(fields))
    sql = f'INSERT INTO {table_name} VALUES (NULL, {placeholders})'
    cursor = con.execute(sql, tuple(fields.values()))
    pk = cursor.lastrowid
    con.commit()
    cursor.close()
    return pk


def fetch_record(table_name, pk):
    con = get_connection()
    check_identifier(table_name)
    sql = f'SELECT * FROM {table_name} WHERE pk = ? LIMIT 2'
    result = list(con.execute(sql, (pk,)))
    if len(result) == 0:
        raise NoSuchRecord(pk)
    elif len(result) == 1:
        return result[0]
    else:
        raise UnexpectedMultipleResults()


def update_record(table_name, pk, fields):
    con = get_connection()
    check_identifier(table_name)
    names = ', '.join(fields.keys())
    placeholders = ', '.join(['?'] * len(fields))
    values = tuple(fields.values()) + (pk,)
    sql = f'UPDATE {table_name} SET ({names}) = ({placeholders}) WHERE pk = ?'
    con.execute(sql, values)
    con.commit()
    return sql, values


def delete_record(table_name, pk):
    con = get_connection()
    check_identifier(table_name)
    sql = f'DELETE FROM {table_name} WHERE pk = ?'
    return con.execute(sql, (pk,))
