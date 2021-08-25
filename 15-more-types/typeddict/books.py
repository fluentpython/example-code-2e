import json
# tag::BOOKDICT[]
from typing import TypedDict

class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: int
# end::BOOKDICT[]

# tag::TOXML[]
AUTHOR_ELEMENT = '<AUTHOR>{}</AUTHOR>'

def to_xml(book: BookDict) -> str:  # <1>
    elements: list[str] = []  # <2>
    for key, value in book.items():
        if isinstance(value, list):  # <3>
            elements.extend(
                AUTHOR_ELEMENT.format(n) for n in value)  # <4>
        else:
            tag = key.upper()
            elements.append(f'<{tag}>{value}</{tag}>')
    xml = '\n\t'.join(elements)
    return f'<BOOK>\n\t{xml}\n</BOOK>'
# end::TOXML[]

# tag::FROMJSON[]
def from_json(data: str) -> BookDict:
    whatever: BookDict = json.loads(data)  # <1>
    return whatever  # <2>
# end::FROMJSON[]
