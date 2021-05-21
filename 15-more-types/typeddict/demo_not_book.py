from books import to_xml, from_json
from typing import TYPE_CHECKING

def demo() -> None:
    NOT_BOOK_JSON = """
        {"title": "Andromeda Strain",
         "flavor": "pistachio",
         "authors": true}
    """
    not_book = from_json(NOT_BOOK_JSON)  # <1>
    if TYPE_CHECKING:  # <2>
        reveal_type(not_book)
        reveal_type(not_book['authors'])

    print(not_book)  # <3>
    print(not_book['flavor'])  # <4>

    xml = to_xml(not_book)  # <5>
    print(xml)  # <6>


if __name__ == '__main__':
    demo()
