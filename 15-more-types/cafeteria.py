from typing import TypeVar, Generic


class Beverage:
    """Any beverage"""


class Juice(Beverage):
    """Any fruit juice"""


class OrangeJuice(Juice):
    """Delicious juice from Brazilian oranges"""


BeverageT = TypeVar('BeverageT', covariant=True)


class BeverageDispenser(Generic[BeverageT]):
    def __init__(self, beverage: BeverageT) -> None:
        self.beverage = beverage

    def dispense(self) -> BeverageT:
        return self.beverage


class Garbage:
    """Any garbage."""


class Biodegradable(Garbage):
    """Biodegradable garbage."""


class Compostable(Biodegradable):
    """Compostable garbage."""


GarbageT = TypeVar('GarbageT', contravariant=True)


class TrashCan(Generic[GarbageT]):
    def put(self, trash) -> None:
        """Store trash until dumped..."""


class Cafeteria:
    def __init__(
        self,
        dispenser: BeverageDispenser[Juice],
        trash_can: TrashCan[Biodegradable]
    ):
        """Initialize..."""


beverage_dispenser = BeverageDispenser(Beverage())
juice_dispenser = BeverageDispenser(Juice())
orange_juice_dispenser = BeverageDispenser(OrangeJuice())

trash_can: TrashCan[Garbage] = TrashCan()
bio_can: TrashCan[Biodegradable] = TrashCan()
compost_can: TrashCan[Compostable] = TrashCan()

arnold_hall = Cafeteria(juice_dispenser, bio_can)

######################## covariance on 1st argument
arnold_hall = Cafeteria(orange_juice_dispenser, trash_can)

## Argument 1 to "Cafeteria" has
## incompatible type "BeverageDispenser[Beverage]"
##          expected "BeverageDispenser[Juice]"
# arnold_hall = Cafeteria(beverage_dispenser, trash_can)


######################## contravariance on 2nd argument

## Argument 2 to "Cafeteria" has
## incompatible type "TrashCan[Compostable]"
##          expected "TrashCan[Biodegradable]"
# arnold_hall = Cafeteria(juice_dispenser, compost_can)

arnold_hall = Cafeteria(juice_dispenser, trash_can)
