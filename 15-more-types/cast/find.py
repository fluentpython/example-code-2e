# tag::CAST[]
from typing import cast

def find_first_str(a: list[object]) -> str:
    index = next(i for i, x in enumerate(a) if isinstance(x, str))
    # We only get here if there's at least one string
    return cast(str, a[index])
# end::CAST[]


from typing import TYPE_CHECKING

l1 = [10, 20, 'thirty', 40]
if TYPE_CHECKING:
    reveal_type(l1)

print(find_first_str(l1))

l2 = [0, ()]
try:
    find_first_str(l2)
except StopIteration as e:
    print(repr(e))
