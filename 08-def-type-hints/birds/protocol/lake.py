from typing import Protocol                    # <1>

class GooseLike(Protocol):
    def honk(self, times: int) -> None: ...    # <2>
    def swim(self) -> None: ...


def alert(waterfowl: GooseLike) -> None:       # <3>
    waterfowl.honk(2)
