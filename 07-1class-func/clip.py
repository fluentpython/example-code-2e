"""
    >>> clip('banana split', 5)
    'banana'
    >>> clip('banana split', 6)
    'banana'
    >>> clip('banana split', 7)
    'banana'
    >>> clip('banana split', 8)
    'banana'
    >>> clip('banana split', 11)
    'banana'
    >>> clip('banana split', 12)
    'banana split'
    >>> clip('banana-split', 3)
    'banana-split'

Jess' tests:

    >>> text = 'The quick brown fox jumps over the lazy dog.'
    >>> clip14 = clip(text, max_len=14)
    >>> clip14
    'The quick'
    >>> len(clip14)
    9
    >>> clip15 = clip(text, max_len=15)
    >>> clip15
    'The quick brown'
    >>> len(clip15)
    15

"""

# tag::CLIP[]
def clip(text, max_len=80):
    """Return max_len characters clipped at space if possible"""
    text = text.rstrip()
    if len(text) <= max_len or ' ' not in text:
        return text
    end = len(text)
    space_at = text.rfind(' ', 0, max_len + 1)
    if space_at >= 0:
        end = space_at
    else:
        space_at = text.find(' ', max_len)
        if space_at >= 0:
            end = space_at
    return text[:end].rstrip()
# end::CLIP[]
