from books import BookDict, to_xml

XML_SAMPLE = """
<BOOK>
\t<ISBN>0134757599</ISBN>
\t<TITLE>Refactoring, 2e</TITLE>
\t<AUTHOR>Martin Fowler</AUTHOR>
\t<AUTHOR>Kent Beck</AUTHOR>
\t<PAGECOUNT>478</PAGECOUNT>
</BOOK>
""".strip()

def test_3() -> None:
    xml = to_xml(BookDict(dict([  # Expected keyword arguments, {...}, or dict(...) in TypedDict constructor
        ('isbn', '0134757599'),
        ('title', 'Refactoring, 2e'),
        ('authors', ['Martin Fowler', 'Kent Beck']),
        ('pagecount', 478),
    ])))
    assert xml == XML_SAMPLE
