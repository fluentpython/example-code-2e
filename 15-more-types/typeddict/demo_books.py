from books import BookDict
from typing import TYPE_CHECKING

def demo() -> None:  # <1>
    book = BookDict(  # <2>
        isbn='0134757599',
        title='Refactoring, 2e',
        authors=['Martin Fowler', 'Kent Beck'],
        pagecount=478
    )
    authors = book['authors'] # <3>
    if TYPE_CHECKING:  # <4>
        reveal_type(authors)  # <5>
    authors = 'Bob'  # <6>
    book['weight'] = 4.2
    del book['title']


if __name__ == '__main__':
    demo()
