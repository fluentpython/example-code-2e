from typing import Sequence, List, Tuple, TypeVar

T = TypeVar('T')

def columnize(sequence: Sequence[T], num_columns: int = 0) -> List[Tuple[T, ...]]:
    if num_columns == 0:
        num_columns = round(len(sequence) ** .5)
    num_rows, reminder = divmod(len(sequence), num_columns)
    num_rows += bool(reminder)
    return [tuple(sequence[i::num_rows]) for i in range(num_rows)]


def demo() -> None:
    nato = ('Alfa Bravo Charlie Delta Echo Foxtrot Golf Hotel India'
            ' Juliett Kilo Lima Mike November Oscar Papa Quebec Romeo'
            ' Sierra Tango Uniform Victor Whiskey X-ray Yankee Zulu'
            ).split()

    for line in columnize(nato):
        for word in line:
            print(f'{word:15}', end='')
        print()

    print()
    for length in range(2, 21, 6):
        values = list(range(1, length + 1))
        for row in columnize(values):
            for cell in row:
                print(f'{cell:5}', end='')
            print()
        print()


if __name__ == '__main__':
    demo()
