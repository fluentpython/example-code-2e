from dataclasses import dataclass
import enum

Suit = enum.IntEnum('Suit', 'spades diamonds clubs hearts')
Rank = enum.Enum('Rank', [str(n) for n in range(2, 10)] + list('JQKA'))

@dataclass(order=True)
class Card:
    rank: Suit
    suit: Rank

    def __str__(self):
        glyphs = [chr(x) for x in range(0x2660, 0x2664)]
        return f'{self.rank} of {glyphs[self.suit-1]}'
