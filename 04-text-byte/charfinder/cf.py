#!/usr/bin/env python3
import sys
import unicodedata

FIRST, LAST = ord(' '), sys.maxunicode              # <1>


def find(*query_words, first=FIRST, last=LAST):     # <2>
    query = {w.upper() for w in query_words}        # <3>
    count = 0
    for code in range(first, last + 1):
        char = chr(code)                            # <4>
        name = unicodedata.name(char, None)         # <5>
        if name and query.issubset(name.split()):   # <6>
            print(f'U+{code:04X}\t{char}\t{name}')  # <7>
            count += 1
    print(f'({count} found)')


def main(words):
    if words:
        find(*words)
    else:
        print('Please provide words to find.')


if __name__ == '__main__':
    main(sys.argv[1:])
