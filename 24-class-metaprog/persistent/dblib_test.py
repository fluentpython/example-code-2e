from textwrap import dedent

import pytest

from dblib import gen_columns_sql, make_schema_sql, connect, read_columns_sql
from dblib import ColumnSchema, insert_record, fetch_record, update_record
from dblib import NoSuchRecord, delete_record, valid_table


@pytest.fixture
def create_movies_sql():
    sql = '''
        CREATE TABLE movies (
            pk INTEGER PRIMARY KEY,
            title TEXT,
            revenue REAL
        )
        '''
    return dedent(sql).strip()


@pytest.mark.parametrize(
    'fields, expected',
    [
        (
            dict(title=str, awards=int),
            [('title', 'TEXT'), ('awards', 'INTEGER')],
        ),
        (
            dict(picture=bytes, score=float),
            [('picture', 'BLOB'), ('score', 'REAL')],
        ),
    ],
)
def test_gen_columns_sql(fields, expected):
    result = list(gen_columns_sql(fields))
    assert result == expected


def test_make_schema_sql(create_movies_sql):
    fields = dict(title=str, revenue=float)
    result = make_schema_sql('movies', fields)
    assert result == create_movies_sql


def test_read_columns_sql(create_movies_sql):
    expected = [
        ColumnSchema(name='pk', sql_type='INTEGER'),
        ColumnSchema(name='title', sql_type='TEXT'),
        ColumnSchema(name='revenue', sql_type='REAL'),
    ]
    with connect() as con:
        con.execute(create_movies_sql)
        result = read_columns_sql('movies')
    assert result == expected


def test_read_columns_sql_no_such_table(create_movies_sql):
    with connect() as con:
        con.execute(create_movies_sql)
        result = read_columns_sql('no_such_table')
    assert result == []


def test_insert_record(create_movies_sql):
    fields = dict(title='Frozen', revenue=1_290_000_000)
    with connect() as con:
        con.execute(create_movies_sql)
        for _ in range(3):
            result = insert_record('movies', fields)
    assert result == 3


def test_fetch_record(create_movies_sql):
    fields = dict(title='Frozen', revenue=1_290_000_000)
    with connect() as con:
        con.execute(create_movies_sql)
        pk = insert_record('movies', fields)
        row = fetch_record('movies', pk)
    assert tuple(row) == (1, 'Frozen', 1_290_000_000.0)


def test_fetch_record_no_such_pk(create_movies_sql):
    with connect() as con:
        con.execute(create_movies_sql)
        with pytest.raises(NoSuchRecord) as e:
            fetch_record('movies', 42)
        assert e.value.pk == 42


def test_update_record(create_movies_sql):
    fields = dict(title='Frozen', revenue=1_290_000_000)
    with connect() as con:
        con.execute(create_movies_sql)
        pk = insert_record('movies', fields)
        fields['revenue'] = 1_299_999_999
        sql, values = update_record('movies', pk, fields)
        row = fetch_record('movies', pk)
    assert sql == 'UPDATE movies SET (title, revenue) = (?, ?) WHERE pk = ?'
    assert values == ('Frozen', 1_299_999_999, 1)
    assert tuple(row) == (1, 'Frozen', 1_299_999_999.0)


def test_delete_record(create_movies_sql):
    fields = dict(title='Frozen', revenue=1_290_000_000)
    with connect() as con:
        con.execute(create_movies_sql)
        pk = insert_record('movies', fields)
        delete_record('movies', pk)
        with pytest.raises(NoSuchRecord) as e:
            fetch_record('movies', pk)
        assert e.value.pk == pk


def test_persistent_valid_table(create_movies_sql):
    fields = dict(title=str, revenue=float)

    with connect() as con:
        con.execute(create_movies_sql)
        con.commit()
        assert valid_table('movies', fields)


def test_persistent_valid_table_false(create_movies_sql):
    # year field not in movies_sql
    fields = dict(title=str, revenue=float, year=int)

    with connect() as con:
        con.execute(create_movies_sql)
        con.commit()
        assert not valid_table('movies', fields)
