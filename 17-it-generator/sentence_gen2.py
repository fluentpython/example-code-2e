"""
Sentence: iterate over words using a generator function
"""

# tag::SENTENCE_GEN2[]
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text):
        self.text = text  # <1>

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):  # <2>
            yield match.group()  # <3>

# end::SENTENCE_GEN2[]
