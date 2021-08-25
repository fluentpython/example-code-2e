# tag::COLUMNIZE[]
from collections.abc import Sequence

def columnize(
    sequence: Sequence[str], num_columns: int = 0
) -> list[tuple[str, ...]]:
    if num_columns == 0:
        num_columns = round(len(sequence) ** 0.5)
    num_rows, reminder = divmod(len(sequence), num_columns)
    num_rows += bool(reminder)
    return [tuple(sequence[i::num_rows]) for i in range(num_rows)]
# end::COLUMNIZE[]


def demo() -> None:
    nato = (
        'Alfa Bravo Charlie Delta Echo Foxtrot Golf Hotel India'
        ' Juliett Kilo Lima Mike November Oscar Papa Quebec Romeo'
        ' Sierra Tango Uniform Victor Whiskey X-ray Yankee Zulu'
    ).split()

    for row in columnize(nato, 4):
        for word in row:
            print(f'{word:15}', end='')
        print()


if __name__ == '__main__':
    demo()
