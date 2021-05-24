from typing import TypeVar, Generic


class Beverage:
    """Any beverage."""


class Juice(Beverage):
    """Any fruit juice."""


class OrangeJuice(Juice):
    """Delicious juice from Brazilian oranges."""


T_co = TypeVar('T_co', covariant=True)


class BeverageDispenser(Generic[T_co]):
    def __init__(self, beverage: T_co) -> None:
        self.beverage = beverage

    def dispense(self) -> T_co:
        return self.beverage


class Garbage:
    """Any garbage."""


class Biodegradable(Garbage):
    """Biodegradable garbage."""


class Compostable(Biodegradable):
    """Compostable garbage."""


T_contra = TypeVar('T_contra', contravariant=True)


class TrashCan(Generic[T_contra]):
    def put(self, trash: T_contra) -> None:
        """Store trash until dumped."""


class Cafeteria:
    def __init__(
        self,
        dispenser: BeverageDispenser[Juice],
        trash_can: TrashCan[Biodegradable],
    ):
        """Initialize..."""


################################################ exact types

juice_dispenser = BeverageDispenser(Juice())
bio_can: TrashCan[Biodegradable] = TrashCan()

arnold_hall = Cafeteria(juice_dispenser, bio_can)


################################################ covariant dispenser

orange_juice_dispenser = BeverageDispenser(OrangeJuice())

arnold_hall = Cafeteria(orange_juice_dispenser, bio_can)


################################################ non-covariant dispenser

beverage_dispenser = BeverageDispenser(Beverage())

## Argument 1 to "Cafeteria" has
## incompatible type "BeverageDispenser[Beverage]"
##          expected "BeverageDispenser[Juice]"
# arnold_hall = Cafeteria(beverage_dispenser, bio_can)


################################################ contravariant trash

trash_can: TrashCan[Garbage] = TrashCan()

arnold_hall = Cafeteria(juice_dispenser, trash_can)


################################################ non-contravariant trash

compost_can: TrashCan[Compostable] = TrashCan()

## Argument 2 to "Cafeteria" has
## incompatible type "TrashCan[Compostable]"
##          expected "TrashCan[Biodegradable]"
# arnold_hall = Cafeteria(juice_dispenser, compost_can)
