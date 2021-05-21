from typing import TypeVar, Generic


class Beverage:
    """Any beverage"""


class Juice(Beverage):
    """Any fruit juice"""


class OrangeJuice(Juice):
    """Delicious juice Brazilian oranges"""


class Coak(Beverage):
    """Secret formula with lots of sugar"""


BeverageT = TypeVar('BeverageT', bound=Beverage)
JuiceT = TypeVar('JuiceT', bound=Juice)


class BeverageDispenser(Generic[BeverageT]):

    beverage: BeverageT

    def __init__(self, beverage: BeverageT) -> None:
        self.beverage = beverage

    def dispense(self) -> BeverageT:
        return self.beverage


class JuiceDispenser(BeverageDispenser[JuiceT]):
    pass


class Cafeteria:
    def __init__(self, dispenser: BeverageDispenser[JuiceT]):
        self.dispenser = dispenser
