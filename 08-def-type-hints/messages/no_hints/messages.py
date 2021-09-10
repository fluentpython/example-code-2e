"""
# tag::SHOW_COUNT_DOCTEST[]
>>> show_count(99, 'bird')
'99 birds'
>>> show_count(1, 'bird')
'1 bird'
>>> show_count(0, 'bird')
'no birds'

# end::SHOW_COUNT_DOCTEST[]
"""

# tag::SHOW_COUNT[]
def show_count(count, word):
    if count == 1:
        return f'1 {word}'
    count_str = str(count) if count else 'no'
    return f'{count_str} {word}s'
# end::SHOW_COUNT[]
