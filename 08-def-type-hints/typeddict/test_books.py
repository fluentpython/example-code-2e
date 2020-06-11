import json
from typing import cast

from books import BookDict, to_xml, from_json

XML_SAMPLE = """
<BOOK>
\t<ISBN>0134757599</ISBN>
\t<TITLE>Refactoring, 2e</TITLE>
\t<AUTHOR>Martin Fowler</AUTHOR>
\t<AUTHOR>Kent Beck</AUTHOR>
\t<PAGECOUNT>478</PAGECOUNT>
</BOOK>
""".strip()


# using plain dicts

def test_1() -> None:
    xml = to_xml({
        'isbn': '0134757599',
        'title': 'Refactoring, 2e',
        'authors': ['Martin Fowler', 'Kent Beck'],
        'pagecount': 478,
    })
    assert xml == XML_SAMPLE

def test_2() -> None:
    xml = to_xml(dict(
        isbn='0134757599',
        title='Refactoring, 2e',
        authors=['Martin Fowler', 'Kent Beck'],
        pagecount=478))
    assert xml == XML_SAMPLE

def test_5() -> None:
    book_data: BookDict = dict(
        isbn='0134757599',
        title='Refactoring, 2e',
        authors=['Martin Fowler', 'Kent Beck'],
        pagecount=478
    )
    xml = to_xml(book_data)
    assert xml == XML_SAMPLE

def test_6() -> None:
    book_data = dict(
        isbn='0134757599',
        title='Refactoring, 2e',
        authors=['Martin Fowler', 'Kent Beck'],
        pagecount=478
    )
    xml = to_xml(cast(BookDict, book_data))  # cast needed
    assert xml == XML_SAMPLE

def test_4() -> None:
    xml = to_xml(BookDict(
        isbn='0134757599',
        title='Refactoring, 2e',
        authors=['Martin Fowler', 'Kent Beck'],
        pagecount=478))
    assert xml == XML_SAMPLE

def test_7() -> None:
    book_data = BookDict(
        isbn='0134757599',
        title='Refactoring, 2e',
        authors=['Martin Fowler', 'Kent Beck'],
        pagecount=478
    )
    xml = to_xml(book_data)
    assert xml == XML_SAMPLE

def test_8() -> None:
    book_data: BookDict = {
        'isbn': '0134757599',
        'title': 'Refactoring, 2e',
        'authors': ['Martin Fowler', 'Kent Beck'],
        'pagecount': 478,
    }
    xml = to_xml(book_data)
    assert xml == XML_SAMPLE

BOOK_JSON = """
    {"isbn": "0134757599",
     "title": "Refactoring, 2e",
     "authors": ["Martin Fowler", "Kent Beck"],
     "pagecount": 478}
"""

def test_load_book_0() -> None:
    book_data: BookDict = json.loads(BOOK_JSON)  # typed var
    xml = to_xml(book_data)
    assert xml == XML_SAMPLE

def test_load_book() -> None:
    book_data = from_json(BOOK_JSON)
    xml = to_xml(book_data)
    assert xml == XML_SAMPLE


NOT_BOOK_JSON = """
    {"isbn": 3.141592653589793
     "title": [1, 2, 3],
     "authors": ["Martin Fowler", "Kent Beck"],
     "flavor": "strawberry"}
"""

def test_load_not_book() -> None:
    book_data: BookDict = json.loads(BOOK_JSON)  # typed var
    xml = to_xml(book_data)
    assert xml == XML_SAMPLE
