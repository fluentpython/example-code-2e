"""
# tag::SHOW_COUNT_DOCTEST[]
>>> show_count(99, 'bird')
'99 birds'
>>> show_count(1, 'bird')
'1 bird'
>>> show_count(0, 'bird')
'no bird'

# end::SHOW_COUNT_DOCTEST[]
"""

# tag::SHOW_COUNT[]
def show_count(count, word):
    if count == 0:
        return f'no {word}'
    elif count == 1:
        return f'{count} {word}'
    return f'{count} {word}s'
# end::SHOW_COUNT[]
