"""
Sentence: access words by index

    >>> text = 'To be, or not to be, that is the question'
    >>> s = Sentence(text)
    >>> len(s)
    10
    >>> s[1], s[5]
    ('be', 'be')
    >>> s
    Sentence('To be, or no... the question')

"""

# tag::SENTENCE_SEQ[]
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)  # <1>

    def __getitem__(self, index):
        return self.words[index]  # <2>

    def __len__(self):  # <3>
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # <4>

# end::SENTENCE_SEQ[]
