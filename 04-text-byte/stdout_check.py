import sys
from unicodedata import name

print(sys.version)
print()
print('sys.stdout.isatty():', sys.stdout.isatty())
print('sys.stdout.encoding:', sys.stdout.encoding)
print()

test_chars = [
    '\u2026',  # HORIZONTAL ELLIPSIS (in cp1252)
    '\u221E',  # INFINITY (in cp437)
    '\u32B7',  # CIRCLED NUMBER FORTY TWO
]

for char in test_chars:
    print(f'Trying to output {name(char)}:')
    print(char)
