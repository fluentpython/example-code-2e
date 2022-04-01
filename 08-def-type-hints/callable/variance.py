from collections.abc import Callable

def update(  # <1>
        probe: Callable[[], float],  # <2>
        display: Callable[[float], None]  # <3>
    ) -> None:
    temperature = probe()
    # imagine lots of control code here
    display(temperature)

def probe_ok() -> int:  # <4>
    return 42

def display_wrong(temperature: int) -> None:  # <5>
    print(hex(temperature))

update(probe_ok, display_wrong)  # type error  # <6>

def display_ok(temperature: complex) -> None:  # <7>
    print(temperature)

update(probe_ok, display_ok)  # OK  # <8>
