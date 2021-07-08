"""
    >>> clip('banana ', 6)
    'banana'
    >>> clip('banana ', 7)
    'banana'
    >>> clip('banana ', 5)
    'banana'
    >>> clip('banana split', 6)
    'banana'
    >>> clip('banana split', 7)
    'banana'
    >>> clip('banana split', 10)
    'banana'
    >>> clip('banana split', 11)
    'banana'
    >>> clip('banana split', 12)
    'banana split'
    >>> clip('bananasplit', 5)
    'bananasplit'
    >>> clip('banana  split', 8)
    'banana'
"""

# tag::CLIP[]
def clip(text, max_len=80):
    """Return text clipped at the last space before or after max_len"""
    text = text.rstrip()
    end = len(text)
    if end <= max_len:
        return text
    space_before = text.rfind(' ', 0, max_len)
    if space_before >= 0:
        end = space_before
    else:
        space_after = text.find(' ', max_len)
        if space_after >= 0:
            end = space_after
    return text[:end].rstrip()
# end::CLIP[]

