"""
Sentence: iterate over words using a generator expression
"""

# tag::SENTENCE_GENEXP[]
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))
# end::SENTENCE_GENEXP[]


def main():
    import sys
    import warnings
    try:
        filename = sys.argv[1]
        word_number = int(sys.argv[2])
    except (IndexError, ValueError):
        print(f'Usage: {sys.argv[0]} <file-name> <word-number>')
        sys.exit(2)  # command line usage error
    with open(filename, 'rt', encoding='utf-8') as text_file:
        s = Sentence(text_file.read())
    for n, word in enumerate(s, 1):
        if n == word_number:
            print(word)
            break
    else:
        warnings.warn(f'last word is #{n}, {word!r}')

if __name__ == '__main__':
    main()
