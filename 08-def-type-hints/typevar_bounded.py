from typing import TypeVar, TYPE_CHECKING

BT = TypeVar('BT', bound=float)

def triple2(a: BT) -> BT:
    return a * 3

res2 = triple2(2)

if TYPE_CHECKING:
    reveal_type(res2)
