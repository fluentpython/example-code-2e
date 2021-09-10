#!/usr/bin/env python3
import sys
import unicodedata

START, END = ord(' '), sys.maxunicode + 1           # <1>

def find(*query_words, start=START, end=END):       # <2>
    query = {w.upper() for w in query_words}        # <3>
    for code in range(start, end):
        char = chr(code)                            # <4>
        name = unicodedata.name(char, None)         # <5>
        if name and query.issubset(name.split()):   # <6>
            print(f'U+{code:04X}\t{char}\t{name}')  # <7>

def main(words):
    if words:
        find(*words)
    else:
        print('Please provide words to find.')

if __name__ == '__main__':
    main(sys.argv[1:])
