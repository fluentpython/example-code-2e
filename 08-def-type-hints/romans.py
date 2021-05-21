values_map = [
    (1000,  900, 500,  400, 100,   90,  50,   40,  10,    9,   5,    4,   1),
    ( 'M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
]

def to_roman(arabic: int) -> str:
    """ Convert an integer to a Roman numeral. """
    if not 0 < arabic < 4000:
        raise ValueError('Argument must be between 1 and 3999')

    result = []
    for value, numeral in zip(*values_map):
        repeat = arabic // value
        result.append(numeral * repeat)
        arabic -= value * repeat
    return ''.join(result)
