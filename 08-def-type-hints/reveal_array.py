from array import array
from typing import MutableSequence

a = array('d')
reveal_type(a)
b: MutableSequence[float] = array('b')
reveal_type(b)

