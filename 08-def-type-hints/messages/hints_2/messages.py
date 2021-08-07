"""
>>> show_count(99, 'bird')
'99 birds'
>>> show_count(1, 'bird')
'1 bird'
>>> show_count(0, 'bird')
'no birds'
>>> show_count(3, 'virus', 'viruses')
'3 viruses'
>>> show_count(1, 'virus', 'viruses')
'1 virus'
>>> show_count(0, 'virus', 'viruses')
'no viruses'
"""

# tag::SHOW_COUNT[]
def show_count(count: int, singular: str, plural: str = '') -> str:
    if count == 1:
        return f'1 {singular}'
    count_str = str(count) if count else 'no'
    if not plural:
        plural = singular + 's'
    return f'{count_str} {plural}'

# end::SHOW_COUNT[]
