from typing import Protocol, Any

class SupportsLessThan(Protocol):  # <1>
    def __lt__(self, other: Any) -> bool: ...  # <2>
