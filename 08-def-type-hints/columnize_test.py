from columnize import columnize


def test_columnize_8_in_2():
    sequence = 'ABCDEFGH'
    expected = [
        ('A', 'E'),
        ('B', 'F'),
        ('C', 'G'),
        ('D', 'H'),
    ]
    result = columnize(sequence, 2)
    assert expected == result


def test_columnize_8_in_4():
    sequence = 'ABCDEFGH'
    expected = [
        ('A', 'C', 'E', 'G'),
        ('B', 'D', 'F', 'H'),
    ]
    result = columnize(sequence, 4)
    assert expected == result


def test_columnize_7_in_2():
    sequence = 'ABCDEFG'
    expected = [
        ('A', 'E'),
        ('B', 'F'),
        ('C', 'G'),
        ('D',),
    ]
    result = columnize(sequence, 2)
    assert expected == result


def test_columnize_8_in_3():
    sequence = 'ABCDEFGH'
    expected = [
        ('A', 'D', 'G',),
        ('B', 'E', 'H',),
        ('C', 'F'),
    ]
    result = columnize(sequence, 3)
    assert expected == result


def test_columnize_8_in_5():
    # Not the right number of columns, but the right number of rows.
    # This actually looks better, so it's OK!
    sequence = 'ABCDEFGH'
    expected = [
        ('A', 'C', 'E', 'G'),
        ('B', 'D', 'F', 'H'),
    ]
    result = columnize(sequence, 5)
    assert expected == result


def test_columnize_7_in_5():
    # Not the right number of columns, but the right number of rows.
    # This actually looks better, so it's OK!
    sequence = 'ABCDEFG'
    expected = [
        ('A', 'C', 'E', 'G'),
        ('B', 'D', 'F'),
    ]
    result = columnize(sequence, 5)
    assert expected == result


def test_columnize_not_enough_items():
    sequence = 'AB'
    expected = [
        ('A', 'B'),
    ]
    result = columnize(sequence, 3)
    assert expected == result