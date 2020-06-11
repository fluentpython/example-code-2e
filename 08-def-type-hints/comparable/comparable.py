from typing import Protocol, Any

class Comparable(Protocol):  # <1>
    def __lt__(self, other: Any) -> bool: ...  # <2>
