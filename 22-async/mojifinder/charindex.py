#!/usr/bin/env python

"""
Class ``InvertedIndex`` builds an inverted index mapping each word to
the set of Unicode characters which contain that word in their names.

Optional arguments to the constructor are ``first`` and ``last+1`` character
codes to index, to make testing easier.

In the example below, only the ASCII range was indexed::

    >>> idx = InvertedIndex(32, 128)
    >>> sorted(idx.entries['SIGN'])
    ['#', '$', '%', '+', '<', '=', '>']
    >>> sorted(idx.entries['DIGIT'])
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> idx.entries['DIGIT'] & idx.entries['EIGHT']
    {'8'}
    >>> idx.search('digit')
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> idx.search('eight digit')
    ['8']
    >>> idx.search('a letter')
    ['A', 'a']
    >>> idx.search('a letter capital')
    ['A']
    >>> idx.search('borogove')
    []

"""

import sys
import unicodedata
from collections import defaultdict
from collections.abc import Iterator

STOP_CODE: int = sys.maxunicode + 1

Char = str
Index = defaultdict[str, set[Char]]


def tokenize(text: str) -> Iterator[str]:
    """return iterator of uppercased words"""
    for word in text.upper().replace('-', ' ').split():
        yield word


class InvertedIndex:
    entries: Index

    def __init__(self, start: int = 32, stop: int = STOP_CODE):
        entries: Index = defaultdict(set)
        for char in (chr(i) for i in range(start, stop)):
            name = unicodedata.name(char, '')
            if name:
                for word in tokenize(name):
                    entries[word].add(char)
        self.entries = entries

    def search(self, query: str) -> list[Char]:
        if words := list(tokenize(query)):
            first = self.entries[words[0]]
            result = first.intersection(*(self.entries[w] for w in words[1:]))
            return sorted(result)
        else:
            return []


def format_results(chars: list[Char]) -> Iterator[str]:
    for char in chars:
        name = unicodedata.name(char)
        code = ord(char)
        yield f'U+{code:04X}\t{char}\t{name}'


def main(words: list[str]) -> None:
    if not words:
        print('Please give one or more words to search.')
        sys.exit()
    index = InvertedIndex()
    chars = index.search(' '.join(words))
    for line in format_results(chars):
        print(line)
    print('─' * 66, f'{len(chars)} found')


if __name__ == '__main__':
    main(sys.argv[1:])
