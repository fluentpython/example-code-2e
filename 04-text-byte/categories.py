import sys
import collections
from unicodedata import category


def category_stats():
    counts = collections.Counter()
    firsts = {}
    for code in range(sys.maxunicode + 1):
        char = chr(code)
        cat = category(char)
        if cat not in counts:
            firsts[cat] = char
        counts[cat] += 1
    return counts, firsts


def category_scan(desired):
    for code in range(sys.maxunicode + 1):
        char = chr(code)
        if category(char) == desired:
            yield char


def main(args):
    count = 0
    if len(args) == 2:
        for char in category_scan(args[1]):
            print(char, end=' ')
            count += 1
            if count > 200:
                break
        print()
        print(count, 'characters shown')
    else:
        counts, firsts = category_stats()
        for i, (cat, count) in enumerate(counts.most_common(), 1):
            first = firsts[cat]
            if cat == 'Cs':
                first = f'(surrogate U+{ord(first):04X})'
            print(f'{i:2} {count:6} {cat} {first}')


if __name__ == '__main__':
    main(sys.argv)
