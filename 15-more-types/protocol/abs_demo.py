import math
from typing import NamedTuple, SupportsAbs

class Vector2d(NamedTuple):
    x: float
    y: float

    def __abs__(self) -> float:  # <1>
        return math.hypot(self.x, self.y)

def is_unit(v: SupportsAbs[float]) -> bool:  # <2>
    """'True' if the magnitude of 'v' is close to 1."""
    return math.isclose(abs(v), 1.0)  # <3>

assert issubclass(Vector2d, SupportsAbs)  # <4>

v0 = Vector2d(0, 1)  # <5>
sqrt2 = math.sqrt(2)
v1 = Vector2d(sqrt2 / 2, sqrt2 / 2)
v2 = Vector2d(1, 1)
v3 = complex(.5, math.sqrt(3) / 2)
v4 = 1  # <6>

assert is_unit(v0)
assert is_unit(v1)
assert not is_unit(v2)
assert is_unit(v3)
assert is_unit(v4)

print('OK')
