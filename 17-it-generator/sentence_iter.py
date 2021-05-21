"""
Sentence: iterate over words using the Iterator Pattern, take #1

WARNING: the Iterator Pattern is much simpler in idiomatic Python;
see: sentence_gen*.py.
"""

# tag::SENTENCE_ITER[]
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):  # <1>
        return SentenceIterator(self.words)  # <2>


class SentenceIterator:

    def __init__(self, words):
        self.words = words  # <3>
        self.index = 0  # <4>

    def __next__(self):
        try:
            word = self.words[self.index]  # <5>
        except IndexError:
            raise StopIteration()  # <6>
        self.index += 1  # <7>
        return word  # <8>

    def __iter__(self):  # <9>
        return self
# end::SENTENCE_ITER[]

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
