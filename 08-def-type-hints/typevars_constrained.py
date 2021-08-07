from typing import TypeVar, TYPE_CHECKING
from decimal import Decimal

# tag::TYPEVAR_RESTRICTED[]
RT = TypeVar('RT', float, Decimal)

def triple1(a: RT) -> RT:
    return a * 3

res1 = triple1(2)

if TYPE_CHECKING:
    reveal_type(res1)
# end::TYPEVAR_RESTRICTED[]

# tag::TYPEVAR_BOUNDED[]
BT = TypeVar('BT', bound=float)

def triple2(a: BT) -> BT:
    return a * 3

res2 = triple2(2)

if TYPE_CHECKING:
    reveal_type(res2)
# tag::TYPEVAR_BOUNDED[]
