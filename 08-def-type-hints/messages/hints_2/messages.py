"""
>>> show_count(99, 'bird')
'99 birds'
>>> show_count(1, 'bird')
'1 bird'
>>> show_count(0, 'bird')
'no bird'
>>> show_count(3, 'virus', 'viruses')
'3 viruses'
"""

# tag::SHOW_COUNT[]
def show_count(count: int, singular: str, plural: str = '') -> str:
    if count == 0:
        return f'no {singular}'
    elif count == 1:
        return f'1 {singular}'
    else:
        if plural:
            return f'{count} {plural}'
        else:
            return f'{count} {singular}s'

# end::SHOW_COUNT[]
